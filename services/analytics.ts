import { getSupabase } from "@/services/supabase";
import {
  gradeQuestion,
  type ExamQuestion,
  type QuestionResponse,
} from "@/features/exams/types";

// ============================================================
// Kiểu dùng chung
// ============================================================
export interface ScorePoint {
  resultId: number;
  examId: number;
  examTitle: string;
  score: number;
  at: string; // ISO
  periodic: boolean; // là bài kiểm tra định kỳ của lớp?
  kindLabel: string; // "Giữa kỳ" / "Cuối kỳ" / …
}

export interface TopicGap {
  key: string; // `${topic}|${form}`
  topicId: number | null;
  topic: string;
  form: string; // "ly_thuyet" | "bai_tap" | ""
  total: number;
  wrong: number;
  pct: number; // % sai, 0..100
}

export interface WrongQuestionRef {
  examId: number;
  examTitle: string;
  examResultId: number;
  questionIndex: number;
  topic: string;
  form: string;
}

interface EqrRow {
  exam_result_id: number;
  exam_id: number;
  question_index: number;
  topic_name: string;
  topic_id: number | null;
  form: string;
  is_correct: boolean;
}

interface AssessmentMeta {
  exam_id: number;
  kind: string;
  sequence: number | null;
  published_at: string;
}

const KIND_LABEL: Record<string, string> = {
  giua_ki: "Giữa kỳ",
  cuoi_ki: "Cuối kỳ",
  chuong: "KT chương",
  thuong_xuyen: "KT thường xuyên",
};

function pct(wrong: number, total: number) {
  return total > 0 ? Math.round((wrong / total) * 100) : 0;
}

// ============================================================
// HỌC SINH
// ============================================================

/** Điểm các bài kiểm tra của học sinh theo thời gian (điểm cao nhất mỗi đề). */
export async function fetchMyScoreHistory(userId: string): Promise<ScorePoint[]> {
  const supabase = getSupabase();
  const [{ data: results }, { data: assessments }] = await Promise.all([
    supabase
      .from("exam_results")
      .select("id, exam_id, score, created_at, exams(title)")
      .eq("student_id", userId)
      .order("created_at", { ascending: true }),
    supabase.from("class_assessments").select("exam_id, kind, sequence, published_at"),
  ]);

  const meta = new Map<number, AssessmentMeta>();
  for (const a of (assessments as AssessmentMeta[]) ?? []) meta.set(a.exam_id, a);

  return ((results ?? []) as {
    id: number;
    exam_id: number;
    score: number;
    created_at: string;
    exams: { title: string } | { title: string }[] | null;
  }[]).map((row) => {
    const examMeta = meta.get(row.exam_id);
    const examValue = Array.isArray(row.exams) ? row.exams[0] : row.exams;
    return {
      resultId: row.id,
      examId: row.exam_id,
      examTitle: examValue?.title ?? "(Đề đã xóa)",
      score: Number(row.score),
      at: row.created_at,
      periodic: Boolean(examMeta),
      kindLabel: examMeta ? (KIND_LABEL[examMeta.kind] ?? "") : "",
    };
  });
}

async function fetchMyEqr(userId: string): Promise<EqrRow[]> {
  const { data } = await getSupabase()
    .from("exam_question_results")
    .select(
      "exam_result_id, exam_id, question_index, topic_name, topic_id, form, is_correct",
    )
    .eq("student_id", userId);
  return (data as EqrRow[]) ?? [];
}

/** Chỗ hổng của học sinh theo Chủ đề × Loại, xếp theo % sai giảm dần. */
export async function fetchMyTopicGaps(userId: string): Promise<TopicGap[]> {
  const rows = await fetchMyEqr(userId);
  const map = new Map<string, TopicGap>();
  for (const r of rows) {
    const topic = r.topic_name || "Chưa gắn chủ đề";
    const key = `${topic}|${r.form}`;
    const g =
      map.get(key) ??
      { key, topicId: r.topic_id, topic, form: r.form, total: 0, wrong: 0, pct: 0 };
    g.total += 1;
    if (!r.is_correct) g.wrong += 1;
    if (r.topic_id) g.topicId = r.topic_id;
    map.set(key, g);
  }
  return [...map.values()]
    .map((g) => ({ ...g, pct: pct(g.wrong, g.total) }))
    .sort((a, b) => b.wrong - a.wrong || b.pct - a.pct);
}

