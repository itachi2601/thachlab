// Chỉ đọc: phiếu công tháng 9 của từng trợ giảng trong hệ thống (để đối chiếu bảng lương Google Sheet).
import { createClient } from "@supabase/supabase-js";
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, { auth: { persistSession: false } });
const { data: tas } = await sb.from("ta_assistants").select("id,short_name");
const { data: ses } = await sb.from("ta_sessions").select("assistant_id,work_date,session_type,hours,status,phudao_students,phudao_student_ids").gte("work_date", "2026-09-01").lt("work_date", "2026-10-01");
const n = s => Math.max(1, (s.phudao_student_ids?.length || 0) || (s.phudao_students?.length || 0));
for (const t of tas) {
  const x = ses.filter(s => s.assistant_id === t.id); if (!x.length) { console.log(t.short_name, "0 phiếu"); continue; }
  const h = k => x.filter(s => s.session_type === k).reduce((a, s) => a + +s.hours, 0);
  const oh = x.reduce((a, s) => a + (s.session_type === "lop" ? +s.hours : s.session_type === "phudao" ? +s.hours * (1 + 0.1 * n(s)) : 0), 0);
  const nh = x.reduce((a, s) => a + (s.session_type === "lop" ? +s.hours : s.session_type === "phudao" ? +s.hours * (n(s) <= 2 ? 1.2 : 1.4) : 0), 0);
  console.log([t.short_name, x.length, "lop", h("lop"), "pd", h("phudao"), "tong", h("lop") + h("phudao"), "cu", oh.toFixed(2), "moi", nh.toFixed(2), x.map(s => s.work_date.slice(8) + s.status[0]).join(",")].join("\t"));
}
