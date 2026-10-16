// Chỉ đọc: liệt kê lesson_items của các bài HSG9 (kind, độ dài body, số dạng, exam_ids + số câu đề, published).
//   node scripts/kiem-muc-bai-hsg9.mjs 164 153
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = Object.fromEntries(fs.readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=")).map((l) => [l.slice(0, l.indexOf("=")), l.slice(l.indexOf("=") + 1).trim()]));
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);
for (const id of process.argv.slice(2).map(Number)) {
  const { data: ls } = await sb.from("lessons").select("id,title,published").eq("id", id).single();
  console.log(`\nBài ${id} "${ls?.title}" published=${ls?.published}`);
  const { data: items } = await sb.from("lesson_items").select("id,kind,title,body_html,questions,exam_ids").eq("lesson_id", id).order("sort_order");
  for (const it of items ?? []) {
    let ex = "";
    if (it.exam_ids?.length) {
      const { data: es } = await sb.from("exams").select("id,question_count,questions,published,subject_code").in("id", it.exam_ids);
      ex = es.map((e) => `đề ${e.id}: ${e.questions?.length ?? e.question_count} câu, published=${e.published}, ${e.subject_code}`).join("; ");
    }
    console.log(`  #${it.id} ${it.kind} · body ${it.body_html?.length ?? 0} ký tự · ${Array.isArray(it.questions) ? it.questions.length : 0} dạng · ${ex}`);
  }
}
