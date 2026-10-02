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

export function dependsOnOtherQuestion(q: ExamQuestion): boolean {
  return CONTEXT_DEPENDENCY_RE.test((q.question ?? "").replace(/<[^>]+>/g, " "));
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
    `Chép lại đầy đủ dữ kiện vào từng câu (mỗi câu phải tự đọc hiểu được) rồi tải lại; nếu câu đã đủ dữ kiện thì bỏ qua cảnh báo.`
  );
}
