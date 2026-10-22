"use client";

import Link from "next/link";
import { useState } from "react";
import type { Lesson } from "@/features/lessons/types";
import {
  HSG9_EXAM_DATE,
  daysBetween,
  ddmm,
  hourVn,
  loadTicks,
  saveTicks,
  todayTaskIndex,
  todayVn,
  upcomingSession,
} from "@/features/hsg9/lo-trinh";
import NenKhtn9 from "./NenKhtn9";
import { SessionLessons, TaskList, type LessonProgressMap } from "./Hsg9Parts";

/**
 * Thẻ "Tuần này" của khoá HSG ở trang lớp (tab Thi chuyên & HSG): buổi thứ Bảy tới, việc hôm nay, tiến độ bài của tuần.
 * Chỉ một việc nổi bật (việc hôm nay, B2/N7); cả tuần và 18 buổi ở trang /lop-hoc/lo-trinh-hsg (N1).
 * Sau 22 giờ không giao việc, nhắc nghỉ (não tuổi 14–15 cần ngủ đủ — docs/QUY-TAC-THIET-KE.md G2).
 */
export default function Hsg9WeekCard({
  userId,
  lessons,
  progress,
}: {
  userId: string | null;
  lessons: Lesson[] | null;
  progress: LessonProgressMap | null;
}) {
  const [ticks, setTicks] = useState<Record<string, boolean>>(() => (userId ? loadTicks(userId) : {}));
  const [today] = useState<string | null>(() => todayVn());
  const [late] = useState(() => hourVn() >= 22 || hourVn() < 5);
  const [ticksUserId, setTicksUserId] = useState(userId);

  if (userId !== ticksUserId) {
    setTicksUserId(userId);
    setTicks(userId ? loadTicks(userId) : {});
  }

  if (!today) return null;
  const session = upcomingSession(today);
  const daysToExam = daysBetween(today, HSG9_EXAM_DATE);
  if (!session) return null;

  const daysToSession = daysBetween(today, session.date);
  const idx = todayTaskIndex(session, today);
  const toggle = userId
    ? (id: string) => {
        const next = { ...ticks, [id]: !ticks[id] };
        setTicks(next);
        saveTicks(userId, next);
      }
    : null;

  return (
    <section className="min-w-0 rounded-2xl border border-line bg-panel p-4" aria-label="Lộ trình HSG tuần này">
      <p className="text-xs font-semibold uppercase tracking-wide text-muted">
        Buổi {session.buoi} · thứ Bảy {ddmm(session.date)}
        {daysToSession === 0 ? " · hôm nay" : ` · còn ${daysToSession} ngày`}
      </p>
      <h2 className="mt-1 text-base font-semibold text-ink">{session.chuDe}</h2>
      {session.kiemTra && <p className="mt-0.5 text-sm text-warn">{session.kiemTra}</p>}

      <div className="mt-3">
        {late ? (
          <p className="text-sm text-muted">Đã sau 22 giờ: nghỉ thôi, mai làm tiếp.</p>
        ) : idx >= 0 ? (
          <TaskList session={session} ticks={ticks} onToggle={toggle} todayIndex={idx} only={idx} />
        ) : daysToSession === 0 ? (
          <p className="text-sm text-ink">Hôm nay có buổi học trên lớp. Mang theo sổ lỗi.</p>
        ) : (
          <p className="text-sm text-muted">Hôm nay không có việc mới. Làm bù việc còn thiếu trong tuần nếu có.</p>
        )}
      </div>

      <div className="mt-2">
        <SessionLessons session={session} lessons={lessons} progress={progress} />
        <NenKhtn9 lessonIds={session.lessons} compact />
      </div>

      <div className="mt-2 flex items-center justify-between gap-3">
        <Link href="/lop-hoc/lo-trinh-hsg" className="lesson-link inline-flex min-h-11 items-center text-sm">
          Cả tuần và 18 buổi
        </Link>
        {daysToExam > 0 && <span className="text-xs text-muted">Thi thành phố: còn {Math.ceil(daysToExam / 7)} tuần</span>}
      </div>
    </section>
  );
}
