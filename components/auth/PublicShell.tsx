import PreviewAsStudentToggle from "@/components/auth/PreviewAsStudentToggle";
import PreviewAsTaToggle from "@/components/tro-giang/PreviewAsTaToggle";
import BugReportWidget from "@/components/BugReportWidget";

/**
 * Bản "nhẹ" của AuthedShell.tsx — cùng 3 widget nổi (để giao diện không đổi) nhưng
 * KHÔNG bọc AuthProvider, nên KHÔNG kéo theo supabase-js/GoTrue. Dùng cho nhóm route
 * công khai, chưa cần đăng nhập: xem app/(public)/layout.tsx.
 *
 * useAuth() bên trong 3 component này (từ components/auth/auth-context.tsx) sẽ rơi về
 * giá trị mặc định "khách" (session/profile null, loading false) vì không có Provider
 * nào ở trên — đúng với người dùng ẩn danh, là đa số truy cập các trang này. Trường hợp
 * hiếm: một admin/giảng viên đang đăng nhập mà ghé các trang này sẽ tạm thời thấy Navbar
 * và các nút này ở trạng thái "khách" (không thấy avatar/link báo lỗi đã gửi) — đây là
 * đánh đổi có chủ đích để đổi lấy việc bỏ ~211KB GoTrue khỏi trang công khai; các trang
 * cần đăng nhập thật (dashboard, lớp học...) vẫn dùng AuthedShell.tsx, không đổi gì.
 */
export default function PublicShell({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <PreviewAsStudentToggle />
      <PreviewAsTaToggle />
      <BugReportWidget />
    </>
  );
}
