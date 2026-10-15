"use client";

import { useMemo } from "react";
import ParentRadar, { type RadarData } from "@/components/parent/ParentRadar";
import { CareLogView, type CareEvent } from "@/components/parent/ParentCareLog";
import { WeekRhythmView, lastSevenDays } from "@/components/parent/ParentWeekRhythm";
import type { ChapterLessonMastery } from "@/services/mastery";
import ScrollToHash from "@/components/ui/ScrollToHash";

/**
 * "Trang mẫu" cho phụ huynh CHƯA đăng nhập (/phu-huynh khách, mở từ trang chủ #trang-mau): dựng đúng các
 * khối phụ huynh sẽ thấy, bằng dữ liệu MINH HOẠ — ghi rõ ở đầu và trên từng khối là không phải học sinh
 * thật (P19, cam kết /dieu-khoan: không công khai điểm của em nào). Dùng chung component với trang thật
 * (CareLogView, WeekRhythmView, ParentRadar `demo`) để mẫu không lệch khỏi thứ phụ huynh nhận được.
 */

const CH = { chapterId: -1, chapterTitle: "Dao động (lớp 11)" };
function lesson(id: number, title: string, pct: number, prevPct: number): [ChapterLessonMastery, ChapterLessonMastery] {
  const base = { ...CH, lessonId: -id, lessonTitle: title, sortOrder: id, answeredCount: 12 };
  const level = (p: number) =>
    (p >= 80 ? "mastered" : p >= 50 ? "practicing" : "weak") as ChapterLessonMastery["level"];
  return [
    { ...base, pct, level: level(pct) },
    { ...base, pct: prevPct, level: level(prevPct) },
  ];
}
const LESSONS = [
  lesson(1, "Dao động điều hoà", 88, 70),
  lesson(2, "Mô tả dao động", 76, 60),
  lesson(3, "Vận tốc, gia tốc", 54, 38),
  lesson(4, "Năng lượng dao động", 68, 55),
  lesson(5, "Dao động tắt dần, cưỡng bức", 82, 64),
];
const RADAR: RadarData = { current: LESSONS.map((l) => l[0]), prev: LESSONS.map((l) => l[1]) };

function daysAgo(n: number, hour = 19) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  d.setHours(hour, 15, 0, 0);
  return d.toISOString();
}

function Sample({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative">
      <span className="absolute -top-3 right-3 z-10 rounded-full border border-line bg-panel px-3 py-0.5 text-[15px] font-semibold text-muted">
        Mẫu
      </span>
      {children}
    </div>
  );
}

export default function ParentSamplePreview() {
  const events = useMemo<CareEvent[]>(
    () => [
      {
        at: daysAgo(1, 21),
        kind: "child",
        text: "Con làm đúng lại phần Vận tốc, gia tốc · bài tập — xong phụ đạo phần này.",
      },
      { at: daysAgo(3, 18), kind: "teacher", text: "Trợ giảng dạy lại riêng phần Vận tốc, gia tốc · bài tập cho con." },
      { at: daysAgo(3, 17), kind: "child", text: "Con đi buổi phụ đạo với trợ giảng." },
      { at: daysAgo(5, 20), kind: "teacher", text: "Thầy kiểm tra bài tập về nhà: con làm được 90%." },
      {
        at: daysAgo(8, 20),
        kind: "web",
        text: "Web chấm bài và báo thầy: con còn sai phần Vận tốc, gia tốc · bài tập.",
        sub: "Sai 5/8 câu — thầy đưa phần này vào danh sách phụ đạo.",
      },
      {
        at: daysAgo(12, 9),
        kind: "teacher",
        text: "Thầy xem lại các bài điểm thấp liên tiếp của con và nhắc con.",
        sub: "Ghi chú của thầy: con hiểu bài nhưng tính vội, dặn con ghi đơn vị từng bước.",
      },
    ],
    [],
  );
  const days = useMemo(() => {
    const d = lastSevenDays();
    const pattern = [
      [1, 1, 0],
      [0, 0, 0],
      [2, 1, 0],
      [0, 2, 1],
      [0, 0, 0],
      [1, 1, 0],
      [1, 0, 0],
    ];
    return d.map((day, i) => ({ ...day, lessons: pattern[i][0], practices: pattern[i][1], exams: pattern[i][2] }));
  }, []);

  return (
    <section id="trang-mau" className="scroll-mt-24 -mx-2 rounded-2xl border-2 border-dashed border-line-strong p-2 sm:mx-0 sm:p-6">
      {/* Khối này tải sau trang khách nên ScrollToHash của trang chạy lúc #trang-mau chưa có — cuộn lại ở đây. */}
      <ScrollToHash />
      <h2 className="font-display text-xl font-bold text-ink">Trang mẫu: phụ huynh sẽ thấy về con như thế này</h2>
      <p className="parent-copy mt-2 text-muted">
        Số liệu dưới đây là <b className="text-ink">ví dụ minh hoạ</b>, không phải của học sinh nào. Khi tài khoản đã
        nối với con, các khối này hiện đúng số liệu của con và tự cập nhật sau mỗi bài con làm.
      </p>

      <div className="mt-6 space-y-2">
        <Sample>
          <div className="mb-6 rounded-2xl border border-line bg-panel p-5">
            <h3 className="font-display text-lg font-bold text-ink">Tóm tắt cho phụ huynh</h3>
            <dl className="mt-3 divide-y divide-line">
              {[
                ["Bài gần nhất", "7,75/10 · Khá", "Kiểm tra 15 phút chương Dao động"],
                ["Điểm trung bình", "7,2", "9 bài đã làm"],
                ["So với bài trước", "+1,25", "tăng 1,25 điểm so với bài trước"],
              ].map(([k, v, sub]) => (
                <div key={k} className="py-3 first:pt-0 last:pb-0">
                  <dt className="text-muted">{k}</dt>
                  <dd className="parent-num font-display text-2xl font-bold text-ink">{v}</dd>
                  <dd className="text-muted">{sub}</dd>
                </div>
              ))}
            </dl>
            <p className="parent-copy mt-3 text-ink">
              Gợi ý cho tối nay: hỏi con “phần <b>Vận tốc, gia tốc</b> con thấy khó ở chỗ nào?”, rồi ngồi cùng con xem
              lại một câu.
            </p>
          </div>
        </Sample>
        <Sample>
          <CareLogView events={events} />
        </Sample>
        <Sample>
          <WeekRhythmView days={days} />
        </Sample>
        <Sample>
          <div className="pt-4">
            <ParentRadar studentId="mau" demo={RADAR} />
          </div>
        </Sample>
      </div>
    </section>
  );
}
