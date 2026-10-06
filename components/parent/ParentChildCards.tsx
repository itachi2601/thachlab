"use client";

import CatchupCard from "@/components/results/CatchupCard";
import ParentHomeworkNotes from "@/components/results/ParentHomeworkNotes";
import ParentUpcoming from "@/components/parent/ParentUpcoming";
import ParentAttendanceCard from "@/components/parent/ParentAttendanceCard";
import ParentStanding from "@/components/parent/ParentStanding";
import type { ComponentProps } from "react";

/**
 * Gom 5 thẻ nhỏ dưới phần tóm tắt kết quả của con (app/phu-huynh/page.tsx, `afterSummary`) vào MỘT
 * file để tải-chậm thành một chunk duy nhất (ParentChildCardsLazy) thay vì 5 chunk lẻ. Nội dung và thứ
 * tự giữ nguyên như trước khi tách; `key` theo con do trang đặt ở chỗ dùng component này.
 */
export default function ParentChildCards({
  studentId,
  classId,
  courses,
}: {
  studentId: string;
  classId: number;
  courses: ComponentProps<typeof ParentUpcoming>["courses"];
}) {
  return (
    <>
      <ParentUpcoming key={`upcoming-${studentId}`} classId={classId} courses={courses} />
      <ParentAttendanceCard key={`attendance-${studentId}`} studentId={studentId} />
      <ParentHomeworkNotes key={`homework-${studentId}`} classId={classId} studentId={studentId} />
      <CatchupCard key={`catchup-${studentId}`} studentId={studentId} classId={classId} viewer="parent" />
      <ParentStanding key={`standing-${studentId}`} studentId={studentId} classId={classId} />
    </>
  );
}
