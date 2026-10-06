// Gán khối (grade) cho các câu trong question_bank đang grade = '' dựa vào ĐỀ NGUỒN:
//   source_exam_id → lesson_items.exam_ids → lessons → chapters → chapter_classes → classes.slug
// (lop-10 → '10', lop-11 → '11', lop-12 → '12', khtn-9 → '9').
//
// Chỉ gán khi đề nguồn nằm trong các bài thuộc ĐÚNG MỘT khối. Đề nằm ở nhiều khối, không nằm trong
// bài nào, hoặc câu không có source_exam_id → BỎ QUA và in ra để thầy gắn tay. Không đoán bừa.
// Chỉ UPDATE cột grade của câu đang trống; không đụng câu đã có khối. Không gọi AI, không tốn tiền.
//
//   npx tsx scripts/backfill-question-bank-grade.mts            # DRY-RUN (mặc định): in bảng + ghi log, KHÔNG ghi DB
//   npx tsx scripts/backfill-question-bank-grade.mts --apply    # ghi thật các đề xác định được khối
//   npx tsx scripts/backfill-question-bank-grade.mts --undo scripts/logs/backfill-bank-grade-<...>.json
//
// Sau khi gán khối, chạy lại: npx tsx scripts/backfill-question-bank-topics.mts  (để gắn YCCĐ).
// Cần .env.local có NEXT_PUBLIC_SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const SLUG_TO_GRADE: Record<string, string> = { "lop-10": "10", "lop-11": "11", "lop-12": "12", "khtn-9": "9" };

function readEnvLocal(key: string): string | undefined {
  const envPath = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs.readFileSync(envPath, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}

function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}

const argv = process.argv.slice(2);
const apply = argv.includes("--apply");
const undoIdx = argv.indexOf("--undo");

const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY trong .env.local");
const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

async function fetchAll<T>(build: (from: number, to: number) => PromiseLike<{ data: T[] | null; error: { message: string } | null }>): Promise<T[]> {
  const out: T[] = [];
  for (let from = 0; ; from += 1000) {
    const { data, error } = await build(from, from + 999);
    if (error) fail(error.message);
    out.push(...(data ?? []));
    if (!data || data.length < 1000) break;
  }
  return out;
}

async function undo(file: string) {
  const log = JSON.parse(fs.readFileSync(file, "utf8")) as { assigned: { exam: number; grade: string; ids: number[] }[] };
  let n = 0;
  for (const g of log.assigned) {
    for (let i = 0; i < g.ids.length; i += 200) {
      const ids = g.ids.slice(i, i + 200);
      // Chỉ hoàn tác câu mà khối hiện tại vẫn đúng như lúc ghi (không đè lên câu thầy đã sửa tay).
      const { data, error } = await supabase.from("question_bank").update({ grade: "" }).in("id", ids).eq("grade", g.grade).select("id");
      if (error) fail(error.message);
      n += data?.length ?? 0;
    }
  }
  console.log(`Đã hoàn tác ${n} câu (grade → '').`);
}

