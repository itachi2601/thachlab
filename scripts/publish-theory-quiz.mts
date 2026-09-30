// Đăng bộ "Kiểm tra nhanh" lý thuyết (scripts/data/theory-quiz/<lesson_id>.json) lên thachlab.
// CHẠY TRÊN MAC (cần service role). Trên cloud chỉ chạy được --dry-run (không cần key, không ghi gì).
//
//   npx tsx scripts/publish-theory-quiz.mts --lesson 3 --lesson 6 [--replace] [--dry-run]
//   npx tsx scripts/publish-theory-quiz.mts --all [--replace] [--dry-run]
//
// Mỗi bài: validate lại (cùng logic validate-quiz) → tra lesson_items thật → tạo 1 dòng exams
// ("Kiểm tra nhanh — <bài>", published, 15 phút, bỏ key `kind`, đổi difficulty sang mã DB) → gắn
// exam_ids + quiz_min_correct vào mục lý thuyết. question_count/type_counts là cột GENERATED nên
// KHÔNG ghi. Không tạo exam_classes (giống exam 209 làm tay: quiz chỉ hiện trong bài học).
// Site export tĩnh: đăng xong phải `bash scripts/deploy.sh` mới thấy trên web.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import { DIFFICULTY_CODE, validateQuiz, type QuizFile } from "../.claude/skills/soan-quiz-ly-thuyet/scripts/quiz-lib.mts";
import { readLesson } from "../.claude/skills/soan-quiz-ly-thuyet/scripts/list-sections.mts";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const QUIZ_DIR = path.join(scriptDir, "data", "theory-quiz");
const TOPICS_FILE = path.join(scriptDir, "data", "question-topics.json");

function readEnvLocal(key: string): string | undefined {
  const envPath = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs.readFileSync(envPath, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}

function askHidden(query: string): Promise<string> {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const rlAny = rl as unknown as { _writeToOutput: (chunk: string) => void; stdoutMuted: boolean };
    rlAny._writeToOutput = (chunk) => (rl as unknown as { output: NodeJS.WritableStream }).output.write(rlAny.stdoutMuted ? "*" : chunk);
    rlAny.stdoutMuted = false;
    rl.question(query, (answer) => {
      rl.close();
      process.stdout.write("\n");
      resolve(answer.trim());
    });
    rlAny.stdoutMuted = true;
  });
}

function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}

interface Args {
  lessons: number[];
  all: boolean;
  dryRun: boolean;
  replace: boolean;
}

function parseArgs(argv: string[]): Args {
  const out: Args = { lessons: [], all: false, dryRun: false, replace: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--lesson") {
      const n = Number(argv[++i]);
      if (!Number.isInteger(n)) fail("--lesson cần số nguyên");
      out.lessons.push(n);
    } else if (a === "--all") out.all = true;
    else if (a === "--dry-run") out.dryRun = true;
    else if (a === "--replace") out.replace = true;
    else fail(`tham số lạ: ${a}`);
  }
  if (!out.all && out.lessons.length === 0) fail("cần --lesson <id> (lặp được) hoặc --all");
  return out;
}

interface ItemRow {
  id: number;
  exam_ids: number[] | null;
  quiz_min_correct: number | null;
}

