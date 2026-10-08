/** Ba đề mẫu trên trang chủ. Câu 1 không có đáp án — xem scripts/build-content.mjs. */
export type ExamSampleShelf = "giua-ki" | "cuoi-ki" | "thi-thu";

export interface ExamSampleQuestion {
  type: "multiple_choice" | "true_false" | "short_answer";
  question: string;
  options?: string[];
  statements?: { text: string }[];
}

export interface ExamSampleCard {
  id: number;
  shelf: ExamSampleShelf;
  label: string;
  gradeLabel: string;
  grade: string;
  classId: number;
  classSlug: string;
  year: string;
  questionCount: number;
  durationMinutes: number;
}

export interface ExamSample extends ExamSampleCard {
  question: ExamSampleQuestion;
}

export function examSampleLine(card: Pick<ExamSampleCard, "label" | "gradeLabel" | "year">) {
  return [card.label, card.gradeLabel, card.year].filter(Boolean).join(" · ");
}

export function examSampleSignupHref(sample: Pick<ExamSampleCard, "id" | "classSlug">) {
  const next = `/kiem-tra/lam?id=${sample.id}`;
  return `/dang-ky?lop=${encodeURIComponent(sample.classSlug)}&next=${encodeURIComponent(next)}`;
}

export function examSampleLoginHref(sample: Pick<ExamSampleCard, "id">) {
  return `/dang-nhap?next=${encodeURIComponent(`/kiem-tra/lam?id=${sample.id}`)}`;
}
