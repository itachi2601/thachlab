// Tạo mục "Các dạng bài tập" (kind='bai_tap_mau') rỗng cho một bài chưa có — để publish-bai-tap-mau.mts ghi được.
// CHẠY TRÊN MAC (service role). Chỉ INSERT một dòng; từ chối nếu bài đã có mục này.
//   npx tsx scripts/tao-muc-bai-tap-mau.mts --lesson 10 [--dry-run] [--yes]
// Rồi ngay sau: npx tsx scripts/publish-bai-tap-mau.mts --lesson 10  (mục rỗng không hiện nội dung cho HS tới lúc đó)
// Hoàn tác: xoá dòng có id in ra ở cuối (delete from lesson_items where id = <id> and kind='bai_tap_mau').
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const fail = (m: string): never => { console.error("Lỗi:", m); process.exit(1); };
const env = (k: string) => {
  const p = path.join(root, ".env.local");
  const l = fs.existsSync(p) ? fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(k + "=")) : undefined;
  return process.env[k] ?? l?.slice(k.length + 1).trim();
};
const argv = process.argv.slice(2);
const lessonId = Number(argv[argv.indexOf("--lesson") + 1]);
const dry = argv.includes("--dry-run"), yes = argv.includes("--yes");
if (!Number.isInteger(lessonId)) fail("cần --lesson <id>");

const url = env("NEXT_PUBLIC_SUPABASE_URL"), key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local");
const sb = createClient(url!, key!, { auth: { persistSession: false, autoRefreshToken: false } });

const { data: lesson, error: le } = await sb.from("lessons").select("id, title").eq("id", lessonId).maybeSingle();
if (le) fail(le.message);
if (!lesson) fail(`không có bài id=${lessonId}`);
const { data: items, error } = await sb.from("lesson_items").select("id, kind, sort_order").eq("lesson_id", lessonId);
if (error) fail(error.message);
console.log(`Bài ${lessonId} "${lesson!.title}" hiện có:`, (items ?? []).map((i) => `#${i.id} ${i.kind} (sort ${i.sort_order})`).join(", ") || "(không mục nào)");
if ((items ?? []).some((i) => i.kind === "bai_tap_mau")) fail("bài đã có mục bai_tap_mau — không tạo thêm; dùng publish-bai-tap-mau.mts");

const row = { lesson_id: lessonId, kind: "bai_tap_mau", title: "Các dạng bài tập", subtitle: "", video_url: "", pdf_url: "", sort_order: 3,
  exam_ids: [] as number[], questions: [] as unknown[], due_at: null, quiz_min_correct: null, practice_pass_score: null, required: true, published_at: new Date().toISOString() };
console.log("Sẽ INSERT:", JSON.stringify({ ...row, questions: "[]" }));
if (dry) { console.log("[DRY-RUN] chưa ghi gì."); process.exit(0); }
if (!yes) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const a = await new Promise<string>((r) => rl.question("Tạo mục này? [y/N] ", r));
  rl.close();
  if (!/^y$/i.test(a.trim())) { console.log("Dừng."); process.exit(0); }
}
const ins = await sb.from("lesson_items").insert(row).select("id").single();
if (ins.error) fail(ins.error.message);
console.log(`✓ Đã tạo mục #${ins.data!.id}. Tiếp: npx tsx scripts/publish-bai-tap-mau.mts --lesson ${lessonId}  rồi  bash scripts/deploy.sh`);
console.log(`Hoàn tác: delete from lesson_items where id = ${ins.data!.id} and kind = 'bai_tap_mau';`);
