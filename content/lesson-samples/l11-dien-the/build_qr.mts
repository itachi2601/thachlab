// Sinh mã QR mở đề Kiểm tra lý thuyết (đề 1215, mục 198) cho màn cuối tren-lop.html rồi giải mã lại để kiểm.
// Dùng: npx tsx content/lesson-samples/l11-dien-the/build_qr.mts content/lesson-samples/l11-dien-the/tren-lop-qr.svg
import jsQR from "jsqr";
import { writeFileSync } from "node:fs";
import { makeQrCode, QR_QUIET_ZONE } from "../../../lib/qr";
import { examQrUrl, examIdFromScan } from "../../../lib/exam-link";
const url = examQrUrl(1215, 198);
const q = makeQrCode(url), n = q.count + 2 * QR_QUIET_ZONE;
const svg = `<svg viewBox="${-QR_QUIET_ZONE} ${-QR_QUIET_ZONE} ${n} ${n}" role="img" aria-label="Mã QR mở đề 1215" shape-rendering="crispEdges"><rect x="${-QR_QUIET_ZONE}" y="${-QR_QUIET_ZONE}" width="${n}" height="${n}" fill="#fff"/><path d="${q.d}" fill="#000"/></svg>`;
writeFileSync(process.argv[2], svg);
const s = 8, W = n * s, px = new Uint8ClampedArray(W * W * 4);
for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) {
  const r = Math.floor(y / s) - QR_QUIET_ZONE, c = Math.floor(x / s) - QR_QUIET_ZONE;
  const dark = r >= 0 && c >= 0 && r < q.count && c < q.count && q.isDark(r, c);
  const i = (y * W + x) * 4; px[i] = px[i + 1] = px[i + 2] = dark ? 0 : 255; px[i + 3] = 255;
}
const dec = jsQR(px, W, W);
console.log(url, "| giải mã:", dec?.data, "| khớp:", dec?.data === url, "| examIdFromScan:", examIdFromScan(dec?.data ?? ""));
