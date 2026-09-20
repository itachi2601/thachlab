// Đăng một "gói bài học" JSON (schema thachlab.lesson-bundle/v1) vào LMS —
// đường dự phòng khi không mở được trang /quan-tri/nhap-bai trong trình duyệt.
//
//   npx tsx scripts/upload-lesson.mts <bundle.json> --lesson <id> [--class <id>]... \
//        [--target luyen_tap|kiem_tra|both] [--mode replace|skip]
//
// App export tĩnh, không có server ở production → cần service role key, CHỈ chạy cục bộ.
// Script đọc NEXT_PUBLIC_SUPABASE_URL từ .env.local rồi hỏi SUPABASE_SERVICE_ROLE_KEY
// (gõ vào sẽ bị ẩn). Ảnh raster phải được nén sẵn (script không có canvas để nén).
//
// Dùng chung `validateBundle`/`bundleToRows` với trang `/quan-tri/nhap-bai`
// (`services/lesson-import.ts`) — sửa quy tắc ở đó thì script này tự theo, không lệch.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import { applyMediaToBundle, bundleToRows, typeCountSubtitle, validateBundle, type LessonBundle } from "@/services/lesson-import";
import { uploadLessonMedia } from "@/services/lesson-media";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));

function readEnvLocal(key: string): string | undefined {
  const envPath = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs
    .readFileSync(envPath, "utf8")
    .split("\n")
    .find((l) => l.startsWith(`${key}=`));
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

interface Args {
  bundle: string | null;
  lesson: number | null;
  classes: number[];
  target: "luyen_tap" | "kiem_tra" | "both";
  mode: "replace" | "skip";
}

function parseArgs(argv: string[]): Args {
  const out: Args = { bundle: null, lesson: null, classes: [], target: "luyen_tap", mode: "replace" };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--lesson") out.lesson = Number(argv[++i]);
    else if (a === "--class") out.classes.push(Number(argv[++i]));
    else if (a === "--target") out.target = argv[++i] as Args["target"];
    else if (a === "--mode") out.mode = argv[++i] as Args["mode"];
    else if (!a.startsWith("--")) out.bundle = a;
  }
  return out;
}

