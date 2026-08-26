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

/** Lớp của học sinh đang đăng nhập. */
export async function fetchMyClassIds(userId: string): Promise<number[]> {
  const { data } = await getSupabase()
    .from("user_classes")
    .select("class_id")
    .eq("user_id", userId);
  return (data ?? []).map((r) => r.class_id as number);
}

export interface ClassStudent {
  id: string;
  full_name: string;
  class_name: string;
}

/** Học sinh thuộc 1 khối lớp — dùng cho dashboard giáo viên THPT. */
export async function fetchClassStudents(classId: number): Promise<ClassStudent[]> {
  const { data, error } = await getSupabase()
    .from("user_classes")
    .select("profiles!user_classes_user_id_fkey(id, full_name, class_name)")
    .eq("class_id", classId);
  if (error) throw error;
  return (data ?? [])
    .map((row) => (Array.isArray(row.profiles) ? row.profiles[0] ?? null : row.profiles))
    .filter((profile): profile is ClassStudent => Boolean(profile));
}
