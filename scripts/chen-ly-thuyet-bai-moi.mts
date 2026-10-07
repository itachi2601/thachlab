// Chèn mục "Lý thuyết" (kind=ly_thuyet) cho bài CHƯA có mục nào. CHỈ INSERT 1 dòng; từ chối nếu bài đã có
// ly_thuyet (bài đã có thì dùng scripts/cap-nhat-ly-thuyet.sh) và KHÔNG đụng Luyện tập/Kiểm tra/Bài tập mẫu.
//
//   npx tsx scripts/chen-ly-thuyet-bai-moi.mts <bundle.json> --lesson <id> [--dry-run]
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createClient } from "@supabase/supabase-js";
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
const file = argv.find((a) => !a.startsWith("--") && a.endsWith(".json"));
const li = argv.indexOf("--lesson");
const lessonId = li >= 0 ? Number(argv[li + 1]) : NaN;
const dry = argv.includes("--dry-run");
if (!file || !lessonId) fail("cần <bundle.json> và --lesson <id>");

const raw = JSON.parse(fs.readFileSync(file, "utf8"));
const check = validateBundle(raw);
if (!check.ok) fail("gói không hợp lệ:\n  - " + check.errors.join("\n  - "));
const row = bundleToRows(raw as LessonBundle, lessonId).lyThuyet;
if (!row.body_html.trim()) fail("gói không có phần lý thuyết");

const url = env("NEXT_PUBLIC_SUPABASE_URL"), key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY");
const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

const { data: lesson } = await sb.from("lessons").select("id, title").eq("id", lessonId).single();
if (!lesson) fail(`không thấy bài ${lessonId}`);
console.log(`Bài #${lesson.id} "${lesson.title}"`);
const { data: items, error: e1 } = await sb.from("lesson_items").select("id, kind").eq("lesson_id", lessonId);
if (e1) fail(e1.message);
console.log(`  mục hiện có: ${(items ?? []).map((i) => `${i.kind}#${i.id}`).join(", ") || "(trống)"}`);
if ((items ?? []).some((i) => i.kind === "ly_thuyet")) fail("bài đã có mục ly_thuyet — dùng cap-nhat-ly-thuyet.sh");
console.log(`  sẽ chèn: "${row.title}" · ${row.body_html.length} ký tự · sort_order ${row.sort_order}`);
if (dry) { console.log("  (dry-run, chưa ghi)"); process.exit(0); }

const { data: ins, error } = await sb.from("lesson_items").insert(row).select("id").single();
if (error) fail("insert: " + error.message);
const { data: after } = await sb.from("lesson_items").select("id, kind").eq("lesson_id", lessonId);
console.log(`  ✓ đã chèn mục #${ins.id}. Mục sau khi ghi: ${(after ?? []).map((i) => `${i.kind}#${i.id}`).join(", ")}`);
