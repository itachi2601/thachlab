// Gán lớp (exam_classes) cho đề published chưa có dòng nào — hiện visibleTo() coi đó là "toàn trường".
//   npx tsx scripts/gan-lop-de-chua-gan.mts            # DRY-RUN: bảng đếm theo lớp + 20 mẫu mỗi nhóm + danh sách không suy được
//   npx tsx scripts/gan-lop-de-chua-gan.mts --apply    # sao lưu JSON ra scripts/logs/ rồi chèn exam_classes, đọc lại đối chiếu
// Suy lớp theo thứ tự: (1) bài học chứa đề (lesson_items.exam_ids → lessons.chapter_id → chapter_classes)
// (2) tiêu đề (gradeFromExamTitle) (3) subject_code khtn* → lớp 15 (19 nếu tiêu đề nói HSG/chuyên). Không suy được → KHÔNG gán.
// Đề suy ra nhiều lớp từ bài học (chương gán nhiều lớp) chỉ nhận lớp khớp khối tiêu đề nếu có, ngược lại nhận tất cả lớp của chương.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { gradeFromExamTitle } from "../features/exams/exam-grade";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function env(key: string): string | undefined {
  const line = fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const GRADE_CLASS: Record<string, number> = { "9": 15, "10": 16, "11": 17, "12": 18 };
const CLASS_NAME: Record<number, string> = { 15: "KHTN 9", 16: "Lớp 10", 17: "Lớp 11", 18: "Lớp 12", 19: "HSG 9", 20: "AVCN" };

async function all<T>(build: (from: number, to: number) => PromiseLike<{ data: T[] | null; error: any }>): Promise<T[]> {
  const out: T[] = [];
  for (let from = 0; ; from += 1000) {
    const { data, error } = await build(from, from + 999);
    if (error) throw new Error(error.message);
    out.push(...(data ?? []));
    if (!data || data.length < 1000) return out;
  }
}

const UNDO = process.argv.includes("--undo") ? process.argv[process.argv.indexOf("--undo") + 1] : null;
if (UNDO) {
  const { inserted } = JSON.parse(fs.readFileSync(UNDO, "utf8")) as { inserted: { exam_id: number; class_id: number }[] };
  for (const r of inserted) {
    const { error } = await sb.from("exam_classes").delete().eq("exam_id", r.exam_id).eq("class_id", r.class_id);
    if (error) { console.error(error.message); process.exit(1); }
  }
  console.log(`Đã xoá ${inserted.length} dòng exam_classes theo ${UNDO}`);
  process.exit(0);
}

const exams = await all<any>((a, b) => sb.from("exams").select("id,title,subject_code").eq("published", true).order("id").range(a, b));
const ec = await all<any>((a, b) => sb.from("exam_classes").select("exam_id,class_id").order("exam_id").range(a, b));
const assigned = new Set(ec.map((r) => r.exam_id));
const todo = exams.filter((e) => !assigned.has(e.id));
const items = await all<any>((a, b) => sb.from("lesson_items").select("id,lesson_id,exam_ids").not("exam_ids", "is", null).order("id").range(a, b));
const lessons = await all<any>((a, b) => sb.from("lessons").select("id,chapter_id").order("id").range(a, b));
const cc = await all<any>((a, b) => sb.from("chapter_classes").select("chapter_id,class_id").range(a, b));

const chapterOfLesson = new Map(lessons.map((l) => [l.id, l.chapter_id]));
const classesOfChapter = new Map<number, Set<number>>();
for (const r of cc) (classesOfChapter.get(r.chapter_id) ?? classesOfChapter.set(r.chapter_id, new Set()).get(r.chapter_id)!).add(r.class_id);
const classesByExamLesson = new Map<number, Set<number>>();
for (const it of items) {
  const set = classesOfChapter.get(chapterOfLesson.get(it.lesson_id) as number);
  if (!set) continue;
  for (const eid of it.exam_ids as number[]) {
    const s = classesByExamLesson.get(eid) ?? classesByExamLesson.set(eid, new Set()).get(eid)!;
    set.forEach((c) => s.add(c));
  }
}

