// Đăng bộ câu "Kiểm tra nhanh" lý thuyết (scripts/data/theory-quiz/<lesson_id>.json, do skill
// soan-quiz-ly-thuyet sinh) lên DB: tạo `exams` rồi gắn exam_ids + quiz_min_correct vào mục ly_thuyet.
// CHẠY TRÊN MAC (cần service role). --dry-run không cần key, không ghi gì.
//
//   npx tsx scripts/publish-theory-quiz.mts --lesson 3 --lesson 6 [--replace] [--dry-run]
//   npx tsx scripts/publish-theory-quiz.mts --all [--replace] [--dry-run]
//
// Site export tĩnh: đăng xong phải `bash scripts/deploy.sh` (build-content chạy ở prebuild) mới thấy trên web.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import { loadTopics, QUIZ_DIR, quizFilesIn, validateQuiz, KEY } from "../.claude/skills/soan-quiz-ly-thuyet/scripts/lib";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
function askHidden(q: string): Promise<string> {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const a = rl as unknown as { _writeToOutput: (c: string) => void; stdoutMuted: boolean };
    a._writeToOutput = (c) => (rl as unknown as { output: NodeJS.WritableStream }).output.write(a.stdoutMuted ? "*" : c);
    a.stdoutMuted = false;
    rl.question(q, (v) => { rl.close(); process.stdout.write("\n"); resolve(v.trim()); });
    a.stdoutMuted = true;
  });
}
function fail(m: string): never { console.error("Lỗi:", m); process.exit(1); }

const argv = process.argv.slice(2);
const lessons: number[] = [];
let all = false, dryRun = false, replace = false;
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === "--lesson") lessons.push(Number(argv[++i]));
  else if (argv[i] === "--all") all = true;
  else if (argv[i] === "--dry-run") dryRun = true;
  else if (argv[i] === "--replace") replace = true;
  else fail(`tham số lạ: ${argv[i]}`);
}
if (!all && lessons.length === 0) fail("cần --lesson <id> (lặp được) hoặc --all");
if (lessons.some((n) => !Number.isInteger(n))) fail("--lesson cần số nguyên");

const files = all
  ? quizFilesIn(QUIZ_DIR)
  : lessons.map((id) => path.join(QUIZ_DIR, `${id}.json`));
for (const f of files) if (!fs.existsSync(f)) fail(`không thấy ${path.relative(process.cwd(), f)}`);

const topics = loadTopics();
if (!topics) console.warn("Cảnh báo: chưa có scripts/data/question-topics.json — không kiểm topic theo YCCĐ (chạy export-question-topics.mts trước).");

interface Quiz { lesson_id: number; lesson_title: string; item_id: number; quiz_min_correct: number; questions: Record<string, unknown>[] }
const quizzes: Quiz[] = [];
let bad = false;
for (const f of files) {
  const data = JSON.parse(fs.readFileSync(f, "utf8"));
  const { errors, warnings } = validateQuiz(data, { topics });
  warnings.forEach((w) => console.warn(`  ! ${path.basename(f)}: ${w}`));
  if (errors.length) { bad = true; console.error(`✗ ${path.basename(f)}:\n   - ${errors.join("\n   - ")}`); }
  else quizzes.push(data);
}
if (bad) fail("có file không qua validate — dừng, chưa ghi gì.");

const stripKind = (qs: Record<string, unknown>[]) => qs.map(({ kind: _k, ...rest }) => rest);
const typeCounts = (qs: Record<string, unknown>[]) => {
  const c: Record<string, number> = {};
  for (const q of qs) c[q.type as string] = (c[q.type as string] ?? 0) + 1;
  return c;
};

let supabase: ReturnType<typeof createClient> | null = null;
if (!dryRun) {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY") ?? (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
  if (!key) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");
  supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
} else {
  console.log("[DRY-RUN] không kết nối DB. Mục đã có exam_ids chỉ kiểm được khi chạy thật (dry-run đọc public/data).\n");
}

// subject_code theo chương (dry-run: đọc catalog.json; chạy thật: đọc DB).
const catalog = JSON.parse(fs.readFileSync(path.resolve(scriptDir, "../public/data/catalog.json"), "utf8"));
function subjectFromCatalog(lessonId: number): string {
  const l = catalog.lessons.find((x: { id: number }) => x.id === lessonId);
  const ch = catalog.chapters.find((x: { id: number }) => x.id === l?.chapter_id);
  return ch?.subjectCode ?? "vat-ly";
}

