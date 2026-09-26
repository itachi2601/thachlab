import {
  normalizeLessonItemKind,
  normalizeLessonKind,
  type Chapter,
  type Lesson,
  type LessonItem,
  type TypeCounts,
} from "@/features/lessons/types";
import type { Exam, ExamQuestion, QuestionResponse } from "@/features/exams/types";
import {
  buildQuestionResults,
  gradeQuestion,
  questionTopicNames,
} from "@/features/exams/types";
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
type LessonRow = Record<string, unknown> & { lesson_items?: { id: number; exam_ids: number[] | null }[] };

/** Tham chiếu gọn tới từng mục của bài (id + đề gắn) — đủ để tính tiến độ theo bài mà không cần tải nội dung mục. */
export interface LessonItemRef {
  id: number;
  exam_ids: number[];
}

/** Lesson kèm danh sách mục gọn (itemRefs) — fetchLessons trả về kiểu này; nơi khác vẫn dùng như Lesson. */
export type LessonWithItemRefs = Lesson & { itemRefs: LessonItemRef[] };

// lesson_items(id, exam_ids) thay cho lesson_items(count): cùng 1 truy vấn, thêm vài byte/mục,
// nhưng trang /lop-hoc và trang chủ HS không phải tải lesson_items lần nữa để tính tiến độ
// (index idx_lesson_items_lesson_cover phủ đúng 3 cột này).
export async function fetchLessons(includeDrafts = false): Promise<LessonWithItemRefs[]> {
  const withKind = getSupabase()
    .from("lessons")
    .select("id, chapter_id, title, sort_order, published, lesson_kind, description, lesson_items(id, exam_ids)")
    .order("sort_order")
    .order("id");
  const legacy = getSupabase()
    .from("lessons")
    .select("id, chapter_id, title, sort_order, published, lesson_items(id, exam_ids)")
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
    itemCount: l.lesson_items?.length ?? 0,
    description: (l.description as string) ?? "",
    itemRefs: (l.lesson_items ?? []).map((item) => ({ id: item.id, exam_ids: item.exam_ids ?? [] })),
  }));
}

export async function fetchLesson(
  id: number,
): Promise<{ lesson: Lesson; chapterTitle: string } | null> {
  const withKind = getSupabase()
    .from("lessons")
    .select("id, chapter_id, title, sort_order, published, lesson_kind, description, chapters(title)")
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
      description: (data.description as string) ?? "",
    } as unknown as Lesson,
    chapterTitle: (data.chapters as unknown as { title: string })?.title ?? "",
  };
}

// Cột due_at là migration mới (docs/supabase-migration-lesson-sections-v4.sql);
// required/quiz_min_correct/practice_pass_score là migration mới hơn nữa
// (docs/supabase-migration-learning-progress.sql) — chọn kèm khi có, tự lùi về
// danh sách cột cũ khi DB chưa chạy migration tương ứng.
const ITEM_COLUMNS =
  "id, lesson_id, kind, title, subtitle, body_html, video_url, pdf_url, questions, exam_ids, sort_order";
const ITEM_COLUMNS_V2 = `${ITEM_COLUMNS}, due_at`;
const ITEM_COLUMNS_V3 = `${ITEM_COLUMNS_V2}, required, quiz_min_correct, practice_pass_score`;
// Cột published_at/draft_payload/draft_saved_at là migration mới (nháp → đăng chính thức
// từng mục, docs/supabase-migration-lesson-item-draft-publish.sql) — chọn kèm khi có, tự
// lùi về V3 khi DB chưa chạy migration (coi như mọi mục đã đăng, giữ hành vi cũ).
const ITEM_COLUMNS_V4 = `${ITEM_COLUMNS_V3}, published_at, draft_payload, draft_saved_at`;

function toLessonItem(item: Record<string, unknown>): LessonItem {
  return {
    ...item,
    kind: normalizeLessonItemKind(item.kind),
    subtitle: item.subtitle ?? "",
    body_html: item.body_html ?? "",
    video_url: item.video_url ?? "",
    pdf_url: item.pdf_url ?? "",
    questions: item.questions ?? [],
    exam_ids: item.exam_ids ?? [],
    due_at: (item.due_at as string | null) ?? null,
    required: (item.required as boolean | undefined) ?? true,
    quiz_min_correct: (item.quiz_min_correct as number | null | undefined) ?? null,
    practice_pass_score: (item.practice_pass_score as number | null | undefined) ?? null,
    // "published_at" in item: cột có được chọn không (đã chạy migration) — không có thì
    // coi như đã đăng từ trước (giữ hành vi cũ, tránh ẩn nhầm nội dung cũ trước khi migrate).
    published_at: "published_at" in item ? (item.published_at as string | null) : "1970-01-01T00:00:00.000Z",
    draft_payload: (item.draft_payload as LessonItem["draft_payload"] | undefined) ?? null,
    draft_saved_at: (item.draft_saved_at as string | null | undefined) ?? null,
  } as unknown as LessonItem;
}

