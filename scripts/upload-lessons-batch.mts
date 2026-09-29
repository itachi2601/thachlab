// Đăng NHIỀU "gói bài học" JSON trong một lượt chạy — chỉ hỏi SUPABASE_SERVICE_ROLE_KEY một lần.
// Dùng chung logic với scripts/upload-lesson.mts (bundleToRows/validateBundle/uploadLessonMedia),
// chỉ khác là lặp qua một "manifest" nhiều bài thay vì một bài.
//
//   npx tsx scripts/upload-lessons-batch.mts manifest.json
//
// manifest.json: mảng các mục
//   { "bundle": "duong/dan/bundle.json", "lesson": 22, "classes": [17],
//     "target": "luyen_tap" | "kiem_tra" | "both", "mode": "replace" | "skip" }
//
// App export tĩnh, không có server ở production → cần service role key, CHỈ chạy cục bộ.

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

interface ManifestEntry {
  bundle: string;
  lesson: number;
  classes?: number[];
  target?: "luyen_tap" | "kiem_tra" | "both";
  mode?: "replace" | "skip";
}

function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}

async function main() {
  const manifestPath = process.argv[2];
  if (!manifestPath) fail("thiếu đường dẫn manifest.json");

  const manifest: ManifestEntry[] = JSON.parse(fs.readFileSync(path.resolve(manifestPath), "utf8"));
  if (!Array.isArray(manifest) || manifest.length === 0) fail("manifest rỗng hoặc không phải mảng");

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const key =
    process.env.SUPABASE_SERVICE_ROLE_KEY ??
    (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role) — dùng chung cho cả lượt: "));
  if (!key) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");

  const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

  console.log(`\nSẽ đăng ${manifest.length} bài:`);
  manifest.forEach((m, i) => console.log(`  ${i + 1}. lesson #${m.lesson} ← ${m.bundle} (target=${m.target ?? "luyen_tap"}, mode=${m.mode ?? "replace"})`));
  console.log("");

  for (const entry of manifest) {
    const target = entry.target ?? "luyen_tap";
    const mode = entry.mode ?? "replace";
    const classes = entry.classes ?? [];

    console.log(`\n=== Bài lesson #${entry.lesson} (${entry.bundle}) ===`);
    const raw: unknown = JSON.parse(fs.readFileSync(path.resolve(entry.bundle), "utf8"));
    const check = validateBundle(raw);
    if (!check.ok) {
      console.error("Lỗi: gói không hợp lệ:\n  - " + check.errors.join("\n  - "));
      console.error("  → BỎ QUA bài này, tiếp tục bài kế tiếp.");
      continue;
    }
    if (check.warnings.length) console.warn("Cảnh báo:\n  ! " + check.warnings.join("\n  ! "));
    let bundle = raw as LessonBundle;

    const { data: lesson, error: lErr } = await supabase.from("lessons").select("id, title").eq("id", entry.lesson).single();
    if (lErr || !lesson) {
      console.error(`Lỗi: không tìm thấy lesson_id ${entry.lesson}: ${lErr?.message ?? ""}`);
      console.error("  → BỎ QUA bài này, tiếp tục bài kế tiếp.");
      continue;
    }
    console.log(`Bài học #${lesson.id} "${lesson.title}"`);

    const rasters = bundle.raster_images ?? [];
    if (rasters.length) {
      console.log(`Tải ${rasters.length} ảnh…`);
      const media = await uploadLessonMedia(supabase, entry.lesson, rasters);
      bundle = applyMediaToBundle(bundle, media);
      console.log(`  ✓ ${media.length} ảnh`);
    }

    const rows = bundleToRows(bundle, entry.lesson);

    console.log(`Tạo đề "${rows.exam.title}"…`);
    const { data: exam, error: exErr } = await supabase.from("exams").insert(rows.exam).select("id").single();
    if (exErr || !exam) {
      console.error(`Lỗi tạo đề: ${exErr?.message}`);
      console.error("  → BỎ QUA bài này, tiếp tục bài kế tiếp.");
      continue;
    }
    const examId = exam.id as number;
    console.log(`  ✓ exam id ${examId}`);

    if (classes.length) {
      await supabase.from("exam_classes").delete().eq("exam_id", examId);
      await supabase.from("exam_classes").insert(classes.map((class_id) => ({ exam_id: examId, class_id })));
      console.log(`  ✓ gán ${classes.length} lớp`);
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
      .eq("lesson_id", entry.lesson);
    const find = (kind: string): ExistingItem | null => (items ?? []).find((it) => it.kind === kind) ?? null;

    async function upsertItem(payload: Record<string, unknown>, cur: ExistingItem | null) {
      const r = cur
        ? await supabase.from("lesson_items").update(payload).eq("id", cur.id)
        : await supabase.from("lesson_items").insert(payload);
      if (r.error) console.error(`Lỗi ${payload.kind}: ${r.error.message}`);
    }

    const lt = find("ly_thuyet");
    if (!rows.lyThuyet.body_html.trim()) console.log("Lý thuyết: gói không có phần này — giữ nguyên nội dung cũ.");
    else if (mode === "skip" && lt) console.log("Lý thuyết: bỏ qua");
    else {
      await upsertItem({ ...rows.lyThuyet, sort_order: lt?.sort_order ?? 1 }, lt);
      console.log(`Lý thuyết: ${lt ? "ghi đè" : "thêm"}`);
    }

    const bt = find("bai_tap_mau");
    if (rows.baiTapMau.questions.length === 0) console.log("Các dạng bài tập: gói không có phần này — giữ nguyên nội dung cũ.");
    else if (mode === "skip" && bt) console.log("Các dạng bài tập: bỏ qua");
    else {
      await upsertItem(
        { ...rows.baiTapMau, subtitle: rows.baiTapMau.subtitle || bt?.subtitle || "", sort_order: bt?.sort_order ?? 3 },
        bt,
      );
      console.log(`Các dạng bài tập: ${bt ? "ghi đè" : "thêm"} (${rows.baiTapMau.questions.length} dạng)`);
    }

    const kinds: ("luyen_tap" | "kiem_tra")[] = target === "both" ? ["luyen_tap", "kiem_tra"] : [target];
    const subtitle = typeCountSubtitle(rows.exam.questions, rows.exam.duration_minutes);
    for (const kind of kinds) {
      const cur = find(kind);
      if (mode === "skip" && (cur?.exam_ids?.length ?? 0) > 0) {
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
          lesson_id: entry.lesson,
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

    console.log(`Xong bài #${entry.lesson}. Kiểm tra: /lop-hoc/bai/?id=${entry.lesson}`);
  }

  console.log("\nHoàn tất cả lượt.");
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
