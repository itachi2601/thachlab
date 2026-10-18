// Áp kết quả Opus kiểm (opus/kl-NN.json): kl="db_dung" → ghi lời giải mới vào question_bank (giữ đáp án DB). "sonnet_dung" (DB sai) và "mo_ho" KHÔNG tự ghi → opus/can-thay.json.
// CHỈ question_bank, KHÔNG đụng exams. Sao lưu scratchpad logs/opus-kiem-backup-*.json.
//   npx tsx scripts/ap-dung-opus-kiem.mts [--apply]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { plain, katexLoi, tachMuiTen, loiMuiTen, khop } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply"), DIR = "scripts/data/giai-lai/opus/";
const kl = new Map<number, any>(); for (const f of fs.readdirSync(DIR).filter((f) => /^kl-\d+\.json$/.test(f))) for (const x of JSON.parse(fs.readFileSync(DIR + f, "utf8"))) kl.set(x.id, x);
const lamSach = (h: string) => h.replace(/(?<!\\)\$(.+?)(?<!\\)\$/gs, (_m, t: string) => "$" + t.replace(/</g, "\\lt ").replace(/>/g, "\\gt ") + "$");
const ids = [...kl.keys()], cur = new Map<number, any>();
for (let i = 0; i < ids.length; i += 200) { const { data, error } = await sb.from("question_bank").select("id,archived,question").in("id", ids.slice(i, i + 200)); if (error) throw new Error(error.message); data!.forEach((r) => cur.set(r.id, r)); }
const plan: any[] = [], canThay: any[] = []; const dem: Record<string, number> = {};
const cong = (k: string) => (dem[k] = (dem[k] || 0) + 1);
for (const k of kl.values()) {
  const r = cur.get(k.id); if (!r || r.archived) { cong("khongThay/luuTru"); continue; }
  if (k.kl !== "db_dung") { canThay.push({ id: k.id, kl: k.kl, dap_an_db: undefined, dap_an_opus: k.dap_an, ly_do: k.ly_do }); cong(k.kl); continue; }
  if (plain(r.question.explanation ?? "").length >= 80) { cong("daCoLoiGiai"); continue; }
  if (!khop(r.question, k.dap_an)) { canThay.push({ id: k.id, kl: "db_dung_nhung_dap_an_khac_dinh_dang", dap_an_opus: k.dap_an, ly_do: k.ly_do }); cong("khacDinhDang"); continue; }
  const ex = tachMuiTen(lamSach(String(k.explanation ?? "")));
  if (plain(ex).length < 80 || katexLoi(ex) > 0 || loiMuiTen(ex) > 0) { cong("loiDinhDang"); canThay.push({ id: k.id, kl: "loi_dinh_dang", ly_do: k.ly_do }); continue; }
  plan.push({ id: k.id, truoc: r.question, sau: { ...r.question, explanation: ex } }); cong("seGhi");
}
fs.writeFileSync(DIR + "can-thay.json", JSON.stringify(canThay, null, 1)); console.log(`kl ${kl.size} ·`, dem);
if (!APPLY) { console.log("dry-run — thêm --apply"); process.exit(0); }
const bp = `scripts/logs/opus-kiem-backup-${Date.now()}.json`; fs.writeFileSync(bp, JSON.stringify(plan.map((p) => ({ id: p.id, question: p.truoc })))); console.log("sao lưu:", bp);
let ok = 0, loi = 0; const q = [...plan];
await Promise.all(Array.from({ length: 4 }, async () => { while (q.length) { const p = q.shift()!;
  for (let t = 1; t <= 4; t++) { const { error } = await sb.from("question_bank").update({ question: p.sau }).eq("id", p.id); if (!error) { ok++; break; } if (t === 4) { loi++; console.log("LỖI", p.id); } } } }));
console.log(`ghi ${ok}, lỗi ${loi}`);
