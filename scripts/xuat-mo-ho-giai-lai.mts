// Xuất 1.070 câu "khớp nhưng Haiku ghi chú mơ hồ" ra các lô nhỏ để agent Sonnet soát (không cần mạng DB).
//   npx tsx scripts/xuat-mo-ho-giai-lai.mts [soCau/lo=100] → scripts/data/giai-lai/mo-ho/lo-NN.json
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const DIR = "scripts/data/giai-lai/";
const N = Number(process.argv[2] ?? 100);
const k: any[] = JSON.parse(fs.readFileSync(DIR + "ket-qua.json", "utf8"));
const m = k.filter((x) => x.khop && x.ghi_chu && !x.katex_loi && !x.mui_ten_con);
const qs = new Map<number, any>();
for (let i = 0; i < m.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,grade,topic_name,question,archived").in("id", m.slice(i, i + 200).map((x) => x.id));
  if (error) throw new Error(error.message);
  data!.forEach((r) => qs.set(r.id, r));
}
const rows = m.filter((x) => !qs.get(x.id)?.archived).map((x) => {
  const q = qs.get(x.id);
  return { id: x.id, lop: q?.grade, chu_de: q?.topic_name, cau_hoi: q?.question, dap_an_db: x.db, loi_giai_cu: q?.question?.explanation ?? "", ghi_chu_haiku: x.ghi_chu, loi_giai_moi: x.explanation };
});
fs.mkdirSync(DIR + "mo-ho", { recursive: true });
for (let i = 0; i < rows.length; i += N) fs.writeFileSync(`${DIR}mo-ho/lo-${String(i / N + 1).padStart(2, "0")}.json`, JSON.stringify(rows.slice(i, i + N)));
console.log(`Đã xuất ${rows.length} câu → ${Math.ceil(rows.length / N)} lô tại ${DIR}mo-ho/`);
