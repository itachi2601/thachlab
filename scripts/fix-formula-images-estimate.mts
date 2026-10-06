// Vá ảnh nền A4 trong đề đã đăng KHI KHÔNG còn file Word nguồn khớp (không biết cỡ khung thật) → ƯỚC cỡ.
//   npx tsx scripts/fix-formula-images-estimate.mts <exam_id> [<exam_id>...] [--dry]
// Quy tắc ước (đo trên ~900 ảnh đã vá chính xác 5/10/2026): ảnh công thức nền A4 bị co về tỉ lệ ≈0,075 px/px khi nội dung
// hẹp (<600px); công thức rộng (≥600px, tràn bề ngang trang) tỉ lệ dao động 0,055–0,21 → dùng 0,09. Sai số cỡ có thể ±30%.
// Ưu tiên dùng fix-formula-images.mts (chính xác, cần docx nguồn) khi còn file.
import { createClient } from "@supabase/supabase-js";
import sharp from "sharp";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { buildImgTag, isPageSizedPng } from "@/services/docx-image-trim";
import { uploadLessonMedia } from "@/services/lesson-media";

const dry = process.argv.includes("--dry");
const ids = process.argv.slice(2).filter((a) => /^\d+$/.test(a)).map(Number);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const env = Object.fromEntries(
  fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#"))
    .map((l) => { const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^"|"$/g, "")]; }),
);
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL!, env.SUPABASE_SERVICE_ROLE_KEY!, { auth: { persistSession: false } });
const backupDir = path.join(root, "scripts/logs/fix-formula-images-backup");
fs.mkdirSync(backupDir, { recursive: true });
const IMG_RE = /<img\b[^>]*?src="([^"]+)"[^>]*?\/>/g;

for (const examId of ids) {
  const { data: ex, error } = await sb.from("exams").select("id, questions").eq("id", examId).single();
  if (error || !ex) { console.log(`exam ${examId}: LỖI đọc ${error?.message}`); continue; }
  fs.writeFileSync(path.join(backupDir, `exam-${examId}-estimate.json`), JSON.stringify(ex));
  const urls = new Set<string>();
  const scan = (x: unknown): void => {
    if (typeof x === "string") for (const m of x.matchAll(IMG_RE)) { if (!/\sstyle="/.test(m[0])) urls.add(m[1]); }
    else if (Array.isArray(x)) x.forEach(scan);
    else if (x && typeof x === "object") Object.values(x).forEach(scan);
  };
  scan(ex.questions);
  const fixed = new Map<string, string>(); // url cũ → thẻ mới
  let n = 0;
  for (const url of urls) {
    const buf = Buffer.from(await (await fetch(url)).arrayBuffer());
    const meta = await sharp(buf).metadata();
    if (!isPageSizedPng(meta.width ?? 0, meta.height ?? 0)) continue;
    const { data, info } = await sharp(await sharp(buf).flatten({ background: "#ffffff" }).toBuffer())
      .trim({ background: "#ffffff", threshold: 12 }).png().toBuffer({ resolveWithObject: true });
    if (info.width >= (meta.width ?? 0) * 0.98) continue;
    const k = info.width >= 600 ? 0.09 : 0.075;
    const size = { w: info.width * k, h: info.height * k };
    let newUrl = "DRY";
    if (!dry) {
      const lessonId = Number(url.match(/lesson-media\/(\d+)\//)?.[1]);
      const name = url.split("/").pop()!.replace(/^\d+-/, "");
      const [m] = await uploadLessonMedia(sb, lessonId, [{ name, dataUri: "data:image/png;base64," + data.toString("base64"), placeholder: "media/x.png" }]);
      newUrl = m.url;
    }
    fixed.set(url, buildImgTag(newUrl, "Hình", size));
    n += 1;
  }
  const fix = (s: string): string => s.replace(IMG_RE, (tag, u: string) => {
    if (/\sstyle="/.test(tag) || !fixed.has(u)) return tag;
    const alt = tag.match(/\balt="([^"]*)"/)?.[1] ?? "Hình";
    return fixed.get(u)!.replace('alt="Hình"', `alt="${alt}"`);
  });
  const map = (x: unknown): unknown =>
    typeof x === "string" ? fix(x) : Array.isArray(x) ? x.map(map)
      : x && typeof x === "object" ? Object.fromEntries(Object.entries(x).map(([k, y]) => [k, map(y)])) : x;
  if (!dry && n) {
    const up = await sb.from("exams").update({ questions: map(ex.questions) }).eq("id", examId);
    if (up.error) { console.log(`exam ${examId}: LỖI ghi ${up.error.message}`); continue; }
    const { data: qb } = await sb.from("question_bank").select("id, question").eq("source_exam_id", examId);
    for (const row of qb ?? []) {
      const nq = map(row.question);
      if (JSON.stringify(nq) !== JSON.stringify(row.question)) await sb.from("question_bank").update({ question: nq }).eq("id", row.id);
    }
  }
  console.log(`exam ${examId}: ${n} ảnh ước cỡ${dry ? " (dry)" : ""}`);
}
