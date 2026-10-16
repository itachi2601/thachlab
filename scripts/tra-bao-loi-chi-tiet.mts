import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const cut = (x: unknown, n = 400) => JSON.stringify(x)?.slice(0, n);
const { data: ex } = await sb.from("exams").select("id,title,published,question_count,questions").in("id", [917, 918, 929]);
for (const e of ex ?? []) {
  console.log("== exam", e.id, e.title, "pub", e.published, "n", e.question_count);
  const qs = (e.questions as any[]) ?? [];
  const pick = e.id === 929 ? [6] : e.id === 918 ? [10] : [];
  for (const i of pick) console.log("  q", i + 1, cut(qs[i], 900));
  if (e.id === 917) qs.forEach((q, i) => { const img = JSON.stringify(q).match(/https?:[^"\\ ]+\.(?:png|jpe?g|webp|svg)/g); if (img) console.log("  q", i + 1, "img", img.join(" "), "|", String(q.question ?? q.text ?? "").slice(0, 120)); });
}
const { data: bugs } = await sb.from("bug_reports").select("id,user_id,created_at").in("id", [107, 112, 110, 111, 113]);
for (const b of bugs ?? []) {
  const { data: p } = await sb.from("profiles").select("full_name,class_id,role").eq("id", b.user_id).maybeSingle();
  const { data: r } = await sb.from("exam_results").select("id,exam_id,score,created_at").eq("student_id", b.user_id).order("created_at", { ascending: false }).limit(3);
  const { data: a } = await sb.from("exam_attempts").select("id,exam_id,item_id,submitted_at,exam_result_id,started_at").eq("student_id", b.user_id).order("started_at", { ascending: false }).limit(3);
  console.log("== bug", b.id, b.created_at, cut(p, 120), "\n  results", cut(r, 400), "\n  attempts", cut(a, 500));
}
