// Xuất / ghi ngân hàng câu hỏi CNC (bảng exams, khoá cnc_key) — dùng chung cho các phiên soạn đề CNC.
//
//   npx tsx scripts/cnc/ngan-hang-cnc.mts xuat                       → scripts/data/cnc-kiem-tra/hien-tai/<cnc_key>.json
//   npx tsx scripts/cnc/ngan-hang-cnc.mts ghi <file.json> [--dry-run] → upsert theo cnc_key, sao lưu bản cũ ra scripts/logs/
//
// File ghi: { "cnc_key": "...", "title": "...", "duration_minutes": 30, "questions": [ {type:"multiple_choice", question, options[4], answer, explanation} ] }
// published luôn false (ngân hàng CNC không lộ ra /kiem-tra công khai). Không xoá ngân hàng nào.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  for (const f of [path.join(root, ".env.local"), "/Users/MAC/Projects/thachlab/.env.local"]) {
    if (!fs.existsSync(f)) continue;
    const l = fs.readFileSync(f, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
    if (l) return l.slice(key.length + 1).trim();
  }
  return undefined;
}
function fail(m: string): never { console.error("Lỗi:", m); process.exit(1); }

const url = env("NEXT_PUBLIC_SUPABASE_URL");
const key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local");
const db = createClient(url, key);
const [cmd, file] = process.argv.slice(2);
const dry = process.argv.includes("--dry-run");

if (cmd === "xuat") {
  const { data, error } = await db.from("exams").select("id, cnc_key, title, duration_minutes, questions").not("cnc_key", "is", null);
  if (error) fail(error.message);
  const dir = path.join(root, "scripts/data/cnc-kiem-tra/hien-tai");
  fs.mkdirSync(dir, { recursive: true });
  for (const r of data ?? []) {
    fs.writeFileSync(path.join(dir, `${r.cnc_key}.json`), JSON.stringify(r, null, 2) + "\n");
    console.log(`${r.cnc_key}\t${(r.questions ?? []).length} câu\t${r.title}`);
  }
  // Bảng cũ cnc_quiz_questions (luyện tập exercise-1/2/6 Bài 2–3, gate) — xuất để rà, không ghi lại.
  const { data: qq, error: e2 } = await db.from("cnc_quiz_questions").select("*").order("quiz_key").order("order_index");
  if (e2) fail(e2.message);
  const groups: Record<string, unknown[]> = {};
  for (const r of qq ?? []) (groups[r.quiz_key] ??= []).push(r);
  for (const [k, rows] of Object.entries(groups)) {
    fs.writeFileSync(path.join(dir, `quiz-${k}.json`), JSON.stringify(rows, null, 2) + "\n");
    console.log(`quiz-${k}\t${rows.length} câu (cnc_quiz_questions)`);
  }
} else if (cmd === "ghi") {
  if (!file || !fs.existsSync(file)) fail("Dùng: ghi <file.json> [--dry-run]");
  const bank = JSON.parse(fs.readFileSync(file, "utf8"));
  if (!bank.cnc_key || !bank.title || !Array.isArray(bank.questions)) fail("Thiếu cnc_key/title/questions");
  bank.questions.forEach((q: { type: string; question: string; options: string[]; answer: number; explanation: string }, i: number) => {
    if (q.type !== "multiple_choice") fail(`Câu ${i + 1}: chỉ nhận multiple_choice (màn CNC chỉ chấm trắc nghiệm)`);
    if (!q.question?.trim() || !q.explanation?.trim()) fail(`Câu ${i + 1}: thiếu đề/lời giải`);
    if (!Array.isArray(q.options) || q.options.length !== 4 || q.options.some((o) => !o?.trim())) fail(`Câu ${i + 1}: cần đúng 4 phương án`);
    if (new Set(q.options).size !== 4) fail(`Câu ${i + 1}: phương án trùng nhau`);
    if (![0, 1, 2, 3].includes(q.answer)) fail(`Câu ${i + 1}: answer phải 0–3`);
  });
  const { data: old } = await db.from("exams").select("*").eq("cnc_key", bank.cnc_key).maybeSingle();
  console.log(`${bank.cnc_key}: ${old ? `${(old.questions ?? []).length} câu cũ (exam ${old.id})` : "chưa có"} → ${bank.questions.length} câu mới`);
  if (dry) { console.log("--dry-run: không ghi."); process.exit(0); }
  if (old) {
    const bak = path.join(root, "scripts/logs", `sao-luu-cnc-${bank.cnc_key}-${new Date().toISOString().replace(/[:.]/g, "-")}.json`);
    fs.mkdirSync(path.dirname(bak), { recursive: true });
    fs.writeFileSync(bak, JSON.stringify(old, null, 2));
    console.log("Sao lưu:", bak);
  }
  const row = { cnc_key: bank.cnc_key, title: bank.title, duration_minutes: bank.duration_minutes ?? 30, topic: "CNC", difficulty: "", published: false, questions: bank.questions, question_count: bank.questions.length };
  const { data, error } = await db.from("exams").upsert(row, { onConflict: "cnc_key" }).select("id, cnc_key, question_count");
  if (error) fail(error.message);
  console.log("Đã ghi:", data);
} else fail("Lệnh: xuat | ghi <file.json> [--dry-run]");
