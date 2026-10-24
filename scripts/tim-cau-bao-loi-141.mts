// Chỉ ĐỌC: tìm câu "điều kiện truyền nhiệt giữa hai vật" (báo lỗi #141, 24/10/2026) trong question_bank + lesson_items.
import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const needle = "điều kiện truyền nhiệt giữa hai vật";
const found: any[] = [];
for (let from = 0; ; from += 1000) {
  const { data, error } = await sb.from("question_bank").select("id,topic_name,difficulty,archived,question").eq("grade", "12").range(from, from + 999);
  if (error) { console.log(error.message); break; }
  if (!data?.length) break;
  for (const q of data) if (JSON.stringify(q.question).includes(needle)) found.push(q);
}
console.log("question_bank", found.length);
for (const q of found) console.log(JSON.stringify(q).slice(0, 2500));
const { data: li } = await sb.from("lesson_items").select("id,lesson_id,title,questions").eq("lesson_id", 3);
for (const it of li ?? []) {
  const s = JSON.stringify(it.questions ?? "");
  if (s.includes(needle)) console.log("lesson_item", it.id, it.title, "idx", (it.questions as any[]).findIndex((x) => JSON.stringify(x).includes(needle)));
}