/** Các câu sai của học sinh thuộc một (chủ đề, loại) cụ thể — để mở xem lại. */
export async function fetchMyWrongQuestions(
  userId: string,
  topic: string,
  form: string,
): Promise<
  { ref: WrongQuestionRef; question: ExamQuestion; response: QuestionResponse }[]
> {
  const rows = (await fetchMyEqr(userId)).filter(
    (r) => !r.is_correct && (r.topic_name || "Chưa gắn chủ đề") === topic && r.form === form,
  );
  if (rows.length === 0) return [];

  const resultIds = [...new Set(rows.map((r) => r.exam_result_id))];
  const { data: results } = await getSupabase()
    .from("exam_results")
    .select("id, exam_id, detail, exams(title, questions)")
    .in("id", resultIds);

  const byResult = new Map(
    ((results as {
      id: number;
      exam_id: number;
      detail: { responses?: QuestionResponse[] } | null;
      exams: { title: string; questions: ExamQuestion[] } | { title: string; questions: ExamQuestion[] }[] | null;
    }[]) ?? []).map((r) => {
      const exam = Array.isArray(r.exams) ? r.exams[0] : r.exams;
      return [r.id, { exam, detail: r.detail }];
    }),
  );

  const out: {
    ref: WrongQuestionRef;
    question: ExamQuestion;
    response: QuestionResponse;
  }[] = [];
  for (const r of rows) {
    const entry = byResult.get(r.exam_result_id);
    const question = entry?.exam?.questions?.[r.question_index];
    if (!question) continue;
    out.push({
      ref: {
        examId: r.exam_id,
        examTitle: entry?.exam?.title ?? "(Đề đã xóa)",
        examResultId: r.exam_result_id,
        questionIndex: r.question_index,
        topic,
        form,
      },
      question,
      response:
        entry?.detail?.responses?.[r.question_index] ??
        (question.type === "true_false"
          ? [null, null, null, null]
          : question.type === "short_answer" || question.type === "essay"
            ? ""
            : null),
    });
  }
  return out;
}

export interface MyExamAttemptDetail {
  examTitle: string;
  questions: ExamQuestion[];
  responses: QuestionResponse[];
  score: number;
  durationSeconds: number;
  createdAt: string;
}

/** Toàn bộ 1 lượt làm bài của chính học sinh — để xem lại nguyên bài (không chỉ câu sai). */
export async function fetchMyExamResultDetail(
  resultId: number,
): Promise<MyExamAttemptDetail | null> {
  const { data, error } = await getSupabase()
    .from("exam_results")
    .select("score, duration_seconds, created_at, detail, exams(title, questions)")
    .eq("id", resultId)
    .single();
  if (error || !data) return null;
  const exam = Array.isArray(data.exams) ? data.exams[0] : data.exams;
  const responses =
    (data.detail as { responses?: QuestionResponse[] } | null)?.responses ?? [];
  return {
    examTitle: exam?.title ?? "(Đề đã xóa)",
    questions: (exam?.questions as ExamQuestion[]) ?? [],
    responses,
    score: Number(data.score),
    durationSeconds: data.duration_seconds as number,
    createdAt: data.created_at as string,
  };
}

export interface ExamRank {
  rank: number;
  total: number;
}

/** Hạng của học sinh trong 1 đề, so với các bạn cùng lớp đã làm đề đó. */
export async function fetchExamRank(examId: number): Promise<ExamRank | null> {
  const { data, error } = await getSupabase().rpc("get_exam_rank", { p_exam_id: examId });
  const row = (data as { rnk: number; total: number }[] | null)?.[0];
  if (error || !row) return null;
  return { rank: row.rnk, total: row.total };
}

export interface PeriodicRank {
  rank: number;
  total: number;
  myAvg: number;
  classAvg: number;
}

/** Hạng của học sinh theo điểm TB các bài kiểm tra định kỳ của 1 lớp. */
export async function fetchPeriodicRank(classId: number): Promise<PeriodicRank | null> {
  const { data, error } = await getSupabase().rpc("get_periodic_rank", {
    p_class_id: classId,
  });
  const row = (data as { rnk: number; total: number; my_avg: number; class_avg: number }[] | null)?.[0];
  if (error || !row) return null;
  return { rank: row.rnk, total: row.total, myAvg: Number(row.my_avg), classAvg: Number(row.class_avg) };
}

