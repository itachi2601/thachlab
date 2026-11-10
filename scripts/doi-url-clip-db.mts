// Đổi đường dẫn clip tự dựng NGAY TRÊN BẢN DB của mục Lý thuyết (không ghi lại cả bài từ file).
// Dùng khi dựng lại clip (tai-clip-len-storage.mts --ban N) mà DB đang có sửa của phiên khác chưa vào file,
// nên cap-nhat-ly-thuyet.sh --chi-video từ chối. Chỉ thay chuỗi `lesson-clips/clip/<tn>-<ngày>.mp4|webp`
// → `<tn>-<ngày>-<ban>.mp4|webp`, mọi chữ khác giữ nguyên byte-cho-byte. Sao lưu ở scripts/logs/.
//
//   npx tsx scripts/doi-url-clip-db.mts --ngay 20261028 --ban 2 19 9 7 …          # xem thử
//   npx tsx scripts/doi-url-clip-db.mts --ngay 20261028 --ban 2 19 9 7 … --apply
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";

const argv = process.argv.slice(2);
const opt = (k: string) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : undefined; };
const ngay = opt("--ngay"), ban = opt("--ban"), apply = argv.includes("--apply");
const ids = argv.filter((a, i) => /^\d+$/.test(a) && !["--ngay", "--ban"].includes(argv[i - 1])).map(Number);
if (!ngay || !ban || !ids.length) { console.error("Dùng: --ngay YYYYMMDD --ban N <lesson_id>… [--apply]"); process.exit(1); }

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const l = fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
  return l ? l.slice(key.length + 1).trim() : undefined;
}
const url = env("NEXT_PUBLIC_SUPABASE_URL"), key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }
const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

const re = new RegExp(`(lesson-clips/clip/tn-[a-z0-9-]+-${ngay})\\.(mp4|webp)`, "g");
let loi = 0;
for (const id of ids) {
  const { data: cur, error } = await sb.from("lesson_items").select("*").eq("lesson_id", id).eq("kind", "ly_thuyet").maybeSingle();
  if (error || !cur) { console.log(`bài ${id}: ✗ không đọc được mục Lý thuyết`); loi++; continue; }
  const html: string = cur.body_html ?? "";
  const n = (html.match(re) ?? []).length;
  const moi = html.replace(re, `$1-${ban}.$2`);
  const daCo = (html.match(new RegExp(`-${ngay}-${ban}\\.(mp4|webp)`, "g")) ?? []).length;
  console.log(`bài ${id}: ${n} chỗ cần đổi, ${daCo} chỗ đã là bản ${ban}`);
  if (!apply || n === 0) continue;
  const bak = path.join(root, "scripts/logs", `ly-thuyet-bai${id}-doi-url-${Date.now()}.json`);
  fs.writeFileSync(bak, JSON.stringify(cur, null, 1));
  const { data: up, error: e2 } = await sb.from("lesson_items").update({ body_html: moi }).eq("id", cur.id).eq("kind", "ly_thuyet").select("id");
  if (e2 || !up?.length) { console.log(`  ✗ ghi lỗi: ${e2?.message ?? "không dòng nào"}`); loi++; continue; }
  console.log(`  ✓ đã ghi · sao lưu ${path.relative(root, bak)}`);
}
console.log(loi ? `── ${loi} bài lỗi` : "── Xong");
