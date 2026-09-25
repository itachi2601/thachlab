// 3 dạng câu hỏi theo cấu trúc đề thi 2025 (GDPT 2018).
// Các trường *html chứa văn bản + ảnh công thức (<img class="eq">) hoặc hình vẽ.

// Nhãn phân tích, gắn khi soạn đề (skill up-de-kiem-tra hoặc trình soạn):
//  topic  -> tên chủ đề, khớp public.question_topics.name (chuẩn hoá theo lớp).
//            Nên trỏ đúng YÊU CẦU CẦN ĐẠT (chủ đề con của bài) chứ không dừng ở tên bài:
//            mục phụ đạo vẫn gom lên tầng bài, còn nhãn mịn cho biết em hổng phần nào.
//  form   -> "lý thuyết" hay "bài tập" — để tách chỗ hổng của học sinh
export type QuestionForm = "ly_thuyet" | "bai_tap";

export const QUESTION_FORM_LABELS: Record<QuestionForm, string> = {
  ly_thuyet: "Lý thuyết",
  bai_tap: "Bài tập",
};

interface QuestionTags {
  topic?: string;
  form?: QuestionForm | "";
  difficulty?: Difficulty;
  /** Chỉ có ý nghĩa khi đề này là quiz "Kiểm tra nhanh" gắn cho đúng 1 bài (item.exam_ids[0]):
   *  vị trí (0-based) của khối <h3> lý thuyết liên quan trong body_html mục lý thuyết của
   *  CHÍNH bài đó — dùng để "Ôn ngay" nhảy thẳng + tô màu đúng đoạn thay vì cả mục lý thuyết.
   *  Xem features/lessons/theory-sections.ts (wrapTheorySections sinh id "theory-sec-<itemId>-<n>"). */
  theorySection?: number;
}

export interface MultipleChoiceQuestion extends QuestionTags {
  type: "multiple_choice";
  question: string;
  options: string[]; // 4 đáp án A–D
  answer: number; // chỉ số đáp án đúng (0–3)
  explanation: string;
}

export interface TrueFalseQuestion extends QuestionTags {
  type: "true_false";
  question: string;
  statements: { text: string; answer: boolean }[]; // 4 ý a) b) c) d)
  explanation: string;
}

export interface ShortAnswerQuestion extends QuestionTags {
  type: "short_answer";
  question: string;
  answer: string; // tối đa 4 ký tự: chữ số, dấu trừ, dấu phẩy (vd "-1,5")
  explanation: string;
}

export interface EssayQuestion extends QuestionTags {
  type: "essay";
  question: string;
  suggestedAnswer: string;
  gradingGuide: string;
  explanation: string;
}

export type ExamQuestion =
  | MultipleChoiceQuestion
  | TrueFalseQuestion
  | ShortAnswerQuestion
  | EssayQuestion;

export const QUESTION_TYPE_LABELS: Record<ExamQuestion["type"], string> = {
  multiple_choice: "Trắc nghiệm nhiều phương án",
  true_false: "Đúng – Sai",
  short_answer: "Trả lời ngắn",
  essay: "Tự luận",
};

/** Thứ tự chuẩn TN 4 đáp án → Đúng–Sai → Trả lời ngắn → Tự luận (cấu trúc đề thi 2025),
 * dùng để nhóm "bảng câu hỏi" lúc học sinh làm bài và sắp lại câu lấy từ ngân hàng câu hỏi. */
export const QUESTION_TYPE_ORDER: ExamQuestion["type"][] = [
  "multiple_choice",
  "true_false",
  "short_answer",
  "essay",
];

/** Gom chỉ số câu (0-based) theo QUESTION_TYPE_ORDER — dùng để vẽ "bảng câu hỏi" chia theo mục
 * mà không đổi số thứ tự câu gốc (giữ nguyên `index+1` để khớp với QuestionCard/chấm điểm). */
export function groupQuestionIndexesByType(
  questions: ExamQuestion[],
): { type: ExamQuestion["type"]; indices: number[] }[] {
  return QUESTION_TYPE_ORDER.map((type) => ({
    type,
    indices: questions.map((_, i) => i).filter((i) => questions[i].type === type),
  })).filter((s) => s.indices.length > 0);
}

export interface SchoolClass {
  id: number;
  name: string;
  slug: string;
  color: string;
  icon: string;
  sort_order: number;
  active: boolean;
}

