// Sửa 5 chỗ trong đề bị báo lỗi (12/11/2026): 1298 (câu 4, 11, 13 và phương án câu 11), 753 câu 9, 23 câu 14.
// CHẠY THỬ, không ghi DB: npx tsx scripts/sua-bao-loi-2026-11-12.mts
// Ghi scripts/logs/sua-bao-loi-1112/{diff.txt, apply-00-saoluu.sql, apply-01-sua.sql, apply-02-kiemtra.sql}.
// Mỗi chỗ sửa áp cho CẢ exams.questions LẪN question_bank (nhận theo content_hash cũ), tính lại content_hash;
// chạy các file sau 22h theo thứ tự: supabase db query --linked -f <file>.
// Câu 1354/13 (thiếu hình) chưa nằm ở đây: chờ thầy cho hình gốc.
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

const Q4_MOI =
  "Cho ba lực đồng quy (tại điểm O), đồng phẳng $\\vec F_1$, $\\vec F_2$, $\\vec F_3$ lần lượt tạo với trục Ox những góc $0^\\circ$, $60^\\circ$, $120^\\circ$ và có độ lớn tương ứng là $F_1 = F_3 = 2F_2 = 10\\ \\text{N}$. Hợp lực của ba lực trên là";

const edits: { exam: number; idx: number; mo_ta: string; f: (q: Q) => Q }[] = [
  { exam: 1298, idx: 3, mo_ta: "câu 4: thay ảnh công thức nhỏ bằng LaTeX", f: (q) => ({ ...q, question: Q4_MOI }) },
  { exam: 1298, idx: 10, mo_ta: "câu 11: \\sin, \\cos thẳng", f: (q) => rep(rep(q, "options", "$Psin\\alpha .$", "$P\\sin\\alpha$"), "options", "$Pcos\\alpha .$", "$P\\cos\\alpha$") },
  { exam: 1298, idx: 11, mo_ta: "câu 12: góc 1500 → 150°", f: (q) => rep(q, "question", "góc 1500 và", "góc $150^\\circ$ và") },
  { exam: 1298, idx: 12, mo_ta: "câu 13: F_{kéo} → F_{\\text{kéo}}", f: (q) => repAll(q, "F_{kéo}", "F_{\\text{kéo}}") },
  {
    exam: 753, idx: 8, mo_ta: "câu 9: nói rõ bình cách nhiệt, dùng ΔU = A + Q",
    f: (q) => ({ ...q, question: "Khí giãn nở trong bình **cách nhiệt hoàn toàn** (không trao đổi nhiệt với bên ngoài). Theo $\\Delta U = A + Q$, nhiệt lượng $Q$ khí nhận được bằng bao nhiêu J?".replace(/\*\*/g, "") }),
  },
  {
    exam: 23, idx: 13, mo_ta: "câu 14: phương án B tránh gần nghĩa với D",
    f: (q) => rep(q, "options", "một chuyển động thẳng nhanh dần.", "một chuyển động thẳng nhanh dần nhưng gia tốc tăng dần."),
  },
];

const out = "scripts/logs/sua-bao-loi-1112";
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

const bk = "public.bk_sua_bao_loi_20261112";
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
