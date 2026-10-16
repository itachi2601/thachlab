// Chỉ đọc: giờ tháng 10 từng trợ giảng theo loại, số em phụ đạo, tuần (để dự phóng). Chạy: node --env-file=.env.local scripts/tinh-thu-chi-phi-tro-giang-thang10.mjs
import { createClient } from "@supabase/supabase-js";
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, { auth: { persistSession: false } });
const { data: tas } = await sb.from("ta_assistants").select("id,short_name");
const { data: ses } = await sb.from("ta_sessions").select("assistant_id,work_date,session_type,hours,papers_graded,status,phudao_students,phudao_student_ids,policy").gte("work_date", "2026-10-01").order("work_date");
const name = Object.fromEntries(tas.map(t => [t.id, t.short_name]));
for (const s of ses) {
  const n = Math.max(1, (s.phudao_student_ids?.length || 0) || (s.phudao_students?.length || 0));
  console.log([s.work_date, new Date(s.work_date).getUTCDay(), name[s.assistant_id], s.status, s.session_type, s.hours, s.session_type === "phudao" ? n : "", s.papers_graded || "", s.policy?.teaching_minutes || "", s.policy?.attendance || ""].join("\t"));
}
