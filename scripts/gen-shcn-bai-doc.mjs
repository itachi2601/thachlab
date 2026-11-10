#!/usr/bin/env node
// Sinh lib/shcn/bai-doc.json — danh mục bài đọc SHCN (bản sinh viên) ĐÃ MỞ cho sinh viên.
// Dùng ở: trang /sinh-hoat/[hk]/[bai] (generateStaticParams), ô "Bài đọc tuần này" của GVCN,
// thẻ tuần của sinh viên. Chạy lại mỗi khi sửa content/shcn-3-nam/hk*/b??.sv.md hoặc mở thêm HK:
//
//   node scripts/gen-shcn-bai-doc.mjs
//
// Chỉ bản .sv.md được đưa lên web; kịch bản giảng viên (.gv.md) chỉ xuất Word, không bao giờ
// vào site (site tĩnh: mọi file build ra đều mở được bằng link).
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import matter from "gray-matter";

/** Học kì đã mở cho sinh viên. Mở thêm: thêm số vào đây rồi chạy lại script. */
const PUBLISHED_HK = [1];

const root = join(import.meta.dirname, "..");
const src = join(root, "content", "shcn-3-nam");
const list = [];
for (const hk of PUBLISHED_HK) {
  const dir = join(src, `hk${hk}`);
  for (const file of readdirSync(dir).filter((f) => /^b\d\d\.sv\.md$/.test(f)).sort()) {
    const { data } = matter(readFileSync(join(dir, file), "utf8"));
    const bai = file.slice(0, 3);
    list.push({
      key: `hk${hk}/${bai}`,
      hk,
      bai: Number(bai.slice(1)),
      ten: String(data.ten ?? "").trim(),
      chu_de: String(data.chu_de ?? "").trim(),
      trong_tam: String(data.trong_tam ?? "").trim(),
    });
  }
}
writeFileSync(join(root, "lib", "shcn", "bai-doc.json"), JSON.stringify(list, null, 2) + "\n");
console.log(`lib/shcn/bai-doc.json: ${list.length} bài (HK ${PUBLISHED_HK.join(", ")})`);
