import type { SchoolClass } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

export function classGrade(className: string): string | null {
  return className.match(/\d+/)?.[0] ?? null;
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
