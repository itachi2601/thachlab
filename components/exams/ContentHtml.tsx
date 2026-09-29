"use client";

import { useEffect, useMemo, useState } from "react";
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
    .replace(/(<p\b[^>]*)>(\s*)[-•●▪][ \t ]+/g, '$1 data-bullet="1">')
    .replace(/<table\b/g, '<div class="table-scroll"><table')
    .replace(/<\/table>/g, "</table></div>");
}

// Nhận diện cả 3 kiểu đánh dấu công thức: "$…$"/"$$…$$" (Azota, phổ biến nhất
// trong dữ liệu hiện có) và "\(…\)"/"\[…\]" (một số nguồn dán vào theo chuẩn
// LaTeX gốc). Chỉ cần MỘT trong 3 ký hiệu xuất hiện là coi như "có thể có công
// thức" — quyết định có tải KaTeX (~290 KB) hay không dựa vào đây.
const MATH_MARKER = /\$|\\\(|\\\[/;
const MATH_PATTERN = /\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$|\\\(([\s\S]+?)\\\)|\\\[([\s\S]+?)\\\]/g;

function hasMath(html: string): boolean {
  return MATH_MARKER.test(html);
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/**
 * Trong lúc chờ KaTeX tải xong (hoặc nếu tải lỗi): hiện nguyên văn LaTeX bọc
 * trong <code> — học sinh vẫn đọc được ký hiệu thô ngay lập tức, không có
 * skeleton/khoảng trắng nên không nhảy layout khi công thức "biến hình" lúc
 * KaTeX tải xong (kích thước <code> và công thức render đã render gần giống
 * nhau về chiều cao dòng).
 */
function renderRawFallback(html: string): string {
  if (!hasMath(html)) return html;
  return html.replace(
    MATH_PATTERN,
    (match) => `<code class="exam-content-raw-tex">${escapeHtml(match)}</code>`,
  );
}

type KatexModule = typeof import("katex");

let katexPromise: Promise<KatexModule> | null = null;

function loadKatex(): Promise<KatexModule> {
  if (!katexPromise) {
    katexPromise = Promise.all([import("katex"), import("katex/dist/katex.min.css")]).then(
      ([mod]) => (("default" in mod ? mod.default : mod) as unknown as KatexModule),
    );
  }
  return katexPromise;
}

function renderWithKatex(html: string, katex: KatexModule): string {
  return html.replace(MATH_PATTERN, (match, display, inline, parenInline, bracketDisplay) => {
    const tex = display ?? inline ?? parenInline ?? bracketDisplay;
    const displayMode = display !== undefined || bracketDisplay !== undefined;
    try {
      return katex.renderToString(tex, { displayMode, throwOnError: false });
    } catch {
      return match; // giữ nguyên văn bản nếu LaTeX lỗi
    }
  });
}

/**
 * Render nội dung câu hỏi/bài học: HTML (ảnh công thức, hình vẽ) + LaTeX $...$.
 *
 * KaTeX (~290 KB) không còn nằm trong JS ban đầu của trang — chỉ `import()`
 * lúc component thực sự mount VÀ nội dung có dấu hiệu công thức ($, \(, \[).
 * Nội dung không có công thức thì không đụng tới KaTeX chút nào (không tải
 * chunk, không có CSS). Khi KaTeX tải xong, công thức được render thành chuỗi
 * HTML rồi đưa vào React (không biến đổi DOM sau khi mount) nên không bị mất
 * khi React re-render.
 */
export default function ContentHtml({
  html,
  className = "",
}: {
  html: string;
  className?: string;
}) {
  const cleaned = useMemo(() => withImageDimensions(stripWordArtifacts(html)), [html]);
  const needsMath = useMemo(() => hasMath(cleaned), [cleaned]);

  // Chỉ giữ bản KaTeX đã render xong ỨNG VỚI đúng `cleaned` hiện tại (so khớp bằng
  // `forHtml`) — html đổi thì coi như chưa có, tự rơi về fallback thô bên dưới mà
  // không cần gọi setState đồng bộ trong effect để "reset" (tránh cascading renders).
  const [katexResult, setKatexResult] = useState<{ forHtml: string; rendered: string } | null>(
    null,
  );

  useEffect(() => {
    if (!needsMath) return; // không có công thức thì không đụng tới KaTeX chút nào
    let cancelled = false;
    loadKatex()
      .then((katex) => {
        if (!cancelled) setKatexResult({ forHtml: cleaned, rendered: renderWithKatex(cleaned, katex) });
      })
      .catch(() => {
        // Tải chunk lỗi (mất mạng, 404…) — giữ nguyên fallback văn bản thô, không kẹt trắng.
      });
    return () => {
      cancelled = true;
    };
  }, [cleaned, needsMath]);

  const rendered = !needsMath
    ? cleaned
    : katexResult && katexResult.forHtml === cleaned
      ? katexResult.rendered
      : renderRawFallback(cleaned);

  return (
    <span
      className={`exam-content ${className}`}
      dangerouslySetInnerHTML={{ __html: rendered }}
    />
  );
}
