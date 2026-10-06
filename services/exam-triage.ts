/**
 * Phân loại câu của một đề trước khi Đăng: câu ổn / câu trùng / câu cần duyệt (thiếu hình, phụ thuộc câu khác).
 * Câu ổn luôn đăng được; câu trùng tự loại (giữ lần xuất hiện đầu); câu cần duyệt nằm riêng, mặc định
 * KHÔNG đăng — thầy tick từng câu muốn đăng. Trước đây một câu lỗi hình khoá cả đề.
 */
import type { ExamQuestion } from "@/features/exams/types";
import { isMissingFigure } from "@/services/question-figures";
import { dependsOnOtherQuestion } from "@/services/question-context";

/** Chuẩn hoá để so trùng: bỏ thẻ HTML, khoảng trắng thừa, hoa/thường; giữ alt của ảnh. */
export function triageKey(q: ExamQuestion): string {
  const html = [q.question ?? "", ..."options" in q && Array.isArray(q.options) ? q.options : []].join(" | ");
  const t = html
    .replace(/<img[^>]*alt="([^"]*)"[^>]*>/g, " $1 ")
    .replace(/<img[^>]*src="([^"]*)"[^>]*>/g, " $1 ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
  return t;
}

export type TriageReason = "figure" | "context";

export interface TriageResult {
  /** Chỉ số (0-based) câu ổn. */
  ok: number[];
  /** Câu trùng → chỉ số câu đầu tiên mà nó trùng. */
  duplicates: { index: number; of: number }[];
  /** Câu cần duyệt kèm lý do. */
  review: { index: number; reasons: TriageReason[] }[];
}

export function triageQuestions(questions: ExamQuestion[]): TriageResult {
  const seen = new Map<string, number>();
  const res: TriageResult = { ok: [], duplicates: [], review: [] };
  questions.forEach((q, i) => {
    const key = triageKey(q);
    const first = key ? seen.get(key) : undefined;
    if (first !== undefined) {
      res.duplicates.push({ index: i, of: first });
      return;
    }
    if (key) seen.set(key, i);
    const reasons: TriageReason[] = [];
    if (isMissingFigure(q)) reasons.push("figure");
    if (dependsOnOtherQuestion(q)) reasons.push("context");
    if (reasons.length) res.review.push({ index: i, reasons });
    else res.ok.push(i);
  });
  return res;
}
