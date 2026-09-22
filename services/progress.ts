// Quá trình học tập: gộp dữ liệu từ lesson_progress / practice_sessions /
// exam_results / exam_question_results / exam_attempts thành trạng thái
// hoàn thành/đạt theo features/progress/types.ts — không có bảng "progress"
// riêng, chỉ đọc tổng hợp từ các bảng đã có + cột mới của migration
// docs/supabase-migration-learning-progress.sql.

import type { LessonItem, LessonItemKind } from "@/features/lessons/types";
import { isExamKind } from "@/features/lessons/types";
import {
  deriveGradedStatus,
  derivePracticeStatus,
  deriveTheoryStatus,
  summarizeProgress,
  type ActivityStatus,
  type GradedAttemptSummary,
  type GradedStatusResult,
  type PracticeStatusResult,
  type ProgressCountable,
  type ProgressSummary,
  type TheoryQuizAttempt,
  type TheoryStatusResult,
} from "@/features/progress/types";
import { getSupabase } from "@/services/supabase";

// ---------- Một mục, đã tính trạng thái ----------
export interface ItemProgress {
  itemId: number;
  kind: LessonItemKind;
  required: boolean;
  /** Mục này có ngưỡng "đạt" do giáo viên cấu hình không (quyết định cách summarizeItemProgress tính % đạt). */
  hasThreshold: boolean;
  theory?: TheoryStatusResult;
  practice?: PracticeStatusResult & { sessionCount: number; bestScore10: number | null };
  graded?: GradedStatusResult;
  lastActivityAt: string | null;
}

function latestOf(...dates: (string | null | undefined)[]): string | null {
  const times = dates.filter((d): d is string => !!d).map((d) => Date.parse(d));
  if (times.length === 0) return null;
  return new Date(Math.max(...times)).toISOString();
}

/** Dữ liệu thô cần cho fetchMyLearningProgress — gom 1 lượt cho cả bài học. */
interface RawProgressData {
  confirmedItemIds: Set<number>;
  confirmedAt: Map<number, string>;
  quizAttemptsByExam: Map<number, TheoryQuizAttempt[]>;
  gradedResultsByExam: Map<number, GradedAttemptSummary[]>;
  openAttemptExamIds: Set<number>;
  practiceByItem: Map<number, { count: number; best: number | null; lastAt: string | null }>;
  examPassScoreById: Map<number, number | null>;
}

function emptyRaw(): RawProgressData {
  return {
    confirmedItemIds: new Set(),
    confirmedAt: new Map(),
    quizAttemptsByExam: new Map(),
    gradedResultsByExam: new Map(),
    openAttemptExamIds: new Set(),
    practiceByItem: new Map(),
    examPassScoreById: new Map(),
  };
}

