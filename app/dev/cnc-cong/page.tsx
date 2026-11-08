"use client";

/**
 * XEM THỬ dải 5 cổng G1–G5 với dữ liệu mẫu (không đăng nhập, không ghi gì):
 * http://localhost:3000/dev/cnc-cong — G1 đạt · G2 đang làm 4/6 · G3 chưa làm · G4 chờ duyệt (làm đủ bài, chưa duyệt) · G5 chưa mở.
 */
import CncCourseWorkspace from "@/components/lessons/CncCourseWorkspace";

const DEMO = {
  passed: [
    "lesson-1:final",
    "lesson-2:exercise-1",
    "lesson-2:exercise-2",
    "lesson-2:exercise-3-short",
    "lesson-2:exercise-3",
    ...["lesson-4-turn", "lesson-4-mill"].flatMap((id) => [`${id}:machine-operation`, `${id}:tool-setup`, `${id}:checklist`]),
  ],
  approved: [],
};

export default function CncCongPreviewPage() {
  return <CncCourseWorkspace demo={DEMO} />;
}
