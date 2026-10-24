// Lấy danh mục chủ đề (yêu cầu cần đạt) lớp 12 -> chu-de-lop12.json cùng dạng chu-de-lop10.json. Chỉ đọc DB.
//   npx tsx scripts/data/nap-ngan-hang-vl12/lay-chu-de.mts
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const U = env("NEXT_PUBLIC_SUPABASE_URL"), K = env("SUPABASE_SERVICE_ROLE_KEY");
const h = { apikey: K, Authorization: `Bearer ${K}` };
const topics = await (await fetch(`${U}/rest/v1/question_topics?grade=eq.12&select=*&order=sort_order&limit=1000`, { headers: h })).json();
if (!Array.isArray(topics)) throw new Error(JSON.stringify(topics));
fs.writeFileSync("scripts/data/nap-ngan-hang-vl12/chu-de-lop12.json", JSON.stringify({ topics }, null, 1));
const bank = await fetch(`${U}/rest/v1/question_bank?grade=eq.12&select=id`, { headers: { ...h, Prefer: "count=exact", Range: "0-0" } });
console.log("chủ đề lớp 12:", topics.length, "· ngân hàng lớp 12:", bank.headers.get("content-range"));
