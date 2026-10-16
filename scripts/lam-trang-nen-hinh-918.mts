// Báo lỗi #108: hình câu 11 đề 918 nền xám + lề thừa. Giữ NGUYÊN hình gốc (thầy chốt 16/10), chỉ: xám → trắng, cắt lề, phóng 2× (lanczos).
//   npx tsx scripts/lam-trang-nen-hinh-918.mts            # dry-run: ra scripts/data/sua-hinh-917-918/918-q11-trang.webp (+ bản 375px), không ghi gì
//   npx tsx scripts/lam-trang-nen-hinh-918.mts --apply    # sao lưu → tải lên Storage → đổi URL trong câu 11 → kiểm lại bản đã ghi
import { createClient } from "@supabase/supabase-js";
import sharp from "sharp";
import fs from "node:fs";
for (const l of fs.readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const URL = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const sb = createClient(URL, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const APPLY = process.argv.includes("--apply");
const out = "scripts/data/sua-hinh-917-918";
fs.mkdirSync(out, { recursive: true });

const SRC = `${URL}/storage/v1/object/public/lesson-media/132/cat-1791045252641-hinh-3.webp`;
const src = Buffer.from(await (await fetch(SRC)).arrayBuffer());
const { data, info } = await sharp(src).removeAlpha().raw().toBuffer({ resolveWithObject: true });
const { width: w, height: h } = info;
// Nền xám ≈128: điểm ít màu (max-min nhỏ) kéo giãn theo độ sáng để 128→255, đen giữ đen (chữ 1, 2, 0). Điểm có màu giữ nguyên.
const px = Buffer.from(data);
for (let i = 0; i < px.length; i += 3) {
  const r = px[i], g = px[i + 1], b = px[i + 2];
  if (Math.max(r, g, b) - Math.min(r, g, b) < 28) {
    const v = Math.min(255, Math.round((r + g + b) / 3 * 255 / 128));
    px[i] = px[i + 1] = px[i + 2] = v;
  }
}
// Hộp nét vẽ (ngưỡng 20 so với trắng) rồi chừa lề 12 px.
let x0 = w, y0 = h, x1 = 0, y1 = 0;
for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const k = (y * w + x) * 3; if (255 - Math.min(px[k], px[k + 1], px[k + 2]) > 20) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); } }
const M = 12;
x0 = Math.max(0, x0 - M); y0 = Math.max(0, y0 - M); x1 = Math.min(w - 1, x1 + M); y1 = Math.min(h - 1, y1 + M);
const cw = x1 - x0 + 1, ch = y1 - y0 + 1;
const webp = await sharp(px, { raw: { width: w, height: h, channels: 3 } })
  .extract({ left: x0, top: y0, width: cw, height: ch })
  .resize({ width: cw * 2, kernel: "lanczos3" })
  .sharpen().webp({ quality: 88 }).toBuffer();
fs.writeFileSync(`${out}/918-q11-trang.webp`, webp);
fs.writeFileSync(`${out}/918-q11-trang-375px.png`, await sharp(webp).resize(343).png().toBuffer());
console.log(`gốc ${w}×${h} → cắt (${x0},${y0})-(${x1},${y1}) ${cw}×${ch} → ${cw * 2}×${ch * 2}, ${(webp.length / 1024).toFixed(0)} KB`);
if (!APPLY) { console.log("dry-run xong, chưa ghi gì."); process.exit(0); }

const ts = new Date().toISOString().replace(/[:.]/g, "-");
const { data: row, error } = await sb.from("exams").select("id,questions").eq("id", 918).single();
if (error || !row) throw new Error("không đọc được đề 918");
const orig = row.questions as any[];
fs.writeFileSync(`scripts/logs/sao-luu-de-918-lam-trang-${ts}.json`, JSON.stringify(orig));
const q = structuredClone(orig);
const m = /lesson-media\/(132\/(?:hinh-lenz-q11-\d+|cat-1791045252641-hinh-3)\.webp)/.exec(q[10].question);
if (!m) throw new Error("918 câu 11: không thấy ảnh cần thay");
const newPath = `132/hinh-lenz-goc-trang-${Date.now()}.webp`;
const up = await sb.storage.from("lesson-media").upload(newPath, webp, { contentType: "image/webp" });
if (up.error) throw new Error("tải ảnh lỗi: " + up.error.message);
q[10].question = q[10].question.replace(m[1], newPath);
const { error: e } = await sb.from("exams").update({ questions: q }).eq("id", 918);
if (e) throw new Error("ghi lỗi: " + e.message);

const { data: after } = await sb.from("exams").select("questions").eq("id", 918).single();
const now = after!.questions as any[];
const probs: string[] = [];
now.forEach((qq, i) => { if (JSON.stringify(qq) !== JSON.stringify(orig[i])) console.log(`  đề 918 câu ${i + 1} đã đổi`); });
if (!now[10].question.includes(newPath)) probs.push("URL mới không có trong bản ghi");
const resp = await fetch(`${URL}/storage/v1/object/public/lesson-media/${newPath}`);
const buf = Buffer.from(await resp.arrayBuffer());
if (!resp.ok) probs.push("Storage " + resp.status);
if (buf.length > 150 * 1024) probs.push("> 150 KB");
const g = await sharp(buf).flatten({ background: "#fff" }).greyscale().raw().toBuffer({ resolveWithObject: true });
const corner = g.data[0];
let a = g.info.width, b = g.info.height, c = 0, d = 0;
for (let y = 0; y < g.info.height; y++) for (let x = 0; x < g.info.width; x++) if (255 - g.data[y * g.info.width + x] > 20) { a = Math.min(a, x); c = Math.max(c, x); b = Math.min(b, y); d = Math.max(d, y); }
const ratio = ((c - a) * (d - b)) / (g.info.width * g.info.height);
console.log(`Storage ${resp.status}, ${(buf.length / 1024).toFixed(0)} KB, ${g.info.width}×${g.info.height}, góc=${corner}, nét chiếm ${(ratio * 100).toFixed(0)}%`);
if (corner < 250) probs.push("nền không trắng");
if (ratio < 0.35) probs.push("nét vẽ < 35% khung");
console.log(probs.length ? "CÒN LỖI:\n - " + probs.join("\n - ") : "KIỂM LẠI: đạt");
