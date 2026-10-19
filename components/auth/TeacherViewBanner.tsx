"use client";

import { useAuth } from "@/components/auth/auth-context";
import { useTeacherView } from "@/components/auth/useTeacherView";

/**
 * Một dòng nhận biết (N1, G1): chế độ giáo viên, kèm lối bật "Xem như học sinh"
 * bằng đúng setPreviewAsStudent của AuthProvider. Nền sáng dùng token có sẵn.
 * Admin đã có pill thoát ở PreviewAsStudentToggle; giảng viên và trợ giảng
 * không có pill đó nên khi đang xem như học sinh thì dòng này đổi thành nút Thoát.
 */
export default function TeacherViewBanner() {
  const { isTeacherView } = useTeacherView();
  const { realProfile, previewAsStudent, setPreviewAsStudent } = useAuth();
  const role = realProfile?.role;
  const exitForStaff = previewAsStudent && (role === "instructor" || role === "tro_giang");

  if (!isTeacherView && !exitForStaff) return null;

  return (
    <div className="flex flex-wrap items-center justify-between gap-x-3 gap-y-1 border-b border-line bg-panel px-4 text-sm text-muted">
      <span>{exitForStaff ? "Đang xem như học sinh" : "Chế độ giáo viên"}</span>
      <button
        type="button"
        onClick={() => setPreviewAsStudent(!exitForStaff)}
        className="inline-flex min-h-11 items-center px-3 font-semibold text-primary"
      >
        {exitForStaff ? "Thoát" : "Xem như học sinh"}
      </button>
    </div>
  );
}
