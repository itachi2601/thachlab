// Mời giảng viên / trợ giảng qua email từ trang "Phân công giảng viên".
// Cần service_role key (auth.admin.inviteUserByEmail) nên phải chạy trên Supabase —
// site build tĩnh, không có server Node. Xem docs/deploy-edge-function.md để deploy
// (thay import-roster bằng invite-staff ở bước `supabase functions deploy`).
//
// Luồng: ghi 1 dòng staff_invites đang chờ -> nếu email chưa có tài khoản thì gửi lời mời
// (trigger zz_claim_staff_invite sẽ tự áp dụng lời mời ngay khi tài khoản được tạo);
// nếu email đã có tài khoản thì gọi thẳng apply_staff_invite để cấp quyền và gán lớp.
// Toàn bộ logic "áp dụng lời mời" nằm trong SQL, function này không viết lại.

import { createClient } from "npm:@supabase/supabase-js@2";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

interface InviteBody {
  email?: string;
  fullName?: string;
  role?: "instructor" | "tro_giang";
  adminArea?: "thpt" | "cttc" | null;
  classId?: number | null;
  courseId?: number | null;
  tier?: "B1" | "B2" | "B3" | null;
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

/** API admin không có "get by email" nên duyệt trang danh sách người dùng. */
async function findUserByEmail(admin: ReturnType<typeof createClient>, email: string) {
  for (let page = 1; page <= 30; page++) {
    const { data, error } = await admin.auth.admin.listUsers({ page, perPage: 200 });
    if (error) throw error;
    const found = data.users.find((u) => u.email?.toLowerCase() === email.toLowerCase());
    if (found) return found;
    if (data.users.length < 200) return null;
  }
  return null;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS_HEADERS });
  if (req.method !== "POST") return jsonResponse({ error: "method not allowed" }, 405);

  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader) return jsonResponse({ error: "Thiếu đăng nhập." }, 401);

  let body: InviteBody;
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Dữ liệu gửi lên không hợp lệ." }, 400);
  }

  const email = (body.email ?? "").trim().toLowerCase();
  const fullName = (body.fullName ?? "").trim();
  const role = body.role;
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return jsonResponse({ error: "Email không hợp lệ." }, 400);
  if (role !== "instructor" && role !== "tro_giang")
    return jsonResponse({ error: "Vai trò phải là instructor hoặc tro_giang." }, 400);

  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
  const anonKey = Deno.env.get("SUPABASE_ANON_KEY")!;
  const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

  // Client mang JWT của người gọi — chỉ quản trị viên thật mới được mời người khác.
  const callerClient = createClient(supabaseUrl, anonKey, {
    global: { headers: { Authorization: authHeader } },
    auth: { persistSession: false },
  });
  const { data: authUser, error: authError } = await callerClient.auth.getUser();
  if (authError || !authUser?.user) return jsonResponse({ error: "Phiên đăng nhập không hợp lệ." }, 401);

  const { data: callerProfile, error: profileError } = await callerClient
    .from("profiles")
    .select("role")
    .eq("id", authUser.user.id)
    .maybeSingle();
  if (profileError) return jsonResponse({ error: profileError.message }, 500);
  if (callerProfile?.role !== "admin")
    return jsonResponse({ error: "Chỉ quản trị viên được mời người mới." }, 403);

  const admin = createClient(supabaseUrl, serviceRoleKey, { auth: { persistSession: false } });

  try {
    // Mời lại thì thay lời mời cũ chưa nhận (chỉ số unique chỉ cho phép 1 lời mời đang chờ).
    const { error: clearError } = await admin
      .from("staff_invites")
      .delete()
      .is("claimed_at", null)
      .ilike("email", email);
    if (clearError) throw clearError;

    const { data: invite, error: insertError } = await admin
      .from("staff_invites")
      .insert({
        email,
        full_name: fullName,
        role,
        admin_area: body.adminArea ?? null,
        class_id: body.classId ?? null,
        course_id: body.courseId ?? null,
        tier: body.tier ?? null,
        invited_by: authUser.user.id,
      })
      .select("id")
      .single();
    if (insertError) throw insertError;

    const existing = await findUserByEmail(admin, email);

    if (existing) {
      // Đã có tài khoản: không gửi mail mời lại, áp dụng quyền và phân công ngay.
      const { error: applyError } = await admin.rpc("apply_staff_invite", {
        p_user_id: existing.id,
        p_email: email,
      });
      if (applyError) throw applyError;
      return jsonResponse({ status: "linked", inviteId: invite.id, userId: existing.id });
    }

    const { data: invited, error: inviteError } = await admin.auth.admin.inviteUserByEmail(email, {
      data: { full_name: fullName },
    });
    if (inviteError) throw inviteError;

    // Trigger zz_claim_staff_invite đã áp dụng lời mời khi tài khoản vừa được tạo.
    return jsonResponse({ status: "invited", inviteId: invite.id, userId: invited.user?.id ?? null });
  } catch (cause) {
    const message = cause instanceof Error ? cause.message : "Không mời được, thử lại.";
    return jsonResponse({ error: message }, 500);
  }
});
