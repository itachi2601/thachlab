/** Đường nội bộ an toàn cho ?next= (một dấu / đầu, không //). */
export function safeNextPath(next: string | null | undefined): string | null {
  if (next && /^\/(?!\/)/.test(next)) return next;
  return null;
}

/**
 * Đích khi đăng nhập không kèm ?next=.
 * Admin về trang chủ — Navbar + bảng việc hôm nay đọc phiên ở đó.
 * Giảng viên vẫn vào /quan-tri (trang đó tự mở đúng khu vực).
 */
export function pathAfterLogin(role: string | null | undefined): string {
  if (role === "admin") return "/";
  if (role === "instructor") return "/quan-tri";
  if (role === "parent") return "/phu-huynh";
  return "/tai-khoan";
}
