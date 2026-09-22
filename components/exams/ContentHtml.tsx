"use client";

import { useMemo } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";

/**
 * Dấu vết định dạng Word còn sót lại khi dán qua: dòng chấm dẫn của mục lục
 * ("I. TÓM TẮT.........."), ký tự thay thế khi font/encoding lỗi, và các
 * đoạn liệt kê gõ tay bằng "-"/"•" ở đầu dòng thay vì thẻ <ul><li> thật —
 * đánh dấu lại bằng data-bullet để CSS vẽ chấm đầu dòng thụt lề nhất quán.
 */
function stripWordArtifacts(html: string): string {
  return html
    .replace(/[�￼]/g, "")
    .replace(/\.{4,}/g, "")
    .replace(/(<p\b[^>]*)>(\s*)[-•●▪][ \t ]+/g, '$1 data-bullet="1">');
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
    const clean = stripWordArtifacts(html);
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
