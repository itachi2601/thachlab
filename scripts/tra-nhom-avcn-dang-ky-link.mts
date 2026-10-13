// CHỈ ĐỌC: liệt kê em đăng ký qua link /dang-ky?lop=avcn (user_classes của lớp avcn) + đã có trong lớp học phần AVCN chưa.
//   npx tsx scripts/tra-nhom-avcn-dang-ky-link.mts
import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";

const env = Object.fromEntries(
  readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#")).map((l) => {
    const i = l.indexOf("=");
    return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^["']|["']$/g, "")];
  }),
);
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);

const { data: cls } = await sb.from("classes").select("id").eq("slug", "avcn").single();
const { data: ucs } = await sb.from("user_classes").select("user_id,status,requested_at").eq("class_id", cls!.id);
const ids = (ucs ?? []).map((u) => u.user_id);
const { data: profs } = await sb.from("profiles").select("id,full_name,class_name,student_code,track,role").in("id", ids);
const { data: offs } = await sb.from("course_offerings").select("id,name,join_code").in("join_code", ["AVCN-23A", "AVCN-CK23A"]);
const { data: enr } = await sb.from("course_enrollments").select("student_id,course_id,status").in("student_id", ids).in("course_id", (offs ?? []).map((o) => o.id));

console.log("Lớp học phần:", offs);
console.log(`Tổng ${ids.length} em trong user_classes của lớp avcn\n`);
for (const p of profs ?? []) {
  const e = (enr ?? []).filter((x) => x.student_id === p.id).map((x) => `${x.course_id}:${x.status}`).join(",") || "—";
  console.log([p.full_name, p.class_name || "", p.student_code || "", `track=${p.track ?? ""}`, `role=${p.role}`, `lớp học phần: ${e}`].join(" | "));
}
