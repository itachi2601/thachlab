// Xuất câu CHƯA có lời giải (ngắn <80 ký tự), không ảnh, không thuộc nhóm đang chờ thầy duyệt (khop+ghi_chu) ra lô nhỏ cho agent giải MÙ (không kèm đáp án DB).
//   npx tsx scripts/xuat-giai-truc-tiep.mts [soCau/lo=75] [--anh]  → scripts/data/giai-lai/truc-tiep/lo-NN.json (+ dapan.json giữ đáp án DB)
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { plain, hasImg, dbAnswer } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const ANH = process.argv.includes("--anh");
const N = Number(process.argv.find((a) => /^\d+$/.test(a)) ?? 75);
const DIR = "scripts/data/giai-lai/truc-tiep" + (ANH ? "-anh" : "") + "/";
const k: any[] = JSON.parse(fs.readFileSync("scripts/data/giai-lai/ket-qua.json", "utf8"));
const cho = new Set(k.filter((x) => x.khop && x.ghi_chu).map((x) => x.id));
let all: any[] = [];
for (let f = 0; ; f += 1000) {
  const { data, error } = await sb.from("question_bank").select("id,grade,topic_name,question,archived").eq("archived", false).order("id").range(f, f + 999);
  if (error) throw error; all = all.concat(data!); if (data!.length < 1000) break;
}
const rows = all.filter((r) => plain(r.question?.explanation ?? "").length < 80 && hasImg(r.question) === ANH && !cho.has(r.id));
fs.mkdirSync(DIR, { recursive: true });
const dapan: Record<number, any> = {};
const out = rows.map((r) => { const q = r.question; dapan[r.id] = dbAnswer(q);
  return { id: r.id, lop: r.grade, chu_de: r.topic_name, loai: q.type, de: q.question, phuong_an: q.options ?? undefined, cac_y: q.statements?.map((s: any) => s.text) };
});
fs.writeFileSync(DIR + "dapan.json", JSON.stringify(dapan));
for (let i = 0; i < out.length; i += N) fs.writeFileSync(`${DIR}lo-${String(i / N + 1).padStart(2, "0")}.json`, JSON.stringify(out.slice(i, i + N)));
console.log(`${out.length} câu → ${Math.ceil(out.length / N)} lô tại ${DIR}`);
