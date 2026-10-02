/**
 * Tải một bài học (Lý thuyết + Bài tập mẫu — đúng phần "bài" mà giáo viên soạn
 * và đăng lên qua skill dang-bai-hoc-thachlab) ngược trở lại thành file
 * Word (.docx) hoặc LaTeX (.tex). Chiều PDF không nằm ở đây — xem
 * LessonDownloadMenu.tsx (in bằng chính bản KaTeX đã render trên trang, chụp
 * "Save as PDF" của trình duyệt là đủ, khỏi dựng PDF tay).
 *
 * Không gồm Luyện tập/Bài tập về nhà/Kiểm tra: các mục đó là ngân hàng đề gắn
 * qua exam_ids, có đáp án — không phải nội dung "bài viết" và có cân nhắc lộ
 * đáp án trước khi làm bài, nên để ngoài phạm vi tính năng này.
 */

import type { LessonItem } from "@/features/lessons/types";
import { parseHtmlToBlocks } from "./html-doc-model";
import { blocksToLatex, escapeLatexText } from "./html-to-latex";
import { buildLessonDocx } from "./docx-writer";

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/** Gộp các mục Lý thuyết + Bài tập mẫu của 1 bài thành 1 khối HTML duy nhất, có tiêu đề mục. */
export function buildLessonArticleHtml(items: LessonItem[]): string {
  const parts: string[] = [];
  const theoryItems = items.filter((i) => i.kind === "ly_thuyet" && i.body_html.trim());
  const workedItems = items.filter((i) => i.kind === "bai_tap_mau" && i.questions?.length);

  theoryItems.forEach((item) => {
    if (theoryItems.length > 1 || item.title) parts.push(`<h2>${escapeHtml(item.title || "Lý thuyết")}</h2>`);
    parts.push(item.body_html);
  });

  workedItems.forEach((item) => {
    parts.push(`<h2>${escapeHtml(item.title || "Bài tập mẫu")}</h2>`);
    item.questions.forEach((q, idx) => {
      if (!q.body_html.trim()) return;
      parts.push(`<h3>${escapeHtml(q.label || `Dạng ${idx + 1}`)}</h3>`);
      parts.push(q.body_html);
    });
  });

  return parts.join("\n");
}

/** Bài có nội dung để tải không (tránh hiện nút tải cho bài chỉ có đề/video). */
export function lessonHasDownloadableContent(items: LessonItem[]): boolean {
  return items.some(
    (i) => (i.kind === "ly_thuyet" && i.body_html.trim()) || (i.kind === "bai_tap_mau" && i.questions?.some((q) => q.body_html.trim())),
  );
}

function toFileSlug(s: string): string {
  const noDia = s
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[đĐ]/g, (m) => (m === "đ" ? "d" : "D"));
  const slug = noDia.trim().replace(/\s+/g, "-").replace(/[^a-zA-Z0-9-]/g, "");
  return slug || "bai-hoc";
}

function downloadBytes(data: Uint8Array | string, mime: string, filename: string) {
  const blob = new Blob([data as BlobPart], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}

export function exportLessonAsLatex(lessonTitle: string, chapterTitle: string, items: LessonItem[]) {
  const html = buildLessonArticleHtml(items);
  const body = blocksToLatex(parseHtmlToBlocks(html));
  const header = [
    `% ${lessonTitle}${chapterTitle ? ` — ${chapterTitle}` : ""}`,
    "% Tải xuống từ thachlab — sửa lại tuỳ ý bằng trình soạn LaTeX quen thuộc.",
    `\\section*{${escapeLatexText(lessonTitle)}}`,
    "",
  ].join("\n");
  downloadBytes(`${header}\n${body}\n`, "text/x-tex;charset=utf-8", `${toFileSlug(lessonTitle)}.tex`);
}

export async function exportLessonAsDocx(lessonTitle: string, chapterTitle: string, items: LessonItem[]) {
  const html = buildLessonArticleHtml(items);
  const blocks = parseHtmlToBlocks(html);
  const bytes = await buildLessonDocx(lessonTitle, chapterTitle, blocks);
  downloadBytes(
    bytes,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    `${toFileSlug(lessonTitle)}.docx`,
  );
}
