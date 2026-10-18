// Thêm MỘT bài mới vào cnc_lessons từ theory.html. Chỉ INSERT (id chưa tồn tại), không đụng bài cũ.
//
//   npx tsx scripts/them-bai-cnc.mts <theory.html> --meta <meta.json> [--dry-run]   (meta: id, title, short, duration)
//   hoặc: … --id flip-1 --title "…" --short "…" --duration "…"
//
// Hoàn tác: xoá đúng dòng đó — delete from cnc_lessons where id = '<id>' (script in sẵn lệnh).
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
const opt = (n: string) => { const i = args.indexOf(`--${n}`); return i >= 0 ? args[i + 1] : undefined; };
const src = args[0];
const metaPath = opt("meta");
const meta: Record<string, string> = metaPath && fs.existsSync(metaPath) ? JSON.parse(fs.readFileSync(metaPath, "utf8")) : {};
const id = opt("id") ?? meta.id, title = opt("title") ?? meta.title, short = opt("short") ?? meta.short, duration = opt("duration") ?? meta.duration ?? "";
const dry = args.includes("--dry-run");
if (!src || src.startsWith("--") || !fs.existsSync(src) || !id || !title || !short) fail("Dùng: <theory.html> --id <id> --title … --short … [--duration …] [--dry-run]");

const html = fs.readFileSync(src, "utf8");
if (/<script|<style|\son\w+\s*=/i.test(html)) fail("HTML chứa <script>/<style>/on*= — không được phép.");
if ((html.match(/\$/g) ?? []).length % 2) fail("Số dấu $ lẻ.");

const url = env("NEXT_PUBLIC_SUPABASE_URL");
const key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local");
const db = createClient(url, key, { auth: { persistSession: false } });

const { data: all, error } = await db.from("cnc_lessons").select("id, title, sort_order").order("sort_order");
if (error) fail(error.message);
console.log("Hiện có:", (all ?? []).map((r) => `${r.id}(${r.sort_order})`).join(", "));
if ((all ?? []).some((r) => r.id === id)) fail(`id=${id} đã tồn tại — dùng cap-nhat-cnc-ly-thuyet.mts để sửa.`);
const sortOrder = Math.max(0, ...(all ?? []).map((r) => (r.sort_order as number) ?? 0)) + 1;
console.log(`Sẽ thêm: id=${id}, sort_order=${sortOrder}, ${html.length} ký tự body_html.`);
if (dry) { console.log("--dry-run: chưa ghi."); process.exit(0); }

const { data: ins, error: e2 } = await db.from("cnc_lessons").insert({
  id, title, short_title: short, duration_label: duration, emphasis: null, body_html: html, resources: [], sort_order: sortOrder,
}).select("id, sort_order");
if (e2) fail(e2.message);
console.log("Đã thêm:", JSON.stringify(ins));
console.log(`Hoàn tác (SQL): delete from cnc_lessons where id = '${id}';`);
