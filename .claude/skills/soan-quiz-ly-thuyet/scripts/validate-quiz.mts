// Kiểm file bộ câu lý thuyết. Exit ≠ 0 nếu có lỗi.
//   npx tsx .claude/skills/soan-quiz-ly-thuyet/scripts/validate-quiz.mts <file.json | thư mục>
import fs from "node:fs";
import { loadTopics, quizFilesIn, validateQuiz } from "./lib";

const target = process.argv[2] ?? "scripts/data/theory-quiz";
if (!fs.existsSync(target)) { console.error("Không thấy:", target); process.exit(2); }
const topics = loadTopics();
if (!topics) console.log("(chưa có scripts/data/question-topics.json — bỏ qua kiểm YCCĐ)");
let bad = 0;
const files = quizFilesIn(target);
for (const f of files) {
  let res;
  try { res = validateQuiz(JSON.parse(fs.readFileSync(f, "utf8")), { topics }); }
  catch (e) { res = { errors: [`JSON hỏng: ${(e as Error).message}`], warnings: [] }; }
  console.log(`${res.errors.length ? "✗" : "✓"} ${f}`);
  res.errors.forEach((m) => console.log("   LỖI:", m));
  res.warnings.forEach((m) => console.log("   cảnh báo:", m));
  if (res.errors.length) bad++;
}
console.log(`\n${files.length - bad}/${files.length} file đạt.`);
process.exit(bad ? 1 : 0);
