#!/usr/bin/env node
// Nén ảnh tĩnh trong public/ (png/jpg/jpeg > 150 KB) bằng sharp.
//
// Ba chế độ, chọn tự động theo nơi ảnh được tham chiếu:
//   webp    — ảnh chỉ được tham chiếu từ code (app/, components/, content/, …):
//             chuyển sang .webp (rộng tối đa 1200 px, quality 80), xoá file gốc
//             khỏi public/ và cập nhật mọi tham chiếu trong code sang .webp.
//   inplace — ảnh KHÔNG tìm thấy tham chiếu trong code (được nhúng từ HTML lưu
//             trong Supabase lesson_items/bài viết), ảnh trong public/lessons,
//             public/exams, và ảnh OG (og-*.png, ảnh `cover:` của blog dùng cho
//             Facebook/Zalo — không đọc WebP tốt): giữ nguyên tên + định dạng,
//             chỉ nén lại + thu về tối đa 1200 px.
//   dual    — ảnh vừa là OG cover vừa được hiển thị trong trang: sinh .webp cho
//             chỗ hiển thị, đồng thời giữ bản PNG/JPG nén tại chỗ cho OG.
//
// Bản gốc luôn được chép sang public/_originals/<đường dẫn cũ> (đã .gitignore).
// Idempotent: public/_originals/manifest.json ghi ảnh đã xử lý; chạy lại bỏ qua.
//
//   node scripts/optimize-images.mjs            # chạy thật
//   node scripts/optimize-images.mjs --dry-run  # chỉ liệt kê kế hoạch
import { readdirSync, statSync, readFileSync, writeFileSync, mkdirSync, copyFileSync, existsSync, unlinkSync } from "node:fs";
import { join, relative, extname, dirname, resolve } from "node:path";
import sharp from "sharp";

const ROOT = resolve(dirname(new URL(import.meta.url).pathname), "..");
const PUBLIC = join(ROOT, "public");
const ORIGINALS = join(PUBLIC, "_originals");
const MANIFEST = join(ORIGINALS, "manifest.json");
const MIN_BYTES = 150 * 1024;
const MAX_WIDTH = 1200;
const QUALITY = 80;
const DRY = process.argv.includes("--dry-run");

// Thư mục chứa code có thể tham chiếu ảnh public.
const CODE_DIRS = ["app", "components", "lib", "features", "content", "data", "home"];
const CODE_EXT = new Set([".ts", ".tsx", ".js", ".jsx", ".mjs", ".md", ".mdx", ".json", ".css"]);
// Không đụng: bản gốc, mảng CNC/CTTC (vùng riêng).
const SKIP_PREFIX = ["/_originals/", "/images/cnc/"];
// Luôn nén tại chỗ (ảnh nhúng từ HTML trong Supabase).
const INPLACE_PREFIX = ["/lessons/", "/exams/"];

