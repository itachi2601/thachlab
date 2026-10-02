// Xoá dòng watermark "thukhoadaihoc.vn" (chữ font lỗi "Taøi lieäu ñöôïc phaùt haønh…") dính trong
// `explanation` của câu hỏi ở bảng exams (đề nhập từ Word). MẶC ĐỊNH DRY-RUN — chỉ in số lượng.
//   node --env-file=.env.local scripts/clean-exam-watermark.mjs            # xem trước
//   node --env-file=.env.local scripts/clean-exam-watermark.mjs --apply    # ghi thật (có backup)
// Backup: scripts/logs/exam-watermark-backup-<ts>.json (id + questions gốc) — khôi phục bằng PATCH lại.
import { mkdirSync, writeFileSync } from "node:fs";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!url || !key) throw new Error("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY");
const apply = process.argv.includes("--apply");
const headers = { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" };

const WATERMARK = /(?:<br\s*\/?>\s*)?\$Taøi lieäu ñöôïc phaùt haønh taïi Website: thukhoadaihoc\.vn\$/g;
const LEFTOVER = /\s*Website: thukhoadaihoc\.vn/g; // trường hợp dính vào giữa công thức $...$

function clean(s) {
  return s.replace(WATERMARK, "").replace(LEFTOVER, "");
}
function walk(v) {
  if (typeof v === "string") return clean(v);
  if (Array.isArray(v)) return v.map(walk);
  return v;
}

const res = await fetch(`${url}/rest/v1/exams?select=id,title,questions&order=id`, { headers });
const exams = await res.json();
const changed = [];
for (const e of exams) {
  let n = 0;
  const questions = (e.questions ?? []).map((q) => {
    if (typeof q?.explanation !== "string") return q;
    const explanation = clean(q.explanation);
    if (explanation !== q.explanation) n++;
    return explanation === q.explanation ? q : { ...q, explanation };
  });
  if (n) changed.push({ id: e.id, title: e.title, n, orig: e.questions, questions });
}
console.log(`${changed.length} đề, ${changed.reduce((a, c) => a + c.n, 0)} lời giải chứa watermark.`);
for (const c of changed) console.log(`  đề ${c.id}: ${c.n} câu — ${c.title}`);
if (!apply) process.exit(0);

mkdirSync("scripts/logs", { recursive: true });
const file = `scripts/logs/exam-watermark-backup-${Date.now()}.json`;
writeFileSync(file, JSON.stringify(changed.map(({ id, orig }) => ({ id, questions: orig }))));
console.log("Backup:", file);
for (const c of changed) {
  const r = await fetch(`${url}/rest/v1/exams?id=eq.${c.id}`, { method: "PATCH", headers, body: JSON.stringify({ questions: c.questions }) });
  console.log(c.id, r.ok ? "ok" : `LỖI ${r.status}`);
}
