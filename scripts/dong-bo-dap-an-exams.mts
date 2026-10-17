// Đồng bộ đáp án bản sao trong exams.questions theo question_bank cho các câu LỆCH nằm trong tập 8.373 câu đã giải lại
// (danh sách từ scripts/so-dap-an-exams-ngan-hang.mts → scripts/data/giai-lai/lech-exams-ds.json). Câu ngoài tập KHÔNG đụng, chỉ xuất ra ngoai-tap-xem.json để thầy xem.
//   npx tsx scripts/dong-bo-dap-an-exams.mts            dry-run
//   npx tsx scripts/dong-bo-dap-an-exams.mts --apply    ghi thật, sao lưu exams trước khi ghi: scripts/logs/dong-bo-dap-an-exams-backup-*.json
// Chỉ đổi trường đáp án của câu; mỗi câu phải còn đúng nội dung + đáp án như lúc so, và mọi bản ngân hàng cùng nội dung phải đồng ý một đáp án.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { dbAnswer } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const key = (q: any) => JSON.stringify([q.type, q.question, q.options ?? null, (q.statements ?? []).map((s: any) => s.text)]);
const eq = (a: any, b: any) => JSON.stringify(a) === JSON.stringify(b);
const lech: any[] = JSON.parse(fs.readFileSync("scripts/data/giai-lai/lech-exams-ds.json", "utf8"));
const trong = lech.filter((x) => x.trongTap8373), ngoai = lech.filter((x) => !x.trongTap8373);

const bankIds = [...new Set(lech.flatMap((x) => x.bankIds))];
const bank = new Map<number, any>();
for (let i = 0; i < bankIds.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,archived,question").in("id", bankIds.slice(i, i + 200));
  if (error) throw new Error(error.message);
  data!.forEach((r) => bank.set(r.id, r));
}
const examIds = [...new Set(lech.map((x) => x.exam))];
const exams = new Map<number, any>();
for (let i = 0; i < examIds.length; i += 50) {
  const { data, error } = await sb.from("exams").select("id,title,questions").in("id", examIds.slice(i, i + 50));
  if (error) throw new Error(error.message);
  data!.forEach((r) => exams.set(r.id, r));
}

// câu ngoài tập: xuất để xem
const xem = ngoai.map((x) => {
  const q = exams.get(x.exam).questions[x.stt - 1];
  return { exam: x.exam, tieuDe: x.tieuDe, stt: x.stt, type: q.type, cauHoi: q.question, options: q.options, statements: q.statements?.map((s: any) => s.text), dapAnTrongDe: x.de, dapAnNganHang: x.nganHang, loiGiaiNganHang: bank.get(x.bankIds[0])?.question?.explanation ?? "", loiGiaiDe: q.explanation ?? "" };
});
fs.writeFileSync("scripts/data/giai-lai/ngoai-tap-xem.json", JSON.stringify(xem, null, 1));

const moi = new Map<number, any[]>(), goc: any[] = []; const boQua: string[] = []; let soCau = 0;
for (const x of trong) {
  const e = exams.get(x.exam); if (!e) { boQua.push(`đề ${x.exam} mất`); continue; }
  const qs: any[] = moi.get(x.exam) ?? structuredClone(e.questions);
  const q = qs[x.stt - 1];
  if (!q || !bank.size) { boQua.push(`${x.exam}#${x.stt} không còn`); continue; }
  const rows = x.bankIds.map((id: number) => bank.get(id)).filter((r: any) => r && (!r.archived || x.bankIds.length === 1));
  const dich = rows.length ? dbAnswer(rows[0].question) : null;
  if (!rows.length || !rows.every((r: any) => key(r.question) === key(q) && eq(dbAnswer(r.question), dich))) { boQua.push(`${x.exam}#${x.stt} ngân hàng không thống nhất/đổi nội dung`); continue; }
  if (!eq(dbAnswer(q), x.de)) { boQua.push(`${x.exam}#${x.stt} đáp án trong đề đã khác lúc so`); continue; }
  if (q.type === "multiple_choice") q.answer = "ABCD".indexOf(dich);
  else if (q.type === "short_answer") q.answer = dich;
  else (q.statements ?? []).forEach((st: any, i: number) => (st.answer = !!dich[i]));
  moi.set(x.exam, qs); soCau++;
}
for (const id of moi.keys()) goc.push({ id, questions: exams.get(id).questions });
console.log(`lệch trong tập ${trong.length} · sẽ đổi ${soCau} câu ở ${moi.size} đề · bỏ qua ${boQua.length}${boQua.length ? ":\n  " + boQua.slice(0, 10).join("\n  ") : ""}`);
console.log(`ngoài tập (không đụng): ${ngoai.length} câu → scripts/data/giai-lai/ngoai-tap-xem.json`);
if (!APPLY) { console.log("dry-run xong — thêm --apply để ghi"); process.exit(0); }

const bp = `scripts/logs/dong-bo-dap-an-exams-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify({ exams: goc }));
console.log("sao lưu:", bp);
let ok = 0, loi = 0, done = 0; const t0 = Date.now();
for (const [id, qs] of moi) {
  for (let t = 1; t <= 3; t++) { const { error } = await sb.from("exams").update({ questions: qs }).eq("id", id); if (!error) { ok++; break; } if (t === 3) { loi++; console.log("LỖI đề", id, error.message); } }
  if (++done % 10 === 0) console.log(`  exams ${done}/${moi.size} · ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
console.log(`exams: ghi ${ok}/${moi.size}, lỗi ${loi} · ${((Date.now() - t0) / 1000).toFixed(0)}s`);
