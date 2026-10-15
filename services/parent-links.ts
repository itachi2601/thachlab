import { getSupabase } from "./supabase";

/**
 * Lỗi từ Supabase là object thuần ({ message, hint }), không phải Error — gói lại để
 * trang gọi hiện được lý do thật (cùng cách với staff-invites.ts).
 */
function supabaseError(error: unknown, fallback: string): Error {
  const raw = error as { message?: unknown; hint?: unknown } | null;
  const message = typeof raw?.message === "string" && raw.message.trim() ? raw.message.trim() : fallback;
  const hint = typeof raw?.hint === "string" && raw.hint.trim() ? ` ${raw.hint.trim()}` : "";
  return new Error(`${message}${hint}`);
}

/** Mã phụ huynh luôn bắt đầu bằng PH — trang /loi-moi dựa vào đây để rẽ nhánh. */
export function isParentCode(code: string): boolean {
  return /^PH[0-9A-F]{6}$/i.test(code.trim());
}

export interface ParentLink {
  id: string;
  code: string;
  student_id: string;
  parent_id: string | null;
  label: string;
  created_at: string;
  claimed_at: string | null;
}

const LINK_SELECT = "id, code, student_id, parent_id, label, created_at, claimed_at";

/** Giáo viên tạo mã cho một học sinh. RLS: chỉ giáo viên được phân công lớp của em (hoặc admin). */
export async function createParentLink(studentId: string, label = ""): Promise<ParentLink> {
  const { data: auth } = await getSupabase().auth.getUser();
  const { data, error } = await getSupabase()
    .from("parent_links")
    .insert({ student_id: studentId, label: label.trim(), created_by: auth.user?.id ?? null })
    .select(LINK_SELECT)
    .single();
  if (error) throw supabaseError(error, "Chưa tạo được mã phụ huynh.");
  return data as ParentLink;
}

/** Mọi mã (đã nhận / chưa nhận) của một học sinh — cho thẻ Phụ huynh trong hồ sơ em. */
export async function fetchParentLinksForStudent(studentId: string): Promise<ParentLink[]> {
  const { data, error } = await getSupabase()
    .from("parent_links")
    .select(LINK_SELECT)
    .eq("student_id", studentId)
    .order("created_at", { ascending: false });
  if (error) throw supabaseError(error, "Chưa đọc được danh sách mã phụ huynh.");
  return (data ?? []) as ParentLink[];
}

/** Huỷ mã chưa nhận, hoặc gỡ liên kết đã nhận — phụ huynh mất quyền xem ngay. */
export async function removeParentLink(id: string): Promise<void> {
  const { error } = await getSupabase().from("parent_links").delete().eq("id", id);
  if (error) throw supabaseError(error, "Chưa gỡ được.");
}

export interface ClaimParentResult {
  student_name: string;
  class_name: string;
}

/** Người đang đăng nhập tự nhận mã phụ huynh. */
export async function claimParentLink(code: string): Promise<ClaimParentResult> {
  const { data, error } = await getSupabase().rpc("claim_parent_link", { p_code: code.trim() });
  if (error) throw supabaseError(error, "Không nhận được mã phụ huynh.");
  const rows = (data ?? []) as ClaimParentResult[];
  if (rows.length === 0) throw new Error("Mã phụ huynh không đúng hoặc đã được dùng.");
  return rows[0];
}

export interface LinkedChild {
  linkId: string;
  studentId: string;
  fullName: string;
  className: string;
  /** Khối lớp đang active — null nếu em chưa được duyệt vào lớp nào. */
  classId: number | null;
  classLabel: string | null;
}

/** Các con đã nối với tài khoản phụ huynh đang đăng nhập. */
export async function fetchMyChildren(parentId: string): Promise<LinkedChild[]> {
  const supabase = getSupabase();
  const { data: links, error } = await supabase
    .from("parent_links")
    .select("id, student_id, profiles!parent_links_student_id_fkey(full_name, class_name)")
    .eq("parent_id", parentId)
    .not("claimed_at", "is", null)
    .order("created_at", { ascending: true });
  if (error) throw supabaseError(error, "Chưa đọc được danh sách con.");

  const rows = (links ?? []) as {
    id: string;
    student_id: string;
    profiles: { full_name: string; class_name: string } | { full_name: string; class_name: string }[] | null;
  }[];
  if (rows.length === 0) return [];

  const ids = rows.map((r) => r.student_id);
  const { data: classes } = await supabase
    .from("user_classes")
    .select("user_id, class_id, classes(name)")
    .in("user_id", ids)
    .eq("status", "active");
  const classByStudent = new Map<string, { id: number; name: string }>();
  for (const row of (classes ?? []) as {
    user_id: string;
    class_id: number;
    classes: { name: string } | { name: string }[] | null;
  }[]) {
    if (classByStudent.has(row.user_id)) continue;
    const cls = Array.isArray(row.classes) ? row.classes[0] : row.classes;
    classByStudent.set(row.user_id, { id: row.class_id, name: cls?.name ?? "" });
  }

  return rows.map((r) => {
    const profile = Array.isArray(r.profiles) ? r.profiles[0] : r.profiles;
    const cls = classByStudent.get(r.student_id) ?? null;
    return {
      linkId: r.id,
      studentId: r.student_id,
      fullName: profile?.full_name ?? "(Chưa có tên)",
      className: profile?.class_name ?? "",
      classId: cls?.id ?? null,
      classLabel: cls?.name ?? null,
    };
  });
}

