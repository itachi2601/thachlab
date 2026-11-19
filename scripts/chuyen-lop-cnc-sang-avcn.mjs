// Chuyển MỘT lớp học phần lỡ tạo dưới môn CNC sang môn Anh văn chuyên ngành (avcn).
// Trang /quan-tri/cnc-mo-lop gắn cứng môn CNC nên lớp AVCN tạo ở đó bị nhầm môn.
// Mặc định chỉ xem (dry-run); thêm --apply để ghi. Không cần node_modules (dùng REST).
//   node scripts/chuyen-lop-cnc-sang-avcn.mjs CNC-C4476C AVCN-CGKL25A [--apply]
import { readFileSync } from "node:fs";

const [fromCode, toCode] = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const apply = process.argv.includes("--apply");
if (!fromCode || !toCode) { console.error("Cần: <mã cũ> <mã mới> [--apply]"); process.exit(1); }

const env = Object.fromEntries(readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#"))
  .map((l) => { const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^["']|["']$/g, "")]; }));
const base = `${env.NEXT_PUBLIC_SUPABASE_URL}/rest/v1`;
const key = env.SUPABASE_SERVICE_ROLE_KEY;
const h = { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" };
async function get(path) {
  const r = await fetch(`${base}/${path}`, { headers: { ...h, Prefer: "count=exact" } });
  if (!r.ok) throw new Error(`${path}: ${r.status} ${await r.text()}`);
  return { rows: await r.json(), count: Number((r.headers.get("content-range") ?? "/0").split("/")[1]) };
}

const { rows: [avcn] } = await get("subjects?code=eq.avcn&select=id,name");
const { rows: [off] } = await get(`course_offerings?join_code=eq.${encodeURIComponent(fromCode)}&select=*,subjects(code)`);
if (!avcn || !off) { console.error("Không thấy môn avcn hoặc lớp", fromCode); process.exit(1); }
console.log("Lớp:", JSON.stringify({ id: off.id, name: off.name, class_label: off.class_label, school_year: off.school_year, mon: off.subjects?.code }));
const { rows: dup } = await get(`course_offerings?join_code=eq.${encodeURIComponent(toCode)}&select=id`);
if (dup.length) { console.error("Mã mới đã có lớp khác dùng:", toCode); process.exit(1); }

let used = 0;
for (const t of ["course_enrollments", "attendance_sessions", "cnc_learning_records", "cnc_grades", "checklist_sessions", "exam_results", "lesson_progress"]) {
  const { count } = await get(`${t}?course_id=eq.${off.id}&select=course_id&limit=1`.replace("select=course_id", t === "attendance_sessions" || t === "checklist_sessions" || t === "exam_results" ? "select=id" : "select=course_id"));
  console.log(`  ${t}: ${count}`);
  if (t !== "course_enrollments") used += count;
}
if (used) { console.error("Lớp đã có dữ liệu CNC — dừng, cần thầy quyết."); process.exit(1); }

const patch = { subject_id: avcn.id, join_code: toCode, name: "CĐN CGKL 25A - Anh văn chuyên ngành Cơ khí" };
console.log(apply ? "GHI:" : "DRY-RUN, sẽ ghi:", JSON.stringify(patch));
if (!apply) process.exit(0);
const r = await fetch(`${base}/course_offerings?id=eq.${off.id}`, { method: "PATCH", headers: { ...h, Prefer: "return=representation" }, body: JSON.stringify(patch) });
if (!r.ok) throw new Error(`PATCH ${r.status} ${await r.text()}`);
console.log("Đã ghi:", JSON.stringify((await r.json()).map((o) => ({ id: o.id, name: o.name, join_code: o.join_code, subject_id: o.subject_id }))));
