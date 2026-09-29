// BTVN ôn tập tự động, tạo từ màn hình Trình chiếu chữa bài (ReviewBoard).
// 10 câu cả lớp sai nhiều nhất trong đề vừa chữa + 20 câu ngẫu nhiên từ ngân hàng
// câu hỏi (mọi yêu cầu cần đạt của các bài học TRƯỚC bài vừa kiểm tra).
// Xem docs/supabase-migration-class-review-homework.sql.

import type { Chapter } from "@/features/lessons/types";
import type { LessonWithItemRefs } from "@/services/lessons";
import { pickRandom, type ExamQuestion } from "@/features/exams/types";
import { fetchQuestionTopics } from "@/services/analytics";
import { fetchBankQuestions, toExamQuestion } from "@/services/question-bank";
import { setItemClasses } from "@/services/classes";
import { fetchSeasons, upsertSources } from "@/services/rank";
import { getSupabase } from "@/services/supabase";

/** Vị trí một bài học trong thứ tự chương → bài, dùng để so sánh "trước/sau". */
export interface LessonBoundary {
  lessonId: number;
  chapterId: number;
  chapterSortOrder: number;
  lessonSortOrder: number;
}

/** Tìm bài học sở hữu một đề, qua lesson_items.exam_ids đã tải sẵn trong `lessons`. */
export function findLessonBoundary(
  examId: number,
  lessons: LessonWithItemRefs[],
  chapters: Chapter[],
): LessonBoundary | null {
  const lesson = lessons.find((l) => l.itemRefs.some((r) => r.exam_ids.includes(examId)));
  if (!lesson) return null;
  const chapter = chapters.find((c) => c.id === lesson.chapter_id);
  if (!chapter) return null;
  return {
    lessonId: lesson.id,
    chapterId: chapter.id,
    chapterSortOrder: chapter.sort_order,
    lessonSortOrder: lesson.sort_order,
  };
}

/** Id các bài học nằm TRƯỚC một mốc (chapter.sort_order rồi lesson.sort_order). */
export function lessonIdsBefore(
  boundaryLessonId: number,
  lessons: LessonWithItemRefs[],
  chapters: Chapter[],
): number[] {
  const chapterOrder = new Map(chapters.map((c) => [c.id, c.sort_order]));
  const boundary = lessons.find((l) => l.id === boundaryLessonId);
  if (!boundary) return [];
  const boundaryChapterOrder = chapterOrder.get(boundary.chapter_id) ?? 0;
  return lessons
    .filter((l) => {
      const co = chapterOrder.get(l.chapter_id) ?? 0;
      if (co !== boundaryChapterOrder) return co < boundaryChapterOrder;
      return l.sort_order < boundary.sort_order;
    })
    .map((l) => l.id);
}

/**
 * Id các chủ đề (ưu tiên chủ đề con — yêu cầu cần đạt) của một danh sách bài học, cho
 * một khối lớp. Nhiều bài chưa được gắn YCCĐ con (danh mục còn đang xây dần) — bài nào
 * chưa có YCCĐ thì lùi về lấy tạm chủ đề tầng bài (parent_id null) của chính bài đó,
 * để không bỏ trắng hoàn toàn phạm vi ôn tập.
 */
export async function outcomeTopicIdsForLessons(grade: string, lessonIds: number[]): Promise<number[]> {
  if (!lessonIds.length) return [];
  const topics = await fetchQuestionTopics(grade);
  const lessonSet = new Set(lessonIds);
  const byLesson = new Map<number, number[]>();
  for (const t of topics) {
    if (t.parentId === null || t.lessonId === null || !lessonSet.has(t.lessonId)) continue;
    const arr = byLesson.get(t.lessonId) ?? [];
    arr.push(t.id);
    byLesson.set(t.lessonId, arr);
  }
  for (const t of topics) {
    if (t.parentId !== null || t.lessonId === null || !lessonSet.has(t.lessonId)) continue;
    if (!byLesson.get(t.lessonId)?.length) byLesson.set(t.lessonId, [t.id]);
  }
  return [...byLesson.values()].flat();
}

// fetchBankQuestions sắp theo topic_id rồi mới limit — trần phải đủ lớn để lấy hết pool
// thật (không chỉ N dòng đầu theo topic_id thấp), nếu không pickRandom() sẽ thiên vị về
// phía chủ đề có id nhỏ. Ngân hàng một khối/một môn hiếm khi vượt mốc này.
export const BANK_POOL_LIMIT = 4000;