/** Gộp 1 lượt cho nhiều học sinh cùng lúc (bảng giáo viên) hoặc 1 học sinh (trang bài học). */
async function fetchRawProgressBatch(
  studentIds: string[],
  items: LessonItem[],
): Promise<Map<string, RawProgressData>> {
  const out = new Map<string, RawProgressData>(studentIds.map((id) => [id, emptyRaw()]));
  if (studentIds.length === 0) return out;
  const supabase = getSupabase();
  const itemIds = items.map((i) => i.id);
  const examIds = [...new Set(items.filter((i) => isExamKind(i.kind) || i.kind === "ly_thuyet").flatMap((i) => i.exam_ids))];
  const practiceItemIds = items.filter((i) => i.kind === "luyen_tap").map((i) => i.id);

  const [progressRes, resultsRes, attemptsRes, practiceRes, examsRes] = await Promise.all([
    itemIds.length
      ? supabase.from("lesson_progress").select("user_id, item_id, done_at").in("user_id", studentIds).in("item_id", itemIds)
      : Promise.resolve({ data: [] as { user_id: string; item_id: number; done_at: string }[] }),
    examIds.length
      ? supabase
          .from("exam_results")
          .select("id, student_id, exam_id, created_at, score, detail")
          .in("student_id", studentIds)
          .in("exam_id", examIds)
      : Promise.resolve({
          data: [] as { id: number; student_id: string; exam_id: number; created_at: string; score: number; detail: unknown }[],
        }),
    examIds.length
      ? supabase
          .from("exam_attempts")
          .select("student_id, exam_id, submitted_at")
          .in("student_id", studentIds)
          .in("exam_id", examIds)
          .is("submitted_at", null)
      : Promise.resolve({ data: [] as { student_id: string; exam_id: number; submitted_at: string | null }[] }),
    practiceItemIds.length
      ? supabase
          .from("practice_sessions")
          .select("student_id, item_id, score, created_at")
          .in("student_id", studentIds)
          .in("item_id", practiceItemIds)
      : Promise.resolve({ data: [] as { student_id: string; item_id: number; score: number; created_at: string }[] }),
    examIds.length
      ? supabase.from("exams").select("id, pass_score").in("id", examIds)
      : Promise.resolve({ data: [] as { id: number; pass_score: number | null }[] }),
  ]);

  const resultIds = (resultsRes.data ?? []).map((r) => r.id);
  const scoresRes = resultIds.length
    ? await supabase.from("exam_result_scores").select("exam_result_id, final_score10, pending_essay_count").in("exam_result_id", resultIds)
    : { data: [] as { exam_result_id: number; final_score10: number | null; pending_essay_count: number }[] };
  const scoreByResultId = new Map((scoresRes.data ?? []).map((s) => [s.exam_result_id, s]));
  const examPassScoreById = new Map((examsRes.data ?? []).map((e) => [e.id, e.pass_score ?? null]));

  for (const row of progressRes.data ?? []) {
    const raw = out.get(row.user_id);
    if (!raw) continue;
    raw.confirmedItemIds.add(row.item_id);
    raw.confirmedAt.set(row.item_id, row.done_at);
  }

  for (const row of resultsRes.data ?? []) {
    const raw = out.get(row.student_id);
    if (!raw) continue;
    const detail = (row.detail as { correctCount?: number } | null) ?? null;
    const correctCount = typeof detail?.correctCount === "number" ? detail.correctCount : 0;
    const quiz = raw.quizAttemptsByExam.get(row.exam_id) ?? [];
    quiz.push({ createdAt: row.created_at, correctCount });
    raw.quizAttemptsByExam.set(row.exam_id, quiz);

    const scoreRow = scoreByResultId.get(row.id);
    const graded = raw.gradedResultsByExam.get(row.exam_id) ?? [];
    graded.push({
      createdAt: row.created_at,
      score10: Number(row.score),
      finalScore10: scoreRow?.final_score10 ?? null,
      pendingEssayCount: scoreRow?.pending_essay_count ?? 0,
    });
    raw.gradedResultsByExam.set(row.exam_id, graded);
  }

  for (const row of attemptsRes.data ?? []) {
    out.get(row.student_id)?.openAttemptExamIds.add(row.exam_id);
  }

  for (const row of practiceRes.data ?? []) {
    if (row.item_id === null) continue;
    const raw = out.get(row.student_id);
    if (!raw) continue;
    const cur = raw.practiceByItem.get(row.item_id) ?? { count: 0, best: null, lastAt: null };
    cur.count += 1;
    cur.best = cur.best === null ? Number(row.score) : Math.max(cur.best, Number(row.score));
    cur.lastAt = latestOf(cur.lastAt, row.created_at);
    raw.practiceByItem.set(row.item_id, cur);
  }

  for (const raw of out.values()) raw.examPassScoreById = examPassScoreById;
  return out;
}

function buildItemProgress(items: LessonItem[], raw: RawProgressData): Map<number, ItemProgress> {
  const out = new Map<number, ItemProgress>();

  for (const item of items) {
    if (item.kind === "video" || item.kind === "bai_tap_mau") {
      // Không có khái niệm "đạt" — chỉ tự xác nhận hoàn thành, tái dùng lesson_progress.
      out.set(item.id, {
        itemId: item.id,
        kind: item.kind,
        required: item.required,
        hasThreshold: false,
        lastActivityAt: raw.confirmedAt.get(item.id) ?? null,
      });
      continue;
    }

    if (item.kind === "ly_thuyet") {
      const hasQuiz = item.exam_ids.length > 0;
      const attempts = hasQuiz ? item.exam_ids.flatMap((id) => raw.quizAttemptsByExam.get(id) ?? []) : [];
      const theory = deriveTheoryStatus({
        confirmedRead: raw.confirmedItemIds.has(item.id),
        quizAttempts: attempts,
        minCorrect: hasQuiz ? item.quiz_min_correct : null,
      });
      out.set(item.id, {
        itemId: item.id,
        kind: item.kind,
        required: item.required,
        hasThreshold: hasQuiz && item.quiz_min_correct !== null,
        theory,
        lastActivityAt: latestOf(raw.confirmedAt.get(item.id), ...attempts.map((a) => a.createdAt)),
      });
      continue;
    }

    if (item.kind === "luyen_tap") {
      const p = raw.practiceByItem.get(item.id) ?? { count: 0, best: null, lastAt: null };
      const practice = derivePracticeStatus({
        sessionCount: p.count,
        bestScore10: p.best,
        passScore: item.practice_pass_score,
      });
      out.set(item.id, {
        itemId: item.id,
        kind: item.kind,
        required: item.required,
        hasThreshold: item.practice_pass_score !== null,
        practice: { ...practice, sessionCount: p.count, bestScore10: p.best },
        lastActivityAt: p.lastAt,
      });
      continue;
    }

    // bai_tap_ve_nha / kiem_tra
    const results = item.exam_ids.flatMap((id) => raw.gradedResultsByExam.get(id) ?? []);
    const hasOpenAttempt = item.exam_ids.some((id) => raw.openAttemptExamIds.has(id));
    const passScore = item.exam_ids.length === 1 ? (raw.examPassScoreById.get(item.exam_ids[0]) ?? null) : null;
    const graded = deriveGradedStatus({ hasOpenAttempt, results, passScore });
    out.set(item.id, {
      itemId: item.id,
      kind: item.kind,
      required: item.required,
      hasThreshold: passScore !== null,
      graded,
      lastActivityAt: latestOf(...results.map((r) => r.createdAt)),
    });
  }

  return out;
}

