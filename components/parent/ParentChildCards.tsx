"use client";

import CatchupCard from "@/components/results/CatchupCard";
import EntryDiagnosticCard from "@/components/results/EntryDiagnosticCard";
import ParentHomeworkNotes from "@/components/results/ParentHomeworkNotes";
import ParentUpcoming from "@/components/parent/ParentUpcoming";
import ParentAttendanceCard from "@/components/parent/ParentAttendanceCard";
import ParentStanding from "@/components/parent/ParentStanding";
import ParentCareLog from "@/components/parent/ParentCareLog";
import ParentWeekRhythm from "@/components/parent/ParentWeekRhythm";
import ParentRadar from "@/components/parent/ParentRadar";
import type { ComponentProps } from "react";

/**
 * 15/10/2026 thêm 3 khối "thầy quan tâm con": Thầy theo dõi con (nhật ký việc người làm cho con),
 * Con tự học 7 ngày qua, Con nắm bài tới đâu (radar) — đặt ngay sau "Sắp tới" vì đó là câu phụ huynh
 * hỏi kế tiếp sau điểm: "thầy có để ý con không, con có tự học không".
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
      <ParentCareLog key={`care-${studentId}`} studentId={studentId} />
      <ParentWeekRhythm key={`rhythm-${studentId}`} studentId={studentId} />
      <ParentRadar key={`radar-${studentId}`} studentId={studentId} />
      <ParentAttendanceCard key={`attendance-${studentId}`} studentId={studentId} />
      <ParentHomeworkNotes key={`homework-${studentId}`} classId={classId} studentId={studentId} />
      <EntryDiagnosticCard key={`diagnostic-${studentId}`} studentId={studentId} viewer="parent" />
      <CatchupCard key={`catchup-${studentId}`} studentId={studentId} classId={classId} viewer="parent" />
      <ParentStanding key={`standing-${studentId}`} studentId={studentId} classId={classId} />
    </>
  );
}
