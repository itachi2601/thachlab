// Đặt lại mật khẩu tài khoản học sinh — cần service_role vì phải gọi auth.admin.updateUserById,
// việc trình duyệt không tự làm được (giống import-roster). Hai chế độ:
//   mode "admin": giáo viên/admin đang đăng nhập đặt thẳng mật khẩu học sinh về mã số HS,
//     dùng khi gặp trực tiếp em (không cần mã).
//   mode "claim": học sinh (đang bị khoá ngoài tài khoản) tự đặt mật khẩu mới bằng mã một-lần
//     giáo viên đã cấp qua Zalo (bảng password_reset_codes) — KHÔNG cần đăng nhập trước, nên
//     không đọc Authorization header ở nhánh này.
//
// SUPABASE_URL / SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY được Supabase tự bơm vào mọi
// Edge Function. Xem docs/deploy-edge-function.md để deploy (đổi "import-roster" thành
// "reset-password" trong lệnh deploy).

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

interface RequestBody {
  mode?: "admin" | "claim";
  studentId?: string;
  code?: string;
  newPassword?: string;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS_HEADERS });
  if (req.method !== "POST") return jsonResponse({ error: "method not allowed" }, 405);

  let body: RequestBody;
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Dữ liệu gửi lên không hợp lệ." }, 400);
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
  const anonKey = Deno.env.get("SUPABASE_ANON_KEY")!;
  const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
  const admin = createClient(supabaseUrl, serviceRoleKey, { auth: { persistSession: false } });

  if (body.mode === "admin") {
    const authHeader = req.headers.get("Authorization") ?? "";
    if (!authHeader) return jsonResponse({ error: "Thiếu đăng nhập." }, 401);
    const studentId = (body.studentId ?? "").trim();
    if (!studentId) return jsonResponse({ error: "Thiếu studentId." }, 400);

    // Client mang JWT của người gọi — dùng đúng hàm teaches_student() hiện có để xác thực
    // quyền, không tự viết lại logic phân quyền trong function.
    const callerClient = createClient(supabaseUrl, anonKey, {
      global: { headers: { Authorization: authHeader } },
      auth: { persistSession: false },
    });
    const { data: authUser, error: authError } = await callerClient.auth.getUser();
    if (authError || !authUser?.user) return jsonResponse({ error: "Phiên đăng nhập không hợp lệ." }, 401);

    const { data: canManage, error: rpcError } = await callerClient.rpc("teaches_student", {
      p_student: studentId,
    });
    if (rpcError) return jsonResponse({ error: rpcError.message }, 500);
    if (!canManage) return jsonResponse({ error: "Bạn không phụ trách học sinh này." }, 403);

    const { data: profile, error: profileError } = await admin
      .from("profiles")
      .select("student_code")
      .eq("id", studentId)
      .maybeSingle();
    if (profileError) return jsonResponse({ error: profileError.message }, 500);
    const newPassword = (profile?.student_code ?? "").trim();
    if (!newPassword) return jsonResponse({ error: "Học sinh này chưa có mã số HS để đặt lại mật khẩu." }, 400);

    const { error: updateError } = await admin.auth.admin.updateUserById(studentId, { password: newPassword });
    if (updateError) return jsonResponse({ error: updateError.message }, 500);

    // Chỉ để làm lịch sử — bảng password_reset_codes coi hàng này là đã dùng ngay từ đầu.
    await admin.from("password_reset_codes").insert({
      student_id: studentId,
      method: "admin_direct",
      created_by: authUser.user.id,
      used_at: new Date().toISOString(),
    });

    return jsonResponse({ password: newPassword });
  }

  if (body.mode === "claim") {
    const code = (body.code ?? "").trim().toUpperCase();
    const newPassword = (body.newPassword ?? "").trim();
    if (!code) return jsonResponse({ error: "Thiếu mã." }, 400);
    if (newPassword.length < 6) return jsonResponse({ error: "Mật khẩu mới phải từ 6 ký tự trở lên." }, 400);

    const { data: reset, error: lookupError } = await admin
      .from("password_reset_codes")
      .select("id, student_id, used_at, expires_at")
      .eq("code", code)
      .maybeSingle();
    if (lookupError) return jsonResponse({ error: lookupError.message }, 500);
    if (!reset) return jsonResponse({ error: "Mã không đúng — nhờ giáo viên cấp lại mã mới." }, 404);
    if (reset.used_at) return jsonResponse({ error: "Mã này đã được dùng — nhờ giáo viên cấp mã mới." }, 400);
    if (new Date(reset.expires_at).getTime() < Date.now()) {
      return jsonResponse({ error: "Mã đã hết hạn — nhờ giáo viên cấp mã mới." }, 400);
    }

    const { data: profile } = await admin
      .from("profiles")
      .select("full_name")
      .eq("id", reset.student_id)
      .maybeSingle();

    const { error: updateError } = await admin.auth.admin.updateUserById(reset.student_id, { password: newPassword });
    if (updateError) return jsonResponse({ error: updateError.message }, 500);

    await admin.from("password_reset_codes").update({ used_at: new Date().toISOString() }).eq("id", reset.id);

    return jsonResponse({ studentName: profile?.full_name ?? "" });
  }

  return jsonResponse({ error: "mode không hợp lệ." }, 400);
});
