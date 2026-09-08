// Đăng một "gói bài học" JSON (schema thachlab.lesson-bundle/v1) vào LMS —
// đường dự phòng khi không mở được trang /quan-tri/nhap-bai trong trình duyệt.
//
//   node scripts/upload-lesson.mjs <bundle.json> --lesson <id> [--class <id>]... \
//        [--target luyen_tap|kiem_tra|both] [--mode replace|skip]
//
// App export tĩnh, không có server ở production → cần service role key, CHỈ chạy cục bộ.
// Script đọc NEXT_PUBLIC_SUPABASE_URL từ .env.local rồi hỏi SUPABASE_SERVICE_ROLE_KEY
// (gõ vào sẽ bị ẩn). Ảnh raster phải được nén sẵn (script không có canvas để nén).

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const BUCKET = "lesson-media";
const SCHEMA = "thachlab.lesson-bundle/v1";

function readEnvLocal(key) {
  const envPath = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs
    .readFileSync(envPath, "utf8")
    .split("\n")
    .find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}

function askHidden(query) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl._writeToOutput = (chunk) => rl.output.write(rl.stdoutMuted ? "*" : chunk);
    rl.stdoutMuted = false;
    rl.question(query, (answer) => {
      rl.close();
      process.stdout.write("\n");
      resolve(answer.trim());
    });
    rl.stdoutMuted = true;
  });
}

function parseArgs(argv) {
  const out = { bundle: null, lesson: null, classes: [], target: "luyen_tap", mode: "replace" };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--lesson") out.lesson = Number(argv[++i]);
    else if (a === "--class") out.classes.push(Number(argv[++i]));
    else if (a === "--target") out.target = argv[++i];
    else if (a === "--mode") out.mode = argv[++i];
    else if (!a.startsWith("--")) out.bundle = a;
  }
  return out;
}

function fail(msg) {
  console.error("Lỗi:", msg);
  process.exit(1);
}

