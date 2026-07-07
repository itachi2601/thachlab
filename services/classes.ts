import type { SchoolClass } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

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
