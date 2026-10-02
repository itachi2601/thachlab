// Chỉ ghi đè mục "Lý thuyết" (lesson_items.kind=ly_thuyet) của một bài từ file bundle.json.
// KHÔNG tạo đề, KHÔNG đụng Luyện tập/Kiểm tra/Bài tập mẫu (khác upload-lesson.mts).
//
//   npx tsx scripts/update-ly-thuyet-from-bundle.mts <bundle.json | theory.html> --lesson <id> [--dry-run] [--with-title]
//
// Mặc định CHỈ ghi body_html (nội dung lý thuyết); tiêu đề/phụ đề giữ nguyên, thêm --with-title mới ghi.
// Nhận thẳng theory.html (không cần bundle). Khôi phục: scripts/khoi-phuc-ly-thuyet.mts.
//
// Tự sao lưu body_html cũ ra scripts/logs/ trước khi ghi. Đọc khoá từ .env.local.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { bundleToRows, validateBundle, type LessonBundle } from "@/services/lesson-import";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const l = fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
  return l ? l.slice(key.length + 1).trim() : undefined;
}
function fail(m: string): never { console.error("Lỗi:", m); process.exit(1); }

const argv = process.argv.slice(2);
const file = argv.find((a) => !a.startsWith("--") && /\.(json|html)$/.test(a));
const withTitle = argv.includes("--with-title");
const li = argv.indexOf("--lesson");
const lessonId = li >= 0 ? Number(argv[li + 1]) : NaN;
const dry = argv.includes("--dry-run");
if (!file || !lessonId) fail("cần <bundle.json> và --lesson <id>");

const raw = file.endsWith(".html")
  ? { schema: "thachlab.lesson-bundle/v1", target: { class_name: "x", lesson_title: "x" }, theory_title: "Lý thuyết trọng tâm", theory_html: fs.readFileSync(file, "utf8"),
      worked_examples: [], exam: { title: "x", duration_minutes: 10, questions: [{ type: "multiple_choice", question: "x", options: ["a", "b", "c", "d"], answer: 0, explanation: "x" }] }, raster_images: [] }
  : JSON.parse(fs.readFileSync(file, "utf8"));
const check = validateBundle(raw);
if (!check.ok) fail("gói không hợp lệ:\n  - " + check.errors.join("\n  - "));
const rows = bundleToRows(raw as LessonBundle, lessonId);
if (!rows.lyThuyet.body_html.trim()) fail("gói không có phần lý thuyết");

const url = env("NEXT_PUBLIC_SUPABASE_URL"), key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY");
const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

const { data: lesson } = await sb.from("lessons").select("id, title").eq("id", lessonId).single();
if (!lesson) fail(`không thấy bài ${lessonId}`);
console.log(`Bài #${lesson.id} "${lesson.title}"`);
const { data: cur } = await sb.from("lesson_items").select("*").eq("lesson_id", lessonId).eq("kind", "ly_thuyet").maybeSingle();
if (!cur) fail("bài chưa có mục ly_thuyet — dừng (không tự tạo)");

fs.mkdirSync(path.join(root, "scripts/logs"), { recursive: true });
const bak = path.join(root, "scripts/logs", `ly-thuyet-bai${lessonId}-backup-${Date.now()}.json`);
fs.writeFileSync(bak, JSON.stringify(cur, null, 1));
console.log(`Sao lưu: ${bak} (${(cur.body_html ?? "").length} → ${rows.lyThuyet.body_html.length} ký tự)`);
if (dry) { console.log("--dry-run: không ghi"); process.exit(0); }

const patch: Record<string, string> = { body_html: rows.lyThuyet.body_html };
if (withTitle) { patch.title = rows.lyThuyet.title; patch.subtitle = rows.lyThuyet.subtitle; }
const { error } = await sb.from("lesson_items").update(patch).eq("id", cur.id);
if (error) fail(error.message);
console.log(`✓ Đã ghi đè ${Object.keys(patch).join(", ")} của mục Lý thuyết (item ${cur.id}). Mọi cột/mục khác giữ nguyên.`);
