import type { SchoolClass } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

interface ManagedClassSeed {
  name: string;
  slug: string;
  color: string;
  icon: string;
  sort_order: number;
}

export const MANAGED_CLASSES: ManagedClassSeed[] = [
  {
    name: "KHTN 9",
    slug: "khtn-9",
    color: "#10B981",
    icon: "🔬",
    sort_order: 1,
  },
  {
    name: "10",
    slug: "lop-10",
    color: "#22D3EE",
    icon: "🎓",
    sort_order: 2,
  },
  {
    name: "11",
    slug: "lop-11",
    color: "#3B82F6",
    icon: "🎓",
    sort_order: 3,
  },
  {
    name: "12",
    slug: "lop-12",
    color: "#8B5CF6",
    icon: "🎓",
    sort_order: 4,
  },
];

const MANAGED_CLASS_NAMES = new Set(MANAGED_CLASSES.map((c) => c.name));
const MANAGED_CLASS_SLUGS = new Set(MANAGED_CLASSES.map((c) => c.slug));

export function isManagedClass(schoolClass: Pick<SchoolClass, "name" | "slug">) {
  return (
    MANAGED_CLASS_NAMES.has(schoolClass.name) ||
    MANAGED_CLASS_SLUGS.has(schoolClass.slug)
  );
}

export function classGrade(className: string): string | null {
  return className.match(/\d+/)?.[0] ?? null;
}

export function displayClassesByGrade(classes: SchoolClass[]): SchoolClass[] {
  const result: SchoolClass[] = [];
  for (const managed of MANAGED_CLASSES) {
    const exact = classes.find(
      (schoolClass) =>
        schoolClass.name === managed.name || schoolClass.slug === managed.slug,
    );
    if (exact) {
      result.push(exact);
      continue;
    }

    const grade = classGrade(managed.name);
    const fallback = classes.find((schoolClass) => classGrade(schoolClass.name) === grade);
    if (fallback) result.push(fallback);
  }
  return result;
}

export function expandClassIdsByGrade(
  classIds: number[] | null,
  classes: SchoolClass[],
): number[] | null {
  if (classIds === null) return null;
  const grades = new Set(
    classes
      .filter((schoolClass) => classIds.includes(schoolClass.id))
      .map((schoolClass) => classGrade(schoolClass.name))
      .filter(Boolean),
  );
  if (grades.size === 0) return classIds;
  return classes
    .filter((schoolClass) => grades.has(classGrade(schoolClass.name)))
    .map((schoolClass) => schoolClass.id);
}

export async function fetchClasses(includeHidden = false) {
  let q = getSupabase()
    .from("classes")
    .select("*")
    .order("sort_order")
    .order("name");
  if (!includeHidden) q = q.eq("active", true);
  const { data } = await q;
  return (data as SchoolClass[]) ?? [];
}

/** Ghi lại danh sách lớp gán cho 1 đề/bài đăng (xóa hết rồi chèn lại). */
export async function setItemClasses(
  table: "exam_classes" | "post_classes" | "chapter_classes",
  idColumn: "exam_id" | "post_id" | "chapter_id",
  itemId: number,
  classIds: number[],
) {
  const supabase = getSupabase();
  await supabase.from(table).delete().eq(idColumn, itemId);
  if (classIds.length > 0) {
    await supabase
      .from(table)
      .insert(classIds.map((class_id) => ({ [idColumn]: itemId, class_id })));
  }
}

/** Lớp đã được duyệt của học sinh đang đăng nhập (không tính yêu cầu còn chờ duyệt). */
export async function fetchMyClassIds(userId: string): Promise<number[]> {
  const { data } = await getSupabase()
    .from("user_classes")
    .select("class_id")
    .eq("user_id", userId)
    .eq("status", "active");
  return (data ?? []).map((r) => r.class_id as number);
}

export interface ClassStudent {
  id: string;
  full_name: string;
  class_name: string;
}

/** Học sinh đã được duyệt vào 1 khối lớp — dùng cho dashboard giáo viên THPT. */
export async function fetchClassStudents(classId: number): Promise<ClassStudent[]> {
  const { data, error } = await getSupabase()
    .from("user_classes")
    .select("profiles!user_classes_user_id_fkey(id, full_name, class_name)")
    .eq("class_id", classId)
    .eq("status", "active");
  if (error) throw error;
  return (data ?? [])
    .map((row) => (Array.isArray(row.profiles) ? row.profiles[0] ?? null : row.profiles))
    .filter((profile): profile is ClassStudent => Boolean(profile));
}

