// Vá ảnh công thức/hình nền A4 trong các đề ĐÃ ĐĂNG bằng cách đọc lại file Word trung gian (có sẵn kích thước khung).
//   npx tsx scripts/fix-formula-images.mts [--run de-l10-24-25|de-l10-23|de-l11] [--only <exam_id>] [--limit N] [--dry]
// Với mỗi đề: đọc scripts/logs/<run>/<slug>/de_thachlab.docx → cắt ảnh cả trang → tải ảnh mới lên lesson-media →
// thay thẻ <img> trong exams.questions và question_bank.question (cùng source_exam_id). Sao lưu questions gốc ra
// scripts/logs/fix-formula-images-backup/. Chạy lại an toàn (thẻ đã có style="" thì bỏ qua). Ảnh cũ để nguyên trên Storage.
import { DOMParser as XmlDomParser } from "@xmldom/xmldom";
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import { readDocx } from "@/services/docx-reader";
import { buildImgTag, trimPageImages } from "@/services/docx-image-trim";
import { uploadLessonMedia } from "@/services/lesson-media";

class NodeDOMParser {
  parseFromString(str: string, type: string) {
    const doc = new XmlDomParser().parseFromString(str, type as never);
    (doc as unknown as { querySelector: () => null }).querySelector = () => null;
    return doc;
  }
}
(globalThis as unknown as { DOMParser: typeof NodeDOMParser }).DOMParser = NodeDOMParser;

const arg = (k: string) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : undefined; };
const dry = process.argv.includes("--dry");
const run = arg("--run") ?? "de-l10-24-25";
const only = arg("--only") ? Number(arg("--only")) : null;
const limit = arg("--limit") ? Number(arg("--limit")) : Infinity;

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const env = Object.fromEntries(
  fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#"))
    .map((l) => { const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^"|"$/g, "")]; }),
);
const supabase = createClient(env.NEXT_PUBLIC_SUPABASE_URL!, env.SUPABASE_SERVICE_ROLE_KEY!, { auth: { persistSession: false } });

// --map <json>: {"<exam_id>": "<đường dẫn de_thachlab/out.docx>"} — dùng cho đề không có run.json (vd thi thử lớp 12)
const mapFile = arg("--map");
const runJson = mapFile ? {} : (JSON.parse(fs.readFileSync(path.join(root, `scripts/data/${run}-run.json`), "utf8")) as Record<string, { status?: string; upload?: string[] }>);
const workRoot = path.join(root, `scripts/logs/${run}`);
const jobs: { bo: string; examId: number; docx: string }[] = mapFile
  ? Object.entries(JSON.parse(fs.readFileSync(mapFile, "utf8")) as Record<string, string>).map(([id, docx]) => ({ bo: `exam-${id}`, examId: Number(id), docx }))
  : Object.entries(runJson).filter(([, v]) => v.status === "OK").map(([bo, v]) => {
      const ky = bo.split("/")[0];
      const slug = `${ky.slice(0, 2)}_${bo.split("/").slice(1).join("/")}`.replace(/[^A-Za-z0-9]+/g, "_").slice(0, 80).replace(/^_+|_+$/g, "");
      return { bo, examId: Number((v.upload ?? []).join(" ").match(/exam (\d+)/)?.[1]), docx: path.join(workRoot, slug, "de_thachlab.docx") };
    });
const backupDir = path.join(root, "scripts/logs/fix-formula-images-backup");
fs.mkdirSync(backupDir, { recursive: true });

const IMG_RE = /<img\b[^>]*?src="([^"]+-hinh-(\d+)\.[a-z]+)"[^>]*?\/>/g;