// ============================================================
// GIÁO VIÊN — theo lớp (danh sách studentIds) / theo đề
// ============================================================

export interface ExamOverview {
  attempts: number;
  average: number;
  passRate: number; // % >= 5
  avgSeconds: number;
  distribution: number[]; // 10 khoảng [0-1) … [9-10]
}

export async function fetchExamOverview(
  examId: number,
  studentIds: string[],
): Promise<ExamOverview> {
  if (studentIds.length === 0)
    return { attempts: 0, average: 0, passRate: 0, avgSeconds: 0, distribution: Array(10).fill(0) };
  const { data } = await getSupabase()
    .from("exam_results")
    .select("student_id, score, duration_seconds")
    .eq("exam_id", examId)
    .in("student_id", studentIds);

  // điểm cao nhất mỗi học sinh
  const best = new Map<string, { score: number; secs: number }>();
  for (const r of (data as { student_id: string; score: number; duration_seconds: number }[]) ?? []) {
    const cur = best.get(r.student_id);
    if (!cur || Number(r.score) > cur.score)
      best.set(r.student_id, { score: Number(r.score), secs: r.duration_seconds });
  }
  const scores = [...best.values()];
  if (scores.length === 0)
    return { attempts: 0, average: 0, passRate: 0, avgSeconds: 0, distribution: Array(10).fill(0) };

  const distribution = Array(10).fill(0);
  for (const s of scores) distribution[Math.min(9, Math.floor(s.score))] += 1;
  const sum = scores.reduce((a, b) => a + b.score, 0);
  return {
    attempts: scores.length,
    average: Math.round((sum / scores.length) * 10) / 10,
    passRate: pct(scores.filter((s) => s.score >= 5).length, scores.length),
    avgSeconds: Math.round(scores.reduce((a, b) => a + b.secs, 0) / scores.length),
    distribution,
  };
}

export interface WrongestQuestion {
  questionIndex: number;
  topic: string;
  form: string;
  qtype: string;
  wrong: number;
  total: number;
  pct: number;
}

/** Câu sai nhiều nhất của một đề (chỉ tính học sinh trong lớp). */
export async function fetchWrongestQuestions(
  examId: number,
  studentIds: string[],
): Promise<WrongestQuestion[]> {
  if (studentIds.length === 0) return [];
  const { data } = await getSupabase()
    .from("exam_question_results")
    .select("question_index, topic_name, form, qtype, is_correct, student_id")
    .eq("exam_id", examId)
    .in("student_id", studentIds);

  const map = new Map<number, WrongestQuestion>();
  const rows = (data ?? []) as {
    question_index: number;
    topic_name: string;
    form: string;
    qtype: string;
    is_correct: boolean;
  }[];
  for (const r of rows) {
    const q =
      map.get(r.question_index) ??
      {
        questionIndex: r.question_index,
        topic: r.topic_name || "Chưa gắn chủ đề",
        form: r.form,
        qtype: r.qtype,
        wrong: 0,
        total: 0,
        pct: 0,
      };
    q.total += 1;
    if (!r.is_correct) q.wrong += 1;
    map.set(r.question_index, q);
  }
  return [...map.values()]
    .map((q) => ({ ...q, pct: pct(q.wrong, q.total) }))
    .sort((a, b) => b.pct - a.pct || b.wrong - a.wrong);
}

/** Ma trận chủ đề yếu của lớp: Chủ đề × Loại → % sai. */
export async function fetchClassTopicMatrix(
  studentIds: string[],
  examId?: number,
): Promise<TopicGap[]> {
  if (studentIds.length === 0) return [];
  let query = getSupabase()
    .from("exam_question_results")
    .select("topic_id, topic_name, form, is_correct")
    .in("student_id", studentIds);
  if (examId) query = query.eq("exam_id", examId);
  const { data } = await query;

  const map = new Map<string, TopicGap>();
  for (const r of (data as Pick<EqrRow, "topic_id" | "topic_name" | "form" | "is_correct">[]) ?? []) {
    const topic = r.topic_name || "Chưa gắn chủ đề";
    const key = `${topic}|${r.form}`;
    const g =
      map.get(key) ??
      { key, topicId: r.topic_id, topic, form: r.form, total: 0, wrong: 0, pct: 0 };
    g.total += 1;
    if (!r.is_correct) g.wrong += 1;
    if (r.topic_id) g.topicId = r.topic_id;
    map.set(key, g);
  }
  return [...map.values()]
    .map((g) => ({ ...g, pct: pct(g.wrong, g.total) }))
    .sort((a, b) => b.pct - a.pct);
}

