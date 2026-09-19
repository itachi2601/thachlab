import { getSupabase } from "./supabase";

export type AccountRole = "student" | "tro_giang" | "instructor" | "admin";
/** Vai trò đổi được từ giao diện — "admin" cố tình nằm ngoài, chỉ đổi bằng SQL. */
export type AssignableRole = Exclude<AccountRole, "admin">;
export type TaTier = "B1" | "B2" | "B3";

export interface AdminAccount {
  id: string;
  full_name: string;
  class_name: string;
  student_code: string | null;
  role: AccountRole;
  admin_area: "thpt" | "cttc" | null;
  track: "thpt" | "cttc" | null;
  email: string;
  ta_tier: TaTier | null;
  ta_active: boolean | null;
}

export const ROLE_LABEL: Record<AccountRole, string> = {
  student: "Học sinh",
  tro_giang: "Trợ giảng",
  instructor: "Giảng viên",
  admin: "Quản trị",
};

function supabaseError(error: unknown, fallback: string): Error {
  const raw = error as { message?: unknown; hint?: unknown } | null;
  const message = typeof raw?.message === "string" && raw.message.trim() ? raw.message.trim() : fallback;
  const hint = typeof raw?.hint === "string" && raw.hint.trim() ? ` ${raw.hint.trim()}` : "";
  return new Error(`${message}${hint}`);
}

/**
 * Tìm tài khoản kèm email và tình trạng trợ giảng. Đi qua RPC vì email nằm ở auth.users,
 * client không đọc thẳng được; hàm SQL tự chặn người không phải quản trị.
 * Bỏ trống cả hai tham số thì trả về 50 tài khoản đầu theo tên.
 */
export async function searchAccounts(query: string, role?: AccountRole | null): Promise<AdminAccount[]> {
  const { data, error } = await getSupabase().rpc("admin_search_accounts", {
    p_query: query.trim(),
    p_role: role ?? null,
  });
  if (error) throw supabaseError(error, "Không tìm được tài khoản.");
  return (data ?? []) as AdminAccount[];
}

/** Đặt vai trò cho một tài khoản; với trợ giảng thì kèm bậc lương (mặc định B1). */
export async function setAccountRole(userId: string, role: AssignableRole, tier?: TaTier | null): Promise<void> {
  const { error } = await getSupabase().rpc("admin_set_account_role", {
    p_user_id: userId,
    p_role: role,
    p_tier: role === "tro_giang" ? (tier ?? null) : null,
  });
  if (error) throw supabaseError(error, "Chưa đổi được vai trò.");
}