type Row = { id: number; title: string; subject: string | null; rule: string; classes: number[] };
const plan: Row[] = [];
const unknown: any[] = [];
for (const e of todo) {
  const title: string = e.title ?? "";
  const g = gradeFromExamTitle(title);
  const hsg = /hsg|chuyên|chuyen|olympic/i.test(title);
  const lessonClasses = classesByExamLesson.get(e.id);
  let classes: number[] = [];
  let rule = "";
  if (lessonClasses && lessonClasses.size) {
    let cs = [...lessonClasses];
    if (g && cs.length > 1 && cs.includes(GRADE_CLASS[g])) cs = [GRADE_CLASS[g]];
    if (/^hsg/i.test(e.subject_code ?? "")) cs = [19];
    // bài học và tiêu đề mâu thuẫn (vd. đề "– 11 –" nằm trong bài lớp 10) → không tự gán, để thầy duyệt
    if (g && !cs.includes(GRADE_CLASS[g]) && !cs.includes(19)) { unknown.push({ id: e.id, title, subject_code: e.subject_code, lech: `bài học → lớp ${cs.join("+")} nhưng tiêu đề nói khối ${g}` }); continue; }
    classes = cs; rule = "1-bai-hoc";
  } else if (g) {
    classes = [hsg && g === "9" ? 19 : GRADE_CLASS[g]]; rule = "2-tieu-de";
  } else if (e.subject_code === "avcn") {
    // Lớp AVCN vào tự do, đề KHÔNG gán lớp (migration 20261013180000; gỡ lại ngày 17/10 bằng go-gan-lop-de-avcn.mts) → bỏ qua.
    continue;
  } else if (/^khtn/i.test(e.subject_code ?? "")) {
    classes = [hsg ? 19 : 15]; rule = "3-subject-khtn";
  }
  if (classes.length) plan.push({ id: e.id, title, subject: e.subject_code, rule, classes });
  else unknown.push({ id: e.id, title, subject_code: e.subject_code });
}

console.log(`Đề published: ${exams.length}; chưa gán lớp: ${todo.length}; suy được: ${plan.length}; KHÔNG suy được: ${unknown.length}`);
const groups = new Map<string, Row[]>();
for (const r of plan) {
  const k = `${r.rule} → ${r.classes.map((c) => `${c} ${CLASS_NAME[c] ?? "?"}`).join("+")}`;
  (groups.get(k) ?? groups.set(k, []).get(k)!).push(r);
}
console.log("\n=== Đếm theo nhóm ===");
for (const [k, v] of [...groups].sort()) console.log(String(v.length).padStart(5), k);
console.log("\n=== Đếm theo lớp ===");
const byClass = new Map<number, number>();
for (const r of plan) for (const c of r.classes) byClass.set(c, (byClass.get(c) ?? 0) + 1);
for (const [c, n] of [...byClass].sort()) console.log(String(n).padStart(5), c, CLASS_NAME[c] ?? "?");
for (const [k, v] of [...groups].sort()) {
  console.log(`\n--- mẫu ${k} (${v.length}) ---`);
  v.slice(0, 20).forEach((r) => console.log(`  #${r.id} [${r.subject}] ${r.title}`));
}
const noTitle = plan.filter((r) => r.rule === "1-bai-hoc" && !gradeFromExamTitle(r.title));
console.log(`\n=== 10 đề ngẫu nhiên chỉ dựa vào bài học (tiêu đề không nói khối; ${noTitle.length} đề) — đối chiếu tay ===`);
[...noTitle].sort(() => Math.random() - 0.5).slice(0, 10).forEach((r) => console.log(`  #${r.id} ${r.title} → ${r.classes.map((c) => CLASS_NAME[c]).join("+")}`));
console.log(`\n=== KHÔNG suy được (${unknown.length}) — KHÔNG gán, chờ thầy duyệt ===`);
unknown.forEach((u) => console.log(`  #${u.id} [${u.subject_code}] ${u.title}`));
fs.mkdirSync(path.join(scriptDir, "logs"), { recursive: true });
const stamp = new Date().toISOString().replace(/[:.]/g, "-");
const unkFile = path.join(scriptDir, "logs", `gan-lop-de-khong-suy-duoc-${stamp}.json`);
fs.writeFileSync(unkFile, JSON.stringify(unknown, null, 1));
console.log(`\nDanh sách không suy được: ${unkFile}`);

if (!APPLY) { console.log("\nDRY-RUN — chưa ghi gì. Thêm --apply để chèn."); process.exit(0); }

const rows = plan.flatMap((r) => r.classes.map((c) => ({ exam_id: r.id, class_id: c })));
const bak = path.join(scriptDir, "logs", `gan-lop-de-${stamp}.json`);
fs.writeFileSync(bak, JSON.stringify({ inserted: rows, exam_classes_before_count: ec.length }, null, 1));
for (let i = 0; i < rows.length; i += 10) {
  let error: any;
  for (let t = 0; t < 4; t++) {
    ({ error } = await sb.from("exam_classes").insert(rows.slice(i, i + 10)));
    if (!error) break;
    await new Promise((r) => setTimeout(r, 3000));
  }
  if (error) { console.error("LỖI chèn:", error.message, "— đã chèn tới", i, "dòng; chạy lại script sẽ gán tiếp phần còn thiếu"); break; }
}
const after = await all<any>((a, b) => sb.from("exam_classes").select("exam_id,class_id").order("exam_id").range(a, b));
console.log(`exam_classes: ${ec.length} → ${after.length} (kỳ vọng ${ec.length + rows.length})`);
console.log(`Hoàn tác: npx tsx scripts/gan-lop-de-chua-gan.mts --undo ${bak}`);