// ============================================================
// CẢNH BÁO PHỤ ĐẠO
// ============================================================
export interface StudentAlert {
  id: number;
  studentId: string;
  classId: number | null;
  kind: "low_score_streak" | "missed_assessment";
  severity: "warning" | "urgent";
  reason: string;
  status: "open" | "contacted" | "tutoring" | "resolved" | "dismissed";
  assignedTo: string | null;
  handledNote: string;
  createdAt: string;
  updatedAt: string;
}

export const ALERT_STATUS_LABEL: Record<StudentAlert["status"], string> = {
  open: "Mới",
  contacted: "Đã liên hệ",
  tutoring: "Đang phụ đạo",
  resolved: "Đã xử lý",
  dismissed: "Bỏ qua",
};

interface AlertRow {
  id: number;
  student_id: string;
  class_id: number | null;
  kind: StudentAlert["kind"];
  severity: StudentAlert["severity"];
  reason: string;
  status: StudentAlert["status"];
  assigned_to: string | null;
  handled_note: string;
  created_at: string;
  updated_at: string;
}

function toAlert(r: AlertRow): StudentAlert {
  return {
    id: r.id,
    studentId: r.student_id,
    classId: r.class_id,
    kind: r.kind,
    severity: r.severity,
    reason: r.reason,
    status: r.status,
    assignedTo: r.assigned_to,
    handledNote: r.handled_note,
    createdAt: r.created_at,
    updatedAt: r.updated_at,
  };
}

/** Cảnh báo của các học sinh trong lớp (giáo viên / trợ giảng). */
export async function fetchClassAlerts(studentIds: string[]): Promise<StudentAlert[]> {
  if (studentIds.length === 0) return [];
  const { data } = await getSupabase()
    .from("student_alerts")
    .select(
      "id, student_id, class_id, kind, severity, reason, status, assigned_to, handled_note, created_at, updated_at",
    )
    .in("student_id", studentIds)
    .order("updated_at", { ascending: false });
  return ((data as AlertRow[]) ?? []).map(toAlert);
}

/** Cảnh báo của chính học sinh — chỉ hiện khi trợ giảng đã xử lý (RLS lọc status='open'). */
export async function fetchMyAlert(userId: string): Promise<StudentAlert | null> {
  const { data } = await getSupabase()
    .from("student_alerts")
    .select(
      "id, student_id, class_id, kind, severity, reason, status, assigned_to, handled_note, created_at, updated_at",
    )
    .eq("student_id", userId)
    .order("updated_at", { ascending: false })
    .limit(1);
  const row = (data as AlertRow[])?.[0];
  return row ? toAlert(row) : null;
}

export async function updateAlert(
  id: number,
  patch: Partial<Pick<StudentAlert, "status" | "assignedTo" | "handledNote">> & {
    handledBy?: string;
  },
): Promise<void> {
  const row: Record<string, unknown> = {};
  if (patch.status !== undefined) row.status = patch.status;
  if (patch.assignedTo !== undefined) row.assigned_to = patch.assignedTo;
  if (patch.handledNote !== undefined) row.handled_note = patch.handledNote;
  if (patch.handledBy !== undefined) row.handled_by = patch.handledBy;
  const { error } = await getSupabase().from("student_alerts").update(row).eq("id", id);
  if (error) throw error;
}

/** Rà "bỏ bài kiểm tra" cho một lớp — gọi khi mở tab Cảnh báo. */
export async function sweepMissedAssessments(classId: number, days = 7): Promise<number> {
  const { data, error } = await getSupabase().rpc("sweep_missed_assessments", {
    p_class: classId,
    p_days: days,
  });
  if (error) return 0;
  return typeof data === "number" ? data : 0;
}

