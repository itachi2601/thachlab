// Chỉ ghi đè mục "Lý thuyết" (lesson_items.kind=ly_thuyet) của một bài từ file bundle.json.
// KHÔNG tạo đề, KHÔNG đụng Luyện tập/Kiểm tra/Bài tập mẫu (khác upload-lesson.mts).
//
//   npx tsx scripts/update-ly-thuyet-from-bundle.mts <bundle.json | theory.html> --lesson <id> [--dry-run] [--with-title]
//
// Mặc định CHỈ ghi body_html (nội dung lý thuyết); tiêu đề/phụ đề giữ nguyên, thêm --with-title mới ghi.
// Nhận thẳng theory.html (không cần bundle). Khôi phục: scripts/khoi-phuc-ly-thuyet.mts.
//
// QUY TẮC (thầy chốt 4/10/2026): đăng bài lý thuyết CHỈ được ghi vào mục Lý thuyết của đúng bài đó,
// KHÔNG làm ảnh hưởng phần còn lại của bài (Luyện tập, Kiểm tra, Bài tập mẫu…) hay bài khác.
// Script tự thực thi quy tắc ấy, không dựa vào việc người chạy nhớ:
//   1. Lọc đúng MỘT mục ly_thuyet của bài; 0 mục hoặc >1 mục → dừng (không tự tạo mục mới).
//   2. Có --dry-run in rõ phạm vi: mục nào sẽ ghi, những mục nào của bài sẽ bị bỏ qua.
//   3. UPDATE ràng buộc cả id lẫn kind='ly_thuyet' và đòi đúng 1 dòng bị ảnh hưởng.
//   4. Chụp toàn bộ lesson_items của bài TRƯỚC và SAU khi ghi rồi đối chiếu: ngoài body_html
//      (và title/subtitle khi --with-title) của mục Lý thuyết, mọi cột/mục khác phải y nguyên.
//      Lệch → in danh sách chỗ lệch + lệnh hoàn tác, exit 1.
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

type Item = Record<string, unknown>;

/** So sánh hai lần chụp lesson_items: trả về danh sách chỗ lệch NGOÀI phạm vi cho phép. */
function diffItemsOutOfScope(before: Item[], after: Item[], targetId: number, allowed: Set<string>): string[] {
  const problems: string[] = [];
  const bById = new Map(before.map((it) => [Number(it.id), it]));
  const aById = new Map(after.map((it) => [Number(it.id), it]));
  if (before.length !== after.length) problems.push(`số mục của bài đổi: ${before.length} → ${after.length}`);
  for (const [id, b] of bById) {
    const a = aById.get(id);
    if (!a) { problems.push(`mục #${id} (${String(b.kind)}) biến mất`); continue; }
    const keys = new Set([...Object.keys(b), ...Object.keys(a)]);
    for (const k of keys) {
      if (JSON.stringify(b[k]) === JSON.stringify(a[k])) continue;
      if (id === targetId && allowed.has(k)) continue;
      problems.push(`mục #${id} (${String(b.kind)}) đổi cột "${k}" — ngoài phạm vi cho phép`);
    }
  }
  for (const id of aById.keys()) if (!bById.has(id)) problems.push(`mục #${id} mới xuất hiện`);
  return problems;
}

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

// 1. Đúng một mục ly_thuyet — không tự tạo, không đoán.
const { data: cur } = await sb.from("lesson_items").select("*").eq("lesson_id", lessonId).eq("kind", "ly_thuyet").maybeSingle();
if (!cur) fail("bài chưa có mục ly_thuyet — dừng (không tự tạo)");

// 2. Chụp toàn bộ mục của bài + in phạm vi để người chạy kiểm bằng mắt trước khi ghi.
const { data: itemsBeforeRaw, error: errBefore } = await sb.from("lesson_items").select("*").eq("lesson_id", lessonId).order("id");
if (errBefore) fail(errBefore.message);
const before = (itemsBeforeRaw ?? []) as Item[];
const others = before.filter((it) => Number(it.id) !== Number(cur.id));
const otherList = others.map((it) => `#${it.id} ${String(it.kind)}`).join(", ");
console.log(`Phạm vi: CHỈ mục #${cur.id} (ly_thuyet). ${others.length} mục khác của bài giữ nguyên${otherList ? ` — ${otherList}` : ""}.`);

fs.mkdirSync(path.join(root, "scripts/logs"), { recursive: true });
const bak = path.join(root, "scripts/logs", `ly-thuyet-bai${lessonId}-backup-${Date.now()}.json`);
fs.writeFileSync(bak, JSON.stringify(cur, null, 1));
console.log(`Sao lưu: ${bak} (${(cur.body_html ?? "").length} → ${rows.lyThuyet.body_html.length} ký tự)`);
if (dry) { console.log("--dry-run: không ghi"); process.exit(0); }

// 3. Ghi, ràng buộc id + kind, đòi đúng 1 dòng.
const patch: Record<string, string> = { body_html: rows.lyThuyet.body_html };
if (withTitle) { patch.title = rows.lyThuyet.title; patch.subtitle = rows.lyThuyet.subtitle; }
const { data: updated, error } = await sb.from("lesson_items").update(patch).eq("id", cur.id).eq("kind", "ly_thuyet").select("id");
if (error) fail(error.message);
if (!updated || updated.length !== 1) fail(`mong đợi ghi đúng 1 mục, thực tế ${updated?.length ?? 0} — kiểm lại DB`);

// 4. Đối chiếu trước/sau: ngoài mục Lý thuyết, không được có gì khác đổi.
const { data: itemsAfterRaw, error: errAfter } = await sb.from("lesson_items").select("*").eq("lesson_id", lessonId).order("id");
if (errAfter) fail(errAfter.message);
const after = (itemsAfterRaw ?? []) as Item[];
const allowed = new Set<string>(["body_html", ...(withTitle ? ["title", "subtitle"] : [])]);
const problems = diffItemsOutOfScope(before, after, Number(cur.id), allowed);
const written = after.find((it) => Number(it.id) === Number(cur.id));
if (written?.body_html !== rows.lyThuyet.body_html) problems.push("nội dung lý thuyết đọc lại không khớp với file gửi lên");

if (problems.length) {
  console.error("✗ Ghi xong nhưng phát hiện thay đổi NGOÀI PHẠM VI (chỉ được đổi mục Lý thuyết):");
  for (const p of problems) console.error("  - " + p);
  console.error(`Hoàn tác mục Lý thuyết: npx tsx scripts/khoi-phuc-ly-thuyet.mts ${bak}`);
  process.exit(1);
}
console.log(`✓ Đã ghi ${Object.keys(patch).join(", ")} của mục Lý thuyết (item ${cur.id}); đã đối chiếu trước/sau: ${others.length} mục khác của bài không đổi.`);
console.log(`Hoàn tác: npx tsx scripts/khoi-phuc-ly-thuyet.mts ${bak}`);
