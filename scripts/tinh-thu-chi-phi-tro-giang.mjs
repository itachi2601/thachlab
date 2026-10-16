// Chỉ đọc: so chi phí trợ giảng cách cũ vs cách mới từ phiếu công thô (ta_sessions).
// Chạy: node --env-file=.env.local scripts/tinh-thu-chi-phi-tro-giang.mjs
import { createClient } from "@supabase/supabase-js";
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, { auth: { persistSession: false } });
const { data: ses } = await sb.from("ta_sessions").select("assistant_id,work_date,session_type,hours,papers_graded,status,phudao_students,phudao_student_ids,policy,video_tier");
const RATE = 60000;
const n = s => Math.max(1, (s.phudao_student_ids?.length || 0) || (s.phudao_students?.length || 0));
const oldH = s => s.session_type === "lop" || s.session_type === "hanhchinh" ? +s.hours : s.session_type === "phudao" ? +s.hours * (1 + 0.1 * n(s)) : 0;
const newH = s => s.session_type === "lop" ? +s.hours : s.session_type === "phudao" ? +s.hours * (n(s) <= 2 ? 1.2 : 1.4) : 0;
const out = {};
for (const s of ses) {
  const m = s.work_date.slice(0, 7), k = m + "|" + s.status;
  const o = out[k] ??= { phieu: 0, lopH: 0, pdH: 0, hcH: 0, papers: 0, oldH: 0, newH: 0, video: 0 };
  o.phieu++; o.papers += s.papers_graded || 0; o.oldH += oldH(s); o.newH += newH(s);
  if (s.session_type === "lop") o.lopH += +s.hours; if (s.session_type === "phudao") o.pdH += +s.hours; if (s.session_type === "hanhchinh") o.hcH += +s.hours;
  if (s.session_type === "video") o.video++;
}
console.log("types", JSON.stringify(ses.reduce((a, s) => (a[s.session_type] = (a[s.session_type] || 0) + 1, a), {})));
for (const [k, o] of Object.entries(out).sort()) {
  const base = o.oldH * RATE, g = o.papers * 1500;
  console.log(k, JSON.stringify(o), "| CU nền", Math.round(base + g), "thưởng+0..4000/giờ", Math.round(o.oldH * 2000), Math.round(o.oldH * 4000), "| MOI (hệ số 1,0)", Math.round(o.newH * RATE + g), "(x0,9:", Math.round(0.9 * o.lopH * RATE + (o.newH - o.lopH) * RATE + g) + ")");
}
