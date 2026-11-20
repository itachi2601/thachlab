import { type LessonItemKind } from "@/features/lessons/types";

/** Một màu nhấn duy nhất cho cả trang — tránh mỗi mục một màu gây phân tâm. */
export const ACCENT = "#3B82F6";

/** Nhãn ngắn cho tab — tên đầy đủ (SECTION_META) quá dài để nằm cạnh nhau trên một hàng tab. */
export const TAB_LABEL: Record<LessonItemKind, string> = {
  ly_thuyet: "Lý thuyết",
  video: "Video",
  bai_tap_mau: "Bài mẫu",
  luyen_tap: "Luyện tập",
  bai_tap_ve_nha: "BTVN",
  kiem_tra: "Kiểm tra",
};

/** Slug trên URL hash cho từng tab — `#muc=luyen-tap` để chia sẻ link đúng tab đang mở. */
export const TAB_SLUG: Record<LessonItemKind, string> = {
  ly_thuyet: "ly-thuyet",
  video: "video",
  bai_tap_mau: "bai-tap-mau",
  luyen_tap: "luyen-tap",
  bai_tap_ve_nha: "btvn",
  kiem_tra: "kiem-tra",
};

export const SLUG_TAB = Object.fromEntries(
  Object.entries(TAB_SLUG).map(([kind, slug]) => [slug, kind as LessonItemKind]),
) as Record<string, LessonItemKind>;

/** 3 mức cỡ chữ đọc (A− / A / A+) — nhân vào cỡ chữ gốc của khối nội dung. */
export const FONT_SCALES = [0.94, 1, 1.08];
export const FONT_STORE = "thachlab-read-font";
export const DIM_STORE = "thachlab-read-dim";
export const LESSON_DONE_STORE = "thachlab-lesson-done-";
/** Mục <h3> lý thuyết đọc dở lần trước, theo lesson_items.id — để "Tiếp tục" trỏ đúng chỗ (L5). */
export const THEORY_POS_STORE = "thachlab-theory-pos-";
/** Mục xa nhất trong mục lục em đã đọc tới, theo bài + tab — để rail đánh ✓ các mục trước đó (B7). */
export const TOC_READ_STORE = "thachlab-toc-read-";
/** Sự kiện nội bộ: yêu cầu TheoryBlock mở một mục <h3> đang thu gọn trước khi cuộn/tô tới nó
 *  (mục lục, "Ôn ngay", thẻ câu sai) — detail là id `theory-sec-<itemId>-<n>`. */
export const OPEN_SECTION_EVENT = "thachlab:open-theory-section";

export function requestOpenTheorySection(hashId: string) {
  window.dispatchEvent(new CustomEvent<string>(OPEN_SECTION_EVENT, { detail: hashId }));
}

/**
 * Đọc tab muốn mở từ hash của URL. Nhận cả 2 kiểu:
 *  - `#muc=luyen-tap` — link chia sẻ tab (trang này tự sinh khi bấm tab)
 *  - `#theory-sec-<itemId>-<n>` — link từ trang làm đề / "Ôn ngay" nhảy tới đúng đoạn lý thuyết
 */
export function parseTabHash(hash: string): { kind: LessonItemKind | null; theoryId: string | null } {
  const raw = hash.replace(/^#/, "");
  if (raw.startsWith("theory-sec-")) return { kind: "ly_thuyet", theoryId: raw };
  for (const part of raw.split("&")) {
    const value = part.startsWith("muc=") ? part.slice(4) : "";
    if (value && SLUG_TAB[value]) return { kind: SLUG_TAB[value], theoryId: null };
  }
  return { kind: null, theoryId: null };
}

export function currentHash() {
  return typeof window === "undefined" ? "" : window.location.hash;
}

/** Cao thêm mà thanh dính (navbar + header bài) che mất khi cuộn tới một đoạn — đo bằng DOM. */
export function stickyOffset() {
  const head = document.querySelector<HTMLElement>(".lesson-head");
  return (head?.offsetHeight ?? 0) + 92;
}

/** Cuộn tới một phần tử với chừa chỗ cho thanh dính; không có id thì cuộn về đầu bài. */
export function scrollToPart(id: string | null) {
  const target = id ? document.getElementById(id) : null;
  if (target) {
    const y = target.getBoundingClientRect().top + window.scrollY - stickyOffset();
    window.scrollTo({ top: Math.max(0, y), behavior: "smooth" });
  } else {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

/** Đổi hash không thêm vào lịch sử duyệt (bấm tab không làm nút "Quay lại" nhảy lung tung). */
export function writeTabHash(hash: string) {
  if (typeof window === "undefined") return;
  window.history.replaceState(null, "", hash || window.location.pathname + window.location.search);
}

/** Cuộn tới + tô vàng một đoạn lý thuyết, tô lại vài nhịp vì bản tĩnh có thể bị bản mới thay thế. */
export function flashTheorySection(hashId: string, times = 6) {
  requestOpenTheorySection(hashId); // mục đang thu gọn thì mở ra trước; các nhịp cuộn lại bên dưới sẽ tới đúng chỗ sau khi React dựng xong
  const el = document.getElementById(hashId);
  if (!el) return;
  el.scrollIntoView({ behavior: "smooth", block: "start" });
  el.classList.add("theory-section--highlight");
  let count = 0;
  const reapply = window.setInterval(() => {
    const target = document.getElementById(hashId);
    target?.classList.add("theory-section--highlight");
    count += 1;
    if (count <= times) target?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 150);
  window.setTimeout(() => {
    window.clearInterval(reapply);
    document.getElementById(hashId)?.classList.remove("theory-section--highlight");
  }, 2600);
}

/** Tô vàng (không giành quyền cuộn) — dùng cho các đoạn phụ khi sai nhiều câu một lúc. */
export function highlightTheorySectionOnly(hashId: string) {
  requestOpenTheorySection(hashId);
  document.getElementById(hashId)?.classList.add("theory-section--highlight");
  window.setTimeout(() => document.getElementById(hashId)?.classList.remove("theory-section--highlight"), 2600);
}
