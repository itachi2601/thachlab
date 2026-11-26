// Sửa câu bị học sinh báo lỗi (26/11/2026): #176 đề 72 câu 37, #174 đề 70 câu 54 ý b, #172 đề 123 câu 2, #171 đề 289 câu 25.
// CHẠY THỬ, không ghi DB: npx tsx scripts/sua-bao-loi-2026-11-26.mts
// Ghi scripts/logs/sua-bao-loi-1126/{diff.txt, apply-00-saoluu.sql, apply-01-sua.sql, apply-02-kiemtra.sql}.
// Mỗi chỗ sửa áp cho CẢ exams.questions LẪN question_bank (nhận theo content_hash cũ), tính lại content_hash.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";

for (const l of fs.readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!, { auth: { persistSession: false } });

type Q = Record<string, unknown>;
/** Thay chuỗi đúng nguyên văn; không thấy thì dừng (không sửa nhầm). */
const rep = (q: Q, field: string, from: string, to: string): Q => {
  const v = JSON.stringify(q[field]);
  const fr = JSON.stringify(from).slice(1, -1);
  if (!v.includes(fr)) throw new Error(`không thấy "${from}" trong ${field}`);
  return { ...q, [field]: JSON.parse(v.split(fr).join(JSON.stringify(to).slice(1, -1))) };
};
const repAll = (q: Q, from: string, to: string): Q => {
  const s = JSON.stringify(q), fr = JSON.stringify(from).slice(1, -1);
  if (!s.includes(fr)) throw new Error(`không thấy "${from}"`);
  return JSON.parse(s.split(fr).join(JSON.stringify(to).slice(1, -1)));
};

const GIAI_176 =
  '<p class="text-base leading-relaxed my-2">Van mở khi $T_m=\\dfrac{10^5}{0,9\\cdot 10^5}\\cdot 300\\approx 333K$. Từ đó van luôn giữ $p_1-p_2=10^5\\,Pa$ đến khi $T=500K$. Tổng lượng khí ở hai bình không đổi: $40p_1+10p_2=\\dfrac{0,9\\cdot 10^5\\cdot 40}{300}\\cdot 500=6\\cdot 10^6$ (Pa·lít). Kết hợp $p_1-p_2=10^5$ suy ra $p_1=1,4\\cdot 10^{5}Pa$, $p_2=p_1-10^5=0,4\\cdot 10^{5}Pa.$</p><p class="text-base leading-relaxed my-2">Chọn D.</p>';

const edits: { exam: number; idx: number; mo_ta: string; f: (q: Q) => Q }[] = [
  { exam: 72, idx: 36, mo_ta: "#176: p2 = 0,4·10^5 Pa, đáp án A → D", f: (q) => { if (q.answer !== 0) throw new Error("answer cũ khác 0"); return { ...q, answer: 3, explanation: GIAI_176 }; } },
  {
    exam: 70, idx: 53, mo_ta: "#174: ý b 6,68 → xấp xỉ 6,69·10^24",
    f: (q) => rep(rep(q, "statements", "nước là $6,68.10^{24}$ phân tử", "nước xấp xỉ $6,69.10^{24}$ phân tử"), "explanation", "\\approx 6{,}68\\cdot 10^{24}", "\\approx 6{,}69\\cdot 10^{24}"),
  },
  { exam: 123, idx: 1, mo_ta: "#172: 'không đúng với' → 'đúng với' (đáp án C V/T giữ nguyên)", f: (q) => rep(q, "question", "không đúng với định luật Charles", "đúng với định luật Charles") },
  {
    exam: 289, idx: 24, mo_ta: "#171: thêm dữ kiện đã nung đến 57 ℃ (câu tách khỏi câu trước bị thiếu)",
    f: (q) => rep(q, "question", "<br>Biết lực ma sát giữa nút chai", "<br>Người ta đã nung nóng khí trong chai đến $57 ℃$ mà nút chưa bật ra. Biết lực ma sát giữa nút chai"),
  },
];

const out = "scripts/logs/sua-bao-loi-1126";
fs.mkdirSync(out, { recursive: true });
const lit = (v: unknown) => `'${JSON.stringify(v).replace(/'/g, "''")}'::jsonb`;
const ids = [...new Set(edits.map((e) => e.exam))];
const { data: exams, error } = await sb.from("exams").select("id,questions").in("id", ids);
if (error) throw error;

const diff: string[] = [];
const upd: string[] = [];
const bank: string[] = [];
const moi: Record<number, Q[]> = {};
for (const e of exams!) moi[e.id] = (e.questions as Q[]).map((q) => ({ ...q }));
for (const ed of edits) {
  const cu = (exams!.find((x) => x.id === ed.exam)!.questions as Q[])[ed.idx];
  const nw = ed.f(cu);
  moi[ed.exam][ed.idx] = nw;
  diff.push(`## đề ${ed.exam} câu ${ed.idx + 1}: ${ed.mo_ta}\n- trước: ${JSON.stringify({ q: cu.question, o: cu.options })}\n- sau:   ${JSON.stringify({ q: nw.question, o: nw.options })}\n`);
  bank.push(
    `update public.question_bank b set question = v.q, updated_at = now(), content_hash = case when exists (select 1 from public.question_bank x where x.content_hash = public.question_content_hash(v.q)) then b.content_hash else public.question_content_hash(v.q) end ` +
      `from (select ${lit(nw)} as q) v where b.content_hash = public.question_content_hash(${lit(cu)}) and b.archived = false;`,
  );
}
for (const id of ids) upd.push(`update public.exams set questions = ${lit(moi[id])} where id = ${id};`);

const bk = "public.bk_sua_bao_loi_20261126";
fs.writeFileSync(`${out}/diff.txt`, diff.join("\n"));
fs.writeFileSync(
  `${out}/apply-00-saoluu.sql`,
  [
    "begin;",
    `create table ${bk}_exams as select id, questions from public.exams where id in (${ids.join(",")});`,
    `alter table ${bk}_exams enable row level security; revoke all on ${bk}_exams from anon, authenticated;`,
    `create table ${bk}_bank as select * from public.question_bank where content_hash in (${edits.map((e) => `public.question_content_hash(${lit((exams!.find((x) => x.id === e.exam)!.questions as Q[])[e.idx])})`).join(",")});`,
    `alter table ${bk}_bank enable row level security; revoke all on ${bk}_bank from anon, authenticated;`,
    `select (select count(*) from ${bk}_exams) as de_sao_luu, (select count(*) from ${bk}_bank) as bank_sao_luu;`,
    "commit;",
  ].join("\n"),
);
fs.writeFileSync(
  `${out}/apply-01-sua.sql`,
  ["begin;", "alter table public.exams disable trigger trg_exams_sync_bank;", ...upd, ...bank, "alter table public.exams enable trigger trg_exams_sync_bank;", "commit;"].join("\n"),
);
fs.writeFileSync(
  `${out}/apply-02-kiemtra.sql`,
  `select (select count(*) from public.exams e join ${bk}_exams k using (id) where e.questions is distinct from k.questions) as de_da_doi, (select count(*) from public.question_bank b join ${bk}_bank k using (id) where b.question is distinct from k.question) as bank_da_doi;`,
);
console.log(diff.join("\n"));
console.log(`\nĐã ghi ${out}/ (CHƯA ghi DB). Sửa ${edits.length} câu; bản đề: ${ids.join(", ")}`);
