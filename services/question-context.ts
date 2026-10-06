/**
 * Phát hiện câu "phụ thuộc câu khác": mở đầu bằng "(Tiếp câu trên)", "Với dữ kiện như câu trước",
 * "ở câu trên"... Câu bị tách khỏi đề (luyện tập bốc ngẫu nhiên từ ngân hàng, đảo thứ tự, ngân hàng
 * câu hỏi) sẽ mất ngữ cảnh — học sinh không làm được (đề 237 câu 3, báo lỗi 2/10/2026).
 * Dùng ở trang Đăng đề / Nhập bài (khoá nút Đăng tới khi sửa hoặc xác nhận) và ở PracticeSession
 * (loại khỏi lượt bốc ngẫu nhiên).
 */
import type { ExamQuestion } from "@/features/exams/types";

export const CONTEXT_DEPENDENCY_RE =
  /\(\s*tiếp\s+(?:theo\s+)?câu|(?:ở|trong|của|như|từ|theo)\s+câu\s+(?:trên|trước)|câu\s+(?:trên|trước)\b|(?:dữ kiện|thông tin|kết quả)\s+(?:của\s+)?câu\s+\d+/i;

/** "Sử dụng thông tin sau cho Câu X và Câu Y:" nằm GIỮA/CUỐI câu dẫn = parser dính đoạn dẫn của câu sau vào câu này
 * (đề 136, 138, 173... bị 2/10/2026). Đứng đầu câu thì là đoạn dẫn của chính câu đó — hợp lệ. */
export const GLUED_PASSAGE_RE = /\S[^<]{0,}?\s(?:sử dụng (?:thông tin|dữ kiện)[^:<]{0,40}?(?:cho|để trả lời|trả lời)[^:<]{0,40}?:)/i;

export function dependsOnOtherQuestion(q: ExamQuestion): boolean {
  const text = (q.question ?? "").replace(/<[^>]+>/g, " ").trim();
  return CONTEXT_DEPENDENCY_RE.test(text) || (GLUED_PASSAGE_RE.test(text) && !/^sử dụng/i.test(text));
}

/** Số thứ tự (1-based) các câu phụ thuộc câu khác. */
export function questionsDependingOnOthers(questions: ExamQuestion[]): number[] {
  const out: number[] = [];
  questions.forEach((q, i) => {
    if (dependsOnOtherQuestion(q)) out.push(i + 1);
  });
  return out;
}

export function contextDependencyWarning(nums: number[]): string | null {
  if (!nums.length) return null;
  const list = nums.length > 12 ? `${nums.slice(0, 12).join(", ")}… (${nums.length} câu)` : nums.join(", ");
  return (
    `Câu ${list} dựa vào "câu trên/câu trước" — khi bốc ngẫu nhiên hoặc đảo thứ tự, học sinh sẽ không thấy dữ kiện. ` +
    `Câu có 'Sử dụng thông tin sau cho Câu…' nằm giữa/cuối là đoạn dẫn của câu sau bị dính vào. Chép lại đầy đủ dữ kiện vào từng câu (mỗi câu phải tự đọc hiểu được) rồi tải lại; nếu câu đã đủ dữ kiện thì bỏ qua cảnh báo.`
  );
}

/** Chuỗi so khớp câu trùng giữa các đề: bỏ HTML, gom khoảng trắng, không phân biệt hoa/thường.
 *  Gồm cả phương án/ý/đáp án để hai câu cùng đề bài nhưng khác lựa chọn không bị coi là một. */
export function questionKey(q: ExamQuestion): string {
  const clean = (t: string) => t.replace(/<[^>]*>/g, " ").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim().toLowerCase();
  const parts = [q.question];
  if (q.type === "multiple_choice") parts.push(...q.options);
  else if (q.type === "true_false") parts.push(...q.statements.map((s) => s.text));
  else if (q.type === "short_answer") parts.push(q.answer);
  return parts.map(clean).join("|");
}