/**
 * Đăng ký tài khoản phụ huynh kèm mã — trigger zz_claim_parent_link nối với con ngay
 * trong lệnh insert auth.users. Dự án tắt xác nhận email nên signUp trả session luôn.
 */
export async function signUpParentWithCode(input: {
  email: string;
  password: string;
  fullName: string;
  code: string;
}): Promise<{ needsEmailConfirm: boolean; userId: string | null }> {
  const { data, error } = await getSupabase().auth.signUp({
    email: input.email.trim(),
    password: input.password,
    // Không mã (/loi-moi?vai=phu-huynh): không gửi invite_code — phụ huynh tự nối con sau ở /phu-huynh.
    options: {
      data: input.code.trim()
        ? { full_name: input.fullName.trim(), invite_code: input.code.trim().toUpperCase() }
        : { full_name: input.fullName.trim() },
    },
  });
  if (error) throw supabaseError(error, "Không tạo được tài khoản.");
  return { needsEmailConfirm: !data.session, userId: data.user?.id ?? null };
}

/** Sau khi đăng ký: đọc lại xem đã nối được với con chưa (mã hết hạn thì trigger lặng lẽ bỏ qua). */
export async function fetchClaimedChild(parentId: string): Promise<ClaimParentResult | null> {
  const children = await fetchMyChildren(parentId).catch(() => []);
  const first = children[0];
  return first ? { student_name: first.fullName, class_name: first.className } : null;
}

/* ---------- Phụ huynh tự nối với con (migration 20261015180000_phu_huynh_tu_noi_con) ---------- */

export type SelfLinkStatus = "linked" | "already" | "no_match" | "locked";
export interface SelfLinkResult {
  status: SelfLinkStatus;
  studentName: string | null;
  className: string | null;
}

/** Khớp ĐỦ họ tên con + ngày sinh con + SĐT phụ huynh đã khai lúc đăng ký học. Sai 5 lần/24 giờ → "locked". */
export async function claimParentByChildInfo(name: string, birth: string, phone: string): Promise<SelfLinkResult> {
  const { data, error } = await getSupabase().rpc("claim_parent_by_child_info", {
    p_name: name.trim(),
    p_birth: birth,
    p_phone: phone.trim(),
  });
  if (error) throw supabaseError(error, "Chưa kiểm tra được thông tin.");
  const row = (Array.isArray(data) ? data[0] : data) as
    | { status: SelfLinkStatus; student_name: string | null; class_name: string | null }
    | undefined;
  return { status: row?.status ?? "no_match", studentName: row?.student_name ?? null, className: row?.class_name ?? null };
}

/** Không khớp → gửi yêu cầu để thầy duyệt. */
export async function requestParentLinkReview(name: string, birth: string, phone: string, note = ""): Promise<number> {
  const { data, error } = await getSupabase().rpc("request_parent_link_review", {
    p_name: name.trim(),
    p_birth: birth || null,
    p_phone: phone.trim(),
    p_note: note.trim() || null,
  });
  if (error) throw supabaseError(error, "Chưa gửi được yêu cầu.");
  return data as number;
}

export interface ParentLinkRequest {
  id: number;
  parent_id: string;
  child_name: string;
  child_birth: string | null;
  parent_phone: string;
  note: string | null;
  matched_student_id: string | null;
  status: "pending" | "approved" | "rejected";
  created_at: string;
  parent: { full_name: string | null } | null;
  matched: { full_name: string | null; class_name: string | null } | null;
}

/** Yêu cầu đang chờ (giáo viên: RLS lọc theo em mình dạy; admin: tất cả; phụ huynh: của mình). */
export async function fetchPendingParentLinkRequests(): Promise<ParentLinkRequest[]> {
  const { data, error } = await getSupabase()
    .from("parent_link_requests")
    .select(
      "id, parent_id, child_name, child_birth, parent_phone, note, matched_student_id, status, created_at, parent:profiles!parent_link_requests_parent_id_fkey(full_name), matched:profiles!parent_link_requests_matched_student_id_fkey(full_name, class_name)",
    )
    .eq("status", "pending")
    .order("created_at", { ascending: true });
  if (error) throw supabaseError(error, "Chưa đọc được yêu cầu nối con.");
  return (data ?? []) as unknown as ParentLinkRequest[];
}

export async function reviewParentLinkRequest(id: number, studentId: string | null, approve: boolean): Promise<void> {
  const { error } = await getSupabase().rpc("review_parent_link_request", {
    p_id: id,
    p_student: studentId,
    p_approve: approve,
  });
  if (error) throw supabaseError(error, approve ? "Chưa duyệt được." : "Chưa từ chối được.");
}

export interface LinkStudentOption {
  id: string;
  full_name: string;
  class_name: string | null;
  birth_date: string | null;
}

export async function searchStudentsForLink(query: string): Promise<LinkStudentOption[]> {
  const { data, error } = await getSupabase().rpc("search_students_for_link", { p_query: query.trim() });
  if (error) throw supabaseError(error, "Chưa tìm được học sinh.");
  return (data ?? []) as LinkStudentOption[];
}