export type Difficulty = "" | "de" | "trung-binh" | "kho";

export const DIFFICULTY_LABELS: Record<Difficulty, string> = {
  "": "Chưa phân loại",
  de: "Dễ",
  "trung-binh": "Trung bình",
  kho: "Khó",
};

export interface Exam {
  id: number;
  title: string;
  duration_minutes: number;
  published: boolean;
  questions: ExamQuestion[];
  topic?: string;
  difficulty?: Difficulty;
  created_at?: string;
  cnc_key?: string | null;
  pass_score?: number | null; // điểm đạt thang 10, null = giáo viên chưa cấu hình
}

// Bài làm của học sinh: song song với mảng questions
//  multiple_choice → number | null; true_false → (boolean|null)[4]; short_answer → string
export type QuestionResponse = number | null | (boolean | null)[] | string;

export interface GradedQuestion {
  earned: number; // điểm đạt được của câu
  max: number; // điểm tối đa của câu
}

// Trọng số chấm: TN 0,25đ/câu; đúng/sai chấm lũy tiến 0,1/0,25/0,5/1đ;
// trả lời ngắn 0,25đ/câu. Điểm cuối quy về thang 10.
const TF_SCALE = [0, 0.1, 0.25, 0.5, 1];

export function gradeQuestion(
  q: ExamQuestion,
  r: QuestionResponse,
): GradedQuestion {
  switch (q.type) {
    case "multiple_choice":
      return { earned: r === q.answer ? 0.25 : 0, max: 0.25 };
    case "true_false": {
      const picks = Array.isArray(r) ? r : [];
      const correct = q.statements.filter(
        (s, i) => picks[i] === s.answer,
      ).length;
      return { earned: TF_SCALE[correct] ?? 0, max: 1 };
    }
    case "short_answer": {
      const norm = (v: string) => v.trim().replace(".", ",");
      const given = typeof r === "string" ? r : "";
      return {
        earned: given && norm(given) === norm(q.answer) ? 0.25 : 0,
        max: 0.25,
      };
    }
    case "essay":
      // Tự luận do giáo viên chấm; không cộng vào điểm tự động.
      return { earned: 0, max: 0 };
  }
}

export interface GradeSummary {
  score10: number; // thang 10, làm tròn 2 chữ số
  earned: number;
  max: number;
  correctCount: number; // số câu đạt trọn điểm
}

export function gradeExam(
  questions: ExamQuestion[],
  responses: QuestionResponse[],
): GradeSummary {
  let earned = 0;
  let max = 0;
  let correctCount = 0;
  questions.forEach((q, i) => {
    const g = gradeQuestion(q, responses[i]);
    earned += g.earned;
    max += g.max;
    if (g.earned === g.max && g.max > 0) correctCount += 1;
  });
  const score10 = max > 0 ? Math.round((earned / max) * 1000) / 100 : 0;
  return { score10, earned, max, correctCount };
}

// Một dòng public.exam_question_results — chốt đúng/sai + nhãn từng câu lúc nộp bài.
export interface QuestionResultRow {
  question_index: number;
  topic_id: number | null;
  topic_name: string;
  form: string;
  qtype: string;
  earned: number;
  max: number;
  is_correct: boolean;
}

export function buildQuestionResults(
  questions: ExamQuestion[],
  responses: QuestionResponse[],
  topicIdByName?: Map<string, number>,
): QuestionResultRow[] {
  return questions.map((q, i) => {
    const g = gradeQuestion(q, responses[i]);
    const name = (q.topic ?? "").trim();
    return {
      question_index: i,
      topic_id: name ? (topicIdByName?.get(name) ?? null) : null,
      topic_name: name,
      form: q.form ?? "",
      qtype: q.type,
      earned: g.earned,
      max: g.max,
      is_correct: g.max > 0 && g.earned === g.max,
    };
  });
}

/** Tên chủ đề xuất hiện trên các câu của đề. */
export function questionTopicNames(questions: ExamQuestion[]): string[] {
  return [
    ...new Set(
      questions.map((q) => (q.topic ?? "").trim()).filter((t) => t !== ""),
    ),
  ];
}

export function emptyResponses(questions: ExamQuestion[]): QuestionResponse[] {
  return questions.map((q) => {
    if (q.type === "true_false") return [null, null, null, null];
    if (q.type === "short_answer" || q.type === "essay") return "";
    return null;
  });
}

