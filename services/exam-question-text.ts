import type { ExamQuestion } from "@/features/exams/types";

const LETTERS = ["A", "B", "C", "D"];

/**
 * Câu lấy từ ngân hàng lưu dạng HTML (`<p class="text-base leading-relaxed my-2">…</p>`) — để nguyên trong ô sửa thì
 * giáo viên phải đọc cả thẻ bọc. Hàm này chỉ bỏ phần thẻ bọc (p/div/span, thuộc tính class/style), đổi xuống đoạn thành
 * dòng mới, giữ nguyên thẻ có nghĩa (img, sup, sub, b, i, u, bảng) và công thức `$…$`. Chỉ dùng để HIỂN THỊ trong ô sửa;
 * dữ liệu chỉ đổi khi giáo viên gõ vào ô (khi đó `editableToHtml` ghi lại, dòng mới → `<br>`).
 */
export function htmlToEditable(html: string): string {
  if (!/<[a-z!/][^>]*>/i.test(html)) return html;
  return html
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/(p|div|li)>\s*/gi, "\n")
    .replace(/<\/?(p|div|span)\b[^>]*>/gi, "")
    .replace(/&nbsp;/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

/** Ngược lại của `htmlToEditable` khi ghi: dòng mới → `<br>` (HTML mới giữ được xuống dòng). */
export function editableToHtml(text: string): string {
  return text.replace(/\r?\n/g, "<br>");
}

/** Văn bản thuần cho AI đọc: bỏ thẻ, hình thành "[có hình]" (không gửi URL/base64 hình). */
function plainForAi(html: string): string {
  return htmlToEditable(html)
    .replace(/<img[^>]*>/gi, " [có hình] ")
    .replace(/<sup>/gi, "^(")
    .replace(/<sub>/gi, "_(")
    .replace(/<\/(sup|sub)>/gi, ")")
    .replace(/<[^>]+>/g, "")
    .replace(/[ \t]+/g, " ")
    .trim();
}

/** Gộp nội dung một câu thành văn bản gọn để gửi AI phân loại (không kèm HTML/ảnh). */
export function questionTextForAi(q: ExamQuestion): string {
  const parts = [plainForAi(q.question)];
  if (q.type === "multiple_choice") {
    parts.push(q.options.map((o, j) => `${LETTERS[j]}. ${plainForAi(o)}${j === q.answer ? " (đáp án đúng)" : ""}`).join("\n"));
  } else if (q.type === "true_false") {
    parts.push(q.statements.map((s, j) => `${["a", "b", "c", "d"][j]}) ${plainForAi(s.text)} — ${s.answer ? "Đúng" : "Sai"}`).join("\n"));
  } else if (q.type === "short_answer") {
    parts.push(`Đáp án: ${q.answer}`);
  }
  if (q.explanation.trim()) parts.push(`Lời giải: ${plainForAi(q.explanation)}`);
  return parts.join("\n");
}
