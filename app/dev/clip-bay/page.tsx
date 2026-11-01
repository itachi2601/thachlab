"use client";

import { NeedRow } from "@/components/results/StudentResultsDashboard";
import type { TutoringNeed } from "@/services/tutoring";
import type { OutcomeGap } from "@/services/analytics";

/**
 * XEM THỬ thẻ mục phụ đạo có clip bẫy (chặng C) — chỉ có nghĩa ở máy dev: http://localhost:3000/dev/clip-bay
 * Dữ liệu GIẢ (không HS thật), dựng đúng NeedRow của /lop-hoc/ket-qua để chụp 375 px mà không cần đăng nhập HS.
 */
const base = {
  studentId: "demo", classId: null, chapterId: 4, form: "ly_thuyet", status: "open", source: "auto",
  assignedTo: null, note: "", firstSeenAt: "2026-10-20T00:00:00Z", lastSeenAt: "2026-10-30T00:00:00Z",
  tutoredAt: null, clearedAt: null,
} as const;
const NEEDS: { need: TutoringNeed; outcomes: OutcomeGap[] }[] = [
  {
    need: { ...base, id: 1, topicId: 66, topicName: "Bài 10. Lực từ. Cảm ứng từ", lessonId: 11, wrong: 7, total: 12, pct: 58 },
    outcomes: [
      { studentId: "demo", parentTopicId: 66, topicId: 234, topicName: "Ngẫu lực từ lên khung dây", form: "ly_thuyet", total: 4, wrong: 3 },
      { studentId: "demo", parentTopicId: 66, topicId: 233, topicName: "Cảm ứng từ và đơn vị tesla", form: "ly_thuyet", total: 5, wrong: 3 },
    ],
  },
];

export default function Page() {
  return (
    <main className="mx-auto max-w-3xl space-y-3 px-4 py-6">
      <h1 className="font-display text-xl font-bold text-ink">Xem thử: mục phụ đạo có clip bẫy</h1>
      {NEEDS.map(({ need, outcomes }) => (
        <NeedRow key={need.id} need={need} outcomes={outcomes} viewer="student" lessonHref={() => "/lop-hoc"} />
      ))}
    </main>
  );
}