export function isAnswered(q: ExamQuestion, r: QuestionResponse): boolean {
  if (q.type === "multiple_choice") return r !== null;
  if (q.type === "true_false")
    return Array.isArray(r) && r.some((v) => v !== null);
  return typeof r === "string" && r.trim() !== "";
}

// ── Xem lại bài làm ────────────────────────────────────────────────────────────
// Trạng thái một câu khi xem lại: "manual" là tự luận, thầy chấm tay.
export type QuestionStatus =
  | "correct"
  | "partial"
  | "wrong"
  | "skipped"
  | "manual";

export const QUESTION_STATUS_LABELS: Record<QuestionStatus, string> = {
  correct: "Đúng",
  partial: "Đúng một phần",
  wrong: "Sai",
  skipped: "Bỏ qua",
  manual: "Thầy chấm",
};

export function questionStatus(
  q: ExamQuestion,
  r: QuestionResponse,
): QuestionStatus {
  if (q.type === "essay") return "manual";
  if (!isAnswered(q, r)) return "skipped";
  const g = gradeQuestion(q, r);
  if (g.max > 0 && g.earned >= g.max) return "correct";
  return g.earned > 0 ? "partial" : "wrong";
}

/** Bảng thống kê theo từng dạng câu hỏi có trong đề. */
export interface TypeStat {
  type: ExamQuestion["type"];
  label: string;
  total: number;
  correct: number;
  partial: number;
  wrong: number;
  skipped: number;
  earned: number;
  max: number;
}

export function statsByType(
  questions: ExamQuestion[],
  responses: QuestionResponse[],
): TypeStat[] {
  const byType = new Map<ExamQuestion["type"], TypeStat>();
  questions.forEach((q, i) => {
    let stat = byType.get(q.type);
    if (!stat) {
      stat = {
        type: q.type,
        label: QUESTION_TYPE_LABELS[q.type],
        total: 0,
        correct: 0,
        partial: 0,
        wrong: 0,
        skipped: 0,
        earned: 0,
        max: 0,
      };
      byType.set(q.type, stat);
    }
    const g = gradeQuestion(q, responses[i]);
    const status = questionStatus(q, responses[i]);
    stat.total += 1;
    stat.earned += g.earned;
    stat.max += g.max;
    if (status === "correct") stat.correct += 1;
    else if (status === "partial") stat.partial += 1;
    else if (status === "wrong") stat.wrong += 1;
    else if (status === "skipped") stat.skipped += 1;
  });
  return [...byType.values()];
}

// ---------- Nhãn chủ đề: so khớp với danh mục public.question_topics ----------
// Nhãn chỉ có giá trị khi `topic` khớp ĐÚNG tên trong danh mục: buildQuestionResults
// tra theo tên để lấy topic_id, mà tutoring_needs.topic_id là NOT NULL — lệch một chữ
// là câu đó rơi khỏi mọi thống kê chủ đề, không báo lỗi ở đâu cả.

/** Khoá so khớp tên chủ đề: gom khoảng trắng, không phân biệt hoa/thường. */
export function topicKey(name: string): string {
  return name.trim().replace(/\s+/g, " ").toLowerCase();
}

function cleanTopic(name: string): string {
  return name.trim().replace(/\s+/g, " ");
}

export interface TagAudit {
  total: number;
  tagged: number; // số câu có cả topic + form
  missingTopic: number[]; // số câu (đếm từ 1) thiếu chủ đề
  missingForm: number[]; // số câu thiếu/sai loại
  missingDifficulty: number[]; // số câu chưa gắn mức độ — không chặn Đăng, chỉ nhắc
  known: { name: string; count: number }[]; // chủ đề có trong danh mục
  unknown: { name: string; count: number }[]; // chủ đề chưa có trong danh mục
  // Gắn ở tầng bài trong khi bài đó đã có yêu cầu cần đạt con — vẫn thống kê được,
  // chỉ là thầy sẽ không biết em hổng đúng phần nào. Nhắc, không chặn.
  coarse: { name: string; count: number }[];
}

/**
 * Soát nhãn của cả đề trước khi đăng.
 * `catalog` là tên mọi chủ đề của khối (cả tầng bài lẫn yêu cầu cần đạt);
 * `coarseNames` là tên chủ đề tầng bài đã có yêu cầu cần đạt con.
 */
