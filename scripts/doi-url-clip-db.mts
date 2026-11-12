// Đổi đường dẫn clip tự dựng NGAY TRÊN BẢN DB của mục Lý thuyết (không ghi lại cả bài từ file).
// Dùng khi dựng lại clip (tai-clip-len-storage.mts --ban N) mà DB đang có sửa của phiên khác chưa vào file,
// nên cap-nhat-ly-thuyet.sh --chi-video từ chối. Chỉ thay chuỗi `lesson-clips/clip/<tn>-<ngày>.mp4|webp`
// → `<tn>-<ngày>-<ban>.mp4|webp`, mọi chữ khác giữ nguyên byte-cho-byte. Sao lưu ở scripts/logs/.
//
//   npx tsx scripts/doi-url-clip-db.mts --ngay 20261028 --ban 2 19 9 7 …          # xem thử
//   npx tsx scripts/doi-url-clip-db.mts --ngay 20261028 --ban 2 19 9 7 … --apply
// Đổi MỘT thí nghiệm sang bản mới khác ngày (12/11/2026): --tn <id> --cu <hậu tố cũ> → <tn>-<ngay>-<ban>.
//   npx tsx scripts/doi-url-clip-db.mts --tn tn-l9-ohm-01 --cu 20261105 --ngay 20261112 --ban 2 [<lesson_id>…] [--apply]
//   (không nêu lesson_id thì tự tìm các mục Lý thuyết có chứa URL cũ)
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";

const argv = process.argv.slice(2);
const opt = (k: string) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : undefined; };
const ngay = opt("--ngay"), ban = opt("--ban"), apply = argv.includes("--apply");
const tnMot = opt("--tn"), cu = opt("--cu");
const ids = argv.filter((a, i) => /^\d+$/.test(a) && !["--ngay", "--ban", "--cu"].includes(argv[i - 1])).map(Number);
if ((tnMot && !cu) || (!tnMot && cu)) { console.error("--tn và --cu đi cùng nhau"); process.exit(1); }
if (!ngay || !ban || (!ids.length && !tnMot)) { console.error("Dùng: --ngay YYYYMMDD --ban N <lesson_id>… [--apply]"); process.exit(1); }

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

const esc = (x: string) => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const re = tnMot
  ? new RegExp(`(lesson-clips/clip/${esc(tnMot)}-)${esc(cu!)}\\.(mp4|webp)`, "g")
  : new RegExp(`(lesson-clips/clip/tn-[a-z0-9-]+-${ngay})\\.(mp4|webp)`, "g");
const thay = tnMot ? `$1${ngay}-${ban}.$2` : `$1-${ban}.$2`;
if (tnMot && !ids.length) {
  const { data, error } = await sb.from("lesson_items").select("lesson_id").eq("kind", "ly_thuyet")
    .like("body_html", `%clip/${tnMot}-${cu}.mp4%`);
  if (error) { console.error("✗ tìm bài:", error.message); process.exit(1); }
  ids.push(...new Set((data ?? []).map((r) => Number(r.lesson_id))));
  console.log(`${tnMot}-${cu}: thấy trong bài ${ids.join(", ") || "(không bài nào)"}`);
}
let loi = 0;
for (const id of ids) {
  const { data: cur, error } = await sb.from("lesson_items").select("*").eq("lesson_id", id).eq("kind", "ly_thuyet").maybeSingle();
  if (error || !cur) { console.log(`bài ${id}: ✗ không đọc được mục Lý thuyết`); loi++; continue; }
  const html: string = cur.body_html ?? "";
  const n = (html.match(re) ?? []).length;
  const moi = html.replace(re, thay);
  const daCo = (html.match(new RegExp(`${tnMot ? esc(tnMot) + "-" : "-"}${ngay}-${ban}\\.(mp4|webp)`, "g")) ?? []).length;
  console.log(`bài ${id}: ${n} chỗ cần đổi, ${daCo} chỗ đã là bản ${ban}`);
  if (!apply || n === 0) continue;
  const bak = path.join(root, "scripts/logs", `ly-thuyet-bai${id}-doi-url-${Date.now()}.json`);
  fs.writeFileSync(bak, JSON.stringify(cur, null, 1));
  const { data: up, error: e2 } = await sb.from("lesson_items").update({ body_html: moi }).eq("id", cur.id).eq("kind", "ly_thuyet").select("id");
  if (e2 || !up?.length) { console.log(`  ✗ ghi lỗi: ${e2?.message ?? "không dòng nào"}`); loi++; continue; }
  console.log(`  ✓ đã ghi · sao lưu ${path.relative(root, bak)}`);
}
console.log(loi ? `── ${loi} bài lỗi` : "── Xong");
