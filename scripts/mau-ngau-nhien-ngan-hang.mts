// Lấy MẪU NGẪU NHIÊN câu question_bank (chưa ẩn) để soát tay tìm lỗi phổ biến — CHỈ ĐỌC.
//   npx tsx scripts/mau-ngau-nhien-ngan-hang.mts 240 [seed]
// Ghi scripts/data/soat-mau/mau-<seed>.json + chia lô lo-NN.json (30 câu/lô) cho agent soát.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const d = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) =>
  fs.readFileSync(path.resolve(d, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });

const n = Number(process.argv[2] ?? 240);
let seed = Number(process.argv[3] ?? Date.now() % 100000);
const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2147483648), seed / 2147483648);

const ids: number[] = [];
for (let from = 0; ; from += 1000) {
  const { data, error } = await sb.from("question_bank").select("id").eq("archived", false).order("id").range(from, from + 999);
  if (error) throw error;
  if (!data?.length) break;
  ids.push(...data.map((r) => r.id as number));
}
const pick = new Set<number>();
while (pick.size < Math.min(n, ids.length)) pick.add(ids[Math.floor(rnd() * ids.length)]);
const { data, error } = await sb
  .from("question_bank")
  .select("id, grade, qtype, topic_name, source_exam_id, source_index, created_at, updated_at, question")
  .in("id", [...pick]);
if (error) throw error;
const out = path.join(d, "data", "soat-mau");
fs.mkdirSync(out, { recursive: true });
const rows = (data ?? []).sort((a, b) => a.id - b.id);
fs.writeFileSync(path.join(out, `mau-${process.argv[3] ?? "x"}.json`), JSON.stringify(rows, null, 1));
for (let i = 0; i < rows.length; i += 30)
  fs.writeFileSync(path.join(out, `lo-${String(i / 30 + 1).padStart(2, "0")}.json`), JSON.stringify(rows.slice(i, i + 30), null, 1));
console.log(`Tổng ${ids.length} câu chưa ẩn · lấy ${rows.length} câu → ${path.relative(process.cwd(), out)} (${Math.ceil(rows.length / 30)} lô)`);
