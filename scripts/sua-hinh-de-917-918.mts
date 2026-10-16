// Báo lỗi #106 (đề 917 câu 3: hình biển điện cao áp gắn nhầm vào phương án B) và #108 (đề 918 câu 11: hình nền xám, mờ, nhỏ).
//   npx tsx scripts/sua-hinh-de-917-918.mts            # dry-run: dựng ảnh ra scripts/data/sua-hinh-917-918/, không ghi gì
//   npx tsx scripts/sua-hinh-de-917-918.mts --apply    # sao lưu questions của 2 đề → tải ảnh lên Storage → ghi DB → kiểm lại bản đã ghi
import { createClient } from "@supabase/supabase-js";
import sharp from "sharp";
import fs from "node:fs";
import path from "node:path";
for (const l of fs.readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const URL = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const sb = createClient(URL, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const APPLY = process.argv.includes("--apply");
const out = "scripts/data/sua-hinh-917-918";
fs.mkdirSync(out, { recursive: true });

// Hình Faraday–Lenz: nam châm S–N (N gần ống dây) rời ra xa, ống dây đầu 1 (gần nam châm) và đầu 2, điện kế.
const loops = Array.from({ length: 9 }, (_, i) => `<ellipse cx="${262 + i * 28}" cy="105" rx="14" ry="46" fill="none" stroke="#1d4ed8" stroke-width="3"/>`).join("");
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 260" width="1120" height="520">
<rect width="560" height="260" fill="#fff"/>
<rect x="30" y="88" width="75" height="34" fill="#67e8f9" stroke="#0e7490" stroke-width="2.5"/><rect x="105" y="88" width="75" height="34" fill="#ef4444" stroke="#991b1b" stroke-width="2.5"/>
<text x="67" y="113" font-family="Arial" font-size="26" font-weight="700" text-anchor="middle" fill="#0f172a">S</text><text x="142" y="113" font-family="Arial" font-size="26" font-weight="700" text-anchor="middle" fill="#fff">N</text>
<line x1="170" y1="58" x2="60" y2="58" stroke="#1d4ed8" stroke-width="4"/><line x1="60" y1="58" x2="76" y2="48" stroke="#1d4ed8" stroke-width="4"/><line x1="60" y1="58" x2="76" y2="68" stroke="#1d4ed8" stroke-width="4"/>
${loops}
<text x="246" y="46" font-family="Arial" font-size="28" font-weight="700" fill="#0f172a">1</text><text x="494" y="46" font-family="Arial" font-size="28" font-weight="700" fill="#0f172a">2</text>
<polyline points="262,151 262,215 340,215" fill="none" stroke="#1d4ed8" stroke-width="3"/><polyline points="486,151 486,215 408,215" fill="none" stroke="#1d4ed8" stroke-width="3"/>
<circle cx="374" cy="215" r="34" fill="#fff" stroke="#1d4ed8" stroke-width="3"/><text x="374" y="198" font-family="Arial" font-size="18" text-anchor="middle" fill="#0f172a">0</text>
<line x1="374" y1="215" x2="356" y2="196" stroke="#dc2626" stroke-width="4"/><circle cx="374" cy="215" r="4" fill="#dc2626"/>
</svg>`;
const webp = await sharp(Buffer.from(svg)).flatten({ background: "#fff" }).webp({ quality: 85 }).toBuffer();
fs.writeFileSync(`${out}/918-q11-moi.webp`, webp);
console.log("ảnh mới", webp.length, "bytes");

const ts = new Date().toISOString().replace(/[:.]/g, "-");
const { data: rows, error } = await sb.from("exams").select("id,questions").in("id", [917, 918]);
if (error || !rows || rows.length !== 2) throw new Error("không đọc được 2 đề: " + error?.message);
const orig = Object.fromEntries(rows.map((r) => [r.id, structuredClone(r.questions) as any[]]));
const IMG3 = /<br>\s*<img[^>]*1791122586038-hinh-5\.png[^>]*\/?>/;
const OLD11 = "lesson-media/132/cat-1791045252641-hinh-3.webp";
const q917 = structuredClone(orig[917]); const q918 = structuredClone(orig[918]);
if (!IMG3.test(q917[2].options[1])) throw new Error("917 câu 3: không thấy hình cần gỡ (đã sửa rồi?)");
q917[2].options[1] = q917[2].options[1].replace(IMG3, "");
if (!q918[10].question.includes(OLD11)) throw new Error("918 câu 11: không thấy ảnh cũ (đã sửa rồi?)");
const newPath = `132/hinh-lenz-q11-${Date.now()}.webp`;
q918[10].question = q918[10].question.replace(OLD11, `lesson-media/${newPath}`);
console.log("917 câu 3 phương án B mới:", JSON.stringify(q917[2].options[1]));
console.log("918 câu 11 đổi ảnh →", newPath);
if (!APPLY) { console.log("dry-run xong, chưa ghi gì."); process.exit(0); }

fs.writeFileSync(`scripts/logs/sao-luu-de-917-918-${ts}.json`, JSON.stringify(orig));
const up = await sb.storage.from("lesson-media").upload(newPath, webp, { contentType: "image/webp" });
if (up.error) throw new Error("tải ảnh lỗi: " + up.error.message);
for (const [id, q] of [[917, q917], [918, q918]] as const) {
  const { error: e } = await sb.from("exams").update({ questions: q }).eq("id", id);
  if (e) throw new Error(`ghi đề ${id} lỗi: ${e.message}`);
}
// Kiểm lại trên bản đã ghi
const { data: after } = await sb.from("exams").select("id,questions").in("id", [917, 918]);
const probs: string[] = [];
for (const r of after!) {
  const was = orig[r.id], now = r.questions as any[];
  now.forEach((q, i) => { if (JSON.stringify(q) !== JSON.stringify(was[i])) console.log(`  đề ${r.id} câu ${i + 1} đã đổi`); });
  if (now.length !== was.length) probs.push(`đề ${r.id} đổi số câu`);
}
const a917 = after!.find((r) => r.id === 917)!.questions as any[];
if (/hinh-5\.png/.test(JSON.stringify(a917[2]))) probs.push("917 câu 3 vẫn còn hình");
const resp = await fetch(`${URL}/storage/v1/object/public/lesson-media/${newPath}`);
const buf = Buffer.from(await resp.arrayBuffer());
if (!resp.ok) probs.push("ảnh Storage " + resp.status);
if (buf.length > 150 * 1024) probs.push("ảnh > 150 KB: " + buf.length);
const { data, info } = await sharp(buf).flatten({ background: "#fff" }).greyscale().raw().toBuffer({ resolveWithObject: true });
let x0 = info.width, y0 = info.height, x1 = 0, y1 = 0, corner = data[0];
for (let y = 0; y < info.height; y++) for (let x = 0; x < info.width; x++) if (255 - data[y * info.width + x] > 20) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
const ratio = ((x1 - x0) * (y1 - y0)) / (info.width * info.height);
console.log(`Storage: ${resp.status}, ${(buf.length / 1024).toFixed(0)} KB, ${info.width}×${info.height}, góc=${corner}, nét vẽ chiếm ${(ratio * 100).toFixed(0)}% khung`);
if (corner < 250) probs.push("nền không trắng");
if (ratio < 0.35) probs.push("nét vẽ < 35% khung");
fs.writeFileSync(`${out}/918-q11-375px.png`, await sharp(buf).resize(343).png().toBuffer());
console.log(probs.length ? "CÒN LỖI:\n - " + probs.join("\n - ") : "KIỂM LẠI: đạt");
