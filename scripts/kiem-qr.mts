/**
 * scripts/kiem-qr.mts — kiểm mã QR của đề thi (lib/qr.ts) bằng cách GIẢI MÃ lại ảnh.
 *
 * Vì sao cần: mã QR sai thì im lặng — không lỗi build, không lỗi console, chỉ tới lúc học sinh
 * giơ điện thoại lên mới biết. Script dựng ảnh bitmap từ ĐÚNG hàm `makeQrCode` mà trang quản trị
 * dùng, rồi đọc lại bằng bộ giải mã QR thật (`jsqr`, cùng bộ sẽ dùng cho mục quét của học sinh).
 *
 * Chạy: npx tsx scripts/kiem-qr.mts
 * Thoát mã 1 nếu có mã nào không giải mã đúng.
 */
import jsQR from "jsqr";
import { makeQrCode, QR_QUIET_ZONE } from "../lib/qr";

const SCALE = 6; // số điểm ảnh mỗi ô — đủ để bộ đọc bắt góc

/** Dựng ảnh RGBA từ ma trận QR (đúng cách ExamQrPanel vẽ, chỉ khác là ra bitmap thay vì SVG). */
function render(text: string): { data: Uint8ClampedArray; side: number } {
  const { count, isDark } = makeQrCode(text);
  const side = (count + QR_QUIET_ZONE * 2) * SCALE;
  const data = new Uint8ClampedArray(side * side * 4).fill(255);
  for (let r = 0; r < count; r += 1) {
    for (let c = 0; c < count; c += 1) {
      if (!isDark(r, c)) continue;
      for (let y = 0; y < SCALE; y += 1) {
        for (let x = 0; x < SCALE; x += 1) {
          const i = (((r + QR_QUIET_ZONE) * SCALE + y) * side + (c + QR_QUIET_ZONE) * SCALE + x) * 4;
          data[i] = 0;
          data[i + 1] = 0;
          data[i + 2] = 0;
          data[i + 3] = 255;
        }
      }
    }
  }
  return { data, side };
}

const CASES = [
  "https://thachlab.id.vn/kiem-tra/lam/?id=1",
  "https://thachlab.id.vn/kiem-tra/lam/?id=770",
  "https://thachlab.id.vn/kiem-tra/lam/?id=123456",
  // Đề nằm trong một bài học: link kèm cả `item` — vẫn phải đọc được.
  "https://thachlab.id.vn/kiem-tra/lam/?id=770&item=1234",
];

let failed = 0;
for (const text of CASES) {
  const { data, side } = render(text);
  const hit = jsQR(data, side, side);
  const ok = hit?.data === text;
  console.log(`${ok ? "✓" : "✕"} ${text}  (${side}×${side}px) → ${hit?.data ?? "KHÔNG ĐỌC ĐƯỢC"}`);
  if (!ok) failed += 1;
}

if (failed > 0) {
  console.error(`\n✕ ${failed}/${CASES.length} mã QR không giải mã đúng.`);
  process.exit(1);
}
console.log(`\n✓ ${CASES.length}/${CASES.length} mã QR giải mã đúng.`);
