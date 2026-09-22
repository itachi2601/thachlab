#!/usr/bin/env node
// Quét ảnh tĩnh trong public/lessons + public/exams, đọc kích thước thật từ header
// file (không cần thư viện ảnh), ghi ra features/lessons/image-dimensions.json.
// ContentHtml dùng bảng này để gắn width/height vào <img class="figure">, giúp
// trình duyệt trừ sẵn chỗ trước khi ảnh tải xong — tránh chữ bị "nhảy"/đè lên
// nhau khi cuộn trên điện thoại (ảnh chưa có kích thước intrinsic thì layout
// nhảy mỗi lần ảnh tải xong). Chạy tự động trước mỗi lần build (xem package.json).
import { readdirSync, statSync, readFileSync, writeFileSync } from "node:fs";
import { join, relative, extname } from "node:path";

const ROOTS = ["public/lessons", "public/exams"];
const OUT = "features/lessons/image-dimensions.json";

function pngSize(buf) {
  if (buf.length < 24 || buf.readUInt32BE(0) !== 0x89504e47) return null;
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

function jpegSize(buf) {
  if (buf.length < 4 || buf[0] !== 0xff || buf[1] !== 0xd8) return null;
  let offset = 2;
  while (offset < buf.length) {
    if (buf[offset] !== 0xff) return null;
    const marker = buf[offset + 1];
    if (marker === 0xd8 || marker === 0xd9) {
      offset += 2;
      continue;
    }
    const len = buf.readUInt16BE(offset + 2);
    // SOF0..SOF15 (trừ DHT/JPG ext) chứa kích thước ảnh thật.
    if (marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc) {
      return { height: buf.readUInt16BE(offset + 5), width: buf.readUInt16BE(offset + 7) };
    }
    offset += 2 + len;
  }
  return null;
}

function sizeOf(path) {
  const buf = readFileSync(path);
  const ext = extname(path).toLowerCase();
  if (ext === ".png") return pngSize(buf);
  if (ext === ".jpg" || ext === ".jpeg") return jpegSize(buf);
  return null;
}

function walk(dir, out) {
  let entries;
  try {
    entries = readdirSync(dir);
  } catch {
    return;
  }
  for (const name of entries) {
    const full = join(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) walk(full, out);
    else {
      const size = sizeOf(full);
      if (size) {
        const publicPath = "/" + relative("public", full).split("\\").join("/");
        out[publicPath] = [size.width, size.height];
      }
    }
  }
}

const map = {};
for (const root of ROOTS) walk(root, map);
writeFileSync(OUT, JSON.stringify(map));
console.log(`✓ ${OUT}: ${Object.keys(map).length} ảnh`);
