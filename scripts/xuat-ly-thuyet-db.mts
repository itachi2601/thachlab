// CHỈ ĐỌC. Xuất body_html của mục Lý thuyết đang có trong DB ra file, để biến đổi ĐÚNG bản đang chạy (giữ bản sửa
// trực tiếp trên web) rồi đẩy lại bằng cap-nhat-ly-thuyet.sh.
//   npx tsx scripts/xuat-ly-thuyet-db.mts <lesson_id> <file_ra.html>
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
const [id, out] = process.argv.slice(2);
if (!id || !out) { console.error("Dùng: npx tsx scripts/xuat-ly-thuyet-db.mts <lesson_id> <file_ra.html>"); process.exit(1); }
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const { data, error } = await sb.from("lesson_items").select("body_html").eq("lesson_id", Number(id)).eq("kind", "ly_thuyet");
if (error || !data || data.length !== 1) { console.error("bài", id, "không có đúng một mục ly_thuyet", error?.message ?? ""); process.exit(1); }
fs.writeFileSync(out, data[0].body_html ?? "", "utf8");
console.log("bài", id, "→", out, (data[0].body_html ?? "").length, "ký tự");
