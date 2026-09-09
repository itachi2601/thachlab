import {
  normalizeLessonItemKind,
  normalizeLessonKind,
  type Chapter,
  type Lesson,
  type LessonItem,
  type TypeCounts,
} from "@/features/lessons/types";
import type { Exam, ExamQuestion, QuestionResponse } from "@/features/exams/types";
import { gradeQuestion } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

interface ClassRef {
  class_id: number;
}

export async function fetchChapters(): Promise<Chapter[]> {
  const { data } = await getSupabase()
    .from("chapters")
    .select("id, title, sort_order, subject_code, chapter_classes(class_id)")
    .order("sort_order")
    .order("id");
  return (data ?? []).map((c) => ({
    id: c.id,
    title: c.title,
    sort_order: c.sort_order,
    classIds: ((c.chapter_classes as ClassRef[]) ?? []).map((r) => r.class_id),
    subjectCode: c.subject_code ?? "vat-ly",
  }));
}

// Cột lesson_kind là migration mới (docs/supabase-migration-lessons-periodic-exam.sql).
// Chọn kèm khi có, tự lùi về danh sách cột cũ khi DB chưa chạy migration.
type LessonRow = Record<string, unknown> & { lesson_items?: { count: number }[] };

export async function fetchLessons(includeDrafts = false): Promise<Lesson[]> {
  const withKind = getSupabase()
    .from("lessons")
    .select("id, chapter_id, title, sort_order, published, lesson_kind, lesson_items(count)")
    .order("sort_order")
    .order("id");
  const legacy = getSupabase()
    .from("lessons")
    .select("id, chapter_id, title, sort_order, published, lesson_items(count)")
    .order("sort_order")
    .order("id");
  const primary = await (includeDrafts ? withKind : withKind.eq("published", true));
  const res = primary.error
    ? await (includeDrafts ? legacy : legacy.eq("published", true))
    : primary;
  return ((res.data ?? []) as LessonRow[]).map((l) => ({
    id: l.id as number,
    chapter_id: l.chapter_id as number,
    title: l.title as string,
    sort_order: l.sort_order as number,
    published: l.published as boolean,
    lesson_kind: normalizeLessonKind(l.lesson_kind),
    itemCount: l.lesson_items?.[0]?.count ?? 0,
  }));
}

export async function fetchLesson(
  id: number,
): Promise<{ lesson: Lesson; chapterTitle: string } | null> {
  const withKind = getSupabase()
    .from("lessons")
    .select("id, chapter_id, title, sort_order, published, lesson_kind, chapters(title)")
    .eq("id", id)
    .single();
  const legacy = getSupabase()
    .from("lessons")
    .select("id, chapter_id, title, sort_order, published, chapters(title)")
    .eq("id", id)
    .single();
  const primary = await withKind;
  const res = primary.error ? await legacy : primary;
  const data = res.data as (Record<string, unknown> & { chapters?: { title: string } }) | null;
  if (!data) return null;
  return {
    lesson: {
      id: data.id,
      chapter_id: data.chapter_id,
      title: data.title,
      sort_order: data.sort_order,
      published: data.published,
      lesson_kind: normalizeLessonKind(data.lesson_kind),
      itemCount: 0,
    } as unknown as Lesson,
    chapterTitle: (data.chapters as unknown as { title: string })?.title ?? "",
  };
}

