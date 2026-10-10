#!/usr/bin/env node
/**
 * Kiểm chứng đợt đổi màu: bỏ TOÀN BỘ chuỗi trong file rồi so bản HEAD với bản đang làm việc.
 *
 * Vì sao so ở mức "bỏ mọi chuỗi" thay vì chỉ bỏ className: className trong JSX hay viết dạng
 * `className={`…${điều kiện ? "a" : "b"}…`}` nên bỏ mỗi giá trị className là không đủ — cắt theo
 * chuỗi sẽ bắt được mọi thay đổi nằm trong chuỗi (tên class, mã màu, cả chữ hiển thị).
 *
 * Kết luận đọc được:
 *   ✓ mã giống hệt  → file chỉ đổi NỘI DUNG CHUỖI (class/màu) — an toàn với logic.
 *   ⚠ mã khác nhau  → có thay đổi ngoài chuỗi, PHẢI đọc tay (thêm import, đổi cấu trúc, xoá khối…).
 *
 * Kèm cảnh báo chữ hiển thị: nếu một chuỗi dài ≥ 12 ký tự hoặc có dấu tiếng Việt bị thêm/xoá thì
 * in ra — vì đợt này KHÔNG được đổi chữ người dùng đọc.
 *
 *   npx tsx scripts/kiem-doi-mau.mts [--chi-tiet]
 */
import { execFileSync } from "node:child_process";
import fs from "node:fs";

const detail = process.argv.includes("--chi-tiet");

/** Bỏ mọi chuỗi: '…', "…" và `…` (template literal vẫn giữ nguyên phần ${…} bên trong). */
function stripStrings(src: string): string {
  let out = "";
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    if (c === '"' || c === "'") {
      i++;
      while (i < src.length && src[i] !== c) i += src[i] === "\\" ? 2 : 1;
      i++;
      out += '""';
      continue;
    }
    if (c === "`") {
      i++;
      let depth = 0;
      while (i < src.length && (src[i] !== "`" || depth > 0)) {
        if (src[i] === "$" && src[i + 1] === "{") {
          depth++;
          out += "${";
          i += 2;
          continue;
        }
        if (depth > 0 && src[i] === "}") {
          depth--;
          out += "}";
          i++;
          continue;
        }
        // Bên trong ${…} vẫn phải bỏ chuỗi: class hay nằm ở đây, ví dụ
        // `${chọn ? "bg-primary text-white" : "border-line text-ink"}` — bỏ sót là báo động giả.
        if (depth > 0 && (src[i] === '"' || src[i] === "'")) {
          const q = src[i];
          i++;
          while (i < src.length && src[i] !== q) i += src[i] === "\\" ? 2 : 1;
          i++;
          out += '""';
          continue;
        }
        // Trong ${…} phải giữ nguyên mã; ngoài ${…} thì bỏ chữ.
        if (depth > 0) out += src[i];
        i++;
      }
      i++;
      out += "`";
      continue;
    }
    if (c === "/" && src[i + 1] === "/") {
      while (i < src.length && src[i] !== "\n") i++;
      continue;
    }
    if (c === "/" && src[i + 1] === "*") {
      i += 2;
      while (i < src.length && !(src[i] === "*" && src[i + 1] === "/")) i++;
      i += 2;
      continue;
    }
    out += c;
    i++;
  }
  return out;
}

/** Chuỗi "chữ người dùng đọc": dài ≥ 12 ký tự hoặc có dấu tiếng Việt. */
function textStrings(src: string): string[] {
  const found = [];
  for (const m of src.matchAll(/(?<![\\\w])"((?:[^"\\]|\\.){6,})"/g)) {
    const s = m[1];
    if (/[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]/i.test(s) || s.includes(" ")) found.push(s);
  }
  return found;
}

const git = (args: string[]) => execFileSync("git", args, { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });

const changed = git(["diff", "--name-only", "--diff-filter=M", "--", "*.tsx", "*.ts"])
  .split("\n")
  .filter(Boolean);

const clean = [];
const flagged = [];
const textChanged = [];

for (const file of changed) {
  const oldSrc = git(["show", `HEAD:${file}`]);
  const newSrc = fs.readFileSync(file, "utf8");
  const sameCode = stripStrings(oldSrc) === stripStrings(newSrc);

  const before = new Set(textStrings(oldSrc));
  const after = new Set(textStrings(newSrc));
  const added = [...after].filter((s) => !before.has(s));
  const removed = [...before].filter((s) => !after.has(s));
  if (added.length || removed.length) {
    textChanged.push({ file, added, removed });
  }

  if (sameCode) clean.push(file);
  else {
    flagged.push(file);
    if (detail) {
      const a = stripStrings(oldSrc).split("\n");
      const b = stripStrings(newSrc).split("\n");
      let i = 0;
      while (i < Math.min(a.length, b.length) && a[i] === b[i]) i++;
      console.log(`\n— ${file} (dòng ${i + 1})`);
      console.log(`  HEAD: ${(a[i] ?? "").trim().slice(0, 200)}`);
      console.log(`  nay : ${(b[i] ?? "").trim().slice(0, 200)}`);
    }
  }
}

console.log(`\n✓ CHỈ ĐỔI CHUỖI (class/màu) — ${clean.length} file:`);
for (const f of clean) console.log(`   ${f}`);
console.log(`\n⚠ CÓ THAY ĐỔI NGOÀI CHUỖI — ${flagged.length} file:`);
for (const f of flagged) console.log(`   ${f}`);
console.log(`\n📝 CHUỖI CHỮ HIỂN THỊ THÊM/BỚT — ${textChanged.length} file:`);
for (const t of textChanged) {
  console.log(`   ${t.file}`);
  for (const s of t.added) console.log(`      + "${s.slice(0, 90)}"`);
  for (const s of t.removed) console.log(`      - "${s.slice(0, 90)}"`);
}