/**
 * Bài học + tên chương + toàn bộ mục trong MỘT truy vấn (select lồng qua FK lesson_items.lesson_id,
 * lessons.chapter_id). Dùng cho trang bài học. Nếu DB thiếu cột mới (chưa chạy migration) thì lùi về
 * fetchLesson + fetchLessonItems (song song) — hai hàm này tự thử lại với danh sách cột cũ.
 */
export async function fetchLessonWithItems(
  id: number,
): Promise<{ lesson: Lesson; chapterTitle: string; items: LessonItem[] } | null> {
  const res = await getSupabase()
    .from("lessons")
    .select(
      `id, chapter_id, title, sort_order, published, lesson_kind, description, chapters(title), lesson_items(${ITEM_COLUMNS_V4})`,
    )
    .eq("id", id)
    .order("sort_order", { referencedTable: "lesson_items" })
    .order("id", { referencedTable: "lesson_items" })
    .maybeSingle();
  if (res.error) {
    const [lesson, items] = await Promise.all([fetchLesson(id), fetchLessonItems(id)]);
    return lesson ? { ...lesson, items } : null;
  }
  const data = res.data as
    | (Record<string, unknown> & { chapters?: { title: string } | null; lesson_items?: Record<string, unknown>[] })
    | null;
  if (!data) return null;
  return {
    lesson: {
      id: data.id,
      chapter_id: data.chapter_id,
      title: data.title,
      sort_order: data.sort_order,
      published: data.published,
      lesson_kind: normalizeLessonKind(data.lesson_kind),
      itemCount: data.lesson_items?.length ?? 0,
      description: (data.description as string) ?? "",
    } as unknown as Lesson,
    chapterTitle: (data.chapters as unknown as { title: string } | null)?.title ?? "",
    items: (data.lesson_items ?? []).map(toLessonItem),
  };
}

export async function fetchLessonItems(lessonId: number): Promise<LessonItem[]> {
  const query = (columns: string) =>
    getSupabase()
      .from("lesson_items")
      .select(columns)
      .eq("lesson_id", lessonId)
      .order("sort_order")
      .order("id");
  let res = await query(ITEM_COLUMNS_V4);
  if (res.error) res = await query(ITEM_COLUMNS_V3);
  if (res.error) res = await query(ITEM_COLUMNS_V2);
  if (res.error) res = await query(ITEM_COLUMNS);
  if (res.error) throw res.error;
  return ((res.data ?? []) as unknown as Record<string, unknown>[]).map(toLessonItem);
}

// Thông tin đề gắn vào mục luyện tập/kiểm tra (cần đăng nhập vì RLS exams)
export interface LessonExamMeta {
  id: number;
  title: string;
  duration_minutes: number;
  question_count: number;
  type_counts: TypeCounts;
  pass_score: number | null;
}

// Đề "ẩn" (published = false) không trả về ở đây — phía học sinh coi như chưa gắn đề.
export async function fetchExamMetas(examIds: number[]): Promise<Map<number, LessonExamMeta>> {
  if (examIds.length === 0) return new Map();
  const withPassScore = await getSupabase()
    .from("exams")
    .select("id, title, duration_minutes, question_count, type_counts, pass_score")
    .eq("published", true)
    .in("id", examIds);
  const res = withPassScore.error
    ? await getSupabase()
        .from("exams")
        .select("id, title, duration_minutes, question_count, type_counts")
        .eq("published", true)
        .in("id", examIds)
    : withPassScore;
  return new Map(
    ((res.data as (LessonExamMeta & { pass_score?: number | null })[]) ?? []).map((e) => [
      e.id,
      { ...e, pass_score: e.pass_score ?? null },
    ]),
  );
}

