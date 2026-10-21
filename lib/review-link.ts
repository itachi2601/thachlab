import { SITE_URL } from "@/lib/site";

/**
 * lib/review-link.ts — "link vào buổi ôn tập theo chặng" của học sinh, dùng chung cho mã QR chiếu ở
 * `/tro-giang/on-tap/chieu` và banner ở `/lop-hoc`. Trang `/lop-hoc/on-tap` tự tìm buổi ôn đang diễn ra của lớp
 * em nên link không cần mã buổi — QR in/chiếu một lần dùng được cho mọi buổi.
 */
export const REVIEW_STUDENT_PATH = "/lop-hoc/on-tap/";

export function reviewStudentUrl(): string {
  return `${SITE_URL}${REVIEW_STUDENT_PATH}`;
}

/** Màn hình điều phối của thầy/trợ giảng. */
export function reviewConsolePath(sessionId: number): string {
  return `/tro-giang/on-tap/?id=${sessionId}`;
}

/** Màn hình chiếu lên tivi (nhân sự đã đăng nhập mở, chỉ hiện số liệu chung). */
export function reviewScreenPath(sessionId: number): string {
  return `/tro-giang/on-tap/chieu/?id=${sessionId}`;
}
