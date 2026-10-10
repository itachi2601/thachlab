// Sinh bảng theory_quiz_keys (đáp án chấm RP bài lý thuyết) từ body_html các mục ly_thuyet đã đăng.
//   npx tsx scripts/sinh-khoa-quiz-ly-thuyet.mts            # xem thử, KHÔNG ghi
//   npx tsx scripts/sinh-khoa-quiz-ly-thuyet.mts --ghi      # ghi các bài CHƯA có khoá (không đè khoá cũ)
//   npx tsx scripts/sinh-khoa-quiz-ly-thuyet.mts --ghi --de # ghi đè cả khoá cũ (sau khi sửa quiz trong bài)
//   thêm --item <id> để chỉ làm một mục
//
// Quy ước khớp với components/lessons/TheoryRpBar.tsx: khoá câu = thuộc tính name của radio trong .tl-quiz,
// đáp án = chữ A–F theo THỨ TỰ lựa chọn có class tl-ok. Mức ⭐ (challenge) để {} vì thử thách phân tầng
// trong bài là câu mở, không phải radio tự chấm. est_read_seconds = estimateTheoryTime * 60.
// Bài có quiz lỗi cấu trúc (không đúng 1 tl-ok, name trùng, <2 lựa chọn) bị BỎ QUA và in lý do.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { estimateTheoryTime } from "@/features/lessons/theory-sections";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const l = fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
  return l ? l.slice(key.length + 1).trim() : undefined;
}
const args = process.argv.slice(2);
const ghi = args.includes("--ghi");
const de = args.includes("--de");
const only = args.includes("--item") ? Number(args[args.indexOf("--item") + 1]) : null;
const LETTERS = ["A", "B", "C", "D", "E", "F"];

function parseKey(html: string): { answers: Record<string, string>; error?: string } {
  const answers: Record<string, string> = {};
  const blocks = html.split(/<div class="tl-quiz"[^>]*>/).slice(1);
  for (const raw of blocks) {
    const block = raw.split('<div class="tl-fb')[0];
    const inputs = [...block.matchAll(/<input[^>]*type="radio"[^>]*name="([^"]+)"[^>]*id="([^"]+)"[^>]*>\s*<label[^>]*for="\2"[^>]*class="([^"]*)"/g)];
    if (inputs.length < 2) return { answers, error: "quiz có <2 lựa chọn đọc được" };
    const name = inputs[0][1];
    if (answers[name]) return { answers, error: `name trùng: ${name}` };
    const ok = inputs.map((m, i) => (/\btl-ok\b/.test(m[3]) ? i : -1)).filter((i) => i >= 0);
    if (ok.length !== 1) return { answers, error: `${name}: có ${ok.length} đáp án tl-ok` };
    answers[name] = LETTERS[ok[0]];
  }
  if (blocks.length === 0) return { answers, error: "không có tl-quiz" };
  return { answers };
}

const url = env("NEXT_PUBLIC_SUPABASE_URL");
const key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local"); process.exit(1); }
const sb = createClient(url, key, { auth: { persistSession: false } });

let q = sb.from("lesson_items").select("id, lesson_id, title, body_html").eq("kind", "ly_thuyet").ilike("body_html", "%tl-quiz%");
if (only) q = q.eq("id", only);
const { data: items, error } = await q;
if (error) { console.error(error.message); process.exit(1); }
const { data: have } = await sb.from("theory_quiz_keys").select("item_id");
const haveSet = new Set((have ?? []).map((r) => Number(r.item_id)));

const rows: { item_id: number; enabled: boolean; answers: Record<string, string>; challenge: object; est_read_seconds: number }[] = [];
let skipped = 0, kept = 0;
for (const it of items ?? []) {
  const { answers, error: err } = parseKey(String(it.body_html));
  if (err) { skipped++; console.log(`✗ item ${it.id} (bài ${it.lesson_id}) bỏ qua: ${err}`); continue; }
  if (haveSet.has(Number(it.id)) && !de) { kept++; continue; }
  const est = estimateTheoryTime(String(it.body_html));
  rows.push({ item_id: Number(it.id), enabled: true, answers, challenge: {}, est_read_seconds: est.minutes * 60 });
}
console.log(`Mục lý thuyết có quiz: ${items?.length ?? 0} · sẽ ghi: ${rows.length} · giữ khoá cũ: ${kept} · bỏ qua lỗi: ${skipped}`);
for (const r of rows.slice(0, 8)) console.log(`  item ${r.item_id}: ${Object.keys(r.answers).length} câu, đọc ~${r.est_read_seconds / 60} phút`);
if (!ghi) { console.log("(xem thử — thêm --ghi để ghi)"); process.exit(0); }
for (let i = 0; i < rows.length; i += 50) {
  const { error: e } = await sb.from("theory_quiz_keys").upsert(rows.slice(i, i + 50), { onConflict: "item_id" });
  if (e) { console.error("Lỗi ghi:", e.message); process.exit(1); }
}
console.log(`Đã ghi ${rows.length} khoá. Hoàn tác: delete from theory_quiz_keys where item_id in (...) — hoặc tắt bằng enabled=false.`);
