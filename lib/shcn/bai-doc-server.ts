// Đọc bản sinh viên của bài SHCN lúc build (Server Component) — chỉ file .sv.md.
import { readFileSync } from "node:fs";
import { join } from "node:path";
import matter from "gray-matter";
import { marked } from "marked";
import { findBaiDoc, type BaiDoc } from "./bai-doc";

const SRC = join(process.cwd(), "content", "shcn-3-nam");

export function readBaiDoc(hk: string, bai: string): (BaiDoc & { muc_tieu: string; html: string }) | null {
  const meta = findBaiDoc(`${hk}/${bai}`);
  if (!meta || !/^hk\d$/.test(hk) || !/^b\d\d$/.test(bai)) return null;
  const { content } = matter(readFileSync(join(SRC, hk, `${bai}.sv.md`), "utf8"));
  // Bỏ tiêu đề "# …" (trang tự in tiêu đề — N4) và tách câu mục tiêu in nghiêng ngay sau nó.
  let body = content.replace(/^\s*# .*\n/, "");
  let muc_tieu = "";
  const goal = body.match(/^\s*\*([^*\n]+)\*\s*\n/);
  if (goal) {
    muc_tieu = goal[1].trim();
    body = body.slice(goal[0].length);
  }
  // Bảng rộng cuộn ngang trong khung riêng, trang không cuộn ngang ở 375px.
  const html = (marked.parse(body, { gfm: true, breaks: false }) as string)
    .replace(/<table>/g, '<div class="shcn-table-wrap"><table>')
    .replace(/<\/table>/g, "</table></div>");
  return { ...meta, muc_tieu, html };
}
