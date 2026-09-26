import AuthedShell from "@/components/auth/AuthedShell";

// /tin-tuc lọc bài theo lớp cho học sinh ĐANG ĐĂNG NHẬP (xem app/tin-tuc/page.tsx —
// dùng session thật để gọi fetchMyClassIds), nên KHÔNG đưa vào nhóm (public) dù trang
// này khách vãng lai cũng xem được — nếu bỏ AuthProvider, học sinh đã đăng nhập sẽ bị
// lộ thấy bài của lớp khác (giống chế độ khách/quản trị) thay vì chỉ bài lớp mình.
export default function Layout({ children }: { children: React.ReactNode }) {
  return <AuthedShell>{children}</AuthedShell>;
}
