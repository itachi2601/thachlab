// CHỈ ĐỌC: liệt kê mọi lớp học phần của môn avcn + sĩ số.
//   npx tsx scripts/tra-lop-hoc-phan-avcn.mts
import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
const env = Object.fromEntries(readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#")).map((l) => { const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^["']|["']$/g, "")]; }));
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);
const { data: s } = await sb.from("subjects").select("id").eq("code", "avcn").single();
const { data: offs } = await sb.from("course_offerings").select("id,name,class_label,school_year,join_code,enrollment_mode,status,created_at").eq("subject_id", s!.id).order("id");
for (const o of offs ?? []) {
  const { count } = await sb.from("course_enrollments").select("*", { count: "exact", head: true }).eq("course_id", o.id);
  console.log(JSON.stringify(o), `→ ${count} em`);
}