const summary: string[] = [];
for (const qz of quizzes) {
  const n = qz.questions.length;
  const title = `Kiểm tra nhanh — ${qz.lesson_title}`;
  console.log(`\n=== Bài ${qz.lesson_id}: ${qz.lesson_title}`);

  let itemId: number;
  let oldExamIds: number[];
  let subject = subjectFromCatalog(qz.lesson_id);
  if (supabase) {
    const { data: items, error } = await supabase.from("lesson_items").select("id, exam_ids").eq("lesson_id", qz.lesson_id).eq("kind", "ly_thuyet");
    if (error) fail(`đọc lesson_items bài ${qz.lesson_id}: ${error.message}`);
    const rows = (items ?? []) as unknown as { id: number; exam_ids: number[] | null }[];
    if (rows.length !== 1) fail(`bài ${qz.lesson_id} có ${rows.length} mục ly_thuyet trong DB (cần đúng 1)`);
    if (rows[0].id !== qz.item_id) fail(`bài ${qz.lesson_id}: item_id trong file (${qz.item_id}) lệch DB (${rows[0].id}) — nội dung/đoạn có thể đã đổi, soạn lại.`);
    itemId = rows[0].id;
    oldExamIds = rows[0].exam_ids ?? [];
    const { data: les } = await supabase.from("lessons").select("chapter_id").eq("id", qz.lesson_id).single();
    const chapterId = (les as { chapter_id?: number } | null)?.chapter_id;
    if (chapterId) {
      const { data: ch } = await supabase.from("chapters").select("subject_code").eq("id", chapterId).single();
      subject = (ch as { subject_code?: string } | null)?.subject_code ?? subject;
    }
  } else {
    itemId = qz.item_id;
    oldExamIds = [];
  }

  if (oldExamIds.length > 0 && !replace) {
    console.log(`  bỏ qua: mục ${itemId} đã có exam_ids [${oldExamIds.join(", ")}] (thêm --replace để gắn đề mới).`);
    summary.push(`Bài ${qz.lesson_id}: BỎ QUA (đã có đề)`);
    continue;
  }

  const row = {
    title,
    duration_minutes: 15,
    published: true,
    subject_code: subject,
    topic: qz.lesson_title,
    difficulty: "de",
    questions: stripKind(qz.questions),
    // question_count / type_counts là cột GENERATED trong DB — không ghi (ghi sẽ lỗi), chỉ in số dự kiến.
    pass_score: Math.round((qz.quiz_min_correct / n) * 10 * 100) / 100,
  };
  console.log(`  exams ← "${title}" · ${n} câu ${JSON.stringify(typeCounts(qz.questions))} (dự kiến, DB tự sinh) · ${row.duration_minutes} phút · pass_score ${row.pass_score} · ${row.subject_code}`);
  console.log(`  lesson_items #${itemId} ← exam_ids=[<id mới>], quiz_min_correct=${qz.quiz_min_correct}`);
  if (oldExamIds.length) console.log(`  (--replace) đề cũ [${oldExamIds.join(", ")}] GIỮ NGUYÊN (có thể có exam_results) — thầy tự dọn.`);

  if (dryRun || !supabase) {
    if (dryRun) {
      const tally = qz.questions.reduce<Record<string, number>>((a, q) => ((a[q.kind as string] = (a[q.kind as string] ?? 0) + 1), a), {});
      console.log(`  [dry-run] loại 'kind' khỏi questions; kind: ${JSON.stringify(tally)}; câu đầu: ${String(qz.questions[0].question).slice(0, 80)}`);
    }
    summary.push(`Bài ${qz.lesson_id}: [dry-run] ${n} câu`);
    continue;
  }

  const { data: exam, error: exErr } = await supabase.from("exams").insert(row as never).select("id").single();
  if (exErr || !exam) fail(`tạo đề bài ${qz.lesson_id}: ${exErr?.message}`);
  const examId = (exam as { id: number }).id;
  const { error: upErr } = await supabase.from("lesson_items").update({ exam_ids: [examId], quiz_min_correct: qz.quiz_min_correct } as never).eq("id", itemId);
  if (upErr) fail(`đề ${examId} đã tạo nhưng gắn vào mục ${itemId} lỗi: ${upErr.message} (gắn tay exam_ids=[${examId}])`);
  console.log(`  ✓ exam ${examId} gắn vào mục ${itemId}`);
  summary.push(`Bài ${qz.lesson_id}: exam ${examId}${oldExamIds.length ? ` (đề cũ ${oldExamIds.join(",")} chưa xoá)` : ""}`);
}

console.log("\n--- Tổng kết ---\n" + summary.join("\n"));
if (!dryRun) console.log("\nSite export tĩnh → chạy tiếp: bash scripts/deploy.sh  (build-content ở prebuild) để thấy trên web.");