export function auditQuestionTags(
  questions: ExamQuestion[],
  catalog: string[],
  coarseNames: string[] = [],
): TagAudit {
  const canon = new Map(catalog.map((n) => [topicKey(n), cleanTopic(n)]));
  const counts = new Map<string, { name: string; count: number; known: boolean }>();
  const audit: TagAudit = {
    total: questions.length,
    tagged: 0,
    missingTopic: [],
    missingForm: [],
    missingDifficulty: [],
    known: [],
    unknown: [],
    coarse: [],
  };
  const coarse = new Set(coarseNames.map(topicKey));
  questions.forEach((q, i) => {
    const name = cleanTopic(q.topic ?? "");
    const form = q.form ?? "";
    const formOk = form === "ly_thuyet" || form === "bai_tap";
    if (!name) audit.missingTopic.push(i + 1);
    if (!formOk) audit.missingForm.push(i + 1);
    if (!q.difficulty) audit.missingDifficulty.push(i + 1);
    if (name && formOk) audit.tagged += 1;
    if (!name) return;
    const key = topicKey(name);
    const cur = counts.get(key) ?? {
      name: canon.get(key) ?? name,
      count: 0,
      known: canon.has(key),
    };
    cur.count += 1;
    counts.set(key, cur);
  });
  for (const v of counts.values()) {
    (v.known ? audit.known : audit.unknown).push({ name: v.name, count: v.count });
    if (v.known && coarse.has(topicKey(v.name)))
      audit.coarse.push({ name: v.name, count: v.count });
  }
  const byCount = (a: { name: string; count: number }, b: { name: string; count: number }) =>
    b.count - a.count || a.name.localeCompare(b.name, "vi");
  audit.known.sort(byCount);
  audit.unknown.sort(byCount);
  audit.coarse.sort(byCount);
  return audit;
}

/** Đề đã gắn đủ nhãn và mọi chủ đề đều có trong danh mục? */
export function tagsComplete(audit: TagAudit): boolean {
  return (
    audit.total > 0 &&
    audit.missingTopic.length === 0 &&
    audit.missingForm.length === 0 &&
    audit.unknown.length === 0
  );
}

/** Ghi lại tên chủ đề theo đúng chính tả trong danh mục (khớp bỏ qua hoa/thường). */
export function canonicalizeQuestionTopics(
  questions: ExamQuestion[],
  catalog: string[],
): ExamQuestion[] {
  const canon = new Map(catalog.map((n) => [topicKey(n), cleanTopic(n)]));
  return questions.map((q) => {
    const raw = cleanTopic(q.topic ?? "");
    if (!raw) return q;
    const name = canon.get(topicKey(raw)) ?? raw;
    return name === q.topic ? q : ({ ...q, topic: name } as ExamQuestion);
  });
}

// ---------- Luyện tập: thời lượng theo dạng câu ----------
// Câu lý thuyết 15 giây, câu bài tập 45 giây. Câu chưa gắn nhãn `form` coi như bài tập
// để không ép giờ quá tay. Tổng thời lượng của phiên = tổng thời lượng các câu.
export const SECONDS_PER_FORM: Record<QuestionForm, number> = {
  ly_thuyet: 15,
  bai_tap: 45,
};

export function questionSeconds(q: ExamQuestion): number {
  return q.form === "ly_thuyet"
    ? SECONDS_PER_FORM.ly_thuyet
    : SECONDS_PER_FORM.bai_tap;
}

export function totalSeconds(questions: ExamQuestion[]): number {
  return questions.reduce((sum, q) => sum + questionSeconds(q), 0);
}

/** Thời lượng trung bình một câu của ngân hàng — để ước lượng trước khi bốc câu. */
export function averageSeconds(questions: ExamQuestion[]): number {
  if (questions.length === 0) return SECONDS_PER_FORM.bai_tap;
  return totalSeconds(questions) / questions.length;
}

/** Bốc ngẫu nhiên n phần tử (Fisher–Yates trên bản sao, không đụng mảng gốc). */
export function pickRandom<T>(items: T[], n: number): T[] {
  const pool = [...items];
  for (let i = pool.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return pool.slice(0, Math.max(0, Math.min(n, pool.length)));
}

/** mm:ss */
export function formatClock(totalSec: number): string {
  const safe = Math.max(0, Math.round(totalSec));
  const m = Math.floor(safe / 60);
  const s = safe % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}
