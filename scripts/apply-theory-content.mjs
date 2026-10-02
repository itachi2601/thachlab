#!/usr/bin/env node
/**
 * scripts/apply-theory-content.mjs
 *
 * Áp nội dung lý thuyết tương tác (docs/LY-THUYET-TUONG-TAC.md) cho MỘT mục lý thuyết:
 *
 *   node scripts/apply-theory-content.mjs \
 *     --lesson 20 --item 2 \
 *     --body    scripts/data/ly-thuyet-tuong-tac/bai20-dao-dong-dieu-hoa.body.html \
 *     --summary scripts/data/ly-thuyet-tuong-tac/bai20-dao-dong-dieu-hoa.summary.html
 *
 * Script KHÔNG ghi lên Supabase (không có service role key ở đây — xem AGENTS.md). Nó làm 2 việc:
 *   1. Chép nội dung mới vào `public/data/lessons/<lesson>.json` (file build, đã gitignore) để xem
 *      trước bằng dev server — không đụng production.
 *   2. Sinh payload JSON + in sẵn lệnh curl PATCH để thầy tự chạy khi đã duyệt.
 *
 * Cờ: --no-preview (bỏ bước 1), --payload <path> (đổi chỗ ghi payload).
 */

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

function arg(name) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : undefined;
}
const has = (name) => process.argv.includes(`--${name}`);

const lessonId = Number(arg("lesson"));
const itemId = Number(arg("item"));
const bodyPath = arg("body");
const summaryPath = arg("summary");

if (!Number.isInteger(lessonId) || !Number.isInteger(itemId) || !bodyPath) {
  console.error(
    "Thiếu tham số. Ví dụ:\n" +
      "  node scripts/apply-theory-content.mjs --lesson 20 --item 2 \\\n" +
      "    --body scripts/data/ly-thuyet-tuong-tac/bai20-dao-dong-dieu-hoa.body.html \\\n" +
      "    --summary scripts/data/ly-thuyet-tuong-tac/bai20-dao-dong-dieu-hoa.summary.html",
  );
  process.exit(2);
}

const bodyHtml = fs.readFileSync(bodyPath, "utf8");
const summaryHtml = summaryPath ? fs.readFileSync(summaryPath, "utf8") : undefined;

// --- 1. payload cho PATCH REST (thầy chạy, xem docs/memory/feedback_lesson_item_edit_via_rest.md)
const payloadPath =
  arg("payload") ?? path.join("scripts/data/ly-thuyet-tuong-tac", `payload-item-${itemId}.json`);
const payload = summaryHtml === undefined
  ? { body_html: bodyHtml }
  : { body_html: bodyHtml, summary_html: summaryHtml };
fs.writeFileSync(payloadPath, JSON.stringify(payload));
console.log(`Payload: ${payloadPath} (${JSON.stringify(payload).length} ký tự)`);

// --- 2. xem trước cục bộ: chép vào file build public/data (gitignore, không phải production)
if (!has("no-preview")) {
  const lessonFile = path.join("public/data/lessons", `${lessonId}.json`);
  if (!fs.existsSync(lessonFile)) {
    console.warn(
      `! Không thấy ${lessonFile} — bỏ qua bước xem trước. Chạy \`npm run build\` (hoặc prebuild) để sinh lại public/data trước.`,
    );
  } else {
    const data = JSON.parse(fs.readFileSync(lessonFile, "utf8"));
    const item = (data.items ?? []).find((it) => it.id === itemId);
    if (!item) {
      console.warn(`! ${lessonFile} không có mục id=${itemId} — bỏ qua bước xem trước.`);
    } else {
      if (item.kind !== "ly_thuyet") {
        console.warn(`! Mục ${itemId} có kind="${item.kind}", không phải ly_thuyet — vẫn ghi đè body_html vì thầy yêu cầu.`);
      }
      item.body_html = bodyHtml;
      if (summaryHtml !== undefined) item.summary_html = summaryHtml;
      fs.writeFileSync(lessonFile, JSON.stringify(data));
      console.log(`Xem trước cục bộ: đã ghi vào ${lessonFile} (mục ${itemId}).`);
    }
  }
}

console.log(`
Xem trước (tuỳ chọn, không đụng production):
  npm run dev   →  http://localhost:3000/lop-hoc/bai/?id=${lessonId}

Khi đã duyệt nội dung, chạy trên máy có .env.local (thầy tự chạy — cần service role key):
  curl -s -X PATCH "$NEXT_PUBLIC_SUPABASE_URL/rest/v1/lesson_items?id=eq.${itemId}" \\
    -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \\
    -H "Content-Type: application/json" -H "Prefer: return=minimal" \\
    --data @${payloadPath}

Sau khi PATCH xong: build + deploy (\`bash scripts/deploy.sh\`) vì nội dung lý thuyết nằm trong
public/data sinh ở bước prebuild; rồi kiểm trên web thật bằng điện thoại (375px).
`);
