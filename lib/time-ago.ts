// Tách khỏi services/notifications.ts: hàm thuần, không đụng supabase — để
// components/layout/NotificationBell.tsx (nằm trong Navbar, render ở MỌI trang kể cả
// trang công khai) có thể dùng ngay lúc render (đồng bộ) mà không phải tải cả
// @supabase/supabase-js chỉ để lấy 1 hàm định dạng thời gian.
/** "5 phút trước", "hôm qua"… cho danh sách ngắn. */
export function timeAgo(iso: string): string {
  const diff = (Date.now() - new Date(iso).getTime()) / 1000;
  if (diff < 60) return "vừa xong";
  if (diff < 3600) return `${Math.floor(diff / 60)} phút trước`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} giờ trước`;
  if (diff < 172800) return "hôm qua";
  return new Date(iso).toLocaleDateString("vi-VN");
}
