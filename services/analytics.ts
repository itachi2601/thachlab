import { getSupabase } from "@/services/supabase";
import { callClassRpc } from "@/services/class-rpc";
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
  examId: number;
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
    .select("exam_id, score, duration_seconds, created_at, detail, exams(title, questions)")
    .eq("id", resultId)
    .single();
  if (error || !data) return null;
  const exam = Array.isArray(data.exams) ? data.exams[0] : data.exams;
  const responses =
    (data.detail as { responses?: QuestionResponse[] } | null)?.responses ?? [];
  return {
    examId: data.exam_id as number,
    examTitle: exam?.title ?? "(Đề đã xóa)",
    questions: (exam?.questions as ExamQuestion[]) ?? [],
    responses,
    score: Number(data.score),
    durationSeconds: data.duration_seconds as number,
    createdAt: data.created_at as string,
  };
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

const EMPTY_OVERVIEW = (): ExamOverview => ({ attempts: 0, average: 0, passRate: 0, avgSeconds: 0, distribution: Array(10).fill(0) });

interface ExamBestRow {
  student_id: string;
  score: number;
  duration_seconds: number;
}

/** Tổng hợp điểm cao nhất mỗi học sinh thành thẻ tổng quan — dùng chung cho cả 2 đường. */
function summarizeExamOverview(scores: { score: number; secs: number }[]): ExamOverview {
  if (scores.length === 0) return EMPTY_OVERVIEW();

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

/** Đường cũ: tải mọi lượt làm của lớp trên đề rồi lấy max ở client. */
export async function fetchExamOverviewDirect(
  examId: number,
  studentIds: string[],
): Promise<ExamOverview> {
  if (studentIds.length === 0) return EMPTY_OVERVIEW();
  const { data } = await getSupabase()
    .from("exam_results")
    .select("student_id, score, duration_seconds")
    .eq("exam_id", examId)
    .in("student_id", studentIds);

  // điểm cao nhất mỗi học sinh
  const best = new Map<string, { score: number; secs: number }>();
  for (const r of (data as ExamBestRow[]) ?? []) {
    const cur = best.get(r.student_id);
    if (!cur || Number(r.score) > cur.score)
      best.set(r.student_id, { score: Number(r.score), secs: r.duration_seconds });
  }
  return summarizeExamOverview([...best.values()]);
}

/** Đường mới: rpc get_class_exam_best trả ≤ 1 dòng / học sinh. null = rpc chưa có. */
export async function fetchExamOverviewRpc(
  examId: number,
  studentIds: string[],
): Promise<ExamOverview | null> {
  if (studentIds.length === 0) return EMPTY_OVERVIEW();
  const rows = await callClassRpc<ExamBestRow[]>("get_class_exam_best", { p_exam: examId, p_students: studentIds });
  if (!rows) return null;
  return summarizeExamOverview(rows.map((r) => ({ score: Number(r.score), secs: r.duration_seconds })));
}

export async function fetchExamOverview(
  examId: number,
  studentIds: string[],
): Promise<ExamOverview> {
  return (await fetchExamOverviewRpc(examId, studentIds)) ?? fetchExamOverviewDirect(examId, studentIds);
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

function sortWrongest(list: WrongestQuestion[]): WrongestQuestion[] {
  return list
    .map((q) => ({ ...q, pct: pct(q.wrong, q.total) }))
    .sort((a, b) => b.pct - a.pct || b.wrong - a.wrong);
}

/** Đường mới: rpc get_class_exam_question_stats đã group theo câu trên server. null = rpc chưa có. */
export async function fetchWrongestQuestionsRpc(
  examId: number,
  studentIds: string[],
): Promise<WrongestQuestion[] | null> {
  if (studentIds.length === 0) return [];
  const rows = await callClassRpc<{ question_index: number; topic_name: string | null; form: string; qtype: string; total: number; wrong: number }[]>(
    "get_class_exam_question_stats",
    { p_exam: examId, p_students: studentIds },
  );
  if (!rows) return null;
  return sortWrongest(rows.map((r) => ({
    questionIndex: r.question_index,
    topic: r.topic_name || "Chưa gắn chủ đề",
    form: r.form,
    qtype: r.qtype,
    wrong: r.wrong,
    total: r.total,
    pct: 0,
  })));
}

/** Câu sai nhiều nhất của một đề (chỉ tính học sinh trong lớp). */
export async function fetchWrongestQuestions(
  examId: number,
  studentIds: string[],
): Promise<WrongestQuestion[]> {
  return (await fetchWrongestQuestionsRpc(examId, studentIds)) ?? fetchWrongestQuestionsDirect(examId, studentIds);
}

/** Đường cũ: tải từng dòng exam_question_results của lớp trên đề rồi group ở client. */
export async function fetchWrongestQuestionsDirect(
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
  return sortWrongest([...map.values()]);
}

function sortTopicGaps(list: TopicGap[]): TopicGap[] {
  return list
    .map((g) => ({ ...g, pct: pct(g.wrong, g.total) }))
    .sort((a, b) => b.pct - a.pct);
}

/** Đường mới: rpc get_class_topic_matrix đã group theo (chủ đề, dạng) trên server. null = rpc chưa có. */
export async function fetchClassTopicMatrixRpc(
  studentIds: string[],
  examId?: number,
): Promise<TopicGap[] | null> {
  if (studentIds.length === 0) return [];
  const rows = await callClassRpc<{ topic_id: number | null; topic_name: string; form: string; total: number; wrong: number }[]>(
    "get_class_topic_matrix",
    { p_students: studentIds, p_exam: examId ?? null },
  );
  if (!rows) return null;
  return sortTopicGaps(rows.map((r) => ({
    key: `${r.topic_name}|${r.form}`,
    topicId: r.topic_id,
    topic: r.topic_name,
    form: r.form,
    total: r.total,
    wrong: r.wrong,
    pct: 0,
  })));
}

/** Ma trận chủ đề yếu của lớp: Chủ đề × Loại → % sai. */
export async function fetchClassTopicMatrix(
  studentIds: string[],
  examId?: number,
): Promise<TopicGap[]> {
  return (await fetchClassTopicMatrixRpc(studentIds, examId)) ?? fetchClassTopicMatrixDirect(studentIds, examId);
}

/** Đường cũ: tải từng dòng exam_question_results của lớp rồi group ở client. */
export async function fetchClassTopicMatrixDirect(
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
  return sortTopicGaps([...map.values()]);
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
  /** null = chủ đề của cả bài; có giá trị = một yêu cầu cần đạt trong bài đó. */
  parentId: number | null;
  name: string;
  sortOrder: number;
}

/** Chủ đề con của một bài (yêu cầu cần đạt), theo thứ tự trong danh mục. */
export function outcomesOf(topics: QuestionTopic[], parentId: number): QuestionTopic[] {
  return topics
    .filter((t) => t.parentId === parentId)
    .sort((a, b) => a.sortOrder - b.sortOrder || a.name.localeCompare(b.name, "vi"));
}

/** Chủ đề tầng bài (không có cha). */
export function lessonTopics(topics: QuestionTopic[]): QuestionTopic[] {
  return topics.filter((t) => t.parentId === null);
}

export async function fetchQuestionTopics(grade?: string): Promise<QuestionTopic[]> {
  let query = getSupabase()
    .from("question_topics")
    .select("id, subject_code, grade, chapter_id, lesson_id, parent_id, name, sort_order")
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
    parent_id: number | null;
    name: string;
    sort_order: number;
  }[]) ?? []).map((r) => ({
    id: r.id,
    subjectCode: r.subject_code,
    grade: r.grade,
    chapterId: r.chapter_id,
    lessonId: r.lesson_id,
    parentId: r.parent_id,
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
  /** Chủ đề cha (tầng bài) nếu đây là một yêu cầu cần đạt. */
  parentId?: number | null;
  sortOrder?: number;
}): Promise<QuestionTopic | null> {
  const { data, error } = await getSupabase()
    .from("question_topics")
    .insert({
      grade: input.grade,
      name: input.name.trim(),
      subject_code: input.subjectCode ?? "vat-ly",
      chapter_id: input.chapterId ?? null,
      lesson_id: input.lessonId ?? null,
      parent_id: input.parentId ?? null,
      ...(input.sortOrder !== undefined ? { sort_order: input.sortOrder } : {}),
    })
    .select("id, subject_code, grade, chapter_id, lesson_id, parent_id, name, sort_order")
    .single();
  if (error || !data) throw error ?? new Error("Không tạo được chủ đề.");
  return {
    id: data.id,
    subjectCode: data.subject_code,
    grade: data.grade,
    chapterId: data.chapter_id,
    lessonId: data.lesson_id,
    parentId: data.parent_id,
    name: data.name,
    sortOrder: data.sort_order,
  };
}

export async function updateQuestionTopic(
  id: number,
  patch: Partial<Pick<QuestionTopic, "name" | "chapterId" | "lessonId" | "sortOrder" | "parentId">>,
): Promise<void> {
  const row: Record<string, unknown> = {};
  if (patch.parentId !== undefined) row.parent_id = patch.parentId;
  if (patch.name !== undefined) row.name = patch.name.trim();
  if (patch.chapterId !== undefined) row.chapter_id = patch.chapterId;
  if (patch.lessonId !== undefined) row.lesson_id = patch.lessonId;
  if (patch.sortOrder !== undefined) row.sort_order = patch.sortOrder;
  const { error } = await getSupabase().from("question_topics").update(row).eq("id", id);
  if (error) throw error;
}

export async function deleteQuestionTopic(id: number): Promise<void> {
  const { error } = await getSupabase().from("question_topics").delete().eq("id", id);
  if (error) throw error;
}

// ============================================================
// Chi tiết: em hổng đúng yêu cầu cần đạt nào
// ============================================================
// Mục phụ đạo mở ở tầng bài (đủ câu mới dám kết luận), còn đây là phần mịn:
// trong 2 bài gần nhất, những yêu cầu cần đạt em còn làm sai.
export interface OutcomeGap {
  studentId: string;
  parentTopicId: number;
  topicId: number;
  topicName: string;
  form: string;
  total: number;
  wrong: number;
}

/** Chi tiết YCCĐ còn sai của một hoặc nhiều em (một lần gọi cho cả màn hình lớp). */
export async function fetchOutcomeGaps(
  studentIds: string | string[],
  window = 2,
): Promise<OutcomeGap[]> {
  const ids = Array.isArray(studentIds) ? studentIds : [studentIds];
  if (ids.length === 0) return [];
  const { data, error } = await getSupabase().rpc("student_outcome_gaps", {
    p_students: ids,
    p_window: window,
  });
  if (error) return [];
  return ((data as {
    student_id: string;
    parent_topic_id: number;
    topic_id: number;
    topic_name: string;
    form: string;
    total: number;
    wrong: number;
  }[]) ?? []).map((r) => ({
    studentId: r.student_id,
    parentTopicId: r.parent_topic_id,
    topicId: r.topic_id,
    topicName: r.topic_name,
    form: r.form,
    total: r.total,
    wrong: r.wrong,
  }));
}

/** Gom chi tiết theo (em, chủ đề bài, loại) — khớp đúng khoá của một mục phụ đạo. */
export function outcomeGapsByNeed(gaps: OutcomeGap[]): Map<string, OutcomeGap[]> {
  const m = new Map<string, OutcomeGap[]>();
  for (const g of gaps) {
    if (g.topicId === g.parentTopicId) continue; // câu gắn thẳng tầng bài, không thêm chi tiết
    const key = `${g.studentId}|${g.parentTopicId}|${g.form}`;
    const arr = m.get(key) ?? [];
    arr.push(g);
    m.set(key, arr);
  }
  for (const arr of m.values()) arr.sort((a, b) => b.wrong - a.wrong || b.total - a.total);
  return m;
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
