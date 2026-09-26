import AuthedShell from "@/components/auth/AuthedShell";

// /khoa-hoc (danh sách, ẩn danh) đã chuyển sang app/(public)/khoa-hoc/ — không có
// AuthProvider. Trang /khoa-hoc/dang-ky vẫn ở đây (path không đổi) vì cần biết đã đăng
// nhập chưa (useAuth) để tự điền / chuyển hướng, nên có layout riêng bọc AuthedShell.
export default function Layout({ children }: { children: React.ReactNode }) {
  return <AuthedShell>{children}</AuthedShell>;
}