function checkBundle(b) {
  const errs = [];
  if (!b || typeof b !== "object") errs.push("gói không phải object");
  if (b.schema !== SCHEMA) errs.push(`sai schema (cần ${SCHEMA})`);
  if (!b.theory_html?.trim()) errs.push("thiếu theory_html");
  if (/\\includegraphics\{|\\begin\{tabular\}|\\section\{/.test(b.theory_html ?? ""))
    errs.push("theory_html còn sót LaTeX chưa chuyển");
  if (!Array.isArray(b.worked_examples)) errs.push("worked_examples phải là mảng");
  if (!b.exam || !Array.isArray(b.exam.questions) || b.exam.questions.length === 0)
    errs.push("exam.questions trống");
  for (const [i, q] of (b.exam?.questions ?? []).entries()) {
    const n = i + 1;
    if (q.type === "multiple_choice" && (!Array.isArray(q.options) || q.options.length !== 4))
      errs.push(`câu ${n}: trắc nghiệm cần 4 phương án`);
    if (q.type === "true_false" && (!Array.isArray(q.statements) || q.statements.length !== 4))
      errs.push(`câu ${n}: đúng/sai cần 4 ý`);
    if (q.type === "short_answer" && String(q.answer ?? "").length > 4)
      errs.push(`câu ${n}: đáp án dài quá 4 ký tự`);
  }
  return errs;
}

function typeCountSubtitle(questions, minutes) {
  const short = { multiple_choice: "TN", true_false: "ĐS", short_answer: "TLN" };
  const counts = {};
  for (const q of questions) counts[q.type] = (counts[q.type] ?? 0) + 1;
  const parts = Object.entries(short)
    .filter(([t]) => counts[t])
    .map(([t, s]) => `${counts[t]} ${s}`);
  return `${questions.length} câu${parts.length ? ` (${parts.join(" · ")})` : ""}${minutes ? ` — ${minutes} phút` : ""}`;
}

async function uploadRasters(supabase, lessonId, images) {
  const media = [];
  for (const img of images) {
    const m = /^data:([^;,]+)?(;base64)?,(.*)$/s.exec(img.dataUri);
    if (!m) fail(`ảnh "${img.name}": data URI không hợp lệ`);
    const buf = m[2] ? Buffer.from(m[3], "base64") : Buffer.from(decodeURIComponent(m[3]));
    if (buf.length > 500 * 1024) console.warn(`  ! ảnh "${img.name}" nặng ${Math.round(buf.length / 1024)} KB — nên nén trước`);
    const safe = (img.name || "hinh")
      .replace(/\.[^.]+$/, "")
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "")
      .replace(/[^a-zA-Z0-9_-]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .toLowerCase();
    const ext = (img.name.split(".").pop() || "png").toLowerCase();
    const storagePath = `${lessonId}/${Date.now()}-${safe}.${ext}`;
    const { error } = await supabase.storage.from(BUCKET).upload(storagePath, buf, {
      contentType: m[1] || "image/png",
      upsert: false,
    });
    if (error) {
      await supabase.storage.from(BUCKET).remove(media.map((x) => x.storagePath));
      fail(`upload "${img.name}": ${error.message}`);
    }
    const { data } = supabase.storage.from(BUCKET).getPublicUrl(storagePath);
    media.push({ placeholder: img.placeholder, url: data.publicUrl, storagePath });
  }
  return media;
}

function applyMedia(str, media) {
  let out = str;
  for (const x of media) out = out.split(x.placeholder).join(x.url);
  return out;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.bundle) fail("thiếu đường dẫn file bundle.json");
  if (!args.lesson) fail("thiếu --lesson <id>");
  if (!["replace", "skip"].includes(args.mode)) fail("--mode chỉ nhận replace|skip");
  if (!["luyen_tap", "kiem_tra", "both"].includes(args.target)) fail("--target chỉ nhận luyen_tap|kiem_tra|both");

  let bundle = JSON.parse(fs.readFileSync(path.resolve(args.bundle), "utf8"));
  const errs = checkBundle(bundle);
  if (errs.length) fail("gói không hợp lệ:\n  - " + errs.join("\n  - "));

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

  // Ảnh
  const rasters = bundle.raster_images ?? [];
  if (rasters.length) {
    console.log(`Tải ${rasters.length} ảnh…`);
    const media = await uploadRasters(supabase, lessonId, rasters);
    bundle = JSON.parse(applyMedia(JSON.stringify(bundle), media));
    console.log(`  ✓ ${media.length} ảnh`);
  }

  // Đề
  const e = bundle.exam;
  const examRow = {
    title: e.title.trim(),
    duration_minutes: e.duration_minutes ?? 20,
    published: true,
    subject_code: e.subject_code || "vat-ly",
    topic: (e.topic ?? "").trim(),
    difficulty: e.difficulty ?? "",
    questions: e.questions,
  };
  console.log(`Tạo đề "${examRow.title}"…`);
  const { data: exam, error: exErr } = await supabase.from("exams").insert(examRow).select("id").single();
  if (exErr || !exam) fail(`tạo đề: ${exErr?.message}`);
  const examId = exam.id;
  console.log(`  ✓ exam id ${examId}`);

  if (args.classes.length) {
    await supabase.from("exam_classes").delete().eq("exam_id", examId);
    await supabase.from("exam_classes").insert(args.classes.map((class_id) => ({ exam_id: examId, class_id })));
    console.log(`  ✓ gán ${args.classes.length} lớp`);
  }

  const { data: items } = await supabase
    .from("lesson_items")
    .select("id, kind, exam_ids, sort_order, subtitle")
    .eq("lesson_id", lessonId);
  const find = (kind) => (items ?? []).find((it) => it.kind === kind) ?? null;

  async function upsertItem(payload, cur) {
    const r = cur
      ? await supabase.from("lesson_items").update(payload).eq("id", cur.id)
      : await supabase.from("lesson_items").insert(payload);
    if (r.error) fail(`${payload.kind}: ${r.error.message}`);
  }

  // Lý thuyết
  const lt = find("ly_thuyet");
  if (args.mode === "skip" && lt) console.log("Lý thuyết: bỏ qua");
  else {
    await upsertItem(
      {
        lesson_id: lessonId,
        kind: "ly_thuyet",
        title: bundle.theory_title?.trim() || "Lý thuyết trọng tâm",
        subtitle: bundle.theory_subtitle?.trim() || "",
        body_html: bundle.theory_html,
        video_url: "",
        pdf_url: "",
        questions: [],
        exam_ids: [],
        sort_order: lt?.sort_order ?? 1,
      },
      lt,
    );
    console.log(`Lý thuyết: ${lt ? "ghi đè" : "thêm"}`);
  }

  // Các dạng bài tập
  const bt = find("bai_tap_mau");
  const worked = (bundle.worked_examples ?? []).filter((w) => w.body_html?.trim());
  if (args.mode === "skip" && bt) console.log("Các dạng bài tập: bỏ qua");
  else {
    await upsertItem(
      {
        lesson_id: lessonId,
        kind: "bai_tap_mau",
        title: "Các dạng bài tập",
        subtitle: worked.length ? `${worked.length} dạng bài kèm lời giải` : bt?.subtitle ?? "",
        body_html: "",
        video_url: "",
        pdf_url: "",
        questions: worked,
        exam_ids: [],
        sort_order: bt?.sort_order ?? 3,
      },
      bt,
    );
    console.log(`Các dạng bài tập: ${bt ? "ghi đè" : "thêm"} (${worked.length} dạng)`);
  }

  // luyen_tap / kiem_tra
  const kinds = args.target === "both" ? ["luyen_tap", "kiem_tra"] : [args.target];
  const subtitle = typeCountSubtitle(examRow.questions, examRow.duration_minutes);
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
        title: kind === "luyen_tap" ? "Luyện tập" : "Kiểm tra",
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

main().catch((err) => fail(err.message ?? String(err)));
