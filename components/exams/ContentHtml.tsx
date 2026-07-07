"use client";

import { useEffect, useRef } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";

/**
 * Render nội dung câu hỏi: HTML (ảnh công thức, hình vẽ) + LaTeX $...$
 * chuyển thành KaTeX sau khi mount.
 */
export default function ContentHtml({
  html,
  className = "",
}: {
  html: string;
  className?: string;
}) {
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || !el.innerHTML.includes("$")) return;
    // duyệt text node, thay $...$ / $$...$$ bằng KaTeX
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const targets: Text[] = [];
    let node: Node | null;
    while ((node = walker.nextNode())) {
      if ((node.textContent ?? "").includes("$")) targets.push(node as Text);
    }
    for (const textNode of targets) {
      const text = textNode.textContent ?? "";
      const parts = text.split(/(\$\$[^$]+\$\$|\$[^$]+\$)/g);
      if (parts.length === 1) continue;
      const frag = document.createDocumentFragment();
      for (const part of parts) {
        const m = part.match(/^(\$\$?)([^$]+)\$\$?$/);
        if (m) {
          const span = document.createElement("span");
          try {
            katex.render(m[2], span, {
              displayMode: m[1] === "$$",
              throwOnError: false,
            });
            frag.appendChild(span);
            continue;
          } catch {
            /* giữ nguyên văn bản nếu LaTeX lỗi */
          }
        }
        frag.appendChild(document.createTextNode(part));
      }
      textNode.replaceWith(frag);
    }
  }, [html]);

  return (
    <span
      ref={ref}
      className={`exam-content ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