// ============================================================
// BÀI KIỂM TRA ĐỊNH KỲ CỦA LỚP
// ============================================================
export interface ClassAssessment {
  id: number;
  classId: number;
  examId: number;
  lessonId: number | null;
  kind: string;
  term: string;
  sequence: number | null;
  weight: number;
  publishedAt: string;
  examTitle: string;
}

export async function fetchClassAssessments(classId: number): Promise<ClassAssessment[]> {
  const { data } = await getSupabase()
    .from("class_assessments")
    .select(
      "id, class_id, exam_id, lesson_id, kind, term, sequence, weight, published_at, exams(title)",
    )
    .eq("class_id", classId)
    .order("published_at", { ascending: false });
  return ((data as {
    id: number;
    class_id: number;
    exam_id: number;
    lesson_id: number | null;
    kind: string;
    term: string;
    sequence: number | null;
    weight: number;
    published_at: string;
    exams: { title: string } | { title: string }[] | null;
  }[]) ?? []).map((r) => ({
    id: r.id,
    classId: r.class_id,
    examId: r.exam_id,
    lessonId: r.lesson_id,
    kind: r.kind,
    term: r.term,
    sequence: r.sequence,
    weight: Number(r.weight),
    publishedAt: r.published_at,
    examTitle: (Array.isArray(r.exams) ? r.exams[0] : r.exams)?.title ?? "(Đề đã xóa)",
  }));
}

export async function publishClassAssessment(input: {
  classId: number;
  examId: number;
  lessonId?: number | null;
  kind: string;
  term: string;
}): Promise<void> {
  const { error } = await getSupabase()
    .from("class_assessments")
    .upsert(
      {
        class_id: input.classId,
        exam_id: input.examId,
        lesson_id: input.lessonId ?? null,
        kind: input.kind,
        term: input.term,
      },
      { onConflict: "class_id,exam_id" },
    );
  if (error) throw error;
}

export async function removeClassAssessment(id: number): Promise<void> {
  const { error } = await getSupabase().from("class_assessments").delete().eq("id", id);
  if (error) throw error;
}

// ============================================================
// DANH MỤC CHỦ ĐỀ
// ============================================================
export interface QuestionTopic {
  id: number;
  subjectCode: string;
  grade: string;
  chapterId: number | null;
  lessonId: number | null;
  name: string;
  sortOrder: number;
}

export async function fetchQuestionTopics(grade?: string): Promise<QuestionTopic[]> {
  let query = getSupabase()
    .from("question_topics")
    .select("id, subject_code, grade, chapter_id, lesson_id, name, sort_order")
    .order("grade")
    .order("sort_order")
    .order("name");
  if (grade) query = query.eq("grade", grade);
  const { data } = await query;
  return ((data as {
    id: number;
    subject_code: string;
    grade: string;
    chapter_id: number | null;
    lesson_id: number | null;
    name: string;
    sort_order: number;
  }[]) ?? []).map((r) => ({
    id: r.id,
    subjectCode: r.subject_code,
    grade: r.grade,
    chapterId: r.chapter_id,
    lessonId: r.lesson_id,
    name: r.name,
    sortOrder: r.sort_order,
  }));
}

export async function createQuestionTopic(input: {
  grade: string;
  name: string;
  subjectCode?: string;
  chapterId?: number | null;
  lessonId?: number | null;
}): Promise<QuestionTopic | null> {
  const { data, error } = await getSupabase()
    .from("question_topics")
    .insert({
      grade: input.grade,
      name: input.name.trim(),
      subject_code: input.subjectCode ?? "vat-ly",
      chapter_id: input.chapterId ?? null,
      lesson_id: input.lessonId ?? null,
    })
    .select("id, subject_code, grade, chapter_id, lesson_id, name, sort_order")
    .single();
  if (error || !data) throw error ?? new Error("Không tạo được chủ đề.");
  return {
    id: data.id,
    subjectCode: data.subject_code,
    grade: data.grade,
    chapterId: data.chapter_id,
    lessonId: data.lesson_id,
    name: data.name,
    sortOrder: data.sort_order,
  };
}

