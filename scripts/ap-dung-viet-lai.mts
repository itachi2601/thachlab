// Ghi lời giải VIẾT LẠI (data/giai-lai/viet-lai/kq-NN.json: thêm "Sai vì…") vào question_bank, ghi đè explanation cũ. Chỉ khi đáp án agent KHỚP DB, không ghi chú, có đoạn "Sai vì". Không đụng exams.
//   npx tsx scripts/ap-dung-viet-lai.mts [viet-lai|viet-lai2] [--apply]
// (gốc: ghi lời giải do agent giải mù (xuat-giai-truc-tiep.mts → kq-NN.json) vào question_bank. CHỈ ghi câu đáp án agent KHỚP đáp án DB;
// câu lệch → <thư-mục>/lech.json để thầy xem. KHÔNG đụng exams (trigger từng ghi đè đáp án).
//   npx tsx scripts/ap-dung-giai-truc-tiep.mts [truc-tiep|truc-tiep-anh] [--apply]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { plain, katexLoi, dbAnswer, tachMuiTen, loiMuiTen, khop } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const DIR = "scripts/data/giai-lai/" + (process.argv.find((a) => /^viet-lai\d*$/.test(a)) ?? "viet-lai") + "/";
const kq = new Map<number, any>();
for (const f of fs.readdirSync(DIR).filter((f) => /^kq-\d+\.json$/.test(f))) for (const x of JSON.parse(fs.readFileSync(DIR + f, "utf8"))) kq.set(x.id, x);
const lamSach = (h: string) => h.replace(/(?<!\\)\$(.+?)(?<!\\)\$/gs, (_m, t: string) => "$" + t.replace(/</g, "\\lt ").replace(/>/g, "\\gt ") + "$");
const ids = [...kq.keys()]; const cur = new Map<number, any>();
for (let i = 0; i < ids.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,archived,question").in("id", ids.slice(i, i + 200));
  if (error) throw new Error(error.message); data!.forEach((r) => cur.set(r.id, r));
}
const plan: any[] = [], lech: any[] = []; const bo: Record<string, number> = { khongThay: 0, luuTru: 0, daCo: 0, ngan: 0, katex: 0, ghiChu: 0 };
for (const k of kq.values()) {
  const r = cur.get(k.id);
  if (!r) { bo.khongThay++; continue; } if (r.archived) { bo.luuTru++; continue; }
  if (!khop(r.question, k.answer)) { lech.push({ id: k.id, db: dbAnswer(r.question), agent: k.answer, ghi_chu: k.ghi_chu }); continue; }
  if (k.ghi_chu && String(k.ghi_chu).trim()) { lech.push({ id: k.id, db: dbAnswer(r.question), agent: k.answer, ghi_chu: k.ghi_chu, khop: true }); bo.ghiChu++; continue; }
  const ex = tachMuiTen(lamSach(String(k.explanation ?? "")));
  if (plain(ex).length < 80) { bo.ngan++; continue; }
  if (!/(sai|không đúng|không khớp) vì/i.test(plain(ex))) { bo.ngan++; lech.push({ id: k.id, loi: "thiếu Sai vì" }); continue; }
  if (katexLoi(ex) > 0 || loiMuiTen(ex) > 0) { bo.katex++; lech.push({ id: k.id, loi: "katex/mui_ten", ex }); continue; }
  plan.push({ id: k.id, truoc: r.question, sau: { ...r.question, explanation: ex } });
}
fs.writeFileSync(DIR + "lech.json", JSON.stringify(lech, null, 1));
console.log(`kq ${kq.size} · sẽ ghi ${plan.length} · lệch/ghi chú/lỗi ${lech.length} (xem lech.json) ·`, bo);
if (!APPLY) { console.log("dry-run — thêm --apply để ghi"); process.exit(0); }
const bp = `scripts/logs/viet-lai-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify(plan.map((p) => ({ id: p.id, question: p.truoc })))); console.log("sao lưu:", bp);
let ok = 0, loi = 0; const q = [...plan];
await Promise.all(Array.from({ length: 8 }, async () => { while (q.length) { const p = q.shift()!;
  for (let t = 1; t <= 3; t++) { const { error } = await sb.from("question_bank").update({ question: p.sau }).eq("id", p.id); if (!error) { ok++; break; } if (t === 3) { loi++; console.log("LỖI", p.id, error.message); } } } }));
console.log(`ghi ${ok}, lỗi ${loi}`);
