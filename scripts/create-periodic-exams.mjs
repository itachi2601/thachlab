// Tạo các mục "Kiểm tra giữa/cuối học kì" xen giữa các chương cho lớp 10, 11, 12.
//
//   node scripts/create-periodic-exams.mjs [--apply]
//
// Không có --apply thì chỉ in ra việc sẽ làm (dry run), không ghi gì vào DB.
// App export tĩnh, không có server ở production → cần service role key, CHỈ chạy
// cục bộ. Script đọc NEXT_PUBLIC_SUPABASE_URL từ .env.local rồi hỏi
// SUPABASE_SERVICE_ROLE_KEY (gõ vào sẽ bị ẩn).
//
// Bài tạo ra để ở trạng thái ẨN (published = false) và đã có sẵn mục "Kiểm tra"
// trống — vào /quan-tri gắn đề xong rồi bấm "Hiện" thì học sinh mới thấy.
// Chạy lại được nhiều lần: chương nào đã có bài đúng loại thì bỏ qua.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));

// Lớp → [thứ tự chương đứng trước, loại bài, tên bài].
// Lớp 11 & 12 có 4 chương, mỗi chương một kì kiểm tra; lớp 10 có 7 chương,
// học kì 1 hết chương 4, học kì 2 hết chương 7.
const PLAN = {
  "10": [
    [2, "kiem_tra_giua_ki", "Kiểm tra giữa học kì 1"],
    [4, "kiem_tra_cuoi_ki", "Kiểm tra cuối học kì 1"],
    [5, "kiem_tra_giua_ki", "Kiểm tra giữa học kì 2"],
    [7, "kiem_tra_cuoi_ki", "Kiểm tra cuối học kì 2"],
  ],
  "11": [
    [1, "kiem_tra_giua_ki", "Kiểm tra giữa học kì 1"],
    [2, "kiem_tra_cuoi_ki", "Kiểm tra cuối học kì 1"],
    [3, "kiem_tra_giua_ki", "Kiểm tra giữa học kì 2"],
    [4, "kiem_tra_cuoi_ki", "Kiểm tra cuối học kì 2"],
  ],
  "12": [
    [1, "kiem_tra_giua_ki", "Kiểm tra giữa học kì 1"],
    [2, "kiem_tra_cuoi_ki", "Kiểm tra cuối học kì 1"],
    [3, "kiem_tra_giua_ki", "Kiểm tra giữa học kì 2"],
    [4, "kiem_tra_cuoi_ki", "Kiểm tra cuối học kì 2"],
  ],
};

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

const apply = process.argv.includes("--apply");

const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
if (!url) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL (biến môi trường hoặc .env.local).");
  process.exit(1);
}
const serviceKey =
  process.env.SUPABASE_SERVICE_ROLE_KEY ||
  (await askHidden("SUPABASE_SERVICE_ROLE_KEY: "));
if (!serviceKey) {
  console.error("Thiếu SUPABASE_SERVICE_ROLE_KEY.");
  process.exit(1);
}

const supabase = createClient(url, serviceKey, {
  auth: { autoRefreshToken: false, persistSession: false },
});

const { data: classes, error: classErr } = await supabase.from("classes").select("id, name");
if (classErr) throw classErr;

const { data: chapters, error: chapterErr } = await supabase
  .from("chapters")
  .select("id, title, sort_order, subject_code, chapter_classes(class_id)");
if (chapterErr) throw chapterErr;

const { data: lessons, error: lessonErr } = await supabase
  .from("lessons")
  .select("id, chapter_id, title, lesson_kind, sort_order");
if (lessonErr) throw lessonErr;

let created = 0;
let renamed = 0;

for (const [className, targets] of Object.entries(PLAN)) {
  const schoolClass = classes.find((c) => c.name === className);
  if (!schoolClass) {
    console.error(`! Không tìm thấy lớp "${className}" — bỏ qua.`);
    continue;
  }
  for (const [chapterOrder, kind, title] of targets) {
    const chapter = chapters.find(
      (c) =>
        c.subject_code === "vat-ly" &&
        c.sort_order === chapterOrder &&
        (c.chapter_classes ?? []).some((r) => r.class_id === schoolClass.id),
    );
    if (!chapter) {
      console.error(`! Lớp ${className}: không có chương thứ ${chapterOrder} — bỏ qua.`);
      continue;
    }
    const inChapter = lessons.filter((l) => l.chapter_id === chapter.id);
    const existing = inChapter.find((l) => l.lesson_kind === kind);
    if (existing) {
      if (existing.title === title) {
        console.log(`= Lớp ${className} · ${chapter.title}: đã có "${title}".`);
        continue;
      }
      console.log(
        `~ Lớp ${className} · ${chapter.title}: đổi tên "${existing.title}" → "${title}".`,
      );
      if (apply) {
        const { error } = await supabase
          .from("lessons")
          .update({ title })
          .eq("id", existing.id);
        if (error) throw error;
      }
      renamed += 1;
      continue;
    }
    const sortOrder = inChapter.reduce((max, l) => Math.max(max, l.sort_order ?? 0), 0) + 1;
    console.log(`+ Lớp ${className} · ${chapter.title}: thêm "${title}" (ẩn, chưa gắn đề).`);
    if (!apply) {
      created += 1;
      continue;
    }
    const { data: lesson, error } = await supabase
      .from("lessons")
      .insert({
        chapter_id: chapter.id,
        title,
        lesson_kind: kind,
        sort_order: sortOrder,
        published: false,
      })
      .select("id")
      .single();
    if (error) throw error;
    const { error: itemErr } = await supabase.from("lesson_items").insert({
      lesson_id: lesson.id,
      kind: "kiem_tra",
      title: "Kiểm tra",
      subtitle: "",
      body_html: "",
      video_url: "",
      pdf_url: "",
      exam_ids: [],
      questions: [],
      sort_order: 1,
    });
    if (itemErr) throw itemErr;
    created += 1;
  }
}

console.log(
  apply
    ? `\nXong: thêm ${created} bài, đổi tên ${renamed} bài. Vào /quan-tri gắn đề rồi bấm "Hiện".`
    : `\nDry run: sẽ thêm ${created} bài, đổi tên ${renamed} bài. Chạy lại kèm --apply để ghi.`,
);
