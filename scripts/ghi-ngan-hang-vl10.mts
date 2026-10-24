// Ghi các câu đã duyệt (cau-final.json + gan-nhan.json) vào question_bank ở trạng thái ẨN (archived=true), qua SQL giao dịch.
//   npx tsx scripts/ghi-ngan-hang-vl10.mts            DRY-RUN: lọc trùng với ngân hàng, in báo cáo, ghi scripts/data/nap-ngan-hang-vl10/ghi.sql
//   npx tsx scripts/ghi-ngan-hang-vl10.mts --apply    chạy ghi.sql bằng `supabase db query --linked`, đếm trước/sau
// Mọi dòng mới có note = NOTE → hoàn tác: delete from public.question_bank where note = '<NOTE>';
// Chống trùng: (1) SQL `where not exists content_hash`, (2) JS so đề+phương án đã chuẩn hoá với ngân hàng lớp 10 hiện có.
import fs from "node:fs";
import { execSync } from "node:child_process";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const U = env("NEXT_PUBLIC_SUPABASE_URL"), K = env("SUPABASE_SERVICE_ROLE_KEY");
const GRADE = process.env.VL_GRADE ?? "10"; // VL12: VL_GRADE=12 VL_TOPICS=<file chu-de>
const DIR = (process.env.VL10_DIR ?? "scripts/data/nap-ngan-hang-vl10") + "/", NOTE = process.env.VL10_NOTE ?? "nap-vl10-c3-20261020";
const cau: any[] = JSON.parse(fs.readFileSync(DIR + "cau-final.json", "utf8"));
const nhan: Record<string, any> = JSON.parse(fs.readFileSync(DIR + "gan-nhan.json", "utf8"));
const topics: any[] = JSON.parse(fs.readFileSync(process.env.VL_TOPICS ?? "scripts/data/nap-ngan-hang-vl10/chu-de-lop10.json", "utf8")).topics;
const rest = async (p: string, range?: string) => (await fetch(`${U}/rest/v1/${p}`, { headers: { apikey: K, Authorization: `Bearer ${K}`, ...(range ? { Range: range } : {}) } })).json();
const norm = (s: string) => s.replace(/<[^>]+>/g, "").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").toLowerCase().replace(/[^a-z0-9]+/g, "");
const sig = (q: any) => norm(String(q.question ?? "")).slice(0, 80) + "|" + norm((q.options ?? (q.statements ?? []).map((s: any) => s.text)).join("")).slice(0, 80);

// ngân hàng lớp 10 hiện có (đề + phương án) để so trùng
const bank: any[] = [];
for (let o = 0; ; o += 500) { const r = await rest("question_bank?grade=eq.${GRADE}&select=id,question&order=id", `${o}-${o + 499}`); if (!Array.isArray(r)) throw new Error(JSON.stringify(r)); bank.push(...r); if (r.length < 500) break; }
const have = new Map(bank.map((b) => [sig(b.question), b.id]));
const rows: any[] = [], trung: any[] = [], thieu: string[] = [];
for (const q of cau) {
  const n = nhan[q.key]; const t = n && topics.find((x) => x.name === n.topic);
  if (!t) { thieu.push(q.key); continue; }
  const jq: any = { type: q.type, form: "bai_tap", topic: t.name, difficulty: n.difficulty, difficultySource: "ai", question: q.question, explanation: q.explanation || "" };
  if (q.type === "multiple_choice") { jq.options = q.options; jq.answer = q.answer; }
  else if (q.type === "true_false") jq.statements = q.statements;
  else jq.answer = String(q.answer);
  const s = sig(jq);
  if (have.has(s)) { trung.push({ key: q.key, bankId: have.get(s) }); continue; }
  have.set(s, -1); // trùng ngay trong lô
  rows.push({ key: q.key, t, jq });
}
const sql: string[] = ["begin;", "create temp table _truoc as select count(*) n from public.question_bank;"];
for (let i = 0; i < rows.length; i += 40) {
  const vals = rows.slice(i, i + 40).map((r) => `($q$${JSON.stringify(r.jq)}$q$::jsonb, ${r.t.id}, $q$${r.t.name}$q$)`).join(",\n");
  sql.push(`insert into public.question_bank (subject_code, grade, topic_id, topic_name, form, qtype, difficulty, difficulty_source, question, content_hash, archived, note)
select 'vat-ly', '${GRADE}', v.tid, v.tname, 'bai_tap', v.q->>'type', v.q->>'difficulty', 'ai', v.q, public.question_content_hash(v.q), true, '${NOTE}'
from (values ${vals}) as v(q, tid, tname)
where not exists (select 1 from public.question_bank b where b.content_hash = public.question_content_hash(v.q));`);
}
sql.push(`select (select n from _truoc) as truoc, count(*) as them_moi from public.question_bank where note = '${NOTE}';`, "commit;");
fs.writeFileSync(DIR + "ghi.sql", sql.join("\n"));
fs.writeFileSync(DIR + "ghi-bao-cao.json", JSON.stringify({ ghi: rows.map((r) => r.key), trung, thieuNhan: thieu }, null, 1));
console.log(`Cần ghi: ${rows.length} · trùng ngân hàng: ${trung.length} · thiếu nhãn: ${thieu.length} · ngân hàng lớp 10 hiện có: ${bank.length}`);
if (process.argv.includes("--apply")) {
  const out = execSync(`supabase db query --linked -f ${DIR}ghi.sql`, { encoding: "utf8", maxBuffer: 1 << 26 });
  console.log(out.slice(-600));
} else console.log("DRY-RUN — chưa ghi DB. Xem ghi-bao-cao.json rồi chạy lại với --apply.");
