// Cắt lề trắng của ảnh nguyên trang A4 trong ngân hàng câu hỏi + các đề đã tạo, rồi trỏ câu sang ảnh mới.
// Đầu vào: scripts/data/kiem-ke-anh-ngan-hang/anh-le-trang.json (do kiem-anh-le-trang.mts sinh ra).
//   npx tsx scripts/cat-anh-le-trang.mts            # DRY-RUN: cắt thử, ghi xem-thu vào scripts/data/cat-anh-le-trang/, KHÔNG ghi gì lên mạng
//   npx tsx scripts/cat-anh-le-trang.mts --apply    # tải ảnh mới lên Storage (lesson-media/<thư mục cũ>/cat-<tên>.webp) + sửa src trong question_bank và exams
//   thêm --exam-only <id> để chỉ sửa một đề (bỏ qua duyệt cả bảng exams)
//   npx tsx scripts/cat-anh-le-trang.mts --rollback <file sao lưu>   # trả question/questions về bản cũ
// An toàn: ảnh cũ KHÔNG bị xoá/ghi đè (file mới tên khác); trước khi sửa DB ghi sao lưu nguyên jsonb cũ ra scripts/logs/.
import { createClient } from "@supabase/supabase-js";
import sharp from "sharp";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }
const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
const BUCKET = "lesson-media";
const PUBLIC = `${url}/storage/v1/object/public/${BUCKET}/`;
const APPLY = process.argv.includes("--apply");
const PAD = 16;

// ---------- hoàn tác ----------
const rbIdx = process.argv.indexOf("--rollback");
if (rbIdx >= 0) {
  const bk = JSON.parse(fs.readFileSync(process.argv[rbIdx + 1], "utf8")) as { bank: { id: number; question: unknown }[]; exams: { id: number; questions: unknown }[] };
  for (const r of bk.bank) { const { error } = await supabase.from("question_bank").update({ question: r.question }).eq("id", r.id); if (error) console.error("bank", r.id, error.message); }
  for (const r of bk.exams) { const { error } = await supabase.from("exams").update({ questions: r.questions }).eq("id", r.id); if (error) console.error("exam", r.id, error.message); }
  console.log(`đã trả ${bk.bank.length} câu ngân hàng, ${bk.exams.length} đề về bản cũ`);
  process.exit(0);
}

// ---------- chọn ảnh cần cắt ----------
const rep = JSON.parse(fs.readFileSync(path.join(scriptDir, "data", "kiem-ke-anh-ngan-hang", "anh-le-trang.json"), "utf8")) as { hits: { src: string; w: number; h: number; frac: number }[] };
const todo = [...new Map(rep.hits.filter((x) => x.w === 794 && x.h === 1123 && x.frac > 0.002 && x.src.startsWith(PUBLIC)).map((x) => [x.src, x])).values()];
console.log(`${todo.length} ảnh A4 cần cắt`);

const outDir = path.join(scriptDir, "data", "cat-anh-le-trang");
fs.mkdirSync(outDir, { recursive: true });

// ---------- cắt ----------
async function crop(src: string): Promise<{ buf: Buffer; w: number; h: number; before: [number, number] } | null> {
  const orig = Buffer.from(await (await fetch(src, { signal: AbortSignal.timeout(30000) })).arrayBuffer());
  const { data, info } = await sharp(orig).flatten({ background: "#ffffff" }).greyscale().raw().toBuffer({ resolveWithObject: true });
  const { width: w, height: h } = info;
  const cnt = new Map<number, number>();
  const at = (x: number, y: number) => data[y * w + x];
  for (let x = 0; x < w; x++) for (const y of [0, h - 1]) cnt.set(at(x, y) >> 3, (cnt.get(at(x, y) >> 3) ?? 0) + 1);
  for (let y = 0; y < h; y++) for (const x of [0, w - 1]) cnt.set(at(x, y) >> 3, (cnt.get(at(x, y) >> 3) ?? 0) + 1);
  const bg = ([...cnt.entries()].sort((a, b) => b[1] - a[1])[0][0] << 3) + 4;
  let x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (Math.abs(at(x, y) - bg) > 20) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  }
  if (x1 < 0) return null;
  x0 = Math.max(0, x0 - PAD); y0 = Math.max(0, y0 - PAD); x1 = Math.min(w - 1, x1 + PAD); y1 = Math.min(h - 1, y1 + PAD);
  const cw = x1 - x0 + 1, ch = y1 - y0 + 1;
  const scale = Math.min(3, Math.max(1, 520 / cw)); // hình nhỏ phóng lên cho nét mịn, tối đa 3×, rộng ≤ ~1200
  const buf = await sharp(orig).flatten({ background: "#ffffff" })
    .extract({ left: x0, top: y0, width: cw, height: ch })
    .resize({ width: Math.round(Math.min(1200, cw * scale)), kernel: "lanczos3" })
    .webp({ quality: 92 }).toBuffer();
  const m = await sharp(buf).metadata();
  return { buf, w: m.width!, h: m.height!, before: [w, h] };
}