/** Trạng thái từng mục của MỘT bài học cho học sinh đang xem — dùng ở trang bài học. */
export async function fetchMyLearningProgress(
  studentId: string,
  items: LessonItem[],
): Promise<Map<number, ItemProgress>> {
  const raw = (await fetchRawProgressBatch([studentId], items)).get(studentId) ?? emptyRaw();
  return buildItemProgress(items, raw);
}

/** Trạng thái từng mục của MỘT bài học cho CẢ LỚP — dùng ở bảng "Quá trình học tập" của giáo viên. */
export async function fetchClassLearningProgress(
  studentIds: string[],
  items: LessonItem[],
): Promise<Map<string, Map<number, ItemProgress>>> {
  const rawByStudent = await fetchRawProgressBatch(studentIds, items);
  const out = new Map<string, Map<number, ItemProgress>>();
  for (const [studentId, raw] of rawByStudent) out.set(studentId, buildItemProgress(items, raw));
  return out;
}

/** % hoàn thành / % đạt trên các mục bắt buộc của một bài học — dùng cho thanh tiến độ. */
export function summarizeItemProgress(progress: Map<number, ItemProgress>, items: LessonItem[]): ProgressSummary {
  const countable: ProgressCountable[] = items.map((item) => {
    const p = progress.get(item.id);
    const status: ActivityStatus = p?.theory?.status ?? p?.practice?.status ?? p?.graded?.status ?? (p?.lastActivityAt ? "submitted" : "not_started");
    return { required: item.required, status, hasThreshold: p?.hasThreshold ?? false };
  });
  return summarizeProgress(countable);
}

// ---------- Bắt đầu/nộp một lượt làm (exam_attempts) — best-effort ----------
export async function startExamAttempt(
  studentId: string,
  clientToken: string,
  examId: number,
  itemId: number | null,
): Promise<void> {
  try {
    await getSupabase()
      .from("exam_attempts")
      .upsert({ client_token: clientToken, student_id: studentId, exam_id: examId, item_id: itemId }, { onConflict: "client_token", ignoreDuplicates: true });
  } catch {
    /* chỉ mất tín hiệu "đang thực hiện" — không chặn làm bài */
  }
}

export async function finishExamAttempt(clientToken: string, examResultId: number): Promise<void> {
  try {
    await getSupabase()
      .from("exam_attempts")
      .update({ submitted_at: new Date().toISOString(), exam_result_id: examResultId })
      .eq("client_token", clientToken);
  } catch {
    /* không ảnh hưởng điểm đã lưu */
  }
}

// ---------- Chống nộp trùng khi thử lại sau lỗi mạng ----------
// Trước khi insert, kiểm tra đã có dòng với client_token này chưa (đọc được
// qua policy "đọc/của mình" sẵn có) — nếu có rồi thì coi như đã lưu, không
// insert lại. Không cần policy UPDATE mới trên bảng điểm.
export async function findExistingExamResultId(clientToken: string): Promise<number | null> {
  const { data } = await getSupabase().from("exam_results").select("id").eq("client_token", clientToken).maybeSingle();
  return (data?.id as number | undefined) ?? null;
}

export async function findExistingPracticeSessionId(clientToken: string): Promise<number | null> {
  const { data } = await getSupabase().from("practice_sessions").select("id").eq("client_token", clientToken).maybeSingle();
  return (data?.id as number | undefined) ?? null;
}

// ---------- Lịch sử học tập của một học sinh (hồ sơ học sinh phía giáo viên) ----------
export interface LearningHistoryEntry {
  at: string;
  activity: "theory" | "practice" | "exam";
  title: string;
  detail: string;
}

