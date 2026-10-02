// Hoàn tác update-ly-thuyet-from-bundle: ghi lại body_html từ file sao lưu trong scripts/logs/.
//   npx tsx scripts/khoi-phuc-ly-thuyet.mts scripts/logs/ly-thuyet-bai31-backup-<ts>.json
// Chỉ ghi body_html của đúng item trong file sao lưu.
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
const file = process.argv[2];
if (!file || !fs.existsSync(file)) { console.error("Dùng: npx tsx scripts/khoi-phuc-ly-thuyet.mts <file-sao-luu.json>"); process.exit(1); }
const bak = JSON.parse(fs.readFileSync(file, "utf8"));
if (!bak.id || typeof bak.body_html !== "string") { console.error("File sao lưu không đúng dạng (cần id, body_html)"); process.exit(1); }
const url = env("NEXT_PUBLIC_SUPABASE_URL"), key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu khoá trong .env.local"); process.exit(1); }
const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
const { error } = await sb.from("lesson_items").update({ body_html: bak.body_html }).eq("id", bak.id);
if (error) { console.error(error.message); process.exit(1); }
console.log(`✓ Đã khôi phục body_html của item ${bak.id} (${bak.body_html.length} ký tự).`);
