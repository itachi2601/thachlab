// CHẠY THỬ (không ghi DB) bộ sửa lib/sua-dinh-dang.ts trên các câu mà quet-dinh-dang-toan-bo.mts đã đánh dấu,
// cho CẢ question_bank LẪN exams.questions (cùng một hàm → hai bản giống nhau, trigger sync không khôi phục lỗi).
//   npx tsx scripts/sua-dinh-dang-hang-loat.mts scripts/data/quet-dinh-dang/<ts>     # chạy sau 22h
// Ghi <ts>/sua/{bank.json, exams.json, nghi-ngo.json, tom-tat.txt, apply-NN.sql}. apply-00 sao lưu; mỗi file sau là
// một giao dịch tắt trg_exams_sync_bank; file cuối đếm số dòng đã đổi — CHỈ chạy khi thầy đồng ý (supabase db query --linked -f).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import katex from "katex";
import { suaCau } from "../lib/sua-dinh-dang";

const d = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) =>
  fs.readFileSync(path.resolve(d, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const dir = path.resolve(process.argv[2] ?? "");
const out = path.join(dir, "sua");
fs.mkdirSync(out, { recursive: true });
const pause = (ms: number) => new Promise((r) => setTimeout(r, ms));

const loiKatex = (v: unknown) => {
  let n = 0;
  for (const m of JSON.stringify(v).matchAll(/\$([^$]+)\$/g)) {
    try { katex.renderToString(JSON.parse(`"${m[1]}"`), { throwOnError: true }); } catch { n++; }
  }
  return n;
};
const dem: Record<string, number> = {};
const nghi: { noi: string; ly_do: string }[] = [];
const boVi: string[] = [];

// Đề bị đánh dấu → sửa mọi câu trong đề; ngân hàng: câu bị đánh dấu + mọi câu nguồn từ các đề đó
const bankFlag: { id: number }[] = JSON.parse(fs.readFileSync(path.join(dir, "bank.json"), "utf8"));
const examFlag: { exam: number }[] = JSON.parse(fs.readFileSync(path.join(dir, "exams.json"), "utf8"));
const examIds = [...new Set(examFlag.map((r) => r.exam))];

const exams: { id: number; questions: unknown[] }[] = [];
const examOut: { id: number; questions: unknown[]; sua: string[] }[] = [];
for (let i = 0; i < examIds.length; i += 50) {
  const { data, error } = await sb.from("exams").select("id, questions").in("id", examIds.slice(i, i + 50));
  if (error) throw error;
  exams.push(...(data as never[]));
  await pause(300);
}
for (const e of exams) {
  const s = new Set<string>();
  const qs = (e.questions ?? []).map((q, idx) => {
    const r = suaCau(q);
    r.nghiNgo.forEach((x) => nghi.push({ noi: `đề ${e.id}#${idx}`, ly_do: x }));
    if (!r.sua.length) return q;
    if (loiKatex(r.q) > loiKatex(q)) { boVi.push(`đề ${e.id}#${idx}`); return q; }
    r.sua.forEach((x) => (s.add(x), (dem["đề:" + x] = (dem["đề:" + x] ?? 0) + 1)));
    return r.q;
  });
  if (s.size) examOut.push({ id: e.id, questions: qs, sua: [...s] });
}

const bankIds = new Set(bankFlag.map((r) => r.id));
for (let i = 0; i < examIds.length; i += 50) {
  const { data, error } = await sb.from("question_bank").select("id").eq("archived", false).in("source_exam_id", examIds.slice(i, i + 50));
  if (error) throw error;
  data!.forEach((r) => bankIds.add(r.id));
  await pause(300);
}
const ids = [...bankIds];
const bankOut: { id: number; question: unknown; sua: string[]; truoc: unknown }[] = [];
for (let i = 0; i < ids.length; i += 500) {
  const { data, error } = await sb.from("question_bank").select("id, question").in("id", ids.slice(i, i + 500));
  if (error) throw error;
  for (const row of data!) {
    const r = suaCau(row.question);
    r.nghiNgo.forEach((x) => nghi.push({ noi: `nh ${row.id}`, ly_do: x }));
    if (!r.sua.length) continue;
    if (loiKatex(r.q) > loiKatex(row.question)) { boVi.push(`nh ${row.id}`); continue; }
    r.sua.forEach((x) => (dem["nh:" + x] = (dem["nh:" + x] ?? 0) + 1));
    bankOut.push({ id: row.id, question: r.q, sua: r.sua, truoc: row.question });
  }
  await pause(300);
}

fs.writeFileSync(path.join(out, "bank.json"), JSON.stringify(bankOut));
fs.writeFileSync(path.join(out, "exams.json"), JSON.stringify(examOut));
fs.writeFileSync(path.join(out, "nghi-ngo.json"), JSON.stringify(nghi, null, 1));

// apply.sql — giao dịch; sao lưu nguyên dòng; tắt trigger đồng bộ; đếm trước/sau
const ts = path.basename(dir).replace(/-/g, "");
const q = (v: unknown) => `'${JSON.stringify(v).replace(/'/g, "''")}'::jsonb`;
const bk = `public.bk_sua_dinh_dang_${ts}`;
const parts: string[] = [
  [
    "begin;",
    `create table ${bk}_bank as select * from public.question_bank where id in (${bankOut.map((r) => r.id).join(",") || "0"});`,
    `create table ${bk}_exams as select id, questions from public.exams where id in (${examOut.map((r) => r.id).join(",") || "0"});`,
    `alter table ${bk}_bank enable row level security; revoke all on ${bk}_bank from anon, authenticated;`,
    `alter table ${bk}_exams enable row level security; revoke all on ${bk}_exams from anon, authenticated;`,
    `select (select count(*) from ${bk}_bank) as bank_sao_luu, (select count(*) from ${bk}_exams) as de_sao_luu;`,
    "commit;",
  ].join("\n"),
];
// content_hash tính lại theo bản sửa (trùng hash câu khác thì giữ hash cũ) để đề khác còn bản lỗi không ghi đè ngược.
// Mỗi file một giao dịch, tắt trigger trong giao dịch
const lo = (lines: string[], _n: number) => {
  // API `supabase db query` từ chối thân >~1 MB (413) → gói theo dung lượng ≤700 KB
  const dong = (xs: string[]) =>
    parts.push(["begin;", "alter table public.exams disable trigger trg_exams_sync_bank;", ...xs, "alter table public.exams enable trigger trg_exams_sync_bank;", "commit;"].join("\n"));
  let cur: string[] = [], size = 0;
  for (const l of lines) {
    if (cur.length && size + l.length > 700_000) (dong(cur), (cur = []), (size = 0));
    cur.push(l), (size += l.length);
  }
  if (cur.length) dong(cur);
};
lo(bankOut.map((r) => `update public.question_bank b set question = v.q, updated_at = now(), content_hash = case when exists (select 1 from public.question_bank x where x.content_hash = public.question_content_hash(v.q)) then b.content_hash else public.question_content_hash(v.q) end ` +
      `from (select ${q(r.question)} as q) v where b.id = ${r.id};`), 400);
lo(examOut.map((r) => `update public.exams set questions = ${q(r.questions)} where id = ${r.id};`), 60);
parts.push(
  `select (select count(*) from public.question_bank b join ${bk}_bank k using (id) where b.question is distinct from k.question) as bank_da_doi, ` +
    `(select count(*) from public.exams e join ${bk}_exams k using (id) where e.questions is distinct from k.questions) as de_da_doi;`,
);
for (const f of fs.readdirSync(out)) if (/^apply-\d+\.sql$/.test(f)) fs.unlinkSync(path.join(out, f));
parts.forEach((p, i) => fs.writeFileSync(path.join(out, `apply-${String(i).padStart(2, "0")}.sql`), p));
const sql = parts.join("\n");

const tom =
  `Ngân hàng: ${bankOut.length} câu sẽ sửa · Đề: ${examOut.length} đề sẽ sửa\n` +
  Object.entries(dem).sort().map(([k, v]) => `  ${k.padEnd(16)} ${v}`).join("\n") +
  `\nBỏ (sửa làm KaTeX lỗi thêm): ${boVi.length} ${boVi.slice(0, 20).join(", ")}\nNghi ngờ (không sửa, chờ duyệt): ${nghi.length}\n` +
  `${parts.length} file apply-NN.sql, tổng ${(sql.length / 1e6).toFixed(1)} MB (00 = sao lưu, cuối = đếm đã đổi)`;
fs.writeFileSync(path.join(out, "tom-tat.txt"), tom);
console.log(tom + "\n→ " + path.relative(process.cwd(), out));
