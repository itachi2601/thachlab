// Kiểm lần 2 sau khi cắt lề trắng: (1) ảnh mới có nét vẽ chạm mép (nghi cắt mất) (2) ngưỡng nhạy hơn (>6) có thấy nét mờ nằm ngoài khung cắt (3) ảnh mới trên Storage tải được, ≤150 KB.
//   npx tsx scripts/kiem-sau-cat-anh.mts
import sharp from "sharp";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), "data", "cat-anh-le-trang");
const env = fs.readFileSync(path.resolve(dir, "..", "..", "..", ".env.local"), "utf8");
const base = env.split("\n").find((l) => l.startsWith("NEXT_PUBLIC_SUPABASE_URL="))!.split("=")[1].trim() + "/storage/v1/object/public/lesson-media/";
const files = fs.readdirSync(dir).filter((f) => f.endsWith(".webp"));
const bad: string[] = [];
async function box(buf: Buffer, thr: number) {
  const { data, info } = await sharp(buf).flatten({ background: "#fff" }).greyscale().raw().toBuffer({ resolveWithObject: true });
  const { width: w, height: h } = info; let x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (255 - data[y * w + x] > thr) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  return { w, h, x0, y0, x1, y1 };
}
let i = 0;
async function worker() {
  for (;;) {
    const f = files[i++]; if (!f) return;
    const m = /^(\d+)-(cat-.+)\.webp$/.exec(f)!; const rel = `${m[1]}/${m[2]}.webp`;
    const local = fs.readFileSync(path.join(dir, f));
    const r = await fetch(base + rel);
    if (!r.ok) { bad.push(`${rel}: Storage ${r.status} (CHƯA tải lên?)`); continue; }
    const remote = Buffer.from(await r.arrayBuffer());
    if (remote.length > 150 * 1024) bad.push(`${rel}: ${(remote.length / 1024).toFixed(0)} KB > 150`);
    if (remote.length !== local.length) bad.push(`${rel}: bản trên mạng khác bản xem thử`);
    const b = await box(remote, 20);
    const edge = 3;
    if (b.x0 < edge || b.y0 < edge || b.x1 > b.w - 1 - edge || b.y1 > b.h - 1 - edge) bad.push(`${rel}: nét vẽ chạm mép (${b.x0},${b.y0},${b.x1},${b.y1} / ${b.w}×${b.h}) — nghi cắt mất`);
    const f2 = await box(remote, 6);
    if (f2.x0 < 2 || f2.y0 < 2 || f2.x1 > f2.w - 3 || f2.y1 > f2.h - 3) bad.push(`${rel}: nét MỜ chạm mép — nghi cắt mất nét nhạt`);
  }
}
await Promise.all(Array.from({ length: 8 }, worker));
console.log(`${files.length} ảnh, ${bad.length} cảnh báo`); bad.forEach((x) => console.log(" -", x));
