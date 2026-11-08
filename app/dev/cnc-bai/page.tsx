"use client";

/**
 * XEM THỬ khuôn bài CNC mới (Lý thuyết · Video · Luyện tập · BTVN · Kiểm tra, cây 4 chương) không qua cổng ghi danh:
 * http://localhost:3000/dev/cnc-bai?bai=lesson-2 (bài mở sẵn theo ?bai=). Không có courseId nên không ghi tiến độ,
 * không hiện quiz chuẩn bị.
 */
import CncCourseWorkspace from "@/components/lessons/CncCourseWorkspace";

export default function CncBaiPreviewPage() {
  return <CncCourseWorkspace />;
}
