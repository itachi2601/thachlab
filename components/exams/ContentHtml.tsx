"use client";

import { useMemo } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";

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
    if (!html.includes("$")) return html;
    return html.replace(
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
