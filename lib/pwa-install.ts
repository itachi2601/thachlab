/**
 * lib/pwa-install.ts — móc nhỏ cho banner "Thêm vào màn hình chính" (GĐ 2.6 / M1).
 *
 * Chỗ GỌI cần thêm (chưa làm vì file thuộc phiên M2): khi học sinh nộp xong lần luyện tập ĐẦU TIÊN
 * (sau khi savePracticeSession thành công), gọi `markFirstPracticeDone()`. Hàm tự chỉ ghi nhận một lần.
 */

export const PWA_FIRST_PRACTICE_KEY = "thachlab-pwa-first-practice";
export const PWA_BANNER_SEEN_KEY = "thachlab-pwa-banner-seen";
export const PWA_FIRST_PRACTICE_EVENT = "thachlab:first-practice-done";

export function markFirstPracticeDone() {
  if (typeof window === "undefined") return;
  try {
    if (localStorage.getItem(PWA_FIRST_PRACTICE_KEY)) return;
    localStorage.setItem(PWA_FIRST_PRACTICE_KEY, "1");
  } catch {
    // localStorage bị chặn: vẫn phát sự kiện trong phiên này.
  }
  window.dispatchEvent(new Event(PWA_FIRST_PRACTICE_EVENT));
}
