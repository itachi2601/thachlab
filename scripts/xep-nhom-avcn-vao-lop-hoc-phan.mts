// Xếp các em đã đăng ký qua link /dang-ky?lop=avcn vào lớp học phần AVCN (course_enrollments, status active).
// Trigger set_profile_track_cttc tự đổi profiles.track sang 'cttc'. Chạy lại an toàn (bỏ qua em đã có).
//   npx tsx scripts/xep-nhom-avcn-vao-lop-hoc-phan.mts AVCN-CK23A
import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";

const joinCode = process.argv[2];
if (!joinCode) throw new Error("Thiếu mã lớp học phần (AVCN-23A hoặc AVCN-CK23A)");
const env = Object.fromEntries(
  readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#")).map((l) => {
    const i = l.indexOf("=");
    return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^["']|["']$/g, "")];
  }),
);
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);

const { data: course } = await sb.from("course_offerings").select("id,name").eq("join_code", joinCode).single();
const { data: cls } = await sb.from("classes").select("id").eq("slug", "avcn").single();
const { data: ucs } = await sb.from("user_classes").select("user_id").eq("class_id", cls!.id);
const ids = (ucs ?? []).map((u) => u.user_id);
const { data: profs } = await sb.from("profiles").select("id").in("id", ids).eq("role", "student");
const { data: have } = await sb.from("course_enrollments").select("student_id").eq("course_id", course!.id);
const skip = new Set((have ?? []).map((h) => h.student_id));
const rows = (profs ?? []).filter((p) => !skip.has(p.id)).map((p) => ({ course_id: course!.id, student_id: p.id, status: "active", approved_at: new Date().toISOString() }));
if (rows.length) {
  const { error } = await sb.from("course_enrollments").insert(rows);
  if (error) throw error;
}
const { data: after } = await sb.from("course_enrollments").select("student_id,status").eq("course_id", course!.id).in("student_id", ids);
const { data: tr } = await sb.from("profiles").select("track").in("id", ids);
console.log(`${course!.name}: thêm ${rows.length} em; trong lớp học phần: ${after?.length}/${ids.length} (active: ${after?.filter((a) => a.status === "active").length}); track cttc: ${tr?.filter((t) => t.track === "cttc").length}/${ids.length}`);
