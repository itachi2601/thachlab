// Chỉ đọc: chi phí từng trợ giảng (cách cũ vs hiện tại, đơn giá 60k/65k). Chạy: node --env-file=.env.local scripts/tinh-thu-chi-phi-tro-giang-tung-em.mjs
import { createClient } from "@supabase/supabase-js";
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, { auth: { persistSession: false } });
const { data: tas } = await sb.from("ta_assistants").select("id,short_name");
const { data: ses } = await sb.from("ta_sessions").select("assistant_id,work_date,session_type,hours,papers_graded,status,phudao_students,phudao_student_ids");
const n = s => Math.max(1, (s.phudao_student_ids?.length || 0) || (s.phudao_students?.length || 0));
const oH = s => ["lop", "hanhchinh"].includes(s.session_type) ? +s.hours : s.session_type === "phudao" ? +s.hours * (1 + 0.1 * n(s)) : 0;
const nH = s => s.session_type === "lop" ? +s.hours : s.session_type === "phudao" ? +s.hours * (n(s) <= 2 ? 1.2 : 1.4) : 0;
for (const st of ["approved", "submitted"]) for (const t of tas) {
  const x = ses.filter(s => s.assistant_id === t.id && s.status === st); if (!x.length) continue;
  const f = k => x.filter(s => s.session_type === k).reduce((a, s) => a + +s.hours, 0);
  const oh = x.reduce((a, s) => a + oH(s), 0), nh = x.reduce((a, s) => a + nH(s), 0), p = x.reduce((a, s) => a + (s.papers_graded || 0), 0) * 1500;
  console.log([st, t.short_name, x.length, f("lop").toFixed(2), f("phudao").toFixed(2), p, Math.round(oh * 6e4 + p), Math.round(nh * 6e4 + p), Math.round(oh * 65e3 + p), Math.round(nh * 65e3 + p)].join("\t"));
}
