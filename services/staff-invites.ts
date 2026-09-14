import { getSupabase } from "./supabase";

/**
 * Lỗi từ Supabase là object thuần ({ message, hint, code }), KHÔNG phải Error — mọi chỗ
 * bắt lỗi trong app đều dùng `error instanceof Error` nên câu giải thích thật bị nuốt và
 * người dùng chỉ thấy một câu chung chung. Gói lại thành Error ngay tại đây, một lần.
 */
function supabaseError(error: unknown, fallback: string): Error {
  const raw = error as { message?: unknown; hint?: unknown } | null;
  const message = typeof raw?.message === "string" && raw.message.trim() ? raw.message.trim() : fallback;
  const hint = typeof raw?.hint === "string" && raw.hint.trim() ? ` ${raw.hint.trim()}` : "";
  return new Error(`${message}${hint}`);
}

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
  if (error) throw supabaseError(error, "Chưa tạo được lời mời.");
  return data as StaffInvite;
}

export async function fetchStaffInvites(): Promise<StaffInvite[]> {
  const { data, error } = await getSupabase()
    .from("staff_invites")
    .select("id, code, email, full_name, role, admin_area, class_id, tier, invited_at, claimed_at")
    .order("invited_at", { ascending: false })
    .limit(50);
  if (error) throw supabaseError(error, "Chưa đọc được danh sách lời mời.");
  return (data ?? []) as StaffInvite[];
}

/** Chỉ huỷ được lời mời chưa ai nhận. */
export async function revokeStaffInvite(id: string): Promise<void> {
  const { error } = await getSupabase()
    .from("staff_invites")
    .delete()
    .eq("id", id)
    .is("claimed_at", null);
  if (error) throw supabaseError(error, "Chưa huỷ được lời mời.");
}

export interface ClaimResult {
  role: StaffInviteRole;
  class_name: string | null;
  tier: "B1" | "B2" | "B3" | null;
}

/** Người đang đăng nhập tự nhận lời mời bằng mã. */
export async function claimStaffInvite(code: string): Promise<ClaimResult> {
  const { data, error } = await getSupabase().rpc("claim_staff_invite", { p_code: code.trim() });
  if (error) throw supabaseError(error, "Không nhận được lời mời.");
  const rows = (data ?? []) as ClaimResult[];
  if (rows.length === 0) throw new Error("Mã mời không đúng hoặc đã được dùng.");
  return rows[0];
}

export interface SignUpWithInviteResult {
  /** true khi dự án bật xác nhận email — chỉ khi đó Supabase mới gửi thư. */
  needsEmailConfirm: boolean;
  userId: string | null;
}

/**
 * Đăng ký tài khoản mới kèm mã mời — trigger zz_claim_staff_invite cấp quyền ngay trong
 * lệnh insert auth.users, không chờ xác nhận email.
 *
 * Dự án đang tắt xác nhận email (mailer_autoconfirm), nên signUp trả luôn session và
 * KHÔNG có thư nào được gửi đi. Trả cờ needsEmailConfirm để trang gọi biết nên báo
 * "vào dùng được ngay" hay "kiểm tra email", đừng đoán.
 */
export async function signUpWithInvite(input: {
  email: string;
  password: string;
  fullName: string;
  code: string;
}): Promise<SignUpWithInviteResult> {
  const { data, error } = await getSupabase().auth.signUp({
    email: input.email.trim(),
    password: input.password,
    options: { data: { full_name: input.fullName.trim(), invite_code: input.code.trim() } },
  });
  if (error) throw supabaseError(error, "Không tạo được tài khoản.");
  return { needsEmailConfirm: !data.session, userId: data.user?.id ?? null };
}

/**
 * Đọc lại quyền thật của chính mình sau khi đăng ký, để báo đúng thay vì tin là trigger
 * đã chạy: mã hết hạn hoặc đã có người dùng thì apply_staff_invite lặng lẽ bỏ qua.
 */
export async function fetchGrantedStaffRole(userId: string): Promise<ClaimResult | null> {
  const [assistant, profile] = await Promise.all([
    getSupabase().from("ta_assistants").select("tier").eq("user_id", userId).maybeSingle(),
    getSupabase().from("profiles").select("role").eq("id", userId).maybeSingle(),
  ]);
  if (assistant.data)
    return {
      role: "tro_giang",
      class_name: null,
      tier: (assistant.data as { tier: ClaimResult["tier"] }).tier,
    };
  if ((profile.data as { role?: string } | null)?.role === "instructor")
    return { role: "instructor", class_name: null, tier: null };
  return null;
}
