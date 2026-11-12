// Quét TOÀN BỘ lỗi mất định dạng (độ C, số mũ dính liền, chỉ số dưới, LaTeX vỡ, tiền tố "Câu 11.", mất ^ cũ)
// trên CẢ question_bank LẪN bản sao trong exams.questions — CHỈ ĐỌC. Quy tắc: lib/question-lint.ts.
//   npx tsx scripts/quet-dinh-dang-toan-bo.mts            # chạy sau 22h (quét ~28k câu + mọi đề)
// Ghi scripts/data/quet-dinh-dang/<ts>/{bank,exams}.json + tom-tat.txt.
// Vì sao quét cả exams: trigger sync_exam_to_bank chép câu trong đề đè lên ngân hàng mỗi khi đề được lưu —
// các đợt sửa 15–17/10 chỉ sửa question_bank nên lỗi quay lại ngày 18–21/10 (đã đối chiếu backup-do-c-*.json).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { lintQuestion, type LintCode } from "../lib/question-lint";

const d = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) =>
  fs.readFileSync(path.resolve(d, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const CODES = new Set<LintCode>(["doCMatDau", "muTran", "chiSoTran", "latexVo", "tienToCau", "matMu"]);
const pause = (ms: number) => new Promise((r) => setTimeout(r, ms));

const bank: { id: number; code: string; ctx: string }[] = [];
let nBank = 0;
for (let from = 0; ; from += 1000) {
  const { data, error } = await sb.from("question_bank").select("id, qtype, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) throw error;
  if (!data?.length) break;
  for (const r of data) {
    nBank++;
    for (const f of lintQuestion(r.question, r.qtype)) if (CODES.has(f.code)) bank.push({ id: r.id, code: f.code, ctx: f.ctx });
  }
  process.stdout.write(`\rngân hàng ${nBank}`);
  await pause(300);
}
console.log();

const exams: { exam: number; idx: number; bank_id: number | null; code: string; ctx: string }[] = [];
let nExam = 0, nQ = 0;
for (let from = 0; ; from += 50) {
  const { data, error } = await sb.from("exams").select("id, questions").order("id").range(from, from + 49);
  if (error) throw error;
  if (!data?.length) break;
  for (const e of data) {
    nExam++;
    (Array.isArray(e.questions) ? e.questions : []).forEach((q: any, idx: number) => {
      nQ++;
      for (const f of lintQuestion(q)) if (CODES.has(f.code)) exams.push({ exam: e.id, idx, bank_id: q?.bank_id ?? null, code: f.code, ctx: f.ctx });
    });
  }
  process.stdout.write(`\rđề ${nExam}`);
  await pause(300);
}
console.log();

const out = path.join(d, "data", "quet-dinh-dang", new Date().toISOString().slice(0, 16).replace(/[:T]/g, "-"));
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, "bank.json"), JSON.stringify(bank, null, 1));
fs.writeFileSync(path.join(out, "exams.json"), JSON.stringify(exams, null, 1));
const dem = (rows: { code: string }[], key: (r: any) => string) => {
  const m: Record<string, Set<string>> = {};
  for (const r of rows) (m[r.code] ??= new Set()).add(key(r));
  return Object.entries(m).map(([k, s]) => `  ${k.padEnd(14)} ${s.size}`).join("\n");
};
const tom =
  `Ngân hàng: ${nBank} câu chưa ẩn\n${dem(bank, (r) => String(r.id))}\n` +
  `Đề: ${nExam} đề · ${nQ} câu\n${dem(exams, (r) => `${r.exam}#${r.idx}`)}\n`;
fs.writeFileSync(path.join(out, "tom-tat.txt"), tom);
console.log(tom + "→ " + path.relative(process.cwd(), out));
