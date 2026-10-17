/**
 * Cấu hình sanitize HTML nội dung bài học/câu hỏi (rà soát bảo mật 17/10/2026, mục A8).
 * Chưa được ContentHtml dùng — hiện chỉ script thử `scripts/thu-sanitize-html.mts` import để kiểm
 * xem allowlist này gỡ gì khỏi nội dung đang có. Khi bật thật: dùng chung đúng hai hàm này.
 *
 * Nguyên tắc: cho đủ thứ bài học đang dùng (svg + SMIL, MathML của KaTeX, input/details/button, data-*,
 * iframe YouTube-nocookie/PhET); cấm script/style/object/embed/form và mọi on*=.
 */

export const IFRAME_SRC_ALLOW = [/^https:\/\/www\.youtube-nocookie\.com\//, /^https:\/\/phet\.colorado\.edu\//];

export const PURIFY_CONFIG = {
  USE_PROFILES: { html: true, svg: true, svgFilters: true, mathMl: true },
  ADD_TAGS: ["iframe", "animate", "animateTransform", "semantics", "annotation"],
  ADD_ATTR: ["allow", "allowfullscreen", "frameborder", "target", "loading", "decoding", "encoding", "calcMode", "from", "to"],
  FORBID_TAGS: ["script", "style", "object", "embed", "form", "base", "meta", "link"],
  FORBID_ATTR: ["srcdoc"],
  ALLOW_DATA_ATTR: true,
  // Gỡ hẳn thay vì giữ nội dung con của thẻ bị cấm (script/style không có chữ hữu ích cần giữ).
  KEEP_CONTENT: false,
} as const;

/** Tối thiểu của DOMPurify mà hook cần (tránh phụ thuộc kiểu khi chưa cài ở app). */
interface PurifyLike {
  addHook(name: "uponSanitizeElement", fn: (node: Element, data: { tagName: string }) => void): void;
}

/** Iframe chỉ giữ khi `src` thuộc IFRAME_SRC_ALLOW; còn lại bị gỡ nguyên thẻ. */
export function installIframeHook(purify: PurifyLike): void {
  purify.addHook("uponSanitizeElement", (node, data) => {
    if (data.tagName !== "iframe") return;
    const src = node.getAttribute?.("src") ?? "";
    if (!IFRAME_SRC_ALLOW.some((re) => re.test(src))) node.parentNode?.removeChild(node);
  });
}

/**
 * Hình SMIL (`animate`, `animateTransform`) cần các thuộc tính from/to/calcMode, nhưng `animate` còn có thể
 * đổi cả `href`/`on*` của phần tử khác (vector XSS qua attributeName). Chỉ gỡ thẻ khi attributeName nhắm vào đó.
 */
export function installSmilHook(purify: PurifyLike): void {
  purify.addHook("uponSanitizeElement", (node, data) => {
    if (data.tagName !== "animate" && data.tagName !== "animatetransform" && data.tagName !== "set") return;
    const target = node.getAttribute?.("attributeName") ?? "";
    if (/^(xlink:)?href$/i.test(target) || /^on/i.test(target)) node.parentNode?.removeChild(node);
  });
}
