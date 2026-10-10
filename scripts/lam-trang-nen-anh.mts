// Giữ nguyên ảnh gốc, chỉ đưa NỀN về trắng (+ phóng 3× cho nét mịn) cho các câu thầy chọn "Vẽ lại" kèm ghi chú nền trắng.
// KHÔNG ghi DB / Storage. Kết quả: scripts/data/gemini-hinh/nen-trang/<id>/anh-N.png + xem-thu.html (gốc ↔ mới).
//   npx tsx scripts/lam-trang-nen-anh.mts 610079,618296,...
// Cách làm: nền = màu phổ biến nhất trong ảnh; mỗi kênh nhân 255/nền (nền → trắng, nét tối/màu giữ tương phản);
// điểm gần trắng (>238 cả ba kênh) ép 255 để hết vệt nền mờ.
import sharp from "sharp";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), "data", "gemini-hinh");
const ids = (process.argv[2] ?? "").split(",").map((s) => s.trim()).filter(Boolean);
if (!ids.length) { console.error("cần danh sách id"); process.exit(1); }
const SCALE = 3;
const rows: string[] = [];
for (const id of ids) {
  const src = path.join(root, "cau", id);
  const dst = path.join(root, "nen-trang", id);
  fs.mkdirSync(dst, { recursive: true });
  const files = fs.readdirSync(src).filter((f) => /^anh-\d+\./.test(f)).sort();
  for (const f of files) {
    const { data, info } = await sharp(path.join(src, f)).removeAlpha().resize({ width: undefined, height: undefined }).raw().toBuffer({ resolveWithObject: true });
    const { width: w, height: h } = info;
    // nền: màu phổ biến nhất toàn ảnh (lượng tử 8 mức/kênh)
    const cnt = new Map<number, { n: number; r: number; g: number; b: number }>();
    const add = (x: number, y: number) => {
      const i = (y * w + x) * 3;
      const k = (data[i] >> 3) * 1024 + (data[i + 1] >> 3) * 32 + (data[i + 2] >> 3);
      const e = cnt.get(k) ?? { n: 0, r: 0, g: 0, b: 0 };
      e.n++; e.r += data[i]; e.g += data[i + 1]; e.b += data[i + 2]; cnt.set(k, e);
    };
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) add(x, y);
    const bg = [...cnt.values()].sort((a, b) => b.n - a.n)[0];
    const B = [bg.r / bg.n, bg.g / bg.n, bg.b / bg.n];
    // phóng 3× rồi mới chỉnh màu để viền không lem
    const big = await sharp(path.join(src, f)).removeAlpha().resize({ width: w * SCALE, kernel: "lanczos3" }).raw().toBuffer({ resolveWithObject: true });
    const out = Buffer.alloc(big.data.length);
    for (let i = 0; i < big.data.length; i += 3) {
      const r = Math.min(255, (big.data[i] * 255) / B[0]);
      const g = Math.min(255, (big.data[i + 1] * 255) / B[1]);
      const b = Math.min(255, (big.data[i + 2] * 255) / B[2]);
      const white = r > 238 && g > 238 && b > 238;
      out[i] = white ? 255 : r; out[i + 1] = white ? 255 : g; out[i + 2] = white ? 255 : b;
    }
    const name = f.replace(/\.\w+$/, ".png");
    await sharp(out, { raw: { width: big.info.width, height: big.info.height, channels: 3 } }).png({ compressionLevel: 9 }).toFile(path.join(dst, name));
    rows.push(`<tr><td>#${id} ${name}<br><small>nền ${B.map((v) => Math.round(v)).join(",")}</small></td><td><img src="../cau/${id}/${f}" height="110" style="image-rendering:pixelated"></td><td><img src="${id}/${name}" height="110"></td></tr>`);
  }
}
fs.writeFileSync(path.join(root, "nen-trang", "xem-thu.html"), `<!doctype html><meta charset="utf-8"><title>Nền trắng</title><body style="font-family:system-ui"><table border="1" cellpadding="6"><tr><th>ảnh</th><th>gốc</th><th>nền trắng</th></tr>${rows.join("")}</table></body>`);
console.log(`xong ${rows.length} ảnh → scripts/data/gemini-hinh/nen-trang/xem-thu.html`);