function walk(dir, out = []) {
  let entries;
  try {
    entries = readdirSync(dir);
  } catch {
    return out;
  }
  for (const name of entries) {
    const full = join(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

function publicPath(file) {
  return "/" + relative(PUBLIC, file).split("\\").join("/");
}

function loadManifest() {
  try {
    return JSON.parse(readFileSync(MANIFEST, "utf8"));
  } catch {
    return {};
  }
}

// Đọc toàn bộ file code một lần, tìm nơi tham chiếu từng ảnh.
const codeFiles = CODE_DIRS.flatMap((d) => walk(join(ROOT, d))).filter((f) => CODE_EXT.has(extname(f).toLowerCase()));
const codeText = new Map(codeFiles.map((f) => [f, readFileSync(f, "utf8")]));

function findRefs(pp) {
  const refs = [];
  let isOg = /\/og-[^/]*$/.test(pp); // og-*.png: ảnh openGraph trong metadata
  for (const [file, text] of codeText) {
    if (!text.includes(pp)) continue;
    refs.push(file);
    // Frontmatter blog `cover:` → dùng làm og:image → phải giữ PNG/JPG.
    if (file.endsWith(".md") && new RegExp(`^cover:\\s*["']?${pp.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}`, "m").test(text)) isOg = true;
  }
  return { refs, isOg };
}

function decideMode(pp, refs, isOg) {
  if (INPLACE_PREFIX.some((p) => pp.startsWith(p))) return "inplace";
  if (refs.length === 0) return "inplace";
  if (isOg) {
    // OG-only (không hiển thị ở đâu khác) → inplace; vừa OG vừa hiển thị → dual.
    const displayRefs = refs.filter((f) => {
      const t = codeText.get(f);
      if (f.endsWith(".md")) return new RegExp(`\\]\\(${pp.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\)`).test(t);
      return !/openGraph|twitter/.test(t); // layout/metadata chỉ dùng cho OG
    });
    return displayRefs.length ? "dual" : "inplace";
  }
  return "webp";
}

async function compressInPlace(file, ext) {
  const src = readFileSync(file);
  let pipe = sharp(src).resize({ width: MAX_WIDTH, withoutEnlargement: true });
  pipe = ext === ".png" ? pipe.png({ quality: QUALITY, palette: true, compressionLevel: 9 }) : pipe.jpeg({ quality: QUALITY, mozjpeg: true });
  const out = await pipe.toBuffer();
  if (out.length >= src.length) return src.length; // không nhỏ hơn thì giữ nguyên
  writeFileSync(file, out);
  return out.length;
}

async function toWebp(file, target) {
  const out = await sharp(readFileSync(file)).resize({ width: MAX_WIDTH, withoutEnlargement: true }).webp({ quality: QUALITY }).toBuffer();
  writeFileSync(target, out);
  return out.length;
}

function backup(file, pp) {
  const dest = join(ORIGINALS, pp);
  if (existsSync(dest)) return;
  mkdirSync(dirname(dest), { recursive: true });
  copyFileSync(file, dest);
}

// Đổi tham chiếu .png/.jpg → .webp trong code; bỏ qua dòng `cover:` (OG) của md.
function rewriteRefs(pp, webpPath, refs) {
  for (const f of refs) {
    const text = codeText.get(f);
    const lines = text.split("\n").map((line) => {
      if (f.endsWith(".md") && /^cover:/.test(line)) return line;
      return line.split(pp).join(webpPath);
    });
    const next = lines.join("\n");
    if (next !== text) {
      codeText.set(f, next);
      if (!DRY) writeFileSync(f, next);
    }
  }
}

function dirSize(dir) {
  return walk(dir).reduce((s, f) => s + statSync(f).size, 0);
}

const manifest = loadManifest();
const before = dirSize(PUBLIC) - (existsSync(ORIGINALS) ? dirSize(ORIGINALS) : 0);
const candidates = walk(PUBLIC).filter((f) => {
  const ext = extname(f).toLowerCase();
  const pp = publicPath(f);
  return [".png", ".jpg", ".jpeg"].includes(ext) && !SKIP_PREFIX.some((p) => pp.startsWith(p)) && statSync(f).size > MIN_BYTES;
});

const summary = { webp: [], inplace: [], dual: [], skipped: [] };
for (const file of candidates.sort()) {
  const pp = publicPath(file);
  const ext = extname(file).toLowerCase();
  if (manifest[pp]) {
    summary.skipped.push(pp);
    continue;
  }
  const { refs, isOg } = findRefs(pp);
  const mode = decideMode(pp, refs, isOg);
  const originalBytes = statSync(file).size;
  const meta = await sharp(file).metadata();
  const webpPath = pp.replace(/\.(png|jpe?g)$/i, ".webp");
  const entry = { mode, originalBytes, width: meta.width, height: meta.height, refs: refs.map((f) => relative(ROOT, f)), date: new Date().toISOString() };
  console.log(`${mode.padEnd(7)} ${(originalBytes / 1024).toFixed(0).padStart(5)} KB  ${meta.width}x${meta.height}  ${pp}${refs.length ? "" : "  (không có tham chiếu trong code)"}`);
  if (DRY) continue;

  backup(file, pp);
  if (mode === "inplace") {
    entry.newBytes = await compressInPlace(file, ext);
  } else if (mode === "webp") {
    const target = join(PUBLIC, webpPath);
    entry.newBytes = await toWebp(file, target);
    entry.output = webpPath;
    unlinkSync(file);
    rewriteRefs(pp, webpPath, refs);
  } else {
    const target = join(PUBLIC, webpPath);
    entry.webpBytes = await toWebp(file, target);
    entry.output = webpPath;
    entry.newBytes = await compressInPlace(file, ext);
    rewriteRefs(pp, webpPath, refs);
  }
  manifest[pp] = entry;
  summary[mode].push(pp);
}

if (!DRY) {
  mkdirSync(ORIGINALS, { recursive: true });
  writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2));
}
const after = dirSize(PUBLIC) - (existsSync(ORIGINALS) ? dirSize(ORIGINALS) : 0);
console.log(`\nwebp: ${summary.webp.length} · inplace: ${summary.inplace.length} · dual: ${summary.dual.length} · bỏ qua (đã nén): ${summary.skipped.length}`);
console.log(`public/ (không tính _originals): ${(before / 1024 / 1024).toFixed(2)} MB → ${(after / 1024 / 1024).toFixed(2)} MB`);
