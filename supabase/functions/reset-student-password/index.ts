// Đặt lại mật khẩu cho học sinh không có email thật (tài khoản @thachlab.local) — các em này
// không tự dùng được trang /quen-mat-khau vì không nhận được mail. Giáo viên phụ trách lớp bấm
// "Đặt lại mật khẩu" trong hồ sơ học sinh, function này xác nhận quyền quản lý lớp rồi đặt mật
// khẩu mới bằng service_role key (auth.admin.updateUserById) — không thể gọi từ trình duyệt.
// Xem docs/deploy-edge-function.md để deploy.

import { createClient } from "npm:@supabase/supabase-js@2";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS_HEADERS });
  if (req.method !== "POST") return jsonResponse({ error: "method not allowed" }, 405);

  // Mọi lỗi "hợp lệ" (thiếu quyền, sai dữ liệu…) trả về status 200 kèm { error } — giữ cho
  // supabase-js trả `data` thay vì ném FunctionsHttpError không đọc được nội dung lỗi gốc.
  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader) return jsonResponse({ error: "Thiếu đăng nhập." });

  let body: { studentId?: string; classId?: number; newPassword?: string };
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Dữ liệu gửi lên không hợp lệ." });
  }

  const studentId = (body.studentId ?? "").trim();
  const classId = body.classId !== undefined ? Number(body.classId) : null;
  const newPassword = body.newPassword ?? "";
  if (!studentId || classId === null || !Number.isFinite(classId)) {
    return jsonResponse({ error: "Thiếu studentId hoặc classId." });
  }
  if (newPassword.length < 6) {
    return jsonResponse({ error: "Mật khẩu mới phải dài tối thiểu 6 ký tự." });
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
  const anonKey = Deno.env.get("SUPABASE_ANON_KEY")!;
  const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

  const callerClient = createClient(supabaseUrl, anonKey, {
    global: { headers: { Authorization: authHeader } },
    auth: { persistSession: false },
  });
  const { data: authUser, error: authError } = await callerClient.auth.getUser();
  if (authError || !authUser?.user) return jsonResponse({ error: "Phiên đăng nhập không hợp lệ." });

  const { data: canManage, error: rpcError } = await callerClient.rpc("can_manage_class", { p_class_id: classId });
  if (rpcError) return jsonResponse({ error: rpcError.message });
  if (!canManage) return jsonResponse({ error: "Bạn không được phân công quản lý lớp này." });

  const admin = createClient(supabaseUrl, serviceRoleKey, { auth: { persistSession: false } });

  // Xác nhận học sinh thật sự thuộc lớp này — tránh trường hợp giáo viên A đổi mật khẩu học sinh của lớp B.
  const { data: membership, error: membershipError } = await admin
    .from("user_classes")
    .select("user_id")
    .eq("user_id", studentId)
    .eq("class_id", classId)
    .maybeSingle();
  if (membershipError) return jsonResponse({ error: membershipError.message });
  if (!membership) return jsonResponse({ error: "Học sinh không thuộc lớp này." });

  const { error: updateError } = await admin.auth.admin.updateUserById(studentId, { password: newPassword });
  if (updateError) return jsonResponse({ error: updateError.message });

  return jsonResponse({ ok: true });
});
