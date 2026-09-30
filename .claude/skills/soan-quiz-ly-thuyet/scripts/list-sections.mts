// In danh sách đoạn lý thuyết của một bài — nguồn DUY NHẤT để gắn `theorySection`.
// Gọi đúng wrapTheorySections (features/lessons/theory-sections.ts) nên chỉ số khớp trang học.
//   npx tsx .claude/skills/soan-quiz-ly-thuyet/scripts/list-sections.mts <lesson_id>
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { wrapTheorySections } from "../../../../features/lessons/theory-sections.ts";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../..");

export interface LessonItem {
  id: number;
  kind: string;
  title: string;
  body_html?: string;
  summary_html?: string;
  exam_ids?: number[];
}
export interface LessonFile {
  lesson: { id: number; title: string; lesson_kind?: string };
  chapterTitle: string;
  items: LessonItem[];
}
export interface SectionRow {
  itemId: number;
  index: number;
  heading: string;
  length: number;
}

export function readLesson(lessonId: number | string): LessonFile {
  const file = path.join(ROOT, "public/data/lessons", `${lessonId}.json`);
  if (!fs.existsSync(file)) {
    throw new Error(`không có ${file} — chạy "node scripts/build-content.mjs" để sinh public/data`);
  }
  return JSON.parse(fs.readFileSync(file, "utf8")) as LessonFile;
}

/** Độ dài (ký tự text thô) mỗi đoạn; đọc lại từ HTML đã bọc để đúng ranh giới. */
export function sectionsOf(item: LessonItem): SectionRow[] {
  const { html, sections } = wrapTheorySections(item.body_html ?? "", item.id);
  return sections.map((s, index) => {
    const m = new RegExp(`<div class="theory-section" id="${s.id}">([\\s\\S]*?)</div>(?=<div class="theory-section"|$)`).exec(html);
    const text = (m?.[1] ?? "").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
    return { itemId: item.id, index, heading: s.heading, length: text.length };
  });
}

/** Số đoạn thật của mục lý thuyết `itemId` (dùng cho validate-quiz / publish). */
export function sectionCount(lessonId: number | string, itemId: number): number {
  const item = readLesson(lessonId).items.find((i) => i.id === itemId);
  return item ? sectionsOf(item).length : 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const id = process.argv[2];
  if (!id) {
    console.error("Cách dùng: list-sections.mts <lesson_id>");
    process.exit(1);
  }
  try {
    const lesson = readLesson(id);
    console.log(`Bài ${lesson.lesson.id}: ${lesson.lesson.title} (${lesson.chapterTitle}) — lesson_kind=${lesson.lesson.lesson_kind}`);
    const theory = lesson.items.filter((i) => i.kind === "ly_thuyet");
    if (theory.length === 0) console.log("(không có mục ly_thuyet)");
    for (const item of theory) {
      const rows = sectionsOf(item);
      console.log(`\nMục ly_thuyet itemId=${item.id} "${item.title}" — exam_ids=${JSON.stringify(item.exam_ids ?? [])} — ${rows.length} đoạn`);
      if (rows.length === 0) console.log("  (không có mốc → theorySection bỏ trống, 'Ôn ngay' nhảy về đầu mục)");
      else {
        console.log("itemId\tđoạn\tđộ dài\ttiêu đề");
        for (const r of rows) console.log(`${r.itemId}\t${r.index}\t${r.length}\t${r.heading}`);
      }
    }
  } catch (e) {
    console.error("Lỗi:", (e as Error).message);
    process.exit(1);
  }
}
