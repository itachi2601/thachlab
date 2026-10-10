import { SITE_URL } from "@/lib/site";

/**
 * lib/exam-link.ts — một chỗ duy nhất quyết định "link mở một đề" là gì, dùng chung cho:
 *  - mã QR in/chiếu ở trang soạn đề (`components/admin/ExamQrPanel.tsx`),
 *  - mục quét mã của học sinh (`app/quet-ma`).
 *
 * Giữ chung một chỗ vì nếu `/kiem-tra/lam` đổi cách nhận mã đề mà hai nơi lệch nhau thì mã QR
 * in ra sẽ chết im lặng — không có lỗi build nào báo.
 */

/** Đường dẫn làm đề trong app (giữ đúng tham số `?id=` mà `/kiem-tra/lam` đang đọc). */
export function examTakePath(examId: number): string {
  return `/kiem-tra/lam/?id=${examId}`;
}

/** Link đầy đủ để in vào mã QR — điện thoại quét là mở thẳng trình duyệt, không cần cài app. */
export function examQrUrl(examId: number): string {
  return `${SITE_URL}${examTakePath(examId)}`;
}

/**
 * Đọc mã đề từ nội dung mã QR (hoặc từ ô nhập tay của học sinh).
 *
 * Nhận 3 kiểu, theo thứ tự:
 *  1. chỉ là số — `770`, `#770` (nhập tay, hoặc mã in trên bảng);
 *  2. đường dẫn — `/kiem-tra/lam/770`;
 *  3. link có tham số — `https://thachlab.id.vn/kiem-tra/lam/?id=770`, `?id=770&item=123`, hoặc
 *     query trần `?id=770`.
 *
 * Cố ý KHÔNG nhận `?id=` của trang khác: `/lop-hoc/bai/?id=9` (id bài học) mà lọt vào đây sẽ mở
 * nhầm thành đề số 9. Và cũng KHÔNG bao giờ điều hướng theo nội dung quét được — chỉ lấy con số
 * rồi tự dựng đường dẫn nội bộ, nên mã QR giả trỏ ra trang ngoài không dụ được học sinh đi đâu.
 *
 * Trả `null` khi không nhận ra — nơi gọi phải báo lỗi rõ ràng, không im lặng bỏ qua.
 */
export function examIdFromScan(raw: string): number | null {
  const text = raw.trim();
  if (!text) return null;

  const bare = text.match(/^#?\s*(\d{1,7})$/);
  if (bare) return Number(bare[1]);

  const questionAt = text.indexOf("?");
  const hashAt = text.indexOf("#");
  const cutAt = [questionAt, hashAt].filter((i) => i >= 0);
  const path = (cutAt.length ? text.slice(0, Math.min(...cutAt)) : text).replace(/\/+$/, "");
  const query = questionAt >= 0 ? text.slice(questionAt + 1, hashAt > questionAt ? hashAt : undefined) : "";

  const byPath = path.match(/\/kiem-tra\/lam\/(\d{1,7})$/);
  if (byPath) return Number(byPath[1]);

  // `path` rỗng = mã chỉ chứa query (`?id=770`); còn lại phải đúng trang làm đề.
  if (path === "" || /(^|\/)kiem-tra\/lam$/.test(path)) {
    const id = new URLSearchParams(query).get("id")?.trim();
    if (id && /^\d{1,7}$/.test(id)) return Number(id);
  }

  return null;
}
