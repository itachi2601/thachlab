// LỌC TRÙNG TRƯỚC khi giải: bỏ khỏi cau-bank.json mọi câu đã có trong question_bank lớp 10 (kể cả đang ẩn) hoặc trùng ngay trong lô.
//   VL10_DIR=scripts/data/nap-ngan-hang-vl10/c2 npx tsx scripts/loc-trung-vl10.mts
// Ghi: cau-bank-truoc-loc.json (bản gốc), cau-bank.json (đã lọc), trung.json (câu bỏ + id ngân hàng trùng). Không đụng DB.
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const U = env("NEXT_PUBLIC_SUPABASE_URL"), K = env("SUPABASE_SERVICE_ROLE_KEY");
const DIR = (process.env.VL10_DIR ?? "scripts/data/nap-ngan-hang-vl10") + "/";
const norm = (s: string) => s.replace(/<[^>]+>/g, "").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").toLowerCase().replace(/[^a-z0-9]+/g, "");
const sig = (q: any) => norm(String(q.question ?? "")).slice(0, 80) + "|" + norm((q.options ?? (q.statements ?? []).map((s: any) => s.text)).join("")).slice(0, 80);
const bank: any[] = [];
for (let o = 0; ; o += 500) {
  const r = await (await fetch(`${U}/rest/v1/question_bank?grade=eq.10&select=id,question&order=id`, { headers: { apikey: K, Authorization: `Bearer ${K}`, Range: `${o}-${o + 499}` } })).json();
  if (!Array.isArray(r)) throw new Error(JSON.stringify(r)); bank.push(...r); if (r.length < 500) break;
}
const have = new Map(bank.map((b) => [sig(b.question), b.id]));
const src: any[] = JSON.parse(fs.readFileSync(DIR + (fs.existsSync(DIR + "cau-bank-truoc-loc.json") ? "cau-bank-truoc-loc.json" : "cau-bank.json"), "utf8"));
if (!fs.existsSync(DIR + "cau-bank-truoc-loc.json")) fs.writeFileSync(DIR + "cau-bank-truoc-loc.json", JSON.stringify(src, null, 1));
const keep: any[] = [], trung: any[] = [];
for (const q of src) {
  const s = sig(q);
  if (norm(q.question).length < 10) { keep.push(q); continue; } // đề quá ngắn/toàn công thức: không đủ căn cứ coi là trùng
  if (have.has(s)) trung.push({ key: q.key, type: q.type, bankId: have.get(s) }); else { have.set(s, -1); keep.push(q); }
}
fs.writeFileSync(DIR + "cau-bank.json", JSON.stringify(keep, null, 1));
fs.writeFileSync(DIR + "trung.json", JSON.stringify(trung, null, 1));
console.log(`Ngân hàng lớp 10: ${bank.length} · trong lô: ${src.length} · TRÙNG (bỏ): ${trung.length} · còn lại cần giải: ${keep.length}`);
