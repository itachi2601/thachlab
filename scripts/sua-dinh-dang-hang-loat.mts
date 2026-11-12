// CHẠY THỬ (không ghi DB) bộ sửa lib/sua-dinh-dang.ts trên các câu mà quet-dinh-dang-toan-bo.mts đã đánh dấu,
// cho CẢ question_bank LẪN exams.questions (cùng một hàm → hai bản giống nhau, trigger sync không khôi phục lỗi).
//   npx tsx scripts/sua-dinh-dang-hang-loat.mts scripts/data/quet-dinh-dang/<ts> [--duyet scripts/data/duyet/<đợt>]   # chạy sau 22h
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
/** Thử lại tối đa 3 lần (DB chậm ban đêm → hết thời gian chờ HTTP). */
async function lay<T>(f: () => PromiseLike<{ data: T | null; error: unknown }>): Promise<T> {
  for (let i = 1; ; i++) {
    try { const { data, error } = await f(); if (error) throw error; return data as T; }
    catch (e) { if (i >= 3) throw e; console.log(`\nthử lại (${i})…`); await pause(5000 * i); }
  }
}

const loiKatex = (v: unknown) => {
  let n = 0;
  for (const m of JSON.stringify(v).matchAll(/\$([^$]+)\$/g)) {
    try { katex.renderToString(JSON.parse(`"${m[1]}"`), { throwOnError: true, strict: "ignore" }); } catch { n++; }
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

// --duyet <thư-mục>: kết quả thầy duyệt (phan-hoi.json) + sửa tay (sua-tay.json: {bankId: [[cũ, mới], …]}).
// de_xuat/y_thay → ép đổi số mũ không hệ số + độ C (ep) và thay chuỗi tay, áp cho câu ngân hàng VÀ câu song sinh trong đề
// (source_exam_id, source_index); bo → ẩn câu ngân hàng (archived = true).
const iDuyet = process.argv.indexOf("--duyet");
const duyetDir = iDuyet > 0 ? path.resolve(process.argv[iDuyet + 1]) : "";
const phanHoi: Record<string, { action: string }> = duyetDir ? JSON.parse(fs.readFileSync(path.join(duyetDir, "phan-hoi.json"), "utf8")).items : {};
const suaTay: Record<string, [string, string][]> = duyetDir && fs.existsSync(path.join(duyetDir, "sua-tay.json")) ? JSON.parse(fs.readFileSync(path.join(duyetDir, "sua-tay.json"), "utf8")) : {};
const epIds = new Set(Object.entries(phanHoi).filter(([, v]) => v.action === "de_xuat" || v.action === "y_thay").map(([k]) => +k));
const boIds = Object.entries(phanHoi).filter(([, v]) => v.action === "bo").map(([k]) => +k);
const twin = new Map<string, number>();
if (epIds.size) {
  const { data, error } = await sb.from("question_bank").select("id, source_exam_id, source_index").in("id", [...epIds]);
  if (error) throw error;
  for (const r of data!) if (r.source_exam_id != null) (twin.set(`${r.source_exam_id}#${r.source_index}`, r.id), examIds.includes(r.source_exam_id) || examIds.push(r.source_exam_id));
}
const thay = (v: unknown, l: [string, string][] = []): unknown =>
  typeof v === "string" ? l.reduce((t, [a, b]) => t.split(a).join(b), v)
  : Array.isArray(v) ? v.map((x) => thay(x, l))
  : v && typeof v === "object" ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, thay(x, l)])) : v;
/** Sửa một câu; bankId != null và thầy đã duyệt → ép + thay tay. Trả null nếu không đổi. */
const xuLy = (q: unknown, bankId: number | null, noi: string) => {
  const ep = bankId != null && epIds.has(bankId);
  const q0 = ep ? thay(q, suaTay[String(bankId)]) : q;
  const r = suaCau(q0, ep);
  r.nghiNgo.forEach((x) => nghi.push({ noi, ly_do: x }));
  if (JSON.stringify(r.q) === JSON.stringify(q)) return null;
  if (!ep && loiKatex(r.q) > loiKatex(q)) { boVi.push(noi); return null; }
  return { q: r.q, sua: ep ? [...r.sua, "duyet"] : r.sua };
};

const exams: { id: number; questions: unknown[] }[] = [];
const examOut: { id: number; questions: unknown[]; sua: string[] }[] = [];
for (let i = 0; i < examIds.length; i += 50) {
  const data = await lay(() => sb.from("exams").select("id, questions").in("id", examIds.slice(i, i + 50)));
  exams.push(...(data as never[]));
  await pause(300);
}
for (const e of exams) {
  const s = new Set<string>();
  const qs = (e.questions ?? []).map((q, idx) => {
    const r = xuLy(q, twin.get(`${e.id}#${idx}`) ?? null, `đề ${e.id}#${idx}`);
    if (!r) return q;
    r.sua.forEach((x) => (s.add(x), (dem["đề:" + x] = (dem["đề:" + x] ?? 0) + 1)));
    return r.q;
  });
  if (s.size) examOut.push({ id: e.id, questions: qs, sua: [...s] });
}

const bankIds = new Set([...bankFlag.map((r) => r.id), ...epIds]);
for (let i = 0; i < examIds.length; i += 20) {
  const data = await lay(() => sb.from("question_bank").select("id").eq("archived", false).in("source_exam_id", examIds.slice(i, i + 20)));
  data!.forEach((r) => bankIds.add(r.id));
  await pause(300);
}
const ids = [...bankIds];
const bankOut: { id: number; question: unknown; sua: string[]; truoc: unknown }[] = [];
for (let i = 0; i < ids.length; i += 200) {
  const data = await lay(() => sb.from("question_bank").select("id, question").in("id", ids.slice(i, i + 200)));
  for (const row of data!) {
    if (boIds.includes(row.id)) continue;
    const r = xuLy(row.question, row.id, `nh ${row.id}`);
    if (!r) continue;
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
    `create table ${bk}_bank as select * from public.question_bank where id in (${[...bankOut.map((r) => r.id), ...boIds].join(",") || "0"});`,
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
if (boIds.length) parts.push(`begin;\nupdate public.question_bank set archived = true, updated_at = now() where id in (${boIds.join(",")});\ncommit;`);
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
