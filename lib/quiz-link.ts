import { SITE_URL } from "@/lib/site";

/**
 * lib/quiz-link.ts — "link vào một phòng Hoạt động lớp học" (PIN 6 số), dùng chung cho:
 *  - mã QR chiếu ở phòng chờ (`components/quiz-live/QuizHostRoom.tsx`),
 *  - mục quét mã của học sinh (`app/quet-ma`), cùng chỗ với mã QR của đề (`lib/exam-link.ts`).
 *
 * `/choi` đọc tham số `?pin=` — đổi tham số ở đó thì phải đổi ở đây, nếu không mã QR chết im lặng.
 */

export function quizJoinPath(pin: string): string {
  return `/choi/?pin=${pin}`;
}

export function quizJoinUrl(pin: string): string {
  return `${SITE_URL}${quizJoinPath(pin)}`;
}

/**
 * Đọc PIN từ nội dung mã QR. CHỈ nhận link/đường dẫn của trang `/choi` có `?pin=` đủ 6 số —
 * cố ý không nhận số trần, vì 6 số trần có thể là số đề (`lib/exam-link.ts`).
 * Không điều hướng theo nội dung quét: chỉ lấy 6 chữ số rồi tự dựng đường dẫn nội bộ.
 */
export function quizPinFromScan(raw: string): string | null {
  const text = raw.trim();
  const q = text.indexOf("?");
  if (q < 0) return null;
  const hash = text.indexOf("#");
  const path = text.slice(0, q).replace(/\/+$/, "");
  if (!/(^|\/)choi$/.test(path)) return null;
  const pin = new URLSearchParams(text.slice(q + 1, hash > q ? hash : undefined)).get("pin")?.trim();
  return pin && /^\d{6}$/.test(pin) ? pin : null;
}
