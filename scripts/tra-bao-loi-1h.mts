// CHỈ ĐỌC: báo lỗi trong N giờ gần đây (mặc định 1) + hồ sơ người báo + lớp học phần AVCN đang ghi danh.
//   npx tsx scripts/tra-bao-loi-1h.mts [giờ]
import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
const env = Object.fromEntries(readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#")).map((l) => { const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^["']|["']$/g, "")]; }));
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);
const h = Number(process.argv[2] ?? 1);
const since = new Date(Date.now() - h * 3600e3).toISOString();
const { data: bugs, error } = await sb.from("bug_reports").select("id,created_at,user_id,reporter_name,reporter_email,page_url,category,description,status").gte("created_at", since).order("created_at");
if (error) throw error;
const ids = [...new Set((bugs ?? []).map((b) => b.user_id).filter(Boolean))];
const { data: profs } = await sb.from("profiles").select("id,full_name,class_name,student_code,role,track").in("id", ids);
const { data: enr } = await sb.from("course_enrollments").select("student_id,course_id,status").in("student_id", ids);
const { data: offs } = await sb.from("course_offerings").select("id,join_code");
for (const b of bugs ?? []) {
  const p = (profs ?? []).find((x) => x.id === b.user_id);
  const e = (enr ?? []).filter((x) => x.student_id === b.user_id).map((x) => `${offs?.find((o) => o.id === x.course_id)?.join_code ?? x.course_id}:${x.status}`).join(",") || "—";
  console.log(`#${b.id} ${b.created_at} [${b.status}] ${b.category} ${b.page_url}\n  ${b.reporter_name} <${b.reporter_email}> uid=${b.user_id}\n  profile=${p ? [p.full_name, p.class_name, p.student_code, p.role, p.track].join(" | ") : "—"} | ghi danh: ${e}\n  ${String(b.description).slice(0, 300)}\n`);
}
console.log(`Tổng ${bugs?.length ?? 0} báo lỗi từ ${since}`);
