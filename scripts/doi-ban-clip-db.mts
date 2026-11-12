// Đổi clip tự dựng sang bản dựng lại NGÀY KHÁC ngay trên DB mục Lý thuyết (tự tìm bài chứa URL cũ).
// Chỉ thay chuỗi `lesson-clips/clip/<tn>-<cu>.mp4|webp` → `<tn>-<moi>.mp4|webp` cho đúng các tn đưa vào;
// mọi chữ khác giữ nguyên byte-cho-byte. Sao lưu từng bài ở scripts/logs/ trước khi ghi.
//
//   npx tsx scripts/doi-ban-clip-db.mts --cu 20261028-2 --moi 20261112-2 --tn tn-l12-a-01,tn-l12-b-02          # xem thử
//   npx tsx scripts/doi-ban-clip-db.mts --cu 20261028-2 --moi 20261112-2 --tn ... --apply
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";

const argv = process.argv.slice(2);
const opt = (k: string) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : undefined; };
const cu = opt("--cu"), moi = opt("--moi"), tns = (opt("--tn") ?? "").split(",").filter(Boolean), apply = argv.includes("--apply");
if (!cu || !moi || !tns.length || !tns.every((t) => /^tn-[a-z0-9-]+$/.test(t))) {
  console.error("Dùng: --cu YYYYMMDD-N --moi YYYYMMDD-N --tn tn-a,tn-b [--apply]"); process.exit(1);
}
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

const re = new RegExp(`(lesson-clips/clip/(?:${tns.join("|")}))-${cu}\\.(mp4|webp)`, "g");
const { data: rows, error } = await sb.from("lesson_items").select("*").eq("kind", "ly_thuyet").like("body_html", `%-${cu}.mp4%`);
if (error) { console.error("✗ đọc lỗi:", error.message); process.exit(1); }
let loi = 0, tong = 0;
const conLai = new Set(tns);
for (const cur of rows ?? []) {
  const html: string = cur.body_html ?? "";
  const hits = html.match(re) ?? [];
  if (!hits.length) continue;
  hits.forEach((h) => conLai.delete(h.replace(/^lesson-clips\/clip\//, "").replace(new RegExp(`-${cu}\\.(mp4|webp)$`), "")));
  tong += hits.length;
  const moiHtml = html.replace(re, `$1-${moi}.$2`);
  console.log(`bài ${cur.lesson_id} (item ${cur.id}): ${hits.length} chỗ · độ dài ${html.length} → ${moiHtml.length}`);
  if (!apply) continue;
  const bak = path.join(root, "scripts/logs", `ly-thuyet-bai${cur.lesson_id}-doi-ban-clip-${Date.now()}.json`);
  fs.mkdirSync(path.dirname(bak), { recursive: true });
  fs.writeFileSync(bak, JSON.stringify(cur, null, 1));
  const { data: up, error: e2 } = await sb.from("lesson_items").update({ body_html: moiHtml }).eq("id", cur.id).eq("kind", "ly_thuyet").select("id");
  if (e2 || !up?.length) { console.log(`  ✗ ghi lỗi: ${e2?.message ?? "không dòng nào"}`); loi++; continue; }
  console.log(`  ✓ đã ghi · sao lưu ${path.relative(root, bak)}`);
}
console.log(`── ${tong} chỗ${conLai.size ? ` · KHÔNG thấy trong DB: ${[...conLai].join(", ")}` : " · đủ mọi tn"}${loi ? ` · ${loi} bài lỗi` : ""}`);
