// Đổi đáp án các câu Opus kết luận "sonnet_dung" (đáp án DB sai): question_bank + bản sao trong exams.questions, trong MỘT giao dịch SQL
// có tắt tạm trigger trg_exams_sync_bank (trigger này chép nguyên câu từ đề đè lên ngân hàng và sinh dòng trùng theo content_hash).
//   npx tsx scripts/doi-dap-an-opus.mts            dry-run: in thống kê, ghi sao lưu + file SQL (scripts/data/giai-lai/opus/doi-dap-an.sql)
// Chạy file SQL: supabase db query --linked -f scripts/data/giai-lai/opus/doi-dap-an.sql (trong tab terminal Mac).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { plain, katexLoi, dbAnswer, tachMuiTen, loiMuiTen } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const DIR = "scripts/data/giai-lai/opus/";
const eq = (a: any, b: any) => JSON.stringify(a) === JSON.stringify(b);
const key = (q: any) => JSON.stringify([q.type, q.question, q.options ?? null, (q.statements ?? []).map((s: any) => s.text)]);
const lamSach = (h: string) => h.replace(/(?<!\\)\$(.+?)(?<!\\)\$/gs, (_m, t: string) => "$" + t.replace(/</g, "\\lt ").replace(/>/g, "\\gt ") + "$");
const rd = (f: string) => JSON.parse(fs.readFileSync(DIR + f, "utf8")) as any[];
const lo = new Map<number, any>(), kl = new Map<number, any>();
for (const f of fs.readdirSync(DIR)) { if (/^lo-\d+\.json$/.test(f)) rd(f).forEach((x) => lo.set(x.id, x)); if (/^kl-\d+\.json$/.test(f)) rd(f).forEach((x) => kl.set(x.id, x)); }
const ds = [...kl.values()].filter((k) => k.kl === "sonnet_dung");
const bank = new Map<number, any>();
for (let i = 0; i < ds.length; i += 100) { const { data, error } = await sb.from("question_bank").select("id,archived,content_hash,question").in("id", ds.slice(i, i + 100).map((k) => k.id)); if (error) throw error; data!.forEach((r) => bank.set(r.id, r)); }
const exams: any[] = [];
for (let f = 0; ; f += 40) { const { data, error } = await sb.from("exams").select("id,title,questions").order("id").range(f, f + 39); if (error) throw error; exams.push(...data!); if (data!.length < 40) break; }
console.log("đề:", exams.length);

const bo: Record<string, number[]> = {}; const bad = (k: string, id: number) => (bo[k] ??= []).push(id);
type Doi = { id: number; truoc: any; sau: any; hashDich?: any; copies: { exam: number; idx: number; truoc: any; patch: any; qtext: string }[] };
const doi: Doi[] = [];
for (const k of ds) {
  const r = bank.get(k.id), s = lo.get(k.id);
  if (!r || !s) { bad("khongThay", k.id); continue; } if (r.archived) { bad("daAn", k.id); continue; }
  const q = r.question, cu = dbAnswer(q);
  if (!eq(cu, s.dap_an_db) && !(q.type === "multiple_choice" && cu === s.dap_an_db)) { bad("dbDaKhac", k.id); continue; }
  const n = structuredClone(q); let dung = k.dap_an;
  if (q.type === "multiple_choice") { if (!/^[A-D]$/.test(String(dung))) { bad("dapAnLa", k.id); continue; } n.answer = "ABCD".indexOf(dung); }
  else if (q.type === "short_answer") { if (dung == null || String(dung).trim() === "" || typeof dung === "object") { bad("dapAnLa", k.id); continue; } n.answer = String(dung); }
  else { if (!Array.isArray(dung) || dung.length !== (q.statements ?? []).length) { bad("dapAnLa", k.id); continue; } n.statements = q.statements.map((st: any, i: number) => ({ ...st, answer: !!dung[i] })); }
  if (eq(dbAnswer(n), cu)) { bad("khongDoi", k.id); continue; }
  const ex = tachMuiTen(lamSach(String(k.explanation ?? "")));
  if (plain(ex).length < 80 || katexLoi(ex) > 0 || loiMuiTen(ex) > 0) { bad("loiGiaiLoi", k.id); continue; }
  n.explanation = ex;
  const copies: Doi["copies"] = [];
  for (const e of exams) (e.questions ?? []).forEach((c: any, idx: number) => {
    if (key(c) !== key(q) || !eq(dbAnswer(c), cu)) return;
    const patch: any = { explanation: ex }; if (q.type === "true_false") patch.statements = c.statements.map((st: any, i: number) => ({ ...st, answer: !!dung[i] })); else patch.answer = n.answer;
    copies.push({ exam: e.id, idx, truoc: c, patch, qtext: c.question });
  });
  doi.push({ id: k.id, truoc: r, sau: n, copies });
}
const nCopies = doi.reduce((a, d) => a + d.copies.length, 0);
console.log(`đổi ${doi.length}/${ds.length} câu ngân hàng · ${nCopies} bản sao trong ${new Set(doi.flatMap((d) => d.copies.map((c) => c.exam))).size} đề · bỏ qua:`, Object.fromEntries(Object.entries(bo).map(([a, b]) => [a, b.length])));
if (doi.some((d) => d.copies.length === 0)) console.log("  câu không có bản sao trong đề:", doi.filter((d) => d.copies.length === 0).length);
const ts = Date.now();
fs.writeFileSync(`scripts/logs/doi-dap-an-opus-backup-${ts}.json`, JSON.stringify({ bank: doi.map((d) => ({ id: d.id, content_hash: d.truoc.content_hash, question: d.truoc.question })), exams: doi.flatMap((d) => d.copies.map((c) => ({ exam: c.exam, idx: c.idx, element: c.truoc }))) }));
const lit = (v: any) => { const s = JSON.stringify(v); if (s.includes("$jj$")) throw new Error("dollar tag"); return `$jj$${s}$jj$::jsonb`; };
const txt = (s: string) => { if (s.includes("$jj$")) throw new Error("dollar tag"); return `$jj$${s}$jj$`; };
const sql: string[] = ["begin;", "alter table public.exams disable trigger trg_exams_sync_bank;"];
for (const d of doi) for (const c of d.copies)
  sql.push(`update public.exams set questions = jsonb_set(questions, '{${c.idx}}', (questions->${c.idx}) || ${lit(c.patch)}) where id = ${c.exam} and (questions->${c.idx}->>'question') = ${txt(c.qtext)};`);
for (const d of doi) {
  sql.push(`update public.question_bank set question = ${lit(d.sau)} where id = ${d.id} and not archived;`);
  if (d.copies.length) { const after = { ...d.copies[0].truoc, ...d.copies[0].patch };
    sql.push(`update public.question_bank b set content_hash = h.nh from (select ${d.id}::bigint as id, public.question_content_hash(${lit(after)}) as nh) h where b.id = h.id and not exists (select 1 from public.question_bank x where x.content_hash = h.nh and x.id <> b.id);`); }
}
sql.push("alter table public.exams enable trigger trg_exams_sync_bank;", "commit;");
fs.writeFileSync(DIR + "doi-dap-an.sql", sql.join("\n") + "\n");
console.log(`SQL: ${DIR}doi-dap-an.sql (${(sql.join("\n").length / 1e6).toFixed(1)} MB, ${sql.length} lệnh) · sao lưu scripts/logs/doi-dap-an-opus-backup-${ts}.json`);
