// Lượt 2 (26/11/2026): bổ sung hình bị mất — #168/#175 đề 1397 câu 9 + đề 462 câu 13 (hình gốc 98 px, hình có i_c = 0 lại là Hình 4 lệch đáp án C → đổi sang phương án chữ, giữ C), #170 đề 96 câu 36 (vẽ SVG nhiệt kế 0–50 °C, ĐCNN 2 °C).
// CHẠY THỬ, không ghi DB: npx tsx scripts/sua-bao-loi-2026-11-26b.mts
// Ghi scripts/logs/sua-bao-loi-1126b/{diff.txt, apply-00-saoluu.sql, apply-01-sua.sql, apply-02-kiemtra.sql}.
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

// Nhiệt kế đứng 0–50 °C, vạch nhỏ 2 °C, vạch số 10 °C (khớp lời giải: GHĐ 50 °C, ĐCNN 2 °C).
const nhietKe = (() => {
  const y0 = 230, y50 = 30, px = (t: number) => y0 - ((y0 - y50) * t) / 50;
  let v = "";
  for (let t = 0; t <= 50; t += 2) {
    const dai = t % 10 === 0 ? 14 : 7;
    v += `<line x1="72" y1="${px(t)}" x2="${72 + dai}" y2="${px(t)}"/>`;
    if (t % 10 === 0) v += `<text x="92" y="${px(t) + 4}" font-size="12" fill="currentColor" stroke="none">${t}</text>`;
  }
  return `<figure class="fig"><svg viewBox="0 0 150 290" width="150" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Nhiệt kế thang 0 đến 50 độ C" stroke="currentColor" fill="none" stroke-width="1.5">` +
    `<path d="M52 20 a8 8 0 0 1 16 0 V242 a16 16 0 1 1 -16 0 Z"/>` +
    `<line x1="60" y1="${px(24)}" x2="60" y2="252" stroke="#dc2626" stroke-width="5"/><circle cx="60" cy="256" r="11" fill="#dc2626" stroke="none"/>` +
    v + `<text x="112" y="18" font-size="12" fill="currentColor" stroke="none">°C</text></svg></figure>`;
})();

const KHUNG_Q = "Khi cho một khung dây dẫn kín (không biến dạng) chuyển động tịnh tiến trong từ trường đều. Phát biểu nào sau đây đúng về dòng điện cảm ứng $i_c$ trong khung?";
const KHUNG_O = [
  "Trong khung xuất hiện dòng điện cảm ứng có chiều không đổi.",
  "Trong khung xuất hiện dòng điện cảm ứng đổi chiều liên tục.",
  "Trong khung không xuất hiện dòng điện cảm ứng ($i_c = 0$).",
  "Trong khung chỉ xuất hiện dòng điện cảm ứng khi khung chuyển động đủ nhanh.",
];
const khung = (q: Q): Q => {
  if (q.answer !== 2 || !String(q.question).includes("chuyển động tịnh tiến trong từ trường đều")) throw new Error("câu khung dây không khớp");
  return { ...q, question: KHUNG_Q, options: KHUNG_O };
};

const edits: { exam: number; idx: number; mo_ta: string; f: (q: Q) => Q }[] = [
  { exam: 1397, idx: 8, mo_ta: "#168/#175: phương án Hình 1–4 → phương án chữ (giữ C)", f: khung },
  { exam: 462, idx: 12, mo_ta: "cùng câu với 1397/9: hình 98 px lệch đáp án → phương án chữ (giữ C)", f: khung },
  {
    exam: 96, idx: 35, mo_ta: "#170: vẽ hình nhiệt kế",
    f: (q) => { if (String(q.question).includes("<svg")) throw new Error("96/35 đã có hình"); return { ...q, question: String(q.question) + nhietKe }; },
  },
];

const out = "scripts/logs/sua-bao-loi-1126b";
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

const bk = "public.bk_sua_bao_loi_20261126b";
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
