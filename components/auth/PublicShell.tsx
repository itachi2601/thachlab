import PreviewAsStudentToggle from "@/components/auth/PreviewAsStudentToggle";
import PublicAuthGate from "@/components/auth/PublicAuthGate";
import BugReportWidget from "@/components/BugReportWidget";

/**
 * Bản "nhẹ" của AuthedShell.tsx — cùng widget nổi, dùng cho route công khai.
 * Khách không có phiên trong localStorage thì không tải supabase-js.
 * Người đã đăng nhập: PublicAuthGate nạp AuthProvider — Navbar hiện tên,
 * admin thấy bảng việc hôm nay trên trang chủ.
 * Trang cần đăng nhập thật (dashboard, lớp học...) vẫn dùng AuthedShell.tsx.
 */
export default function PublicShell({ children }: { children: React.ReactNode }) {
  return (
    <PublicAuthGate>
      {children}
      <PreviewAsStudentToggle />
      <BugReportWidget />
    </PublicAuthGate>
  );
}
