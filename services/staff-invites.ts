import { getSupabase } from "./supabase";

export type StaffInviteRole = "instructor" | "tro_giang";

export interface StaffInvite {
  id: string;
  email: string;
  full_name: string;
  role: StaffInviteRole;
  admin_area: "thpt" | "cttc" | null;
  class_id: number | null;
  tier: "B1" | "B2" | "B3" | null;
  invited_at: string;
  claimed_at: string | null;
}

export interface InviteStaffInput {
  email: string;
  fullName: string;
  role: StaffInviteRole;
  adminArea?: "thpt" | "cttc" | null;
  classId?: number | null;
  courseId?: number | null;
  tier?: "B1" | "B2" | "B3" | null;
}

/**
 * "invited" = đã gửi email mời đặt mật khẩu; "linked" = email đã có tài khoản nên
 * cấp quyền và phân công ngay, không gửi mail lại.
 */
export interface InviteStaffResult {
  status: "invited" | "linked";
  inviteId: string;
  userId: string | null;
}

export async function inviteStaff(input: InviteStaffInput): Promise<InviteStaffResult> {
  const { data, error } = await getSupabase().functions.invoke("invite-staff", { body: input });
  if (error) throw error;
  if (data?.error) throw new Error(data.error as string);
  return data as InviteStaffResult;
}

export async function fetchStaffInvites(): Promise<StaffInvite[]> {
  const { data, error } = await getSupabase()
    .from("staff_invites")
    .select("id, email, full_name, role, admin_area, class_id, tier, invited_at, claimed_at")
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
