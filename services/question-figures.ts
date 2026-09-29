/**
 * Kiểm tra "câu nhắc tới đồ thị / hình vẽ nhưng không có ảnh".
 *
 * Dùng chung cho: parser đề (cảnh báo lúc dựng đề), trang Đăng đề / Nhập bài (cờ đỏ trước khi
 * Đăng) và trang Ngân hàng câu hỏi (bộ lọc "Nhắc hình, thiếu ảnh"). Regex ở đây và chuỗi
 * FIGURE_WORDS_PG phải giữ cùng nghĩa vì FIGURE_WORDS_PG được gửi thẳng cho PostgREST (`imatch`).
 */
import type { ExamQuestion } from "@/features/exams/types";

/** Từ khoá cho biết câu cần có hình. Không có dấu phẩy/ngoặc để dùng được trong bộ lọc PostgREST. */
export const FIGURE_WORDS_PG = "đồ thị|hình vẽ|hình bên|hình dưới|hình trên|như hình|sơ đồ|mạch điện như";
export const FIGURE_WORDS_RE = new RegExp(FIGURE_WORDS_PG, "i");

/** Có ảnh thật (img/svg) hay chưa. */
export const HAS_IMAGE_PG = "<img|<svg";
export const HAS_IMAGE_RE = new RegExp(HAS_IMAGE_PG, "i");

/** Các mốc mà trình đọc Word / parser chèn thay cho hình không lấy được. */
export const FIGURE_MARK_PG = "⟦ảnh WMF⟧|⟦hình vẽ Word⟧|⟦hình TikZ⟧";
export const FIGURE_MARK_RE = new RegExp(FIGURE_MARK_PG);

function stemOf(q: ExamQuestion): string {
  return q.question ?? "";
}

function allHtml(q: ExamQuestion): string {
  const parts: string[] = [stemOf(q)];
  if ("options" in q && Array.isArray(q.options)) parts.push(...q.options);
  if ("statements" in q && Array.isArray(q.statements)) parts.push(...q.statements.map((s) => s.text));
  return parts.join("\n");
}

/** Câu dẫn nhắc tới hình (không xét lời giải/nhãn). */
export function mentionsFigure(q: ExamQuestion): boolean {
  return FIGURE_WORDS_RE.test(stemOf(q).replace(/<[^>]+>/g, " "));
}

/** Đã có ảnh ở câu dẫn hoặc phương án. */
export function hasFigure(q: ExamQuestion): boolean {
  return HAS_IMAGE_RE.test(allHtml(q));
}

/** Còn mốc "⟦…⟧" thay cho hình — chắc chắn thiếu, dù có nhắc hình hay không. */
export function hasFigureMark(q: ExamQuestion): boolean {
  return FIGURE_MARK_RE.test(allHtml(q));
}

/** Câu thiếu hình: nhắc hình mà không có ảnh, hoặc còn mốc hình chưa thay. */
export function isMissingFigure(q: ExamQuestion): boolean {
  return hasFigureMark(q) || (mentionsFigure(q) && !hasFigure(q));
}

/** Số thứ tự (1-based) các câu thiếu hình trong một đề. */
export function questionsMissingFigure(questions: ExamQuestion[]): number[] {
  const out: number[] = [];
  questions.forEach((q, i) => {
    if (isMissingFigure(q)) out.push(i + 1);
  });
  return out;
}

/** Câu cảnh báo dùng chung ở parser / trang Đăng đề. */
export function missingFigureWarning(nums: number[]): string | null {
  if (!nums.length) return null;
  const list = nums.length > 12 ? `${nums.slice(0, 12).join(", ")}… (${nums.length} câu)` : nums.join(", ");
  return (
    `Câu ${list} nhắc tới đồ thị/hình vẽ nhưng không có ảnh — ` +
    `học sinh sẽ không làm được. Chèn lại hình (ảnh PNG/JPG trong Word, hoặc \\includegraphics trong .tex) rồi tải lên lần nữa; ` +
    `nếu câu thật sự không cần hình thì bỏ qua cảnh báo này.`
  );
}
