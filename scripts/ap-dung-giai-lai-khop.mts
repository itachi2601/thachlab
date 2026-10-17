// Ghi lời giải Haiku cho các câu có đáp án KHỚP DB (scripts/data/giai-lai/ket-qua.json) vào question_bank + mọi bản sao trong exams.questions.
// Chỉ ghi câu: khop, không KaTeX lỗi, không ⇒ sai chỗ, Haiku KHÔNG ghi chú "đề mơ hồ" (nhóm có ghi chú để thầy duyệt riêng), và lời giải hiện tại còn trống/ngắn (<80 ký tự).
// Tự sửa nhẹ: dấu < > trần trong $…$ → \lt \gt. Không đổi đáp án. Sao lưu trước khi ghi.
//   npx tsx scripts/ap-dung-giai-lai-khop.mts            dry-run   |   --apply  ghi thật (chạy lại được: câu đã có lời giải dài tự bị bỏ qua)
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { plain, katexLoi } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const arg = (k: string, d: number) => Number(process.argv.find((a) => a.startsWith(`--${k}=`))?.slice(k.length + 3) ?? d);
const CONC = arg("conc", 6), MAXDE = arg("max-de", 1e9);
const k1: any[] = JSON.parse(fs.readFileSync("scripts/data/giai-lai/ket-qua.json", "utf8"));
const lamSach = (h: string) => h.replace(/(?<!\\)\$(.+?)(?<!\\)\$/gs, (_m, t: string) => "$" + t.replace(/</g, "\\lt ").replace(/>/g, "\\gt ") + "$");

const dung = k1.filter((x) => !x.loi && x.khop && !x.katex_loi && !x.mui_ten_con && !String(x.ghi_chu ?? "").trim());
const giuLai = k1.filter((x) => !x.loi && x.khop && !x.katex_loi && !x.mui_ten_con && String(x.ghi_chu ?? "").trim()).length;
console.log(`khớp dùng được ${dung.length} (giữ lại cho thầy duyệt vì Haiku ghi chú mơ hồ: ${giuLai})`);

const bank = new Map<number, any>();
for (let i = 0; i < dung.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,question,archived").in("id", dung.slice(i, i + 200).map((x) => x.id));
  if (error) throw new Error(error.message);
  data!.forEach((r) => bank.set(r.id, r));
}
const key = (q: any) => JSON.stringify([q.type, q.question, q.options ?? null, (q.statements ?? []).map((s: any) => s.text)]);
const plan: { id: number; truoc: any; sau: any }[] = []; const thayThe = new Map<string, string>();
let boQua = { daCoLoiGiai: 0, katex: 0, khongThay: 0 };
for (const x of dung) {
  const r = bank.get(x.id); if (!r || r.archived) { boQua.khongThay++; continue; }
  if (plain(r.question.explanation).length >= 80) { boQua.daCoLoiGiai++; continue; }
  const ex = lamSach(x.explanation);
  if (katexLoi(ex) > 0) { boQua.katex++; continue; }
  plan.push({ id: x.id, truoc: r.question, sau: { ...r.question, explanation: ex } });
  thayThe.set(key(r.question), ex);
}
console.log(`sẽ ghi ngân hàng ${plan.length} câu · bỏ qua: đã có lời giải ${boQua.daCoLoiGiai}, KaTeX sau sửa nhẹ ${boQua.katex}, lưu trữ/không thấy ${boQua.khongThay}`);

const exams: any[] = [];
for (let o = 0; ; o += 100) {
  const { data, error } = await sb.from("exams").select("id,questions").order("id").range(o, o + 99);
  if (error) throw new Error(error.message);
  exams.push(...data!); if (data!.length < 100) break;
}
const examMoi = new Map<number, any[]>(), examGoc: any[] = []; let banSao = 0;
for (const e of exams) {
  if (!Array.isArray(e.questions)) continue;
  let doi = false;
  const qs = e.questions.map((q: any) => { const ex = thayThe.get(key(q)); if (!ex || plain(q.explanation).length >= 80) return q; doi = true; banSao++; return { ...q, explanation: ex }; });
  if (doi) { examMoi.set(e.id, qs); examGoc.push({ id: e.id, questions: e.questions }); }
}
console.log(`bản sao trong exams: ${banSao} câu ở ${examMoi.size} đề`);
if (!APPLY) { console.log("dry-run xong — thêm --apply để ghi"); process.exit(0); }

const bp = `scripts/logs/giai-lai-khop-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify({ bank: plan.map((p) => ({ id: p.id, question: p.truoc })), exams: examGoc }));
console.log("sao lưu:", bp);
async function song<T>(items: T[], conc: number, fn: (x: T) => Promise<void>) { const q = [...items]; await Promise.all(Array.from({ length: conc }, async () => { while (q.length) await fn(q.shift()!); })); }
let okE = 0, loiE = 0, done = 0;
const t0 = Date.now();
await song([...examMoi].slice(0, MAXDE), CONC, async ([id, qs]) => {
  for (let t = 1; t <= 3; t++) { const { error } = await sb.from("exams").update({ questions: qs }).eq("id", id); if (!error) { okE++; break; } if (t === 3) { loiE++; console.log("LỖI đề", id, error.message); } }
  if (++done % 25 === 0) console.log(`  exams ${done}/${examMoi.size}`);
});
console.log(`exams: ghi ${okE}/${examMoi.size}, lỗi ${loiE} · ${((Date.now() - t0) / 1000).toFixed(0)}s`);
if (MAXDE < 1e9) { console.log("chạy thử --max-de: dừng trước bước ngân hàng"); process.exit(0); }
// bank: đọc lại, chỉ ghi câu chưa có lời giải mới (trigger từ exams có thể đã đồng bộ)
const cur = new Map<number, string>();
for (let i = 0; i < plan.length; i += 200) {
  const { data } = await sb.from("question_bank").select("id,question").in("id", plan.slice(i, i + 200).map((p) => p.id));
  data!.forEach((r) => cur.set(r.id, r.question.explanation));
}
const can = plan.filter((p) => cur.get(p.id) !== p.sau.explanation);
console.log(`ngân hàng: ${plan.length - can.length} câu đã được trigger đồng bộ, còn ghi ${can.length}`);
let okB = 0, loiB = 0; done = 0;
await song(can, 12, async (p) => {
  for (let t = 1; t <= 3; t++) { const { error } = await sb.from("question_bank").update({ question: p.sau }).eq("id", p.id); if (!error) { okB++; break; } if (t === 3) { loiB++; console.log("LỖI", p.id, error.message); } }
  if (++done % 500 === 0) console.log(`  bank ${done}/${can.length}`);
});
console.log(`ngân hàng: ghi ${okB}, lỗi ${loiB}`);
