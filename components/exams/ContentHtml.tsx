"use client";

import { useMemo } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";
import imageDimensions from "@/features/lessons/image-dimensions.json";

const IMAGE_DIMENSIONS = imageDimensions as Record<string, number[]>;

/**
 * Ảnh tĩnh (hình vẽ, công thức quét) không có width/height trong HTML lưu —
 * trình duyệt không biết trước tỉ lệ nên chừa 0px chỗ rồi "nhảy" layout khi
 * ảnh tải xong, dễ thấy nhất khi đang cuộn trên điện thoại (chữ bị đè/lệch
 * trong khoảnh khắc ảnh vừa hiện). Gắn sẵn width/height thật (đọc lúc build,
 * xem scripts/gen-image-dimensions.mjs) để trình duyệt trừ chỗ đúng ngay từ đầu.
 * Ảnh trong bài học hầu hết nằm dưới màn hình đầu → gắn thêm decoding="async" cho
 * mọi ảnh, và loading="lazy" cho ảnh đã có width/height (ảnh chưa biết kích thước
 * mà lazy thì layout sẽ nhảy lúc cuộn tới, nên vẫn để tải sớm như cũ).
 */
function withImageDimensions(html: string): string {
  if (!html.includes("<img")) return html;
  return html.replace(/<img\b([^>]*)>/g, (tag, attrs: string) => {
    const decoding = /\bdecoding=/.test(attrs) ? "" : ' decoding="async"';
    const lazy = /\bloading=/.test(attrs) ? "" : ' loading="lazy"';
    if (/\bwidth=/.test(attrs)) return `<img${attrs}${lazy}${decoding}>`;
    const src = attrs.match(/\bsrc="([^"]+)"/)?.[1];
    const dims = src ? IMAGE_DIMENSIONS[src] : undefined;
    if (!dims) return decoding ? `<img${attrs}${decoding}>` : tag;
    return `<img${attrs} width="${dims[0]}" height="${dims[1]}"${lazy}${decoding}>`;
  });
}

/**
 * Dấu vết định dạng Word còn sót lại khi dán qua: dòng chấm dẫn của mục lục
 * ("I. TÓM TẮT.........."), ký tự thay thế khi font/encoding lỗi, và các
 * đoạn liệt kê gõ tay bằng "-"/"•" ở đầu dòng thay vì thẻ <ul><li> thật —
 * đánh dấu lại bằng data-bullet để CSS vẽ chấm đầu dòng thụt lề nhất quán.
 * Bảng dán từ Word có sẵn min-width cố định, tràn màn hình điện thoại nếu
 * để nguyên — bọc riêng một lớp cuộn ngang cho bảng, không đẩy tràn cả trang.
 */
function stripWordArtifacts(html: string): string {
  return html
    .replace(/[�￼]/g, "")
    .replace(/\.{4,}/g, "")
    .replace(/(<p\b[^>]*)>(\s*)[-•●▪][ \t ]+/g, '$1 data-bullet="1">')
    .replace(/<table\b/g, '<div class="table-scroll"><table')
    .replace(/<\/table>/g, "</table></div>");
}

/**
 * Render nội dung câu hỏi/bài học: HTML (ảnh công thức, hình vẽ) + LaTeX $...$.
 * KaTeX được render thành chuỗi HTML trước khi đưa vào React (không biến đổi
 * DOM sau khi mount) nên công thức không bị mất khi React re-render.
 */
export default function ContentHtml({
  html,
  className = "",
}: {
  html: string;
  className?: string;
}) {
  const rendered = useMemo(() => {
    const clean = withImageDimensions(stripWordArtifacts(html));
    if (!clean.includes("$")) return clean;
    return clean.replace(
      /\$\$([^$]+)\$\$|\$([^$]+)\$/g,
      (match, display, inline) => {
        try {
          return katex.renderToString(display ?? inline, {
            displayMode: display !== undefined,
            throwOnError: false,
          });
        } catch {
          return match; // giữ nguyên văn bản nếu LaTeX lỗi
        }
      },
    );
  }, [html]);

  return (
    <span
      className={`exam-content ${className}`}
      dangerouslySetInnerHTML={{ __html: rendered }}
    />
  );
}
