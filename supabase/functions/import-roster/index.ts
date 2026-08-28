// Nhập danh sách lớp: tạo tài khoản Supabase Auth cho từng sinh viên (mật khẩu = mã số sinh
// viên) rồi ghi danh vào khóa học CTTC (body.courseId → course_enrollments) hoặc thêm vào
// khối lớp THPT (body.classId → user_classes). Chạy trong Edge Function vì cần service_role
// key (auth.admin.createUser) — không thể gọi từ trình duyệt (site build tĩnh, không có
// server Node). Xem docs/deploy-edge-function.md để deploy.
//
// SUPABASE_URL / SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY được Supabase tự bơm vào mọi
// Edge Function, không cần "supabase secrets set" cho 3 biến này.

import { createClient } from "npm:@supabase/supabase-js@2";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

interface RosterStudent {
  studentCode: string;
  fullName: string;
  className?: string;
  /** dd/mm/yyyy, đúng định dạng cột "Ngày Sinh" trong file gốc. */
  birthDate?: string;
}

function toIsoDate(vnDate: string | undefined): string | null {
  const match = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec((vnDate ?? "").trim());
  if (!match) return null;
  const [, d, m, y] = match;
  return `${y}-${m.padStart(2, "0")}-${d.padStart(2, "0")}`;
}

interface ImportRow {
  studentCode: string;
  status: "created" | "linked" | "error";
  message?: string;
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

function loginEmail(studentCode: string) {
  return `${studentCode.trim().toLowerCase()}@thachlab.local`;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS_HEADERS });
  if (req.method !== "POST") return jsonResponse({ error: "method not allowed" }, 405);

  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader) return jsonResponse({ error: "Thiếu đăng nhập." }, 401);

  let body: { courseId?: number; classId?: number; students: RosterStudent[] };
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Dữ liệu gửi lên không hợp lệ." }, 400);
  }
  const students = Array.isArray(body.students) ? body.students : [];
  // Chế độ CTTC: ghi danh vào course_offerings. Chế độ THPT: thêm vào khối lớp (user_classes).
  const courseId = body.courseId !== undefined ? Number(body.courseId) : null;
  const classId = body.classId !== undefined ? Number(body.classId) : null;
  const isClassMode = classId !== null;
  const targetId = isClassMode ? classId : courseId;
  if (targetId === null || !Number.isFinite(targetId) || students.length === 0) {
    return jsonResponse({ error: "Thiếu courseId/classId hoặc danh sách sinh viên rỗng." }, 400);
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
  const anonKey = Deno.env.get("SUPABASE_ANON_KEY")!;
  const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

  // Client mang JWT của người gọi — dùng đúng RLS/RPC hiện có để xác thực quyền,
  // không tự viết lại logic phân quyền trong function.
  const callerClient = createClient(supabaseUrl, anonKey, {
    global: { headers: { Authorization: authHeader } },
    auth: { persistSession: false },
  });
  const { data: authUser, error: authError } = await callerClient.auth.getUser();
  if (authError || !authUser?.user) return jsonResponse({ error: "Phiên đăng nhập không hợp lệ." }, 401);

  const { data: canManage, error: rpcError } = isClassMode
    ? await callerClient.rpc("can_manage_class", { p_class_id: targetId })
    : await callerClient.rpc("can_manage_course", { p_course_id: targetId });
  if (rpcError) return jsonResponse({ error: rpcError.message }, 500);
  if (!canManage) return jsonResponse({ error: "Bạn không được phân công quản lý lớp này." }, 403);

  const admin = createClient(supabaseUrl, serviceRoleKey, { auth: { persistSession: false } });
  const callerId = authUser.user.id;
  const results: ImportRow[] = [];

  for (const raw of students) {
    const studentCode = (raw.studentCode ?? "").trim();
    const fullName = (raw.fullName ?? "").trim();
    if (!studentCode || !fullName) {
      results.push({ studentCode: studentCode || "(trống)", status: "error", message: "Thiếu mã SV hoặc họ tên." });
      continue;
    }

    try {
      const { data: existingProfile, error: lookupError } = await admin
        .from("profiles")
        .select("id, full_name")
        .ilike("student_code", studentCode)
        .maybeSingle();
      if (lookupError) throw lookupError;

      let studentId = existingProfile?.id as string | undefined;
      let status: ImportRow["status"] = "linked";
      const birthDate = toIsoDate(raw.birthDate);

      if (!studentId) {
        const { data: created, error: createError } = await admin.auth.admin.createUser({
          email: loginEmail(studentCode),
          password: studentCode,
          email_confirm: true,
          user_metadata: { full_name: fullName },
        });
        if (createError) throw createError;
        studentId = created.user.id;
        status = "created";

        const { error: profileError } = await admin
          .from("profiles")
          .update({ full_name: fullName, class_name: raw.className ?? "", role: "student", student_code: studentCode, birth_date: birthDate })
          .eq("id", studentId);
        if (profileError) throw profileError;
      } else {
        const patch: Record<string, unknown> = {};
        if (!existingProfile?.full_name) patch.full_name = fullName;
        if (birthDate) patch.birth_date = birthDate;
        if (Object.keys(patch).length) await admin.from("profiles").update(patch).eq("id", studentId);
      }

      const { error: enrollError } = isClassMode
        ? await admin
            .from("user_classes")
            .upsert({ user_id: studentId, class_id: targetId }, { onConflict: "user_id,class_id" })
        : await admin
            .from("course_enrollments")
            .upsert(
              { course_id: targetId, student_id: studentId, status: "active", approved_by: callerId, approved_at: new Date().toISOString() },
              { onConflict: "course_id,student_id" },
            );
      if (enrollError) throw enrollError;

      results.push({ studentCode, status });
    } catch (cause) {
      results.push({ studentCode, status: "error", message: cause instanceof Error ? cause.message : String(cause) });
    }
  }

  return jsonResponse({ results });
});
