// Kiểm thẻ "Vật lý quanh ta": hook/badge/quiz + ảnh thẻ (file, kích thước, ghi công, giấy phép).
// Chạy: npx tsx scripts/kiem-anh-vat-ly-quanh-ta.mts   (exit 1 nếu có LỖI; thiếu ảnh chỉ là CẢNH BÁO)
// Quy tắc: docs/ANH-VAT-LY-QUANH-TA.md
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import matter from "gray-matter";
import sharp from "sharp";

const BLOG = join(process.cwd(), "content", "blog");
const MAX_BYTES = 150 * 1024;
// Chỉ giấy phép mở cho phép dùng lại + sửa + đăng thương mại; NC/ND và "all rights reserved" bị loại.
const LICENSE_OK = /^(CC0( 1\.0)?|Public Domain|CC BY(-SA)? [1-4]\.\d)$/i;
const HOST_OK = /^https:\/\/(thachlab\.id\.vn|commons\.wikimedia\.org|upload\.wikimedia\.org|phet\.colorado\.edu|openverse\.org|www\.flickr\.com)\//;

let errors = 0;
let warns = 0;
const err = (slug: string, msg: string) => { errors++; console.log(`  LỖI     ${slug}: ${msg}`); };
const warn = (slug: string, msg: string) => { warns++; console.log(`  CẢNH BÁO ${slug}: ${msg}`); };

for (const file of readdirSync(BLOG).filter((f) => f.endsWith(".md")).sort()) {
  const slug = file.replace(/\.md$/, "");
  const fm = matter(readFileSync(join(BLOG, file), "utf8")).data as Record<string, any>;
  if (fm.category !== "Vật lý quanh ta") continue;

  if (!fm.hook) err(slug, "thiếu hook");
  if (!fm.badge) err(slug, "thiếu badge");
  const q = fm.quiz;
  if (!q) err(slug, "thiếu quiz");
  else {
    if (!q.question || !q.why) err(slug, "quiz thiếu question/why");
    if (!Array.isArray(q.options) || q.options.length < 2 || q.options.length > 4) err(slug, "quiz cần 2–4 options");
    else {
      if (!Number.isInteger(q.answer) || q.answer < 0 || q.answer >= q.options.length) err(slug, "quiz.answer ngoài phạm vi");
      q.options.forEach((o: string, i: number) => { if (o.length > 70) warn(slug, `option ${"ABCD"[i]} dài ${o.length} ký tự (>70, rút gọn cho thẻ nhỏ)`); });
    }
  }

  if (!fm.photo) { warn(slug, "chưa có ảnh thẻ (đang hiện khung giữ chỗ)"); continue; }
  const path = join(process.cwd(), "public", String(fm.photo).replace(/^\//, ""));
  if (!existsSync(path)) { err(slug, `photo không tồn tại: ${fm.photo}`); continue; }
  if (!/\.webp$/i.test(path)) err(slug, "photo phải là .webp");
  const size = statSync(path).size;
  if (size > MAX_BYTES) err(slug, `photo ${(size / 1024).toFixed(0)} KB > 150 KB`);
  const meta = await sharp(path).metadata();
  const w = meta.width ?? 0, h = meta.height ?? 0;
  if (w > 1200) err(slug, `photo rộng ${w}px > 1200px`);
  if (w < 800) warn(slug, `photo rộng ${w}px < 800px (mờ trên màn lớn)`);
  if (w && h && Math.abs(w / h - 16 / 9) > 0.03) err(slug, `photo ${w}×${h} không phải 16:9`);
  if (!fm.photoAlt || String(fm.photoAlt).length < 15) err(slug, "photoAlt thiếu hoặc quá ngắn (mô tả cái ảnh thể hiện)");
  const c = fm.photoCredit ?? {};
  if (!c.author) err(slug, "photoCredit.author trống");
  if (!c.license || !LICENSE_OK.test(String(c.license).trim())) err(slug, `giấy phép "${c.license ?? ""}" không nằm trong danh sách cho phép (CC0, Public Domain, CC BY, CC BY-SA)`);
  if (!c.sourceUrl || !HOST_OK.test(String(c.sourceUrl))) err(slug, `sourceUrl "${c.sourceUrl ?? ""}" thiếu hoặc không thuộc nguồn đã duyệt`);
  if (/^CC BY/i.test(String(c.license ?? "")) && !c.licenseUrl) warn(slug, "CC BY nên có licenseUrl");
  console.log(`  ok      ${slug}: ảnh ${w}×${h}, ${(size / 1024).toFixed(0)} KB, ${c.license}`);
}
console.log(`\n${errors} lỗi, ${warns} cảnh báo`);
process.exit(errors ? 1 : 0);
