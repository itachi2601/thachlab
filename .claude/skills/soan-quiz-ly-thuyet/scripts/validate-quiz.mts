// Kiểm file JSON bộ câu lý thuyết (schema: xem SKILL.md / scripts/data/theory-quiz/*.json).
//   npx tsx .claude/skills/soan-quiz-ly-thuyet/scripts/validate-quiz.mts <file.json | thư mục>
// Exit code ≠ 0 nếu có lỗi. Cần public/data (node scripts/build-content.mjs).
import fs from "node:fs";
import path from "node:path";
import { validateQuiz } from "./quiz-lib.mts";

const target = process.argv[2];
if (!target) {
  console.error("Cách dùng: validate-quiz.mts <file.json | thư mục>");
  process.exit(2);
}
const files = fs.statSync(target).isDirectory()
  ? fs.readdirSync(target).filter((f) => f.endsWith(".json")).map((f) => path.join(target, f))
  : [target];
if (files.length === 0) {
  console.error(`Không có file .json trong ${target}`);
  process.exit(2);
}
let bad = 0;
for (const file of files) {
  let data: unknown;
  try {
    data = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (e) {
    console.error(`✗ ${file}: JSON hỏng — ${(e as Error).message}`);
    bad += 1;
    continue;
  }
  const { errors, warnings } = validateQuiz(data, path.basename(file));
  for (const w of warnings) console.warn(`⚠ ${w}`);
  for (const e of errors) console.error(`✗ ${e}`);
  const n = (data as { questions?: unknown[] })?.questions?.length ?? 0;
  if (errors.length) bad += 1;
  else console.log(`✓ ${file} — ${n} câu hợp lệ`);
}
if (bad) {
  console.error(`\n${bad}/${files.length} file lỗi.`);
  process.exit(1);
}
