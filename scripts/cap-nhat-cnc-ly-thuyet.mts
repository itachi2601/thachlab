// Chỉ ghi đè cột body_html của MỘT bài trong cnc_lessons (CTTC/CNC) từ theory.html — không đụng tiêu đề,
// thời lượng, tài nguyên, sort_order, video, tệp, đề. Tự sao lưu body_html cũ ra scripts/logs/.
//
//   npx tsx scripts/cap-nhat-cnc-ly-thuyet.mts <theory.html> --lesson lesson-1 [--dry-run]
//
// Hoàn tác: npx tsx scripts/cap-nhat-cnc-ly-thuyet.mts <file sao lưu .html> --lesson lesson-1
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const l = fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
  return l ? l.slice(key.length + 1).trim() : undefined;
}
function fail(m: string): never { console.error("Lỗi:", m); process.exit(1); }

const args = process.argv.slice(2);
const src = args.find((a) => !a.startsWith("--") && a !== args[args.indexOf("--lesson") + 1]);
const lesson = args[args.indexOf("--lesson") + 1];
const dry = args.includes("--dry-run");
if (!src || !fs.existsSync(src) || !lesson || lesson.startsWith("--")) fail("Dùng: <theory.html> --lesson <id> [--dry-run]");

const html = fs.readFileSync(src, "utf8");
if (/<script|<style|\son\w+\s*=/i.test(html)) fail("HTML chứa <script>/<style>/on*= — không được phép.");
if ((html.match(/\$/g) ?? []).length % 2) fail("Số dấu $ lẻ.");

const url = env("NEXT_PUBLIC_SUPABASE_URL");
const key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local");
const db = createClient(url, key, { auth: { persistSession: false } });

const { data: before, error } = await db.from("cnc_lessons").select("*").eq("id", lesson);
if (error) fail(error.message);
if (!before || before.length !== 1) fail(`Phải có đúng 1 bài id=${lesson}, thấy ${before?.length ?? 0}.`);
const old = before[0];
console.log(`Bài: ${old.id} — ${old.title}`);
console.log(`body_html: ${(old.body_html as string).length} → ${html.length} ký tự. Chỉ cột body_html bị ghi.`);
if (dry) { console.log("--dry-run: chưa ghi."); process.exit(0); }

fs.mkdirSync(path.join(root, "scripts/logs"), { recursive: true });
const bak = path.join(root, `scripts/logs/cnc-${lesson}-body-backup-${Date.now()}.html`);
fs.writeFileSync(bak, old.body_html as string);
console.log("Sao lưu:", bak);

const { data: upd, error: e2 } = await db.from("cnc_lessons").update({ body_html: html }).eq("id", lesson).select("*");
if (e2) fail(e2.message);
if (!upd || upd.length !== 1) fail(`UPDATE ảnh hưởng ${upd?.length ?? 0} dòng, mong đợi 1.`);
const diff = Object.keys(old).filter((k) => k !== "body_html" && JSON.stringify(old[k]) !== JSON.stringify(upd[0][k]));
if (diff.length) fail(`Cột khác đã đổi: ${diff.join(", ")}. Hoàn tác bằng file sao lưu ở trên.`);
console.log("Đã ghi body_html; các cột khác y nguyên. Hoàn tác: npx tsx scripts/cap-nhat-cnc-ly-thuyet.mts", bak, "--lesson", lesson);
