import { getSupabase } from "./supabase";

export type StaffInviteRole = "instructor" | "tro_giang";

export interface StaffInvite {
  id: string;
  code: string;
  email: string | null;
  full_name: string;
  role: StaffInviteRole;
  admin_area: "thpt" | "cttc" | null;
  class_id: number | null;
  tier: "B1" | "B2" | "B3" | null;
  invited_at: string;
  claimed_at: string | null;
}

export interface CreateStaffInviteInput {
  fullName: string;
  email?: string | null;
  role: StaffInviteRole;
  adminArea?: "thpt" | "cttc" | null;
  classId?: number | null;
  tier?: "B1" | "B2" | "B3" | null;
}

/**
 * Tạo lời mời và trả về mã. Không gửi email — giáo viên tự gửi link /loi-moi?ma=<code>
 * qua Zalo/Messenger. Ghi thẳng từ trình duyệt, RLS chỉ cho role admin ghi bảng này.
 */
export async function createStaffInvite(input: CreateStaffInviteInput): Promise<StaffInvite> {
  const { data: auth } = await getSupabase().auth.getUser();
  const { data, error } = await getSupabase()
    .from("staff_invites")
    .insert({
      full_name: input.fullName,
      email: input.email?.trim() ? input.email.trim().toLowerCase() : null,
      role: input.role,
      admin_area: input.adminArea ?? null,
      class_id: input.classId ?? null,
      tier: input.tier ?? null,
      invited_by: auth.user?.id ?? null,
    })
    .select("id, code, email, full_name, role, admin_area, class_id, tier, invited_at, claimed_at")
    .single();
  if (error) throw error;
  return data as StaffInvite;
}

export async function fetchStaffInvites(): Promise<StaffInvite[]> {
  const { data, error } = await getSupabase()
    .from("staff_invites")
    .select("id, code, email, full_name, role, admin_area, class_id, tier, invited_at, claimed_at")
    .order("invited_at", { ascending: false })
    .limit(50);
  if (error) throw error;
  return (data ?? []) as StaffInvite[];
}

/** Chỉ huỷ được lời mời chưa ai nhận. */
export async function revokeStaffInvite(id: string): Promise<void> {
  const { error } = await getSupabase()
    .from("staff_invites")
    .delete()
    .eq("id", id)
    .is("claimed_at", null);
  if (error) throw error;
}

export interface ClaimResult {
  role: StaffInviteRole;
  class_name: string | null;
  tier: "B1" | "B2" | "B3" | null;
}

/** Người đang đăng nhập tự nhận lời mời bằng mã. */
export async function claimStaffInvite(code: string): Promise<ClaimResult> {
  const { data, error } = await getSupabase().rpc("claim_staff_invite", { p_code: code.trim() });
  if (error) throw error;
  const rows = (data ?? []) as ClaimResult[];
  if (rows.length === 0) throw new Error("Mã mời không đúng hoặc đã được dùng.");
  return rows[0];
}

/** Đăng ký tài khoản mới kèm mã mời — trigger sẽ cấp quyền ngay khi tài khoản được tạo. */
export async function signUpWithInvite(input: {
  email: string;
  password: string;
  fullName: string;
  code: string;
}): Promise<void> {
  const { error } = await getSupabase().auth.signUp({
    email: input.email.trim(),
    password: input.password,
    options: { data: { full_name: input.fullName.trim(), invite_code: input.code.trim() } },
  });
  if (error) throw error;
}