function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.bundle) fail("thiếu đường dẫn file bundle.json");
  if (!args.lesson) fail("thiếu --lesson <id>");
  if (!["replace", "skip"].includes(args.mode)) fail("--mode chỉ nhận replace|skip");
  if (!["luyen_tap", "kiem_tra", "both"].includes(args.target)) fail("--target chỉ nhận luyen_tap|kiem_tra|both");

  const raw: unknown = JSON.parse(fs.readFileSync(path.resolve(args.bundle), "utf8"));
  const check = validateBundle(raw);
  if (!check.ok) fail("gói không hợp lệ:\n  - " + check.errors.join("\n  - "));
  if (check.warnings.length) console.warn("Cảnh báo:\n  ! " + check.warnings.join("\n  ! "));
  let bundle = raw as LessonBundle;

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const key =
    process.env.SUPABASE_SERVICE_ROLE_KEY ??
    (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
  if (!key) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");

  const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
  const lessonId = args.lesson;

  const { data: lesson, error: lErr } = await supabase
    .from("lessons")
    .select("id, title")
    .eq("id", lessonId)
    .single();
  if (lErr || !lesson) fail(`không tìm thấy lesson_id ${lessonId}: ${lErr?.message ?? ""}`);
  console.log(`Bài học #${lesson.id} "${lesson.title}"`);

  // Ảnh — cùng hàm upload với trình duyệt (services/lesson-media.ts).
  const rasters = bundle.raster_images ?? [];
  if (rasters.length) {
    console.log(`Tải ${rasters.length} ảnh…`);
    const media = await uploadLessonMedia(supabase, lessonId, rasters);
    bundle = applyMediaToBundle(bundle, media);
    console.log(`  ✓ ${media.length} ảnh`);
  }

  const rows = bundleToRows(bundle, lessonId);

  console.log(`Tạo đề "${rows.exam.title}"…`);
  const { data: exam, error: exErr } = await supabase.from("exams").insert(rows.exam).select("id").single();
  if (exErr || !exam) fail(`tạo đề: ${exErr?.message}`);
  const examId = exam.id as number;
  console.log(`  ✓ exam id ${examId}`);

  if (args.classes.length) {
    await supabase.from("exam_classes").delete().eq("exam_id", examId);
    await supabase.from("exam_classes").insert(args.classes.map((class_id) => ({ exam_id: examId, class_id })));
    console.log(`  ✓ gán ${args.classes.length} lớp`);
  }

  interface ExistingItem {
    id: number;
    kind: string;
    title: string;
    exam_ids: number[];
    sort_order: number;
    subtitle: string;
    body_html?: string;
    questions?: unknown[];
  }
  const { data: items } = await supabase
    .from("lesson_items")
    .select("id, kind, title, exam_ids, sort_order, subtitle, body_html, questions")
    .eq("lesson_id", lessonId);
  const find = (kind: string): ExistingItem | null => (items ?? []).find((it) => it.kind === kind) ?? null;

  async function upsertItem(payload: Record<string, unknown>, cur: ExistingItem | null) {
    const r = cur
      ? await supabase.from("lesson_items").update(payload).eq("id", cur.id)
      : await supabase.from("lesson_items").insert(payload);
    if (r.error) fail(`${payload.kind}: ${r.error.message}`);
  }

  // Lý thuyết
  const lt = find("ly_thuyet");
  if (!rows.lyThuyet.body_html.trim()) console.log("Lý thuyết: gói không có phần này — giữ nguyên nội dung cũ.");
  else if (args.mode === "skip" && lt) console.log("Lý thuyết: bỏ qua");
  else {
    await upsertItem({ ...rows.lyThuyet, sort_order: lt?.sort_order ?? 1 }, lt);
    console.log(`Lý thuyết: ${lt ? "ghi đè" : "thêm"}`);
  }

  // Các dạng bài tập
  const bt = find("bai_tap_mau");
  if (rows.baiTapMau.questions.length === 0) console.log("Các dạng bài tập: gói không có phần này — giữ nguyên nội dung cũ.");
  else if (args.mode === "skip" && bt) console.log("Các dạng bài tập: bỏ qua");
  else {
    await upsertItem(
      { ...rows.baiTapMau, subtitle: rows.baiTapMau.subtitle || bt?.subtitle || "", sort_order: bt?.sort_order ?? 3 },
      bt,
    );
    console.log(`Các dạng bài tập: ${bt ? "ghi đè" : "thêm"} (${rows.baiTapMau.questions.length} dạng)`);
  }

  // luyen_tap / kiem_tra
  const kinds: ("luyen_tap" | "kiem_tra")[] = args.target === "both" ? ["luyen_tap", "kiem_tra"] : [args.target];
  const subtitle = typeCountSubtitle(rows.exam.questions, rows.exam.duration_minutes);
  for (const kind of kinds) {
    const cur = find(kind);
    if (args.mode === "skip" && (cur?.exam_ids?.length ?? 0) > 0) {
      console.log(`${kind}: bỏ qua (giữ đề cũ)`);
      continue;
    }
    const stale = (cur?.exam_ids ?? []).filter((id) => id !== examId);
    if (stale.length) {
      await supabase.from("exams").delete().in("id", stale);
      console.log(`${kind}: xóa ${stale.length} đề cũ`);
    }
    await upsertItem(
      {
        lesson_id: lessonId,
        kind,
        title: cur?.title || (kind === "luyen_tap" ? "Luyện tập" : "Kiểm tra"),
        subtitle,
        body_html: "",
        video_url: "",
        pdf_url: "",
        questions: [],
        exam_ids: [examId],
        sort_order: cur?.sort_order ?? (kind === "luyen_tap" ? 4 : 5),
      },
      cur,
    );
    console.log(`${kind}: gắn đề ${examId}`);
  }

  console.log(`\nXong. Kiểm tra: /lop-hoc/bai/?id=${lessonId}`);
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
