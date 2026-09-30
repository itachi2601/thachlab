// In các đoạn lý thuyết của bài — đúng theo wrapTheorySections (nguồn duy nhất để gắn theorySection).
//   npx tsx .claude/skills/soan-quiz-ly-thuyet/scripts/list-sections.mts <lesson_id>
import { getLessonInfo } from "./lib";

const id = Number(process.argv[2]);
if (!Number.isInteger(id)) { console.error("Cách dùng: list-sections.mts <lesson_id>"); process.exit(2); }
try {
  const info = getLessonInfo(id);
  console.log(`Bài ${info.id}: ${info.title}`);
  if (info.items.length === 0) console.log("(không có mục ly_thuyet)");
  for (const it of info.items) {
    console.log(`\nitemId ${it.itemId} — ${it.title}${it.existingExamIds.length ? `  [đã có exam_ids: ${it.existingExamIds.join(",")}]` : ""}`);
    if (it.sections.length === 0) console.log("  (không có mốc chia đoạn → KHÔNG gắn theorySection)");
    for (const s of it.sections) console.log(`  itemId=${it.itemId}  đoạn=${s.index}  độ dài=${String(s.length).padStart(5)}  ${s.heading}`);
  }
} catch (e) { console.error("Lỗi:", (e as Error).message); process.exit(1); }
