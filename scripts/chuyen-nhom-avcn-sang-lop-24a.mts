// Tạo lớp học phần "AVCN 24A" (môn avcn), chuyển các em đang ở lớp 23A AVCN sang, rồi xoá 2 lớp 23A rỗng (nếu không còn dữ liệu tham chiếu).
//   npx tsx scripts/chuyen-nhom-avcn-sang-lop-24a.mts
import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
const env = Object.fromEntries(readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#")).map((l) => { const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^["']|["']$/g, "")]; }));
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);

const { data: s } = await sb.from("subjects").select("id").eq("code", "avcn").single();
let { data: c24 } = await sb.from("course_offerings").select("id,join_code").eq("subject_id", s!.id).eq("join_code", "AVCN-24A").maybeSingle();
if (!c24) {
  const { data, error } = await sb.from("course_offerings").insert({ subject_id: s!.id, name: "AVCN 24A - Tiếng Anh chuyên ngành", class_label: "AVCN 24A", school_year: "2026-2027", join_code: "AVCN-24A", enrollment_mode: "approval", status: "active" }).select("id,join_code").single();
  if (error) throw error;
  c24 = data;
}
const { data: old } = await sb.from("course_offerings").select("id").eq("subject_id", s!.id).in("join_code", ["AVCN-23A", "AVCN-CK23A"]);
const oldIds = (old ?? []).map((o) => o.id);
const { data: moved, error: e2 } = await sb.from("course_enrollments").update({ course_id: c24!.id }).in("course_id", oldIds).select("student_id");
if (e2) throw e2;
console.log(`Lớp AVCN 24A id=${c24!.id}: chuyển ${moved?.length ?? 0} em`);
for (const id of oldIds) {
  const { error } = await sb.from("course_offerings").delete().eq("id", id);
  console.log(`xoá lớp 23A id=${id}:`, error ? `GIỮ LẠI (${error.message})` : "đã xoá");
}
const { count } = await sb.from("course_enrollments").select("*", { count: "exact", head: true }).eq("course_id", c24!.id).eq("status", "active");
console.log(`AVCN 24A: ${count} em active, mã tham gia AVCN-24A`);
