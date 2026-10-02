// Chuyển một đề văn bản kiểu Azota (de.txt — cùng định dạng trang /quan-tri/dang-de
// đọc: dấu "*" trước phương án đúng, "PHẦN I/II/III", "Chủ đề:"/"Dạng:" mỗi câu) thành
// gói `thachlab.lesson-bundle/v1` để đăng bằng `upload-lesson.mts` — không cần mở
// trình duyệt / trang admin.
//
//   npx tsx scripts/text-to-bundle.mts de.txt --title "Kiểm tra: ..." \
//       [--duration 45] [--subject vat-ly] -o bundle.json
//
// Dùng đúng `docxTextToBundle` (services/docx-exam-parser.ts) mà trang /quan-tri/dang-de
// dùng — sửa quy tắc tách câu/đáp án ở đó thì script này tự theo, không lệch. Chạy
// `soat_nhan.py` (skill up-de-kiem-tra) TRƯỚC để soát tên "Chủ đề:" đúng danh mục khối
// — script này chỉ kiểm câu nào thiếu nhãn, không tra danh mục.

import fs from "node:fs";
import path from "node:path";
import type { ExamQuestion } from "@/features/exams/types";
import { validateBundle } from "@/services/lesson-import";
import { docxTextToBundle } from "@/services/docx-exam-parser";

interface Args {
  text: string | null;
  title: string | null;
  duration: number | undefined;
  subject: string;
  out: string;
}

function parseArgs(argv: string[]): Args {
  const out: Args = { text: null, title: null, duration: undefined, subject: "vat-ly", out: "bundle.json" };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--title") out.title = argv[++i];
    else if (a === "--duration") out.duration = Number(argv[++i]);
    else if (a === "--subject") out.subject = argv[++i];
    else if (a === "-o" || a === "--out") out.out = argv[++i];
    else if (!a.startsWith("--")) out.text = a;
  }
  return out;
}

function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.text) fail("thiếu đường dẫn de.txt");

  const raw = fs.readFileSync(path.resolve(args.text), "utf8");
  const draft = docxTextToBundle(raw, {
    title: args.title ?? undefined,
    subjectCode: args.subject,
    durationMinutes: args.duration,
  });
  if (draft.notes.length) console.warn("Ghi chú khi tách câu:\n  ! " + draft.notes.join("\n  ! "));

  const questions = draft.bundle.exam.questions;
  if (questions.length === 0) fail("không tách được câu nào — kiểm tra lại mốc 'Câu n.' / 'PHẦN I/II/III'.");

  const missing = questions
    .map((q, i) => ({ n: i + 1, topic: (q as ExamQuestion).topic, form: (q as ExamQuestion).form }))
    .filter((q) => !q.topic || !q.form);
  if (missing.length)
    fail(
      `${missing.length}/${questions.length} câu thiếu "Chủ đề:"/"Dạng:" (câu ${missing.map((q) => q.n).join(", ")}) — ` +
        `chạy soat_nhan.py de.txt --grade <khối> --fix trước rồi tạo lại de.txt.`,
    );

  const check = validateBundle(draft.bundle);
  if (check.warnings.length) console.warn("Cảnh báo:\n  ! " + check.warnings.join("\n  ! "));
  if (!check.ok) fail("gói không hợp lệ:\n  - " + check.errors.join("\n  - "));

  fs.writeFileSync(path.resolve(args.out), JSON.stringify(draft.bundle, null, 2));
  const topicCount = new Set(questions.map((q) => (q as ExamQuestion).topic).filter(Boolean)).size;
  console.log(`✓ ${args.out}: ${questions.length} câu · ${topicCount} chủ đề · "${draft.bundle.exam.title}"`);
}

main();
