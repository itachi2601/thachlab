// CHỈ ĐỌC. So đáp án của từng câu trong exams.questions với câu cùng nội dung trong question_bank.
//   npx tsx scripts/so-dap-an-exams-ngan-hang.mts  → scripts/data/giai-lai/lech-exams-ds.json
// Khớp câu theo nội dung (type, question, options, statements[].text); nhiều dòng ngân hàng cùng nội dung mà khác đáp án = "mơ hồ".
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { dbAnswer } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const key = (q: any) => JSON.stringify([q.type, q.question, q.options ?? null, (q.statements ?? []).map((s: any) => s.text)]);
const eq = (a: any, b: any) => JSON.stringify(a) === JSON.stringify(b);
const bank = new Map<string, { id: number; ans: any; archived: boolean }[]>();
let nBank = 0;
for (let o = 0; ; o += 1000) {
  const { data, error } = await sb.from("question_bank").select("id,archived,question").order("id").range(o, o + 999);
  if (error) throw new Error(error.message);
  for (const r of data!) { const k = key(r.question); (bank.get(k) ?? bank.set(k, []).get(k)!).push({ id: r.id, ans: dbAnswer(r.question), archived: r.archived }); nBank++; }
  if (data!.length < 1000) break;
}
const set8373 = new Set<number>((JSON.parse(fs.readFileSync("scripts/data/giai-lai/ket-qua.json", "utf8")) as any[]).map((x) => x.id));
let nExam = 0, nQ = 0, khongThay = 0, khop = 0, mơHo = 0;
const lech: any[] = [];
for (let o = 0; ; o += 100) {
  const { data, error } = await sb.from("exams").select("id,title,questions").order("id").range(o, o + 99);
  if (error) throw new Error(error.message);
  for (const e of data!) {
    if (!Array.isArray(e.questions)) continue; nExam++;
    e.questions.forEach((q: any, i: number) => {
      nQ++; const rows = bank.get(key(q)); if (!rows) { khongThay++; return; }
      const a = dbAnswer(q), live = rows.filter((r) => !r.archived), use = live.length ? live : rows;
      if (use.every((r) => eq(r.ans, a))) { khop++; return; }
      if (use.some((r) => eq(r.ans, a))) { mơHo++; return; }
      lech.push({ exam: e.id, tieuDe: e.title, stt: i + 1, type: q.type, de: a, nganHang: use[0].ans, bankIds: use.map((r) => r.id), trongTap8373: use.some((r) => set8373.has(r.id)) });
    });
  }
  if (data!.length < 100) break;
}
const dem = (f: (x: any) => string) => lech.reduce((m: any, x) => ((m[f(x)] = (m[f(x)] ?? 0) + 1), m), {});
console.log(`ngân hàng ${nBank} câu · ${nExam} đề · ${nQ} câu trong đề`);
console.log(`khớp nội dung+đáp án ${khop} · không thấy trong ngân hàng ${khongThay} · nhiều bản ngân hàng, có bản khớp đề ${mơHo}`);
console.log(`LỆCH ĐÁP ÁN: ${lech.length} câu ở ${new Set(lech.map((x) => x.exam)).size} đề · theo loại`, dem((x) => x.type), `· trong tập 8.373: ${lech.filter((x) => x.trongTap8373).length}, ngoài tập: ${lech.filter((x) => !x.trongTap8373).length}`);
fs.writeFileSync("scripts/data/giai-lai/lech-exams-ds.json", JSON.stringify(lech));
