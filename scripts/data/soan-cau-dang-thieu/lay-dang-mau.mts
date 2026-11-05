// Lấy bài tập mẫu + chủ đề YCCĐ + câu chắc đã có của các dạng lý thuyết thiếu câu
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const root = "/Users/MAC/Projects/thachlab";
const env = (k: string) => fs.readFileSync(root + "/.env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const want: [number, number][] = [[2,1],[2,2],[3,1],[6,1],[10,1],[10,2],[127,1],[15,2],[17,1],[25,1],[28,1],[30,3],[41,1],[42,2],[46,1],[46,3],[47,1],[47,2],[68,1],[74,3],[76,1],[77,1],[78,1],[161,2],[150,2],[152,1]];
const lids = [...new Set(want.map((w) => w[0]))];
const out: any = {};
const strip = (t: string) => t.replace(/<svg[\s\S]*?<\/svg>/g, "[HÌNH]").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").slice(0, 2500);
const { data: les } = await sb.from("lessons").select("id,title,chapter_id").in("id", lids);
const { data: items, error } = await sb.from("lesson_items").select("lesson_id,kind,questions").in("lesson_id", lids).eq("kind", "bai_tap_mau");
if (error) throw error;
const { data: tops } = await sb.from("question_topics").select("id,name,lesson_id,grade,parent_id").in("lesson_id", lids);
const { data: qd } = await sb.from("question_dang").select("question_id,lesson_id,dang_label,unsure").in("lesson_id", lids);
for (const [lid, dn] of want) {
  const l = les!.find((x) => x.id === lid);
  const it = items!.filter((x) => x.lesson_id === lid);
  const qs: any[] = it.flatMap((x) => (Array.isArray(x.questions) ? x.questions : []));
  const dang = qs.filter((q) => new RegExp(`^\\s*Dạng\\s*${dn}\\b`).test(String(q.label ?? "")) );
  const existing = (qd ?? []).filter((d) => d.lesson_id === lid && new RegExp(`^\\s*Dạng\\s*${dn}\\b`).test(d.dang_label));
  let exQ: any[] = [];
  if (existing.length) {
    const { data } = await sb.from("question_bank").select("id,topic_id,topic_name,grade,qtype,question").in("id", existing.map((e) => e.question_id));
    exQ = (data ?? []).map((q) => ({ ...q, unsure: existing.find((e) => e.question_id === q.id)?.unsure }));
  }
  out[`${lid}-${dn}`] = { lesson: l, topics: (tops ?? []).filter((t) => t.lesson_id === lid), dangItems: dang.map((q) => Object.fromEntries(Object.entries(q).map(([k, v]) => [k, typeof v === "string" ? strip(v) : strip(JSON.stringify(v))]))), existing: exQ, labels: [...new Set(existing.map((e) => e.dang_label))] };
}
fs.writeFileSync(process.argv[2], JSON.stringify(out, null, 1));
console.log("xong", Object.keys(out).length);