const map = new Map<string, string>(); // src cũ -> src mới
const rows: string[] = ["# Xem thử: ảnh cắt lề", "", "| Cũ | Mới | KB |", "|---|---|---|"];
let cursor = 0, fail = 0;
async function worker() {
  for (;;) {
    const s = todo[cursor++];
    if (!s) return;
    try {
      const r = await crop(s.src);
      if (!r) { fail++; console.log("trống:", s.src); continue; }
      const rel = s.src.slice(PUBLIC.length); // 132/1791045252641-hinh-3.png
      const dir = path.dirname(rel), base = path.basename(rel).replace(/\.[a-z]+$/i, "");
      const newRel = `${dir}/cat-${base}.webp`;
      const local = path.join(outDir, `${dir}-cat-${base}.webp`);
      fs.writeFileSync(local, r.buf);
      if (APPLY) {
        const { error } = await supabase.storage.from(BUCKET).upload(newRel, r.buf, { contentType: "image/webp", upsert: false });
        if (error && !/already exists|Duplicate/i.test(error.message)) throw new Error(error.message);
      }
      map.set(s.src, PUBLIC + newRel);
      rows.push(`| ![](${s.src}) | ![](${path.basename(local)}) | ${(r.buf.length / 1024).toFixed(0)} (${r.w}×${r.h}) |`);
    } catch (e) { fail++; console.error("lỗi", s.src, (e as Error).message); }
  }
}
await Promise.all(Array.from({ length: 8 }, worker));
fs.writeFileSync(path.join(outDir, "xem-thu.md"), rows.join("\n") + "\n");
const sizes = fs.readdirSync(outDir).filter((f) => f.endsWith(".webp")).map((f) => fs.statSync(path.join(outDir, f)).size);
console.log(`cắt xong ${map.size}/${todo.length} (lỗi ${fail}); ảnh mới lớn nhất ${(Math.max(...sizes) / 1024).toFixed(0)} KB, trung bình ${(sizes.reduce((a, b) => a + b, 0) / sizes.length / 1024).toFixed(0)} KB`);
if (!APPLY) { console.log("DRY-RUN: chưa tải lên, chưa sửa DB. Xem scripts/data/cat-anh-le-trang/"); process.exit(0); }

// ---------- sửa DB (có sao lưu) ----------
const swap = (json: unknown): { out: unknown; n: number } => {
  let s = JSON.stringify(json), n = 0;
  for (const [o, nw] of map) if (s.includes(o)) { s = s.split(o).join(nw); n++; }
  return { out: JSON.parse(s), n };
};
const backup = { bank: [] as { id: number; question: unknown }[], exams: [] as { id: number; questions: unknown }[] };
const logDir = path.join(scriptDir, "logs"); fs.mkdirSync(logDir, { recursive: true });
const stamp = new Date().toISOString().replace(/[:.]/g, "-");
const bkFile = path.join(logDir, `cat-anh-le-trang-${stamp}.backup.json`);

// ngân hàng: chỉ các câu có ảnh trong danh sách
const ids = [...new Set(rep.hits.map((h) => h as unknown as { id?: number }).map((h) => h.id).filter((x): x is number => !!x))];
for (let from = 0; from < ids.length; from += 50) {
  const { data, error } = await supabase.from("question_bank").select("id, question").in("id", ids.slice(from, from + 50));
  if (error) { console.error(error.message); break; }
  for (const r of data ?? []) {
    const { out, n } = swap(r.question);
    if (!n) continue;
    backup.bank.push({ id: r.id, question: r.question });
    fs.writeFileSync(bkFile, JSON.stringify(backup));
    const u = await supabase.from("question_bank").update({ question: out }).eq("id", r.id);
    if (u.error) console.error("bank", r.id, u.error.message);
  }
}
// đề: duyệt từng đề (questions là jsonb lớn nên đọc nhỏ giọt)
const onlyExam = process.argv.indexOf("--exam-only") >= 0 ? Number(process.argv[process.argv.indexOf("--exam-only") + 1]) : null;
const { data: exIds } = onlyExam ? { data: [{ id: onlyExam }] } : await supabase.from("exams").select("id").order("id");
for (const { id } of exIds ?? []) {
  const { data, error } = await supabase.from("exams").select("id, questions").eq("id", id).single();
  if (error || !data) continue;
  const { out, n } = swap(data.questions);
  if (!n) continue;
  backup.exams.push({ id: data.id, questions: data.questions });
  fs.writeFileSync(bkFile, JSON.stringify(backup));
  let u = await supabase.from("exams").update({ questions: out }).eq("id", data.id);
  for (let t = 1; u.error && t <= 4; t++) { console.error("exam", data.id, u.error.message, `— thử lại ${t}/4`); await new Promise((r) => setTimeout(r, 5000 * t)); u = await supabase.from("exams").update({ questions: out }).eq("id", data.id); }
  if (u.error) console.error("exam", data.id, "THẤT BẠI:", u.error.message);
}
fs.writeFileSync(bkFile, JSON.stringify(backup));
console.log(`đã sửa ${backup.bank.length} câu ngân hàng, ${backup.exams.length} đề. Sao lưu: ${bkFile}`);
console.log(`Hoàn tác: npx tsx scripts/cat-anh-le-trang.mts --rollback ${bkFile}`);