function loadTopicIndex(): Map<number, Set<string>> | null {
  if (!fs.existsSync(TOPICS_FILE)) return null;
  const { topics } = JSON.parse(fs.readFileSync(TOPICS_FILE, "utf8")) as {
    topics: { id: number; lesson_id: number | null; name: string; parent_id: number | null }[];
  };
  const byParent = new Map<number, typeof topics>();
  for (const t of topics) if (t.parent_id != null) byParent.set(t.parent_id, [...(byParent.get(t.parent_id) ?? []), t]);
  const out = new Map<number, Set<string>>();
  for (const t of topics) {
    if (t.lesson_id == null) continue;
    const set = out.get(t.lesson_id) ?? new Set<string>();
    const stack = [t];
    while (stack.length) {
      const cur = stack.pop()!;
      set.add(cur.name);
      stack.push(...(byParent.get(cur.id) ?? []));
    }
    out.set(t.lesson_id, set);
  }
  return out;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const ids = args.all
    ? fs.readdirSync(QUIZ_DIR).filter((f) => /^\d+\.json$/.test(f)).map((f) => Number(f.replace(".json", ""))).sort((a, b) => a - b)
    : [...new Set(args.lessons)];
  if (ids.length === 0) fail(`không có file nào trong ${QUIZ_DIR}`);

  // 1) Đọc + validate hết trước khi đụng DB.
  const quizzes = new Map<number, QuizFile>();
  let bad = 0;
  for (const id of ids) {
    const file = path.join(QUIZ_DIR, `${id}.json`);
    if (!fs.existsSync(file)) fail(`không có ${file}`);
    const data = JSON.parse(fs.readFileSync(file, "utf8")) as QuizFile;
    if (data.lesson_id !== id) fail(`${id}.json có lesson_id=${data.lesson_id}`);
    const { errors, warnings } = validateQuiz(data, `${id}.json`);
    warnings.forEach((w) => console.warn(`⚠ ${w}`));
    errors.forEach((e) => console.error(`✗ ${e}`));
    if (errors.length) bad += 1;
    quizzes.set(id, data);
  }
  if (bad) fail(`${bad} file không qua validate — sửa rồi chạy lại`);

  const topicIndex = loadTopicIndex();
  if (!topicIndex) console.warn(`⚠ chưa có ${path.relative(process.cwd(), TOPICS_FILE)} (chạy scripts/export-question-topics.mts) — bỏ qua kiểm topic`);

  // 2) Kết nối (dry-run: không cần key; tra mục lý thuyết từ public/data).
  type Sb = ReturnType<typeof createClient>;
  let supabase: Sb | null = null;
  if (!args.dryRun) {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
    if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
    const key =
      process.env.SUPABASE_SERVICE_ROLE_KEY ??
      readEnvLocal("SUPABASE_SERVICE_ROLE_KEY") ??
      (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
    if (!key) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");
    supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
  } else console.log("— DRY RUN: không ghi gì, mục lý thuyết tra từ public/data —\n");

  async function findTheoryItems(lessonId: number): Promise<ItemRow[]> {
    if (supabase) {
      const { data, error } = await supabase
        .from("lesson_items")
        .select("id, exam_ids, quiz_min_correct")
        .eq("lesson_id", lessonId)
        .eq("kind", "ly_thuyet");
      if (error) fail(`đọc lesson_items ${lessonId}: ${error.message}`);
      return (data ?? []) as ItemRow[];
    }
    return readLesson(lessonId).items
      .filter((i) => i.kind === "ly_thuyet")
      .map((i) => ({ id: i.id, exam_ids: i.exam_ids ?? [], quiz_min_correct: null }));
  }

  const done: string[] = [];
  const skipped: string[] = [];
  for (const id of ids) {
    const quiz = quizzes.get(id)!;
    const items = await findTheoryItems(id);
    if (items.length !== 1) fail(`bài ${id}: cần đúng 1 mục ly_thuyet, thấy ${items.length}`);
    const item = items[0];
    if (item.id !== quiz.item_id) fail(`bài ${id}: item_id trong file (${quiz.item_id}) lệch mục thật (${item.id}) — dừng`);

    const allowed = topicIndex?.get(id);
    if (topicIndex) {
      if (!allowed) console.warn(`⚠ bài ${id}: question_topics.json không có chủ đề nào của bài — giữ nguyên topic`);
      else {
        const unknown = [...new Set(quiz.questions.map((q) => q.topic))].filter((t) => t !== quiz.lesson_title && !allowed.has(t));
        if (unknown.length) console.warn(`⚠ bài ${id}: topic không có trong YCCĐ của bài: ${unknown.map((t) => JSON.stringify(t)).join(", ")} (giữ nguyên)`);
      }
    }

    const oldIds = item.exam_ids ?? [];
    if (oldIds.length > 0 && !args.replace) {
      console.log(`↷ bài ${id}: mục ${item.id} đã có exam_ids ${JSON.stringify(oldIds)} — bỏ qua (thêm --replace để thay)`);
      skipped.push(`${id}`);
      continue;
    }

    const questions = quiz.questions.map((q) => {
      const { kind: _kind, ...rest } = q;
      void _kind;
      return { ...rest, difficulty: DIFFICULTY_CODE[q.difficulty] };
    });
    const chapterSubject = (() => {
      const cat = JSON.parse(fs.readFileSync(path.join(scriptDir, "..", "public/data/catalog.json"), "utf8")) as {
        chapters: { id: number; subjectCode?: string }[];
        lessons: { id: number; chapter_id: number }[];
      };
      const ls = cat.lessons.find((l) => l.id === id);
      return cat.chapters.find((c) => c.id === ls?.chapter_id)?.subjectCode || "vat-ly";
    })();
    const counts = questions.reduce<Record<string, number>>((m, q) => ((m[q.type] = (m[q.type] ?? 0) + 1), m), {});
    const exam = {
      title: `Kiểm tra nhanh — ${quiz.lesson_title}`,
      duration_minutes: 15,
      published: true,
      subject_code: chapterSubject,
      topic: quiz.lesson_title,
      difficulty: "de",
      pass_score: Math.round((quiz.quiz_min_correct / questions.length) * 1000) / 100,
      questions,
    };

    console.log(`▶ bài ${id} "${quiz.lesson_title}" — mục ly_thuyet ${item.id}`);
    console.log(`  exams: "${exam.title}" · ${exam.duration_minutes}' · subject ${exam.subject_code} · pass_score ${exam.pass_score} · ${questions.length} câu ${JSON.stringify(counts)} (question_count/type_counts DB tự tính)`);
    console.log(`  lesson_items[${item.id}]: exam_ids ← [<id mới>], quiz_min_correct ← ${quiz.quiz_min_correct}`);
    if (oldIds.length) console.log(`  (--replace) exam cũ ${JSON.stringify(oldIds)} được GIỮ NGUYÊN (có thể đã có exam_results) — thầy tự dọn nếu muốn`);
    if (args.dryRun) {
      questions.forEach((q, i) => {
        const ans = q.type === "multiple_choice" ? `đáp án ${"ABCD"[q.answer as number]}` : q.type === "short_answer" ? `= ${q.answer}` : q.statements!.map((s) => (s.answer ? "Đ" : "S")).join("");
        console.log(`    ${String(i + 1).padStart(2)}. [${q.type}|${q.difficulty}|đoạn ${q.theorySection ?? "-"}] ${q.question.replace(/\s+/g, " ").slice(0, 80)} → ${ans}`);
      });
      done.push(`${id}`);
      continue;
    }

    const { data: created, error: exErr } = await supabase!.from("exams").insert(exam).select("id").single();
    if (exErr || !created) fail(`bài ${id}: tạo exams: ${exErr?.message}`);
    const examId = (created as { id: number }).id;
    const { error: upErr } = await supabase!
      .from("lesson_items")
      .update({ exam_ids: [examId], quiz_min_correct: quiz.quiz_min_correct })
      .eq("id", item.id);
    if (upErr) fail(`bài ${id}: exam ${examId} đã tạo nhưng gắn vào mục ${item.id} lỗi: ${upErr.message}`);
    console.log(`  ✓ exam ${examId} gắn vào mục ${item.id}`);
    done.push(`${id}→exam ${examId}`);
  }

  console.log(`\n${args.dryRun ? "[DRY RUN] sẽ đăng" : "Đã đăng"}: ${done.join(", ") || "(không có)"}${skipped.length ? ` · bỏ qua: ${skipped.join(", ")}` : ""}`);
  if (!args.dryRun && done.length) console.log("Site export tĩnh → chạy `bash scripts/deploy.sh` (build-content ở prebuild) mới thấy trên web.");
}

main().catch((e) => fail(e instanceof Error ? e.message : String(e)));
