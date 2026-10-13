// Ghi danh (active) các em báo lỗi #99–#102 xin chuyển sang lớp học phần AVCN 24A.
//   npx tsx scripts/ghi-danh-bao-loi-avcn-24a.mts
import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
const env = Object.fromEntries(readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#")).map((l) => { const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^["']|["']$/g, "")]; }));
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);
const { data: c } = await sb.from("course_offerings").select("id").eq("join_code", "AVCN-24A").single();
const { data: bugs } = await sb.from("bug_reports").select("id,user_id").in("id", [99, 100, 101, 102]);
const now = new Date().toISOString();
for (const b of bugs ?? []) {
  const { error } = await sb.from("course_enrollments").upsert({ course_id: c!.id, student_id: b.user_id, status: "active", approved_at: now }, { onConflict: "course_id,student_id" });
  console.log(`#${b.id} ${b.user_id}:`, error ? error.message : "đã ghi danh");
}
const { data: chk } = await sb.from("course_enrollments").select("student_id,status").eq("course_id", c!.id).in("student_id", (bugs ?? []).map((b) => b.user_id));
console.log("kiểm lại:", chk);