let done = 0, changedExams = 0, imagesNew = 0, tagsNew = 0, failed: string[] = [];
for (const { bo, examId, docx } of jobs) {
  if (!examId || (only && examId !== only)) continue;
  if (done >= limit) break;
  done += 1;
  try {
    if (!fs.existsSync(docx)) throw new Error("không thấy " + docx);
    const read = await readDocx(new Uint8Array(fs.readFileSync(docx)), { imageSizes: true });
    const origSha = new Map(read.images.map((im) => [im.placeholder, crypto.createHash("sha256").update(Buffer.from(im.dataUri.split(",")[1], "base64")).digest("hex")]));
    const { stats, finals, trimmedPlaceholders } = await trimPageImages(read.images, read.text);
    if (!stats.trimmed) { console.log(`exam ${examId}: không có ảnh nền A4`); continue; }
    const byN = new Map(read.images.map((im) => [Number(im.placeholder.match(/hinh-(\d+)\./)![1]), im]));

    const { data: ex, error } = await supabase.from("exams").select("id, title, questions").eq("id", examId).single();
    if (error || !ex) throw new Error("đọc exam: " + error?.message);
    fs.writeFileSync(path.join(backupDir, `exam-${examId}.json`), JSON.stringify(ex));

    const newUrl = new Map<number, string>(); // N → url ảnh đã cắt
    const lessonOf = (url: string) => Number(url.match(/lesson-media\/(\d+)\//)?.[1]);
    let lessonId = 0;
    const need = new Set<number>();
    const oldUrl = new Map<number, string>();
    const scan = (x: unknown): void => {
      if (typeof x === "string") { for (const m of x.matchAll(IMG_RE)) { if (!/\sstyle="/.test(m[0])) { need.add(Number(m[2])); oldUrl.set(Number(m[2]), m[1]); lessonId ||= lessonOf(m[1]); } } }
      else if (Array.isArray(x)) x.forEach(scan);
      else if (x && typeof x === "object") Object.values(x).forEach(scan);
    };
    scan(ex.questions);
    const toUpload = [...need].filter((n) => byN.has(n) && trimmedPlaceholders.has(byN.get(n)!.placeholder));
    if (!toUpload.length) { console.log(`exam ${examId}: không có thẻ nào cần vá`); continue; }
    // Chốt an toàn: ảnh cũ trên Storage phải trùng từng byte với ảnh đọc lại từ docx (đảm bảo hinh-N đúng ảnh)
    for (const n of toUpload) {
      const url = oldUrl.get(n)!;
      if (!url.endsWith(".png")) continue; // đã nén webp — không so được
      const got = Buffer.from(await (await fetch(url)).arrayBuffer());
      if (crypto.createHash("sha256").update(got).digest("hex") !== origSha.get(byN.get(n)!.placeholder)) throw new Error(`ảnh hinh-${n} không khớp file docx dựng lại — bỏ qua đề`);
    }
    if (!dry) {
      const media = await uploadLessonMedia(supabase, lessonId, toUpload.map((n) => byN.get(n)!));
      for (const m of media) newUrl.set(Number(m.placeholder.match(/hinh-(\d+)\./)![1]), m.url);
    } else for (const n of toUpload) newUrl.set(n, "DRY");

    let touched = 0;
    const fix = (s: string): string => s.replace(IMG_RE, (tag, _src: string, n: string) => {
      const N = Number(n);
      const alt = tag.match(/\balt="([^"]*)"/)?.[1] ?? "";
      if (/\sstyle="/.test(tag) || alt !== `Hình ${N}` || !newUrl.has(N)) return tag;
      touched += 1;
      return buildImgTag(newUrl.get(N)!, alt, finals.get(byN.get(N)!.placeholder)!);
    });
    const map = (x: unknown): unknown =>
      typeof x === "string" ? fix(x) : Array.isArray(x) ? x.map(map)
        : x && typeof x === "object" ? Object.fromEntries(Object.entries(x).map(([k, y]) => [k, map(y)])) : x;

    const newQuestions = map(ex.questions);
    const nExam = touched;
    if (!dry) {
      const up = await supabase.from("exams").update({ questions: newQuestions }).eq("id", examId);
      if (up.error) throw new Error("ghi exam: " + up.error.message);
      const { data: qb } = await supabase.from("question_bank").select("id, question").eq("source_exam_id", examId);
      for (const row of qb ?? []) {
        const nq = map(row.question);
        if (JSON.stringify(nq) !== JSON.stringify(row.question)) {
          const u = await supabase.from("question_bank").update({ question: nq }).eq("id", row.id);
          if (u.error) throw new Error("ghi question_bank " + row.id + ": " + u.error.message);
        }
      }
    }
    changedExams += 1; imagesNew += toUpload.length; tagsNew += nExam;
    console.log(`exam ${examId}: ${toUpload.length} ảnh cắt, ${nExam} thẻ vá${dry ? " (dry)" : ""}`);
  } catch (e) {
    failed.push(`${bo}: ${(e as Error).message}`);
    console.log(`exam ${examId}: LỖI ${(e as Error).message}`);
  }
}
console.log(`\nXong: ${changedExams} đề, ${imagesNew} ảnh mới, ${tagsNew} thẻ vá, ${failed.length} lỗi`);
