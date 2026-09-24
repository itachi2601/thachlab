#!/usr/bin/env node
// Liệt kê ảnh nặng (> 150 KB) trong Supabase Storage — CHỈ DRY-RUN.
// Không upload, không xoá, không sửa gì; chỉ in danh sách để quyết định nén sau.
//
//   node scripts/optimize-storage-images.mjs
//
// Đọc NEXT_PUBLIC_SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY từ biến môi trường
// hoặc .env.local (service role để thấy cả bucket private).
import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { createClient } from "@supabase/supabase-js";

const ROOT = resolve(dirname(new URL(import.meta.url).pathname), "..");
const MIN_BYTES = 150 * 1024;
const IMAGE_EXT = /\.(png|jpe?g|webp|gif|bmp|tiff?|heic|avif)$/i;

function readEnvLocal(key) {
  const p = resolve(ROOT, ".env.local");
  if (!existsSync(p)) return undefined;
  for (const line of readFileSync(p, "utf8").split("\n")) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m && m[1] === key) return m[2].replace(/^["']|["']$/g, "");
  }
  return undefined;
}

const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY (.env.local)");
  process.exit(1);
}
const supabase = createClient(url, key, { auth: { persistSession: false } });

// Duyệt đệ quy một bucket: list() trả cả thư mục (id null) lẫn file (có metadata.size).
async function listAll(bucket, prefix = "", out = []) {
  const PAGE = 1000;
  for (let offset = 0; ; offset += PAGE) {
    const { data, error } = await supabase.storage.from(bucket).list(prefix, { limit: PAGE, offset });
    if (error) throw new Error(`${bucket}/${prefix}: ${error.message}`);
    for (const item of data) {
      const path = prefix ? `${prefix}/${item.name}` : item.name;
      if (item.id === null) await listAll(bucket, path, out);
      else out.push({ bucket, path, size: item.metadata?.size ?? 0, mime: item.metadata?.mimetype ?? "" });
    }
    if (data.length < PAGE) break;
  }
  return out;
}

const { data: buckets, error } = await supabase.storage.listBuckets();
if (error) {
  console.error("listBuckets:", error.message);
  process.exit(1);
}

let grandTotal = 0;
let grandCount = 0;
const heavy = [];
for (const b of buckets) {
  const files = await listAll(b.name);
  const images = files.filter((f) => IMAGE_EXT.test(f.path) || f.mime.startsWith("image/"));
  const total = files.reduce((s, f) => s + f.size, 0);
  const imgTotal = images.reduce((s, f) => s + f.size, 0);
  console.log(`bucket ${b.name}${b.public ? " (public)" : ""}: ${files.length} file, ${(total / 1024 / 1024).toFixed(2)} MB · ảnh: ${images.length} file, ${(imgTotal / 1024 / 1024).toFixed(2)} MB`);
  grandTotal += total;
  grandCount += files.length;
  heavy.push(...images.filter((f) => f.size > MIN_BYTES));
}

heavy.sort((a, b) => b.size - a.size);
console.log(`\nẢnh > ${MIN_BYTES / 1024} KB: ${heavy.length} file, ${(heavy.reduce((s, f) => s + f.size, 0) / 1024 / 1024).toFixed(2)} MB`);
for (const f of heavy) console.log(`${(f.size / 1024).toFixed(0).padStart(6)} KB  ${f.bucket}/${f.path}`);
console.log(`\nTổng Storage: ${grandCount} file, ${(grandTotal / 1024 / 1024).toFixed(2)} MB (dry-run, không thay đổi gì)`);
