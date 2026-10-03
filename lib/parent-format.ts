/* Định dạng dùng chung cho các khối trang phụ huynh (P11: ngày có thứ; P12: màu luôn kèm chữ). */

const pad = (n: number) => String(n).padStart(2, "0");
const WEEKDAYS = ["Chủ nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"];

/** "Thứ Ba, 30/09/2026" — nhận ISO đầy đủ hoặc "YYYY-MM-DD". */
export function longDate(iso: string): string {
  const d = new Date(iso.length === 10 ? `${iso}T00:00:00` : iso);
  return `${WEEKDAYS[d.getDay()]}, ${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()}`;
}

/** "Thứ Ba, 30/09" (không năm) — cho lịch sắp tới. */
export function dayMonth(d: Date): string {
  return `${WEEKDAYS[d.getDay()]}, ${pad(d.getDate())}/${pad(d.getMonth() + 1)}`;
}

export function scoreText(score: number): string {
  return score.toLocaleString("vi-VN", { minimumFractionDigits: 0, maximumFractionDigits: 2 });
}

/**
 * Xếp loại theo cách phụ huynh đã quen từ sổ liên lạc (Giỏi/Khá/Trung bình), thay cho mốc "Đạt 6,5" tự đặt.
 * Nhãn thấp nhất cố ý là "Cần cố gắng thêm" chứ không phải "Yếu" (P15: không phán xét).
 */
export interface GradeBand {
  label: string;
  /** Màu chữ — luôn đi cùng `label` bằng chữ (P12). */
  cls: string;
  /** Màu cột của biểu đồ cột. */
  bar: string;
}

export function gradeBand(score: number): GradeBand {
  if (score >= 8) return { label: "Giỏi", cls: "text-emerald-300", bar: "bg-emerald-400" };
  if (score >= 6.5) return { label: "Khá", cls: "text-cyan-300", bar: "bg-cyan-400" };
  if (score >= 5) return { label: "Trung bình", cls: "text-amber-300", bar: "bg-amber-400" };
  return { label: "Cần cố gắng thêm", cls: "text-red-300", bar: "bg-red-400" };
}

/** "25/09" — luôn dùng dấu gạch chéo, không phụ thuộc locale của trình duyệt. */
export function shortDate(iso: string): string {
  const d = new Date(iso);
  return `${pad(d.getDate())}/${pad(d.getMonth() + 1)}`;
}
