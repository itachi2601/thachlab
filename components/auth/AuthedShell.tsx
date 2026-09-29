import AuthProvider from "@/components/auth/AuthProvider";
import PreviewAsStudentToggle from "@/components/auth/PreviewAsStudentToggle";
import PreviewAsTaToggle from "@/components/tro-giang/PreviewAsTaToggle";
import BugReportWidget from "@/components/BugReportWidget";

/**
 * Bọc auth thật (AuthProvider, có supabase-js/GoTrue) + 2 nút nổi + widget báo lỗi —
 * dùng trong layout.tsx của TỪNG nhóm route cần đăng nhập (dashboard, lớp học, kiểm
 * tra, quản trị, tài khoản...). Trước đây khối này nằm thẳng trong app/layout.tsx (áp
 * dụng cho MỌI trang kể cả trang công khai chưa đăng nhập); giờ tách ra để các trang
 * công khai (/, /blog, /khoa-hoc) không phải tải GoTrue.
 *
 * Trang công khai vẫn cần 3 widget này hiện ra y như cũ (không đổi giao diện) nhưng
 * KHÔNG có AuthProvider — xem app/(public)/layout.tsx, dùng cùng 3 component nhưng
 * không bọc AuthProvider (useAuth() ở đó tự rơi về giá trị mặc định "khách" nhờ
 * components/auth/auth-context.tsx tách riêng, không kéo theo supabase-js).
 */
export default function AuthedShell({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      {children}
      <PreviewAsStudentToggle />
      <PreviewAsTaToggle />
      <BugReportWidget />
    </AuthProvider>
  );
}
