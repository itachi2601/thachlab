import AuthedShell from "@/components/auth/AuthedShell";

// /quet-ma cần biết vai để thanh đáy hiện đúng bộ nút (học sinh đã đăng nhập không được thấy
// tab "Đăng nhập"). KHÔNG bọc RequireAuth: khách vẫn quét được, chỉ tới lúc mở đề mới cần đăng
// nhập — và RequireAuth ở /kiem-tra/lam giờ giữ `?next=` nên em quay lại đúng đề vừa quét.
export default function Layout({ children }: { children: React.ReactNode }) {
  return <AuthedShell>{children}</AuthedShell>;
}