export async function updateQuestionTopic(
  id: number,
  patch: Partial<Pick<QuestionTopic, "name" | "chapterId" | "lessonId" | "sortOrder">>,
): Promise<void> {
  const row: Record<string, unknown> = {};
  if (patch.name !== undefined) row.name = patch.name.trim();
  if (patch.chapterId !== undefined) row.chapter_id = patch.chapterId;
  if (patch.lessonId !== undefined) row.lesson_id = patch.lessonId;
  if (patch.sortOrder !== undefined) row.sort_order = patch.sortOrder;
  const { error } = await getSupabase().from("question_topics").update(row).eq("id", id);
  if (error) throw error;
}

// ============================================================
// Tiện ích chấm lại (dùng cho backfill / kiểm tra)
// ============================================================
export function regrade(question: ExamQuestion, response: QuestionResponse) {
  return gradeQuestion(question, response);
}

// ============================================================
// Bảng chữa bài (trình chiếu lên TV) — thống kê thật theo từng câu
// ============================================================
export interface ReviewQuestionStat {
  attempted: number; // số học sinh đã nộp đề (lượt gần nhất/em)
  correctN: number;
  optionCounts?: number[]; // multiple_choice: số em chọn mỗi phương án A–D
  statementCorrectN?: number[]; // true_false: số em chọn đúng ở mỗi ý a–d
}

export interface ExamReviewData {
  examTitle: string;
  durationMinutes: number;
  questions: ExamQuestion[];
  totalStudents: number; // số lượt (1 học sinh = 1 lượt gần nhất)
  stats: ReviewQuestionStat[]; // cùng thứ tự với questions
}

/** Dữ liệu cho màn hình chữa bài: đề + thống kê thật (lượt nộp gần nhất của mỗi học sinh trong lớp). */
export async function fetchExamReviewData(
  examId: number,
  studentIds: string[],
): Promise<ExamReviewData> {
  const supabase = getSupabase();
  const [{ data: exam, error: examError }, { data: results, error: resultsError }] =
    await Promise.all([
      supabase
        .from("exams")
        .select("title, duration_minutes, questions")
        .eq("id", examId)
        .single(),
      studentIds.length === 0
        ? Promise.resolve({ data: [] as never[], error: null })
        : supabase
            .from("exam_results")
            .select("student_id, created_at, detail")
            .eq("exam_id", examId)
            .in("student_id", studentIds),
    ]);
  if (examError || !exam) throw examError ?? new Error("Không tìm thấy đề.");
  if (resultsError) throw resultsError;

  const questions = (exam.questions as ExamQuestion[]) ?? [];

  // Lấy lượt nộp gần nhất của mỗi học sinh — tránh đếm trùng khi có làm lại.
  const latestByStudent = new Map<
    string,
    { created_at: string; responses: QuestionResponse[] }
  >();
  for (const r of (results as {
    student_id: string;
    created_at: string;
    detail: { responses?: QuestionResponse[] } | null;
  }[]) ?? []) {
    const responses = r.detail?.responses;
    if (!Array.isArray(responses)) continue;
    const cur = latestByStudent.get(r.student_id);
    if (!cur || r.created_at > cur.created_at) {
      latestByStudent.set(r.student_id, { created_at: r.created_at, responses });
    }
  }
  const attempts = [...latestByStudent.values()];

  const stats: ReviewQuestionStat[] = questions.map((q) => {
    const stat: ReviewQuestionStat = { attempted: 0, correctN: 0 };
    if (q.type === "multiple_choice") stat.optionCounts = [0, 0, 0, 0];
    if (q.type === "true_false") stat.statementCorrectN = [0, 0, 0, 0];
    return stat;
  });

  for (const attempt of attempts) {
    questions.forEach((q, i) => {
      const response = attempt.responses[i];
      const stat = stats[i];
      if (response === undefined) return;
      stat.attempted += 1;
      const g = gradeQuestion(q, response);
      if (g.max > 0 && g.earned === g.max) stat.correctN += 1;

      if (q.type === "multiple_choice" && stat.optionCounts && typeof response === "number") {
        if (response >= 0 && response < stat.optionCounts.length) stat.optionCounts[response] += 1;
      }
      if (q.type === "true_false" && stat.statementCorrectN && Array.isArray(response)) {
        q.statements.forEach((s, si) => {
          if (response[si] === s.answer) stat.statementCorrectN![si] += 1;
        });
      }
    });
  }

  return {
    examTitle: exam.title as string,
    durationMinutes: exam.duration_minutes as number,
    questions,
    totalStudents: attempts.length,
    stats,
  };
}