export type ClassJoinStatus = "pending" | "active" | "rejected";

export interface MyClassRequest {
  classId: number;
  className: string;
  status: ClassJoinStatus;
}

/** Trạng thái mới nhất của học sinh với 1 khối lớp bất kỳ — dùng cho /tai-khoan. */
export async function fetchMyClassRequest(userId: string): Promise<MyClassRequest | null> {
  const { data, error } = await getSupabase()
    .from("user_classes")
    .select("class_id, status, classes(name)")
    .eq("user_id", userId);
  if (error) throw error;
  const rows = (data ?? []) as {
    class_id: number;
    status: ClassJoinStatus;
    classes: { name: string } | { name: string }[] | null;
  }[];
  if (!rows.length) return null;
  const rank: Record<ClassJoinStatus, number> = { active: 0, pending: 1, rejected: 2 };
  const best = rows.slice().sort((a, b) => rank[a.status] - rank[b.status])[0];
  const schoolClass = Array.isArray(best.classes) ? best.classes[0] : best.classes;
  return { classId: best.class_id, className: schoolClass?.name ?? "", status: best.status };
}

/** Học sinh tự gửi yêu cầu vào 1 khối lớp (chờ giáo viên duyệt). Gửi lại được sau khi bị từ chối. */
export async function requestClassJoin(classId: number): Promise<void> {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const userId = auth.user?.id;
  if (!userId) throw new Error("Bạn cần đăng nhập.");

  const { error: insertError } = await supabase
    .from("user_classes")
    .insert({ user_id: userId, class_id: classId, status: "pending" });
  if (!insertError) return;
  if (insertError.code !== "23505") throw insertError; // đã có dòng (ví dụ đã từng bị từ chối) -> chuyển sang cập nhật

  const { error: updateError } = await supabase
    .from("user_classes")
    .update({ status: "pending", requested_at: new Date().toISOString(), reviewed_by: null, reviewed_at: null })
    .eq("user_id", userId)
    .eq("class_id", classId);
  if (updateError) throw updateError;
}

export interface ClassJoinRequest {
  userId: string;
  fullName: string;
  requestedAt: string;
}

/** Học sinh đang chờ duyệt vào 1 khối lớp — dùng cho trang quản trị Học sinh. */
export async function fetchPendingClassRequests(classId: number): Promise<ClassJoinRequest[]> {
  const { data, error } = await getSupabase()
    .from("user_classes")
    .select("user_id, requested_at, profiles!user_classes_user_id_fkey(full_name)")
    .eq("class_id", classId)
    .eq("status", "pending")
    .order("requested_at");
  if (error) throw error;
  return (data ?? []).map((row) => {
    const profile = Array.isArray(row.profiles) ? row.profiles[0] : row.profiles;
    return { userId: row.user_id as string, fullName: profile?.full_name ?? "(chưa rõ tên)", requestedAt: row.requested_at as string };
  });
}

/** Duyệt/từ chối yêu cầu vào lớp, hoặc admin gán thẳng 1 học sinh vào lớp (upsert -> 'active'). */
export async function setUserClassStatus(userId: string, classId: number, status: ClassJoinStatus): Promise<void> {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { error } = await supabase
    .from("user_classes")
    .upsert(
      { user_id: userId, class_id: classId, status, reviewed_by: auth.user?.id ?? null, reviewed_at: new Date().toISOString() },
      { onConflict: "user_id,class_id" },
    );
  if (error) throw error;
}

export interface UnassignedStudent {
  id: string;
  full_name: string;
}

/**
 * Học sinh (role='student') chưa có yêu cầu hoặc chưa thuộc khối lớp THPT nào —
 * thường là tài khoản tự đăng ký ở /dang-ky. Việc đã tham gia một khóa học khác
 * không làm học sinh biến mất khỏi danh sách phân lớp THPT.
 */
export async function fetchUnassignedStudents(): Promise<UnassignedStudent[]> {
  const supabase = getSupabase();
  const [{ data: students, error: studentsError }, { data: classed, error: classedError }] =
    await Promise.all([
      supabase.from("profiles").select("id, full_name").eq("role", "student"),
      supabase.from("user_classes").select("user_id").in("status", ["active", "pending"]),
    ]);
  if (studentsError) throw studentsError;
  if (classedError) throw classedError;

  const linked = new Set<string>((classed ?? []).map((row) => row.user_id as string));
  return (students ?? []).filter((student) => !linked.has(student.id));
}
