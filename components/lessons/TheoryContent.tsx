"use client";

/**
 * components/lessons/TheoryContent.tsx
 *
 * Render `body_html` của một mục lý thuyết, có hỗ trợ khối tương tác (widget React).
 *
 * Vì sao không dùng ContentHtml trực tiếp: ContentHtml render HTML thô, không thể nhét
 * component React vào giữa chuỗi. Ở đây cắt chuỗi thành từng mảnh tại các thẻ
 * `<div data-tl-widget="…"></div>` rồi render mảnh HTML + widget xen kẽ.
 *
 * Thứ tự thao tác quan trọng: CẮT TRƯỚC, BỌC ĐOẠN SAU.
 * `wrapTheorySections` bọc mỗi đoạn `<h3>` trong một `<div class="theory-section">` — cắt sau
 * khi bọc sẽ làm thẻ div đó bị hở giữa hai mảnh, và quiz "Kiểm tra nhanh" (cuộn + tô vàng đúng
 * đoạn khi trả lời sai) sẽ chỉ tô được nửa đoạn. Vì vậy cắt chuỗi thô trước, rồi bọc từng mảnh
 * với `startIndex` nối tiếp để id `theory-sec-<item>-<i>` vẫn khớp `theorySection` đã ghi trong
 * scripts/data/theory-quiz/<lesson>.json.
 */

import { useMemo } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import { splitTheoryWidgets, wrapTheorySections } from "@/features/lessons/theory-sections";
import TheoryWidget from "./TheoryWidget";

type Block =
  | { kind: "html"; html: string }
  | { kind: "widget"; name: string };

export default function TheoryContent({
  html,
  itemId,
  className = "block leading-relaxed",
}: {
  html: string;
  itemId: number | string;
  className?: string;
}) {
  const blocks = useMemo<Block[]>(() => {
    const out: Block[] = [];
    let sectionIndex = 0;
    for (const segment of splitTheoryWidgets(html)) {
      if (segment.kind === "widget") {
        out.push(segment);
        continue;
      }
      const wrapped = wrapTheorySections(segment.html, itemId, sectionIndex);
      sectionIndex += wrapped.sections.length;
      if (wrapped.html.trim()) out.push({ kind: "html", html: wrapped.html });
    }
    return out;
  }, [html, itemId]);

  return (
    <>
      {blocks.map((block, i) =>
        block.kind === "widget" ? (
          <TheoryWidget key={`w-${i}-${block.name}`} name={block.name} />
        ) : (
          <ContentHtml key={`h-${i}`} html={block.html} className={className} />
        ),
      )}
    </>
  );
}
