import qrcode from "qrcode-generator";

/**
 * lib/qr.ts — sinh mã QR thuần tính toán (không đụng DOM), dùng cho mã QR của đề thi.
 *
 * Tách khỏi component để kiểm chứng được: `npx tsx scripts/kiem-qr.mts` dựng lại ảnh từ đúng
 * hàm này rồi GIẢI MÃ bằng bộ đọc QR thật, đối chiếu chuỗi gốc — mã QR sai thì im lặng, không
 * ai biết cho tới lúc học sinh không quét được, nên phải có bước kiểm máy.
 *
 * Dùng `qrcode-generator` (MIT, cùng gói mà bản in sách ở `book/` dùng) — không gọi dịch vụ
 * ngoài, không thêm request, chạy được cả trong web xuất tĩnh.
 */

/** Vùng trắng bao quanh mã, tính bằng số ô. Chuẩn QR cần ≥ 4 ô để máy ảnh bắt được góc. */
export const QR_QUIET_ZONE = 4;

export interface QrCode {
  /** Số ô mỗi cạnh (chưa tính vùng trắng). */
  count: number;
  /** Đường SVG gộp: mỗi ô đen là một hình vuông 1×1 đặt tại (cột, hàng). */
  d: string;
  /** Ô (hàng, cột) có đen không — dùng để vẽ ảnh PNG hoặc kiểm chứng. */
  isDark(row: number, col: number): boolean;
}

/** Sinh ma trận QR cho một chuỗi. Mức sửa lỗi M: cân bằng giữa mật độ và khả năng chịu lỗi. */
export function makeQrCode(text: string): QrCode {
  const qr = qrcode(0, "M");
  qr.addData(text);
  qr.make();
  const count = qr.getModuleCount();
  let d = "";
  for (let r = 0; r < count; r += 1) {
    for (let c = 0; c < count; c += 1) {
      if (qr.isDark(r, c)) d += `M${c} ${r}h1v1h-1z`;
    }
  }
  return { count, d, isDark: (r: number, c: number) => qr.isDark(r, c) };
}
