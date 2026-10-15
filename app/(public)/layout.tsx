import PublicShell from "@/components/auth/PublicShell";

// Nhóm route công khai — không đăng nhập cũng xem được: trang chủ, /blog, /khoa-hoc
// (danh sách khoá học, ẩn danh xem được). Khách không tải AuthProvider (xem PublicShell.tsx).
// Có phiên trong localStorage thì PublicAuthGate mới nạp SDK.
//
// /khoa-hoc/dang-ky KHÔNG nằm trong nhóm này — trang đó cần biết đã đăng nhập chưa nên
// vẫn ở app/khoa-hoc/dang-ky/ với layout riêng bọc AuthProvider thật (xem file đó).
export default function PublicLayout({ children }: { children: React.ReactNode }) {
  return <PublicShell>{children}</PublicShell>;
}
