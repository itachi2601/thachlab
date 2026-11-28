"use client";

/**
 * XEM THỬ màn chấm thi thực hành CNC trên điện thoại với SV mẫu (không cần đăng nhập; chưa đăng nhập thì
 * danh sách trống điểm, bấm Lưu sẽ báo lỗi quyền — không ghi gì): http://localhost:3000/dev/cnc-cham
 */
import TeacherRubricExamPanel from "@/components/dashboard/TeacherRubricExamPanel";

const STUDENTS = ["SV mẫu An", "SV mẫu Bình", "SV mẫu Chi", "SV mẫu Dũng", "SV mẫu Hà"].map((name, i) => ({
  id: `00000000-0000-0000-0000-00000000000${i + 1}`,
  name,
  className: "CĐT mẫu",
  records: [],
}));

export default function CncChamPreviewPage() {
  return <main className="mx-auto max-w-3xl px-4 py-6">
    <TeacherRubricExamPanel courseId={-1} students={STUDENTS} />
  </main>;
}
