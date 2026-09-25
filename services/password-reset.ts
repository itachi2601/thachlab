import { getSupabase } from "./supabase";

/**
 * Lỗi từ Supabase là object thuần ({ message, hint }), không phải Error — gói lại để trang
 * gọi hiện được lý do thật (cùng cách với staff-invites.ts / parent-links.ts).
 */
function supabaseError(error: unknown, fallback: string): Error {
  const raw = error as { message?: unknown; hint?: unknown } | null;
  const message = typeof raw?.message === "string" && raw.message.trim() ? raw.message.trim() : fallback;
  const hint = typeof raw?.hint === "string" && raw.hint.trim() ? ` ${raw.hint.trim()}` : "";
  return new Error(`${message}${hint}`);
}

/**
 * Lỗi từ Edge Function reset-password: supabase-js chỉ trả "non-2xx status code" chung
 * chung khi gọi lỗi — thông báo thật (mã sai/hết hạn, không phụ trách học sinh này…) nằm
 * trong body JSON của response. Đọc lại từ đó thay vì hiện một câu mơ hồ.
 */
async function functionError(error: unknown, fallback: string): Promise<Error> {
  const withContext = error as { context?: Response; message?: string } | null;
  if (withContext?.context instanceof Response) {
    try {
      const body = await withContext.context.clone().json();
      if (typeof body?.error === "string" && body.error.trim()) return new Error(body.error.trim());
    } catch {
      // Response không phải JSON (vd chưa deploy function) — rơi xuống fallback bên dưới.
    }
  }
  return new Error(withContext?.message || fallback);
}

export interface PasswordResetCode {
  id: string;
  code: string;
  student_id: string;
  method: "self_service" | "admin_direct";
  created_at: string;
  expires_at: string;
  used_at: string | null;
}

const CODE_SELECT = "id, code, student_id, method, created_at, expires_at, used_at";

/** Giáo viên tạo mã cho học sinh tự đặt mật khẩu mới. RLS: chỉ giáo viên phụ trách em (hoặc admin). */
export async function createPasswordResetCode(studentId: string): Promise<PasswordResetCode> {
  const { data: auth } = await getSupabase().auth.getUser();
  const { data, error } = await getSupabase()
    .from("password_reset_codes")
    .insert({ student_id: studentId, created_by: auth.user?.id ?? null })
    .select(CODE_SELECT)
    .single();
  if (error) throw supabaseError(error, "Chưa tạo được mã đặt lại mật khẩu.");
  return data as PasswordResetCode;
}

/** Mã còn hiệu lực + lịch sử gần đây của một học sinh — cho thẻ "Mật khẩu" trong hồ sơ em. */
export async function fetchPasswordResetCodesForStudent(studentId: string): Promise<PasswordResetCode[]> {
  const { data, error } = await getSupabase()
    .from("password_reset_codes")
    .select(CODE_SELECT)
    .eq("student_id", studentId)
    .order("created_at", { ascending: false })
    .limit(20);
  if (error) throw supabaseError(error, "Chưa đọc được danh sách mã.");
  return (data ?? []) as PasswordResetCode[];
}

export async function revokePasswordResetCode(id: string): Promise<void> {
  const { error } = await getSupabase().from("password_reset_codes").delete().eq("id", id);
  if (error) throw supabaseError(error, "Chưa huỷ được mã.");
}

/**
 * Giáo viên/admin đặt thẳng mật khẩu học sinh về mã số HS — dùng khi gặp trực tiếp em,
 * không cần tạo mã. Trả về mật khẩu mới để hiện lại cho giáo viên đọc cho học sinh.
 */
export async function adminResetPasswordToStudentCode(studentId: string): Promise<string> {
  const { data, error } = await getSupabase().functions.invoke("reset-password", {
    body: { mode: "admin", studentId },
  });
  if (error) throw await functionError(error, "Chưa đặt lại được mật khẩu.");
  const password = (data as { password?: string } | null)?.password;
  if (!password) throw new Error("Không nhận được mật khẩu mới.");
  return password;
}

export interface ClaimPasswordResetResult {
  studentName: string;
}

/** Học sinh tự đặt mật khẩu mới bằng mã giáo viên cấp — không cần đăng nhập trước. */
export async function claimPasswordReset(code: string, newPassword: string): Promise<ClaimPasswordResetResult> {
  const { data, error } = await getSupabase().functions.invoke("reset-password", {
    body: { mode: "claim", code: code.trim().toUpperCase(), newPassword },
  });
  if (error) throw await functionError(error, "Chưa đặt lại được mật khẩu.");
  return { studentName: (data as { studentName?: string } | null)?.studentName ?? "" };
}
