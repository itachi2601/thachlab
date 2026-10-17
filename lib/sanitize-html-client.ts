import DOMPurify from "dompurify";
import { PURIFY_CONFIG, installIframeHook, installSmilHook } from "./sanitize-html";

/**
 * Sanitize HTML nội dung bài học/câu hỏi ngay trước khi đưa vào dangerouslySetInnerHTML (rà soát bảo mật
 * 17/10/2026, A8). Gọi trên chuỗi CUỐI (sau KaTeX): KaTeX nhận chuỗi thô có `&`, `<`, `>` trong công thức,
 * nên sanitize trước KaTeX sẽ đổi `&` thành `&amp;` và làm hỏng \begin{aligned} a &= b.
 * Cấu hình dùng chung với scripts/thu-sanitize-html.mts (đã thử trên 27.600 chuỗi nội dung thật).
 */
let ready = false;
const cache = new Map<string, string>();
const CACHE_MAX = 300;

export function sanitizeContentHtml(html: string): string {
  // Không có thẻ thì không có gì để gỡ. Phía server (build tĩnh) không có DOM: nội dung lúc build là của repo.
  if (!html.includes("<") || typeof window === "undefined") return html;
  const hit = cache.get(html);
  if (hit !== undefined) return hit;
  if (!ready) {
    installIframeHook(DOMPurify as never);
    installSmilHook(DOMPurify as never);
    ready = true;
  }
  const clean = DOMPurify.sanitize(html, PURIFY_CONFIG as never) as unknown as string;
  if (cache.size >= CACHE_MAX) cache.delete(cache.keys().next().value as string);
  cache.set(html, clean);
  return clean;
}
