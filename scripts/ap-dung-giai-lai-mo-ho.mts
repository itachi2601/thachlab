// Ghi lời giải mới cho các câu "khớp nhưng Haiku ghi chú mơ hồ" mà Sonnet soát và cho ghi thẳng (kl="ghi", không "sua").
// CHỈ cập nhật question_bank (KHÔNG đụng exams: trigger exams→ngân hàng từng ghi đè đáp án, xem project_thachlab_giai_lai_ngan_hang).
// Lời giải lấy từ lo-NN.json (loi_giai_moi) với quyết định từ kq-NN.json (kq-08b.json đè kq-08). Không đổi đáp án.
//   npx tsx scripts/ap-dung-giai-lai-mo-ho.mts            dry-run   |   --apply  ghi thật (sao lưu scripts/logs/giai-lai-mo-ho-backup-*.json)
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { plain, katexLoi, dbAnswer } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const DIR = "scripts/data/giai-lai/mo-ho/";
const ls = fs.readdirSync(DIR), rd = (f: string) => JSON.parse(fs.readFileSync(DIR + f, "utf8")) as any[];
const src = new Map<number, any>(), kq = new Map<number, any>();
for (const f of ls.filter((f) => /^lo-\d+\.json$/.test(f))) rd(f).forEach((x) => src.set(x.id, x));
for (const f of ls.filter((f) => /^kq-\d+\.json$/.test(f))) rd(f).forEach((x) => kq.set(x.id, x));
if (ls.includes("kq-08b.json")) rd("kq-08b.json").forEach((x) => kq.set(x.id, x));
const lamSach = (h: string) => h.replace(/(?<!\\)\$(.+?)(?<!\\)\$/gs, (_m, t: string) => "$" + t.replace(/</g, "\\lt ").replace(/>/g, "\\gt ") + "$");
const ds = [...kq.values()].filter((k) => k.kl === "ghi" && !k.sua);
console.log(`Sonnet cho ghi thẳng: ${ds.length} câu`);
const cur = new Map<number, any>();
for (let i = 0; i < ds.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,archived,question").in("id", ds.slice(i, i + 200).map((x) => x.id));
  if (error) throw new Error(error.message);
  data!.forEach((r) => cur.set(r.id, r));
}
const plan: { id: number; truoc: any; sau: any }[] = []; const bo: Record<string, number> = { khongThay: 0, luuTru: 0, daCoLoiGiai: 0, lechDapAn: 0, katex: 0, rong: 0 };
for (const k of ds) {
  const r = cur.get(k.id), s = src.get(k.id);
  if (!r) { bo.khongThay++; continue; }
  if (r.archived) { bo.luuTru++; continue; }
  if (plain(r.question.explanation).length >= 80) { bo.daCoLoiGiai++; continue; }
  if (JSON.stringify(dbAnswer(r.question)) !== JSON.stringify(s.dap_an_db) && !(r.question.type === "multiple_choice" && dbAnswer(r.question) === s.dap_an_db)) { bo.lechDapAn++; continue; }
  const ex = lamSach(String(s.loi_giai_moi ?? ""));
  if (plain(ex).length < 40) { bo.rong++; continue; }
  if (katexLoi(ex) > 0) { bo.katex++; continue; }
  plan.push({ id: k.id, truoc: r.question, sau: { ...r.question, explanation: ex } });
}
console.log(`sẽ ghi ${plan.length} câu · bỏ qua`, bo);
if (!APPLY) { console.log("dry-run xong — thêm --apply để ghi"); process.exit(0); }
const bp = `scripts/logs/giai-lai-mo-ho-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify(plan.map((p) => ({ id: p.id, question: p.truoc })))); console.log("sao lưu:", bp);
let ok = 0, loi = 0, done = 0; const q = [...plan];
await Promise.all(Array.from({ length: 8 }, async () => { while (q.length) { const p = q.shift()!;
  for (let t = 1; t <= 3; t++) { const { error } = await sb.from("question_bank").update({ question: p.sau }).eq("id", p.id); if (!error) { ok++; break; } if (t === 3) { loi++; console.log("LỖI", p.id, error.message); } }
  if (++done % 100 === 0) console.log(`  bank ${done}/${plan.length}`); } }));
console.log(`ghi ${ok}, lỗi ${loi}`);
