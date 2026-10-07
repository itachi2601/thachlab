// Ghi cả `subtitle` ("N dạng bài kèm lời giải") theo số dạng thật — trước đây subtitle cũ ("19 dạng…") còn sót sau khi thay dạng.
// Đăng "Bài tập mẫu có cấu trúc" (scripts/data/bai-tap-mau/<lesson_id>.json, do skill soan-bai-tap-mau sinh)
// vào CHỈ cột `questions` của mục kind='bai_tap_mau' của đúng bài. Không đụng exam_ids/lý thuyết/luyện tập.
// CHẠY TRÊN MAC (service role). --dry-run không kết nối DB. Tự sao lưu `questions` cũ ra scripts/logs/.
//   npx tsx scripts/publish-bai-tap-mau.mts --lesson 57 [--dry-run] [--yes]
// Site tĩnh: ghi xong phải `bash scripts/deploy.sh` mới thấy trên web.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import { composeBody, DATA_DIR, loadTopics, validate, type Dang } from "../.claude/skills/soan-bai-tap-mau/scripts/lib";

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
// --giu-cu: các dạng ĐANG có trong DB (chưa phải dạng mới) được nối vào sau dạng mới, không bị ghi đè.
const keepOld = argv.includes("--giu-cu");
const fromBackup = argv.includes("--cu-tu") ? argv[argv.indexOf("--cu-tu") + 1] : undefined; // khôi phục dạng cũ từ file sao lưu
if (!Number.isInteger(lessonId)) fail("cần --lesson <id>");

const file = path.join(DATA_DIR, `${lessonId}.json`);
if (!fs.existsSync(file)) fail(`không thấy ${path.relative(root, file)}`);
const data = JSON.parse(fs.readFileSync(file, "utf8"));
const topics = loadTopics();
const { errors, warnings } = validate(data, topics);
warnings.forEach((w) => console.warn("  ! " + w));
if (errors.length) fail("không qua validate:\n   - " + errors.join("\n   - "));

const questions = (data.dang_bai as Dang[]).map((d) => ({
  label: d.label,
  body_html: composeBody(d),
  problem_html: d.problem_html,
  analysis_html: d.analysis_html,
  solution_html: d.solution_html,
  topic: d.topic,
  topic_id: topics?.find((t) => t.name.trim() === d.topic.trim())?.id,
  form: d.form ?? "bai_tap",
}));
if (data.tu_luan) questions.push({ label: data.tu_luan.label, body_html: data.tu_luan.body_html } as (typeof questions)[number]); // mục tự luận (dạng cũ biên tập lại) luôn đứng cuối
console.log(`Bài ${lessonId} "${data.lesson_title ?? ""}": ${questions.length} dạng → chỉ ghi lesson_items.questions (kind=bai_tap_mau)`);
questions.forEach((q, i) => console.log(`  ${i + 1}. ${q.label} · topic_id=${q.topic_id ?? "?"} · form=${q.form}`));
if (dry) { console.log("[DRY-RUN] chưa ghi gì."); process.exit(0); }

const url = env("NEXT_PUBLIC_SUPABASE_URL"), key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local");
const sb = createClient(url!, key!, { auth: { persistSession: false, autoRefreshToken: false } });
const { data: rows, error } = await sb.from("lesson_items").select("id, questions, exam_ids").eq("lesson_id", lessonId).eq("kind", "bai_tap_mau");
if (error) fail(error.message);
if (!rows || rows.length !== 1) fail(`bài ${lessonId} có ${rows?.length ?? 0} mục bai_tap_mau (cần đúng 1)`);
const item = rows![0] as { id: number; questions: unknown[]; exam_ids: number[] };
const backup = path.join(root, "scripts/logs", `bai-tap-mau-bai${lessonId}-${Date.now()}.json`);
fs.mkdirSync(path.dirname(backup), { recursive: true });
fs.writeFileSync(backup, JSON.stringify({ item_id: item.id, questions: item.questions }, null, 1));
console.log(`Đã sao lưu ${item.questions?.length ?? 0} dạng cũ → ${path.relative(root, backup)}`);
if (!yes) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const a = await new Promise<string>((r) => rl.question(`Ghi đè questions của mục ${item.id}? [y/N] `, r));
  rl.close();
  if (!/^y$/i.test(a.trim())) { console.log("Dừng."); process.exit(0); }
}
let finalQ: unknown[] = questions;
if (keepOld || fromBackup) {
  const old = (fromBackup ? JSON.parse(fs.readFileSync(fromBackup, "utf8")).questions : item.questions) as { problem_html?: string }[];
  finalQ = [...questions, ...old.filter((q) => !q.problem_html)];
  console.log(`Giữ ${finalQ.length - questions.length} dạng cũ sau ${questions.length} dạng mới.`);
}
const upd = await sb.from("lesson_items").update({ questions: finalQ, subtitle: `${finalQ.length} dạng bài kèm lời giải` }).eq("id", item.id).eq("kind", "bai_tap_mau").select("id");
if (upd.error || upd.data?.length !== 1) fail(upd.error?.message ?? "UPDATE không đúng 1 dòng");
console.log(`✓ Đã ghi. Hoàn tác: cập nhật lại questions từ ${path.relative(root, backup)}. Rồi: bash scripts/deploy.sh`);
