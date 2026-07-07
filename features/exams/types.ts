// 3 dạng câu hỏi theo cấu trúc đề thi 2025 (GDPT 2018).
// Các trường *html chứa văn bản + ảnh công thức (<img class="eq">) hoặc hình vẽ.

export interface MultipleChoiceQuestion {
  type: "multiple_choice";
  question: string;
  options: string[]; // 4 đáp án A–D
  answer: number; // chỉ số đáp án đúng (0–3)
  explanation: string;
}

export interface TrueFalseQuestion {
  type: "true_false";
  question: string;
  statements: { text: string; answer: boolean }[]; // 4 ý a) b) c) d)
  explanation: string;
}

export interface ShortAnswerQuestion {
  type: "short_answer";
  question: string;
  answer: string; // tối đa 4 ký tự: chữ số, dấu trừ, dấu phẩy (vd "-1,5")
  explanation: string;
}

export type ExamQuestion =
  | MultipleChoiceQuestion
  | TrueFalseQuestion
  | ShortAnswerQuestion;

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

export function emptyResponses(questions: ExamQuestion[]): QuestionResponse[] {
  return questions.map((q) => {
    if (q.type === "true_false") return [null, null, null, null];
    if (q.type === "short_answer") return "";
    return null;
  });
}

export function isAnswered(q: ExamQuestion, r: QuestionResponse): boolean {
  if (q.type === "multiple_choice") return r !== null;
  if (q.type === "true_false")
    return Array.isArray(r) && r.some((v) => v !== null);
  return typeof r === "string" && r.trim() !== "";
}