/** Đề đầy đủ (kèm câu hỏi) — dùng cho lưới tự chấm của mục Luyện tập. Đề ẩn cũng không trả về. */
export async function fetchExamsFull(examIds: number[]): Promise<Map<number, Exam>> {
  if (examIds.length === 0) return new Map();
  const { data } = await getSupabase()
    .from("exams")
    .select("id, title, duration_minutes, published, questions")
    .eq("published", true)
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

/** Dấu "đã học" của học sinh: mục đã đánh dấu + đề đã từng làm — 2 truy vấn song song, không phụ thuộc danh sách bài. */
export interface MyProgressMarks {
  completedItems: Set<number>;
  completedExams: Set<number>;
}

export async function fetchMyProgressMarks(userId: string): Promise<MyProgressMarks> {
  const supabase = getSupabase();
  const [{ data: progressRows, error: progressError }, { data: resultRows, error: resultError }] = await Promise.all([
    supabase.from("lesson_progress").select("item_id").eq("user_id", userId),
    supabase.from("exam_results").select("exam_id").eq("student_id", userId),
  ]);
  if (progressError) throw progressError;
  if (resultError) throw resultError;
  return {
    completedItems: new Set((progressRows ?? []).map((row) => row.item_id as number)),
    completedExams: new Set((resultRows ?? []).map((row) => row.exam_id as number)),
  };
}

/** Tính tiến độ theo bài từ dữ liệu đã có (itemRefs của fetchLessons + dấu đã học) — không truy vấn. */
export function summarizeLessonProgress(
  lessons: { id: number; itemRefs: LessonItemRef[] }[],
  marks: MyProgressMarks,
): Map<number, LessonProgressSummary> {
  const summaries = new Map<number, LessonProgressSummary>();
  for (const lesson of lessons) {
    for (const item of lesson.itemRefs) {
      const current = summaries.get(lesson.id) ?? { completed: 0, total: 0 };
      current.total += 1;
      // Mục gắn đề tính là xong khi đã làm hết đề — khớp với isDone() ở trang bài học.
      const examsDone = item.exam_ids.length > 0 && item.exam_ids.every((id) => marks.completedExams.has(id));
      if (marks.completedItems.has(item.id) || examsDone) current.completed += 1;
      summaries.set(lesson.id, current);
    }
  }
  return summaries;
}

/** Tiến độ theo bài, gồm mục nội dung đã đánh dấu và đề đã từng làm (tự tải lesson_items). */
export async function fetchLessonProgressSummaries(
  userId: string,
  lessonIds: number[],
): Promise<Map<number, LessonProgressSummary>> {
  if (lessonIds.length === 0) return new Map();
  const [{ data: itemRows, error: itemError }, marks] = await Promise.all([
    getSupabase().from("lesson_items").select("id, lesson_id, exam_ids").in("lesson_id", lessonIds),
    fetchMyProgressMarks(userId),
  ]);
  if (itemError) throw itemError;
  const refsByLesson = new Map<number, LessonItemRef[]>();
  for (const row of itemRows ?? []) {
    const arr = refsByLesson.get(row.lesson_id) ?? [];
    arr.push({ id: row.id as number, exam_ids: (row.exam_ids as number[] | null) ?? [] });
    refsByLesson.set(row.lesson_id, arr);
  }
  return summarizeLessonProgress(
    Array.from(refsByLesson, ([id, itemRefs]) => ({ id, itemRefs })),
    marks,
  );
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

// ---------- Phiên luyện tập ----------
// Điểm luyện tập KHÔNG vào bảng điểm (không ghi exam_results); chỉ lưu ở
// practice_sessions + practice_question_results để em tự theo dõi và để phần
// Phân tích/Cảnh báo phụ đạo biết em hổng chủ đề nào.

export interface PracticePick {
  question: ExamQuestion;
  examId: number;
  sourceIndex: number;
}

export interface PracticeSessionInput {
  studentId: string;
  lessonId: number | null;
  itemId: number | null;
  picks: PracticePick[];
  responses: QuestionResponse[];
  score10: number;
  correctCount: number;
  durationSeconds: number;
  timedOut: boolean;
  /** Sinh 1 lần/phiên, giữ nguyên khi bấm lại — chống lưu trùng khi mạng lỗi rồi thử lại. */
  clientToken: string;
}

/** Lưu kết quả một phiên luyện tập. Lỗi ở đây chỉ mất dữ liệu phân tích — không chặn em xem lời giải. */
export async function savePracticeSession(input: PracticeSessionInput): Promise<boolean> {
  const supabase = getSupabase();
  try {
    const existing = await supabase
      .from("practice_sessions")
      .select("id")
      .eq("client_token", input.clientToken)
      .maybeSingle();
    let sessionId = existing.data?.id as number | undefined;
    if (!sessionId) {
      const base = {
        student_id: input.studentId,
        lesson_id: input.lessonId,
        item_id: input.itemId,
        question_count: input.picks.length,
        correct_count: input.correctCount,
        score: input.score10,
        duration_seconds: input.durationSeconds,
        timed_out: input.timedOut,
      };
      let res = await supabase
        .from("practice_sessions")
        .insert({ ...base, client_token: input.clientToken })
        .select("id")
        .single();
      // client_token là cột mới (migration chưa chạy) — lùi về insert không có token.
      if (res.error) res = await supabase.from("practice_sessions").insert(base).select("id").single();
      if (res.error || !res.data) return false;
      sessionId = res.data.id as number;
    }
    const data = { id: sessionId };

    const questions = input.picks.map((p) => p.question);
    const names = questionTopicNames(questions);
    const idByName = new Map<string, number>();
    if (names.length) {
      const { data: topics } = await supabase
        .from("question_topics")
        .select("id, name")
        .in("name", names);
      for (const t of topics ?? []) idByName.set(t.name as string, t.id as number);
    }
    const rows = buildQuestionResults(questions, input.responses, idByName).map((r, i) => ({
      session_id: data.id,
      question_index: r.question_index,
      student_id: input.studentId,
      exam_id: input.picks[i].examId,
      source_index: input.picks[i].sourceIndex,
      topic_id: r.topic_id,
      topic_name: r.topic_name,
      form: r.form,
      qtype: r.qtype,
      earned: r.earned,
      max: r.max,
      is_correct: r.is_correct,
    }));
    await supabase.from("practice_question_results").insert(rows);
    return true;
  } catch {
    return false;
  }
}
