// Sinh docs/DATABASE.md (bảng) + docs/DATABASE-RPC.md (hàm) từ schema thật, chỉ đọc.
// Chạy: node scripts/gen-database-doc.mjs   (cần supabase CLI đã `link`)
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const TABLES_SQL = `
select c.relname as t, coalesce(c.reltuples::bigint, 0) as n,
  string_agg(a.attname || ':' ||
    case format_type(a.atttypid, a.atttypmod)
      when 'timestamp with time zone' then 'ts' when 'timestamp without time zone' then 'ts'
      when 'character varying' then 'text' when 'boolean' then 'bool' when 'integer' then 'int'
      when 'bigint' then 'int8' when 'double precision' then 'float' when 'numeric' then 'num'
      else format_type(a.atttypid, a.atttypmod) end
    || case when exists (select 1 from pg_constraint k where k.conrelid = c.oid and k.contype = 'p' and a.attnum = any(k.conkey)) then '*' else '' end
    || coalesce((select '>' || cf.relname from pg_constraint k join pg_class cf on cf.oid = k.confrelid
                 where k.conrelid = c.oid and k.contype = 'f' and a.attnum = any(k.conkey) limit 1), ''),
    ', ' order by a.attnum) as cols
from pg_class c join pg_namespace n on n.oid = c.relnamespace
join pg_attribute a on a.attrelid = c.oid and a.attnum > 0 and not a.attisdropped
where n.nspname = 'public' and c.relkind in ('r', 'p')
group by c.relname, c.reltuples order by c.relname;`;

const RPC_SQL = `
select p.proname as f, pg_get_function_identity_arguments(p.oid) as a, pg_get_function_result(p.oid) as r
from pg_proc p join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public' and p.prokind = 'f' order by p.proname;`;

function query(sql) {
  const f = path.join(os.tmpdir(), `dbdoc-${process.pid}-${Math.random().toString(36).slice(2)}.sql`);
  fs.writeFileSync(f, sql);
  try {
    const out = execFileSync("supabase", ["db", "query", "--linked", "-f", f], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    return JSON.parse(out.slice(out.indexOf("{"), out.lastIndexOf("}") + 1)).rows;
  } finally {
    fs.unlinkSync(f);
  }
}

const GROUPS = [
  ["Tài khoản · lớp · khoá học", /^(profiles|user_classes|classes|class_|course_|parent_|staff_|password_|thpt_|academic_)/],
  ["Học liệu THPT: chương · bài · mục", /^(chapters?|chapter_|lessons?|lesson_|subjects?)/],
  ["Đề · câu hỏi · bài làm", /^(exams?|exam_|question_|practice_|rubric_|tutoring_exit|bug_report)/],
  ["Rank · huy hiệu", /^rank_/],
  ["Phụ đạo · thông báo · bài đăng", /^(tutoring_|student_alert|notification|messages|posts?|post_)/],
  ["CTTC: CNC · điểm danh · checklist · máy", /^(cnc_|attendance_|machine|checklist_|equipment_|homeroom_|student_learning)/],
  ["Trợ giảng", /^ta_/],
];

const tables = query(TABLES_SQL);
const rpcs = query(RPC_SQL);
const today = new Date().toISOString().slice(0, 10);
const buckets = new Map([...GROUPS.map(([g]) => [g, []]), ["Khác", []]]);
for (const t of tables) buckets.get((GROUPS.find(([, re]) => re.test(t.t)) ?? ["Khác"])[0]).push(t);

let md = `# Sơ đồ dữ liệu Supabase (schema public) — sinh tự động ${today}

Sinh bằng \`node scripts/gen-database-doc.mjs\` (chỉ đọc \`pg_class\`/\`pg_attribute\`). **Không sửa
tay** — chạy lại sau khi migration mới đã chạy trên production. Danh sách hàm/RPC ở
\`docs/DATABASE-RPC.md\` (tách riêng vì dài, chỉ mở khi cần tên hàm hoặc chữ ký tham số).

Ký hiệu: \`ten:kieu\` · \`*\` khoá chính · \`>bang\` khoá ngoại · \`(~n)\` số dòng ước lượng của planner
(−1 = chưa ANALYZE). ts = timestamptz, int8 = bigint, num = numeric.

Xương sống THPT: \`classes\` → \`chapters\` → \`lessons\` → \`lesson_items\` (lý thuyết / luyện tập /
kiểm tra / BTVN) → \`exams\` ↔ \`exam_attempts\` (bài làm) ↔ \`exam_question_results\` (từng câu).
Tài khoản: \`profiles\` (role, track THPT/CTTC, admin_area); ghi danh lớp: \`user_classes\`.
Xương sống CTTC: \`course_offerings\` → \`course_enrollments\`, điểm danh \`attendance_sessions\`.

`;
for (const [g, list] of buckets) {
  if (!list.length) continue;
  md += `## ${g} — ${list.length} bảng\n\n`;
  for (const t of list) md += `- **${t.t}** (~${t.n}): ${t.cols}\n`;
  md += "\n";
}
fs.writeFileSync("docs/DATABASE.md", md);

let rpcMd = `# Hàm SQL / RPC (schema public) — ${rpcs.length} hàm, sinh tự động ${today}

Sinh bằng \`node scripts/gen-database-doc.mjs\`. Gọi từ client bằng \`supabase.rpc("ten_ham", {...})\`.
Định nghĩa đầy đủ: grep tên hàm trong \`supabase/migrations/\` (hàm cũ hơn 9/2026 không có trong
repo — xem trên Supabase Dashboard).

`;
for (const r of rpcs) rpcMd += `- \`${r.f}(${r.a})\` → ${r.r}\n`;
fs.writeFileSync("docs/DATABASE-RPC.md", rpcMd);

console.log(`docs/DATABASE.md: ${tables.length} bảng, ${md.length} byte · docs/DATABASE-RPC.md: ${rpcs.length} hàm, ${rpcMd.length} byte`);
console.log("Khác:", buckets.get("Khác").map((t) => t.t).join(", ") || "(trống)");