async function main() {
  if (undoIdx >= 0) return undo(argv[undoIdx + 1] ?? fail("thiếu đường dẫn file log sau --undo"));

  const classes = await fetchAll<{ id: number; slug: string }>((a, b) => supabase.from("classes").select("id, slug").range(a, b));
  const classGrade = new Map<number, string>();
  for (const c of classes) if (SLUG_TO_GRADE[c.slug]) classGrade.set(c.id, SLUG_TO_GRADE[c.slug]);

  const chapterClasses = await fetchAll<{ chapter_id: number; class_id: number }>((a, b) => supabase.from("chapter_classes").select("chapter_id, class_id").range(a, b));
  const chapterGrades = new Map<number, Set<string>>();
  for (const cc of chapterClasses) {
    const g = classGrade.get(cc.class_id);
    if (!g) continue;
    (chapterGrades.get(cc.chapter_id) ?? chapterGrades.set(cc.chapter_id, new Set()).get(cc.chapter_id)!).add(g);
  }

  const lessons = await fetchAll<{ id: number; chapter_id: number }>((a, b) => supabase.from("lessons").select("id, chapter_id").range(a, b));
  const lessonChapter = new Map(lessons.map((l) => [l.id, l.chapter_id]));

  const items = await fetchAll<{ lesson_id: number; exam_ids: number[] | null }>((a, b) => supabase.from("lesson_items").select("lesson_id, exam_ids").range(a, b));
  const examGrades = new Map<number, Set<string>>();
  for (const it of items) {
    const ch = lessonChapter.get(it.lesson_id);
    const gs = ch != null ? chapterGrades.get(ch) : undefined;
    if (!gs) continue;
    for (const e of it.exam_ids ?? []) {
      const set = examGrades.get(e) ?? examGrades.set(e, new Set()).get(e)!;
      gs.forEach((g) => set.add(g));
    }
  }

  const rows = await fetchAll<{ id: number; source_exam_id: number | null }>((a, b) =>
    supabase.from("question_bank").select("id, source_exam_id").eq("grade", "").eq("archived", false).order("id").range(a, b),
  );
  console.log(`${rows.length} câu chưa có khối.\n`);

  const byExam = new Map<number | null, number[]>();
  for (const r of rows) (byExam.get(r.source_exam_id) ?? byExam.set(r.source_exam_id, []).get(r.source_exam_id)!).push(r.id);

  const assigned: { exam: number; grade: string; ids: number[] }[] = [];
  const ambiguous: { exam: number; grades: string[]; n: number }[] = [];
  const noLesson: { exam: number | null; n: number }[] = [];
  for (const [exam, ids] of byExam) {
    if (exam == null) { noLesson.push({ exam, n: ids.length }); continue; }
    const gs = examGrades.get(exam);
    if (!gs || gs.size === 0) noLesson.push({ exam, n: ids.length });
    else if (gs.size > 1) ambiguous.push({ exam, grades: [...gs].sort(), n: ids.length });
    else assigned.push({ exam, grade: [...gs][0], ids });
  }

  const sum = (a: { n?: number; ids?: number[] }[]) => a.reduce((s, x) => s + (x.n ?? x.ids?.length ?? 0), 0);
  const perGrade = new Map<string, { exams: number; q: number }>();
  for (const a of assigned) {
    const p = perGrade.get(a.grade) ?? { exams: 0, q: 0 };
    p.exams += 1; p.q += a.ids.length;
    perGrade.set(a.grade, p);
  }
  console.log("XÁC ĐỊNH ĐƯỢC KHỐI (đề nằm trong bài của đúng 1 khối):");
  for (const [g, p] of [...perGrade].sort()) console.log(`  lớp ${g}: ${p.exams} đề, ${p.q} câu`);
  console.log(`  → tổng ${assigned.length} đề, ${sum(assigned)} câu`);
  console.log(`\nĐỀ NẰM Ở NHIỀU KHỐI (bỏ qua): ${ambiguous.length} đề, ${sum(ambiguous)} câu`);
  ambiguous.slice(0, 15).forEach((a) => console.log(`  đề ${a.exam}: khối ${a.grades.join("+")} (${a.n} câu)`));
  console.log(`\nĐỀ KHÔNG NẰM TRONG BÀI NÀO / CÂU KHÔNG CÓ ĐỀ NGUỒN (bỏ qua): ${noLesson.length} nhóm, ${sum(noLesson)} câu`);
  noLesson.slice(0, 15).forEach((a) => console.log(`  đề ${a.exam ?? "(không có)"}: ${a.n} câu`));

  fs.mkdirSync(path.resolve(scriptDir, "logs"), { recursive: true });
  const logPath = path.resolve(scriptDir, "logs", `backfill-bank-grade-${new Date().toISOString().replace(/[:.]/g, "-")}${apply ? "" : "-dryrun"}.json`);

  if (apply) {
    let n = 0;
    for (const g of assigned) {
      for (let i = 0; i < g.ids.length; i += 200) {
        const { data, error } = await supabase.from("question_bank").update({ grade: g.grade }).in("id", g.ids.slice(i, i + 200)).eq("grade", "").select("id");
        if (error) fail(`đề ${g.exam}: ${error.message}`);
        n += data?.length ?? 0;
      }
    }
    console.log(`\nĐã ghi grade cho ${n} câu.`);
  } else {
    console.log("\n[DRY-RUN] chưa ghi DB. Rà bảng trên rồi chạy lại với --apply.");
  }
  fs.writeFileSync(logPath, JSON.stringify({ mode: apply ? "apply" : "dry-run", assigned, ambiguous, noLesson }, null, 1));
  console.log(`Log: ${path.relative(path.resolve(scriptDir, ".."), logPath)}`);
  if (apply) console.log(`Hoàn tác: npx tsx scripts/backfill-question-bank-grade.mts --undo ${path.relative(path.resolve(scriptDir, ".."), logPath)}`);
}

main().catch((e) => fail(e instanceof Error ? e.message : String(e)));
