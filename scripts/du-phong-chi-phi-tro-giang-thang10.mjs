// Chỉ đọc: giờ T9 và T10 (đến hôm nay) theo trợ giảng/loại/số em phụ đạo, đơn giá — để dự phóng chi phí T10. Chạy: node --env-file=.env.local scripts/du-phong-chi-phi-tro-giang-thang10.mjs
import { createClient } from "@supabase/supabase-js";
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, { auth: { persistSession: false } });
const { data: tas } = await sb.from("ta_assistants").select("*");
const { data: rates } = await sb.from("ta_rates").select("*");
console.log("RATES", JSON.stringify(rates));
const { data: ses } = await sb.from("ta_sessions").select("assistant_id,work_date,session_type,hours,papers_graded,status,phudao_students,phudao_student_ids,policy").gte("work_date", "2026-09-01").order("work_date");
const n = s => Math.max(1, (s.phudao_student_ids?.length || 0) || (s.phudao_students?.length || 0));
for (const t of tas) {
  console.log("TA", t.short_name, "tier", t.tier, "retained", t.retained_rate);
  for (const [lbl, a, b] of [["T9", "2026-09-01", "2026-10-01"], ["T10", "2026-10-01", "2026-11-01"]]) {
    const x = ses.filter(s => s.assistant_id === t.id && s.work_date >= a && s.work_date < b);
    if (!x.length) continue;
    const agg = {};
    for (const s of x) {
      const k = [s.status, s.session_type, s.session_type === "phudao" ? "n" + n(s) : ""].join("|");
      agg[k] = agg[k] || { h: 0, c: 0, p: 0, tm: 0 };
      agg[k].h += +s.hours; agg[k].c++; agg[k].p += s.papers_graded || 0; agg[k].tm += +(s.policy?.teaching_minutes || 0);
    }
    for (const [k, v] of Object.entries(agg)) console.log(" ", lbl, k, "gio", v.h, "buoi", v.c, "bai", v.p, "phut_chua", v.tm);
  }
}
