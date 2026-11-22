#!/usr/bin/env node
// Chèn "Chuyện có thật" (content/shcn-3-nam/chuyen-that/bai/*.md) vào bài SHCN:
//   - bản SV  hk*/bNN.sv.md : mục "## Chuyện có thật" ngay trước "## 3 điều cần nhớ"
//   - bản GV  hk*/bNN.gv.md : mục "## Chuyện có thật — cách dùng" ngay trước "## Phiếu hoạt động"
// Khối chèn nằm giữa hai dấu <!-- chuyen-that:start/end --> nên chạy lại bao nhiêu lần cũng được
// (thay khối cũ). Xoá file chuyện → chạy lại sẽ gỡ khối khỏi bài.
//
//   node scripts/chen-chuyen-that-shcn.mjs           # ghi
//   node scripts/chen-chuyen-that-shcn.mjs --dry-run # chỉ liệt kê
//
// Sau khi chạy: node scripts/gen-shcn-bai-doc.mjs (nếu có bài HK đã mở) rồi build/deploy như thường.
import { existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import matter from "gray-matter";

const DRY = process.argv.includes("--dry-run");
const root = join(import.meta.dirname, "..");
const src = join(root, "content", "shcn-3-nam");
const khoDir = join(src, "chuyen-that", "bai");
const START = "<!-- chuyen-that:start -->";
const END = "<!-- chuyen-that:end -->";
const blockRe = new RegExp(`${START}[\\s\\S]*?${END}\\n*`, "g");

/** @type {Map<string, {data: any, body: string, file: string}>} */
const stories = new Map();
for (const f of readdirSync(khoDir).filter((f) => f.endsWith(".md")).sort()) {
  const { data, content } = matter(readFileSync(join(khoDir, f), "utf8"));
  const bai = String(data.bai ?? "");
  if (!/^hk\d-b\d\d$/.test(bai)) throw new Error(`${f}: thiếu/sai "bai" (vd hk1-b10)`);
  for (const k of ["nguon", "link", "cau_hoi"]) if (!data[k]) throw new Error(`${f}: thiếu "${k}"`);
  if (stories.has(bai)) throw new Error(`${f}: trùng bài ${bai} với ${stories.get(bai).file}`);
  stories.set(bai, { data, body: content.trim(), file: f });
}

function nguonLine(d) {
  const note = d.ghi_chu_nguon ? ` ${String(d.ghi_chu_nguon).trim()}` : "";
  return `*Kể lại tóm tắt theo ${d.nguon} — [đọc bài gốc](${d.link}).${note}*`;
}

function svBlock({ data, body }) {
  return `${START}\n## Chuyện có thật\n\n${body}\n\n${nguonLine(data)}\n\n**Bạn nghĩ sao:** ${data.cau_hoi}\n${END}\n\n`;
}

function gvBlock({ data, body }) {
  return (
    `${START}\n## Chuyện có thật — cách dùng\n\n` +
    `Dùng ở **Mở (2')** thay chuyện nhân vật giả định, hoặc ở **Chốt** nếu còn 1 phút: đọc to (khoảng 1 phút), rồi hỏi:\n\n` +
    `> "${data.cau_hoi}"\n\n` +
    `Không bắt SV kể chuyện riêng của mình. Nguồn: ${data.nguon} — ${data.link}\n\n` +
    `${body.replace(/^/gm, "> ")}\n${END}\n\n`
  );
}

function apply(file, block, anchor) {
  const before = readFileSync(file, "utf8");
  let s = before.replace(blockRe, "");
  if (block) {
    const i = s.indexOf(`\n${anchor}`);
    if (i < 0) throw new Error(`${file}: không thấy "${anchor}"`);
    s = s.slice(0, i + 1) + block + s.slice(i + 1);
  }
  if (s !== before) {
    if (!DRY) writeFileSync(file, s);
    return true;
  }
  return false;
}

let changed = 0;
for (const hkDir of readdirSync(src).filter((d) => /^hk\d$/.test(d)).sort()) {
  for (const f of readdirSync(join(src, hkDir)).filter((f) => /^b\d\d\.sv\.md$/.test(f)).sort()) {
    const bai = `${hkDir}-${f.slice(0, 3)}`;
    const st = stories.get(bai);
    const sv = join(src, hkDir, f);
    const gv = join(src, hkDir, f.replace(".sv.", ".gv."));
    const a = apply(sv, st ? svBlock(st) : "", "## 3 điều cần nhớ");
    const b = existsSync(gv) ? apply(gv, st ? gvBlock(st) : "", "## Phiếu hoạt động") : false;
    if (a || b) {
      changed++;
      console.log(`${DRY ? "[dry] " : ""}${bai}: ${st ? `chèn ${st.file}` : "gỡ khối cũ"}`);
    }
    stories.delete(bai);
  }
}
for (const [bai, st] of stories) console.warn(`! ${st.file}: không có bài ${bai}`);
console.log(`${changed} bài thay đổi${DRY ? " (dry-run)" : ""}.`);
