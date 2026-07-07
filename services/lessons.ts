import type { Chapter, Lesson, LessonItem, TypeCounts } from "@/features/lessons/types";
import { getSupabase } from "@/services/supabase";

interface ClassRef {
  class_id: number;
}

export async function fetchChapters(): Promise<Chapter[]> {
  const { data } = await getSupabase()
    .from("chapters")
    .select("id, title, sort_order, chapter_classes(class_id)")
    .order("sort_order")
    .order("id");
  return (data ?? []).map((c) => ({
    id: c.id,
    title: c.title,
    sort_order: c.sort_order,
    classIds: ((c.chapter_classes as ClassRef[]) ?? []).map((r) => r.class_id),
  }));
}

export async function fetchLessons(includeDrafts = false): Promise<Lesson[]> {
  let q = getSupabase()
    .from("lessons")
    .select("id, chapter_id, title, sort_order, published, lesson_items(count)")
    .order("sort_order")
    .order("id");
  if (!includeDrafts) q = q.eq("published", true);
  const { data } = await q;
  return (data ?? []).map((l) => ({
    id: l.id,
    chapter_id: l.chapter_id,
    title: l.title,
    sort_order: l.sort_order,
    published: l.published,
    itemCount: (l.lesson_items as { count: number }[])?.[0]?.count ?? 0,
  }));
}

export async function fetchLesson(
  id: number,
): Promise<{ lesson: Lesson; chapterTitle: string } | null> {
  const { data } = await getSupabase()
    .from("lessons")
    .select("id, chapter_id, title, sort_order, published, chapters(title)")
    .eq("id", id)
    .single();
  if (!data) return null;
  return {
    lesson: { ...data, itemCount: 0 } as unknown as Lesson,
    chapterTitle: (data.chapters as unknown as { title: string })?.title ?? "",
  };
}

export async function fetchLessonItems(lessonId: number): Promise<LessonItem[]> {
  const { data } = await getSupabase()
    .from("lesson_items")
    .select(
      "id, lesson_id, kind, title, subtitle, body_html, video_url, pdf_url, exam_id, sort_order",
    )
    .eq("lesson_id", lessonId)
    .order("sort_order")
    .order("id");
  return (data as LessonItem[]) ?? [];
}

// Thông tin đề gắn vào mục luyện tập/kiểm tra (cần đăng nhập vì RLS exams)
export interface LessonExamMeta {
  id: number;
  title: string;
  duration_minutes: number;
  question_count: number;
  type_counts: TypeCounts;
}

export async function fetchExamMetas(examIds: number[]): Promise<Map<number, LessonExamMeta>> {
  if (examIds.length === 0) return new Map();
  const { data } = await getSupabase()
    .from("exams")
    .select("id, title, duration_minutes, question_count, type_counts")
    .in("id", examIds);
  return new Map(((data as LessonExamMeta[]) ?? []).map((e) => [e.id, e]));
}

/** Điểm cao nhất từng đề của học sinh — quyết định trạng thái "Đã làm". */
export async function fetchMyExamScores(userId: string): Promise<Map<number, number>> {
  const { data } = await getSupabase()
    .from("exam_results")
    .select("exam_id, score")
    .eq("student_id", userId);
  const best = new Map<number, number>();
  for (const r of data ?? []) {
    const prev = best.get(r.exam_id);
    if (prev === undefined || r.score > prev) best.set(r.exam_id, Number(r.score));
  }
  return best;
}

/** Các mục đã hoàn thành (xem lý thuyết/video…) của học sinh. */
export async function fetchMyProgress(userId: string): Promise<Set<number>> {
  const { data } = await getSupabase()
    .from("lesson_progress")
    .select("item_id")
    .eq("user_id", userId);
  return new Set((data ?? []).map((r) => r.item_id as number));
}

export async function markItemDone(userId: string, itemId: number) {
  await getSupabase()
    .from("lesson_progress")
    .upsert({ user_id: userId, item_id: itemId }, { ignoreDuplicates: true });
}