export async function fetchStudentLearningHistory(studentId: string): Promise<LearningHistoryEntry[]> {
  const supabase = getSupabase();
  const [progressRes, practiceRes, resultsRes] = await Promise.all([
    supabase
      .from("lesson_progress")
      .select("item_id, done_at, lesson_items(title, lessons(title))")
      .eq("user_id", studentId)
      .order("done_at", { ascending: false })
      .limit(100),
    supabase
      .from("practice_sessions")
      .select("id, score, correct_count, question_count, created_at, lessons(title)")
      .eq("student_id", studentId)
      .order("created_at", { ascending: false })
      .limit(100),
    supabase
      .from("exam_results")
      .select("id, score, created_at, detail, exams(title, questions)")
      .eq("student_id", studentId)
      .order("created_at", { ascending: false })
      .limit(100),
  ]);

  const entries: LearningHistoryEntry[] = [];

  for (const row of (progressRes.data ?? []) as unknown as Record<string, unknown>[]) {
    const item = Array.isArray(row.lesson_items) ? row.lesson_items[0] : row.lesson_items;
    const lesson = item && Array.isArray((item as Record<string, unknown>).lessons)
      ? ((item as Record<string, unknown>).lessons as unknown[])[0]
      : (item as Record<string, unknown> | null)?.lessons;
    entries.push({
      at: row.done_at as string,
      activity: "theory",
      title: `${(lesson as { title?: string } | null)?.title ?? ""} — ${(item as { title?: string } | null)?.title ?? ""}`,
      detail: "Đã tự xác nhận đọc",
    });
  }

  for (const row of (practiceRes.data ?? []) as unknown as Record<string, unknown>[]) {
    const lesson = Array.isArray(row.lessons) ? row.lessons[0] : row.lessons;
    entries.push({
      at: row.created_at as string,
      activity: "practice",
      title: (lesson as { title?: string } | null)?.title ?? "Luyện tập",
      detail: `${row.score} điểm · đúng ${row.correct_count}/${row.question_count} câu`,
    });
  }

  for (const row of (resultsRes.data ?? []) as unknown as Record<string, unknown>[]) {
    const exam = Array.isArray(row.exams) ? row.exams[0] : row.exams;
    const detail = row.detail as { correctCount?: number } | null;
    const hasEssay = ((exam as { questions?: { type: string }[] } | null)?.questions ?? []).some((q) => q.type === "essay");
    entries.push({
      at: row.created_at as string,
      activity: "exam",
      title: (exam as { title?: string } | null)?.title ?? "Đề kiểm tra",
      detail: `${row.score} điểm${detail?.correctCount != null ? ` · đúng ${detail.correctCount} câu` : ""}${hasEssay ? " · có câu tự luận" : ""}`,
    });
  }

  return entries.sort((a, b) => Date.parse(b.at) - Date.parse(a.at));
}

// ---------- Chờ chấm: hàng đợi câu tự luận ----------
export interface PendingEssay {
  examResultId: number;
  questionIndex: number;
  studentId: string;
  studentName: string;
  examId: number;
  examTitle: string;
  question: string;
  answer: string;
  submittedAt: string;
}

export async function fetchPendingEssays(studentIds: string[]): Promise<PendingEssay[]> {
  if (studentIds.length === 0) return [];
  const supabase = getSupabase();
  const { data, error } = await supabase
    .from("exam_question_results")
    .select(
      "exam_result_id, question_index, student_id, exam_id, qtype, graded_at, exam_results(created_at, detail), exams(title, questions), profiles(full_name)",
    )
    .eq("qtype", "essay")
    .is("graded_at", null)
    .in("student_id", studentIds);
  if (error || !data) return [];
  return (data as unknown as Record<string, unknown>[]).map((row) => {
    const examResult = Array.isArray(row.exam_results) ? row.exam_results[0] : row.exam_results;
    const exam = Array.isArray(row.exams) ? row.exams[0] : row.exams;
    const profile = Array.isArray(row.profiles) ? row.profiles[0] : row.profiles;
    const detail = (examResult as { detail?: { responses?: unknown[] } } | null)?.detail;
    const questionIndex = row.question_index as number;
    const questions = ((exam as { questions?: { question: string }[] } | null)?.questions ?? []) as { question: string }[];
    const responses = (detail?.responses ?? []) as string[];
    return {
      examResultId: row.exam_result_id as number,
      questionIndex,
      studentId: row.student_id as string,
      studentName: (profile as { full_name?: string } | null)?.full_name ?? "",
      examId: row.exam_id as number,
      examTitle: (exam as { title?: string } | null)?.title ?? "",
      question: questions[questionIndex]?.question ?? "",
      answer: typeof responses[questionIndex] === "string" ? responses[questionIndex] : "",
      submittedAt: (examResult as { created_at?: string } | null)?.created_at ?? "",
    };
  });
}

export async function gradeEssayAnswer(
  examResultId: number,
  questionIndex: number,
  earned: number,
  max: number,
): Promise<{ ok: true } | { ok: false; message: string }> {
  const { error } = await getSupabase().rpc("grade_essay_answer", {
    p_exam_result_id: examResultId,
    p_question_index: questionIndex,
    p_earned: earned,
    p_max: max,
  });
  if (error) return { ok: false, message: error.message };
  return { ok: true };
}