export async function fetchLessonItems(lessonId: number): Promise<LessonItem[]> {
  const { data, error } = await getSupabase()
    .from("lesson_items")
    .select(
      "id, lesson_id, kind, title, subtitle, body_html, video_url, pdf_url, questions, exam_ids, sort_order",
    )
    .eq("lesson_id", lessonId)
    .order("sort_order")
    .order("id");
  if (error) throw error;
  return (data ?? []).map((item) => ({
    ...item,
    kind: normalizeLessonItemKind(item.kind),
    subtitle: item.subtitle ?? "",
    body_html: item.body_html ?? "",
    video_url: item.video_url ?? "",
    pdf_url: item.pdf_url ?? "",
    questions: item.questions ?? [],
    exam_ids: item.exam_ids ?? [],
  })) as LessonItem[];
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

/** Đề đầy đủ (kèm câu hỏi) — dùng cho lưới tự chấm của mục Luyện tập. */
export async function fetchExamsFull(examIds: number[]): Promise<Map<number, Exam>> {
  if (examIds.length === 0) return new Map();
  const { data } = await getSupabase()
    .from("exams")
    .select("id, title, duration_minutes, published, questions")
    .in("id", examIds);
  return new Map(((data as Exam[]) ?? []).map((e) => [e.id, e]));
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

/** Danh sách item_id của từng bài học — dùng để tính % tiến độ theo bài/chương. */
export async function fetchItemIdsByLessons(
  lessonIds: number[],
): Promise<Map<number, number[]>> {
  if (lessonIds.length === 0) return new Map();
  const { data } = await getSupabase()
    .from("lesson_items")
    .select("id, lesson_id")
    .in("lesson_id", lessonIds);
  const map = new Map<number, number[]>();
  for (const row of data ?? []) {
    const arr = map.get(row.lesson_id) ?? [];
    arr.push(row.id);
    map.set(row.lesson_id, arr);
  }
  return map;
}

export interface LessonProgressSummary {
  completed: number;
  total: number;
}

/** Tiến độ theo bài, gồm mục nội dung đã đánh dấu và đề đã từng làm. */
export async function fetchLessonProgressSummaries(
  userId: string,
  lessonIds: number[],
): Promise<Map<number, LessonProgressSummary>> {
  if (lessonIds.length === 0) return new Map();
  const supabase = getSupabase();
  const [{ data: itemRows, error: itemError }, { data: progressRows, error: progressError }, { data: resultRows, error: resultError }] = await Promise.all([
    supabase.from("lesson_items").select("id, lesson_id, exam_ids").in("lesson_id", lessonIds),
    supabase.from("lesson_progress").select("item_id").eq("user_id", userId),
    supabase.from("exam_results").select("exam_id").eq("student_id", userId),
  ]);
  if (itemError) throw itemError;
  if (progressError) throw progressError;
  if (resultError) throw resultError;

  const completedItems = new Set((progressRows ?? []).map((row) => row.item_id as number));
  const completedExams = new Set((resultRows ?? []).map((row) => row.exam_id as number));
  const summaries = new Map<number, LessonProgressSummary>();
  for (const row of itemRows ?? []) {
    const current = summaries.get(row.lesson_id) ?? { completed: 0, total: 0 };
    current.total += 1;
    // Mục gắn đề tính là xong khi đã làm hết đề — khớp với isDone() ở trang bài học.
    const examIds = (row.exam_ids as number[] | null) ?? [];
    const examsDone = examIds.length > 0 && examIds.every((id) => completedExams.has(id));
    if (completedItems.has(row.id) || examsDone) current.completed += 1;
    summaries.set(row.lesson_id, current);
  }
  return summaries;
}

export async function markItemDone(userId: string, itemId: number) {
  await getSupabase()
    .from("lesson_progress")
    .upsert({ user_id: userId, item_id: itemId }, { ignoreDuplicates: true });
}

export interface MistakeReviewItem {
  examId: number;
  examTitle: string;
  questionIndex: number;
  question: ExamQuestion;
  response: QuestionResponse;
}

/** Câu chưa đạt trọn điểm trong lần làm gần nhất của từng đề. */
export async function fetchMyLatestMistakes(userId: string): Promise<MistakeReviewItem[]> {
  const { data, error } = await getSupabase()
    .from("exam_results")
    .select("exam_id, created_at, detail, exams(id, title, questions)")
    .eq("student_id", userId)
    .order("created_at", { ascending: false });
  if (error) throw error;

  const seenExamIds = new Set<number>();
  const mistakes: MistakeReviewItem[] = [];
  for (const row of data ?? []) {
    if (seenExamIds.has(row.exam_id)) continue;
    seenExamIds.add(row.exam_id);
    const examValue = Array.isArray(row.exams) ? row.exams[0] : row.exams;
    const exam = examValue as { id: number; title: string; questions: ExamQuestion[] } | null;
    const detail = row.detail as { responses?: QuestionResponse[] } | null;
    if (!exam?.questions || !detail?.responses) continue;
    exam.questions.forEach((question, index) => {
      const response = detail.responses?.[index] ?? (question.type === "true_false" ? [null, null, null, null] : question.type === "short_answer" || question.type === "essay" ? "" : null);
      const grade = gradeQuestion(question, response);
      if (grade.earned < grade.max) {
        mistakes.push({ examId: exam.id, examTitle: exam.title, questionIndex: index, question, response });
      }
    });
  }
  return mistakes;
}