export interface CreateReviewHomeworkInput {
  classId: number;
  sourceExamId: number;
  subjectCode: string;
  title: string;
  wrongQuestions: ExamQuestion[]; // đúng 10 câu sai nhiều nhất, đã cắt sẵn từ đề đang chữa
  grade: string;
  topicIds: number[]; // yêu cầu cần đạt của các bài học trước, để bốc câu ngân hàng
  randomCount?: number; // mặc định 20
  durationMinutes?: number; // mặc định 40
  createdBy: string;
}

export interface CreateReviewHomeworkResult {
  examId: number;
  homeworkId: number;
  bankCount: number;
}

/**
 * Tạo đề BTVN mới (10 câu sai + N câu ngân hàng ngẫu nhiên), gán cho lớp, đăng ký
 * làm nguồn RP nếu lớp đang có mùa rank mở, rồi ghi 1 dòng class_review_homework.
 * Có lỗi giữa chừng thì xoá đề vừa tạo (không để đề mồ côi).
 */
export async function createReviewHomework(
  input: CreateReviewHomeworkInput,
): Promise<CreateReviewHomeworkResult> {
  const supabase = getSupabase();
  const randomCount = input.randomCount ?? 20;
  const durationMinutes = input.durationMinutes ?? 40;

  const pool = input.topicIds.length
    ? await fetchBankQuestions({ grade: input.grade, topicIds: input.topicIds, limit: BANK_POOL_LIMIT })
    : [];
  const bankPicks = pickRandom(
    pool.filter((q) => q.sourceExamId !== input.sourceExamId),
    randomCount,
  ).map(toExamQuestion);

  const questions: ExamQuestion[] = [...input.wrongQuestions, ...bankPicks];

  let examId: number | null = null;
  try {
    const { data: examRow, error: examErr } = await supabase
      .from("exams")
      .insert({
        title: input.title,
        duration_minutes: durationMinutes,
        published: true,
        subject_code: input.subjectCode,
        questions,
      })
      .select("id")
      .single();
    if (examErr || !examRow) throw new Error(`Tạo đề lỗi: ${examErr?.message}`);
    examId = examRow.id as number;

    await setItemClasses("exam_classes", "exam_id", examId, [input.classId]);

    const seasons = await fetchSeasons();
    const activeSeason = seasons.find(
      (s) => s.status === "active" && (s.class_ids.length === 0 || s.class_ids.includes(input.classId)),
    );
    if (activeSeason) {
      await upsertSources([
        { season_id: activeSeason.id, source_kind: "exam", source_id: examId, max_rp: 20, enabled: true },
      ]);
    }

    const { data: hwRow, error: hwErr } = await supabase
      .from("class_review_homework")
      .insert({
        class_id: input.classId,
        source_exam_id: input.sourceExamId,
        exam_id: examId,
        title: input.title,
        wrong_count: input.wrongQuestions.length,
        bank_count: bankPicks.length,
        created_by: input.createdBy,
      })
      .select("id")
      .single();
    if (hwErr || !hwRow) throw new Error(`Ghi gói BTVN lỗi: ${hwErr?.message}`);

    return { examId, homeworkId: hwRow.id as number, bankCount: bankPicks.length };
  } catch (e) {
    if (examId !== null) await supabase.from("exams").delete().eq("id", examId);
    throw e;
  }
}

export interface ClassReviewHomework {
  id: number;
  classId: number;
  examId: number;
  title: string;
  wrongCount: number;
  bankCount: number;
  createdAt: string;
}

/** BTVN ôn tập của một lớp, mới nhất trước — dùng ở trang chủ học sinh. */
export async function fetchOpenClassReviewHomework(classId: number): Promise<ClassReviewHomework[]> {
  const { data, error } = await getSupabase()
    .from("class_review_homework")
    .select("id, class_id, exam_id, title, wrong_count, bank_count, created_at")
    .eq("class_id", classId)
    .order("created_at", { ascending: false })
    .limit(10);
  if (error) throw new Error(error.message);
  return (data ?? []).map((r) => ({
    id: r.id as number,
    classId: r.class_id as number,
    examId: r.exam_id as number,
    title: r.title as string,
    wrongCount: (r.wrong_count as number) ?? 0,
    bankCount: (r.bank_count as number) ?? 0,
    createdAt: r.created_at as string,
  }));
}
