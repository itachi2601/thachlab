import type { ExamQuestion } from "@/features/exams/types";

const LETTERS = ["A", "B", "C", "D"];

/** Gộp nội dung một câu thành văn bản gọn để gửi AI phân loại (không kèm HTML/ảnh). */
export function questionTextForAi(q: ExamQuestion): string {
  const parts = [q.question];
  if (q.type === "multiple_choice") {
    parts.push(q.options.map((o, j) => `${LETTERS[j]}. ${o}${j === q.answer ? " (đáp án đúng)" : ""}`).join("\n"));
  } else if (q.type === "true_false") {
    parts.push(q.statements.map((s, j) => `${["a", "b", "c", "d"][j]}) ${s.text} — ${s.answer ? "Đúng" : "Sai"}`).join("\n"));
  } else if (q.type === "short_answer") {
    parts.push(`Đáp án: ${q.answer}`);
  }
  if (q.explanation.trim()) parts.push(`Lời giải: ${q.explanation}`);
  return parts.join("\n");
}
