// Ghi mốc "lớp đang dạy tới bài" cho khoá Vật lí trên thachlab khi thầy báo tiến độ.
// Gọi RPC teaching_set (ghi thpt_teaching_progress + đồng bộ thpt_courses.current_topic_id) dưới danh nghĩa thầy
// qua `supabase db query --linked` (sandbox Bash chặn supabase.co → chạy trong tab terminal).
//
//   npx tsx .claude/skills/lich-tuan/scripts/ghi-moc-bai.mts --tim "sóng dừng"          # tìm id chủ đề tầng bài
//   npx tsx .claude/skills/lich-tuan/scripts/ghi-moc-bai.mts --khoa                       # liệt kê khoá + mốc hiện tại
//   npx tsx .claude/skills/lich-tuan/scripts/ghi-moc-bai.mts 4:46:2026-10-16 1:22:2026-10-13   # <course_id>:<topic_id>:<ngày dạy>
//   npx tsx .claude/skills/lich-tuan/scripts/ghi-moc-bai.mts --tro-giang [21]          # nội dung trợ giảng ghi ở phiếu buổi lớp (N ngày gần nhất)
//   thêm --email <email thầy> nếu không phải itachi2601@gmail.com
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const args = process.argv.slice(2);
const arg = (k: string) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : undefined; };
const email = (arg("--email") ?? "itachi2601@gmail.com").toLowerCase().replace(/'/g, "");

function runSql(sql: string) {
  const f = path.join(os.tmpdir(), `ghi-moc-bai-${Date.now()}.sql`);
  fs.writeFileSync(f, sql);
  try {
    const out = execFileSync("supabase", ["db", "query", "--linked", "-f", f], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    process.stdout.write(out);
  } finally { fs.unlinkSync(f); }
}

if (arg("--tim")) {
  const q = arg("--tim")!.replace(/'/g, "''");
  runSql(`select id, grade, name, sort_order from question_topics where parent_id is null and name ilike '%${q}%' order by grade, sort_order;`);
} else if (args.includes("--tro-giang")) {
  // Phiếu buổi lớp của trợ giảng có ô "Nội dung thầy đã dạy buổi hôm đó" (ta_sessions.policy->>'lesson_content').
  // Ghép buổi → khoá theo khối (class_id) + thứ trong tuần (thpt_course_schedules.weekday 1=T2…7=CN = isodow).
  // moi = true khi buổi sau lần tick "đã dạy" cuối của khoá → ứng viên để ghi mốc.
  const n = Number(arg("--tro-giang")) || 21;
  runSql(`select c.id as course_id, c.name as khoa, t.name as moc_hien_tai, s.work_date, a.short_name as tro_giang,
  s.work_date > coalesce((select max(p.taught_on) from thpt_teaching_progress p where p.course_id = c.id), date '2000-01-01') as moi,
  s.policy->>'lesson_content' as noi_dung
from ta_sessions s
join thpt_course_schedules sc on sc.weekday = extract(isodow from s.work_date)
join thpt_courses c on c.id = sc.course_id and c.class_id = s.class_id and c.status <> 'closed'
left join question_topics t on t.id = c.current_topic_id
left join ta_assistants a on a.id = s.assistant_id
where s.session_type = 'lop' and coalesce(btrim(s.policy->>'lesson_content'), '') <> ''
  and s.work_date >= current_date - ${n}
order by c.id, s.work_date;`);
} else if (args.includes("--khoa")) {
  runSql(`select c.id, c.name, c.current_topic_id, t.name as moc from thpt_courses c left join question_topics t on t.id = c.current_topic_id where c.status <> 'closed' order by c.id;`);
} else {
  const triples = args.filter((a) => /^\d+:\d+:\d{4}-\d{2}-\d{2}$/.test(a));
  if (!triples.length) { console.error("Cần ít nhất một bộ <course_id>:<topic_id>:<yyyy-mm-dd>, hoặc --tim/--khoa."); process.exit(1); }
  const calls = triples.map((t) => { const [c, p, d] = t.split(":"); return `select public.teaching_set(${c}, ${p}, true, '${d}');`; }).join("\n");
  runSql(`begin;
select set_config('request.jwt.claims', json_build_object('sub', (select id from auth.users where email = '${email}'), 'role', 'authenticated')::text, true);
${calls}
commit;
select c.id, c.name, c.current_topic_id, t.name as moc from thpt_courses c left join question_topics t on t.id = c.current_topic_id where c.status <> 'closed' order by c.id;`);
  console.log("Đã ghi. Chạy lại lich-tuan.mts --ghi để lịch tuần trên web cập nhật dòng 'Đã tới · Tiếp'.");
}
