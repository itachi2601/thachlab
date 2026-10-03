"use client";

import { useEffect, useState } from "react";
import { CalendarClock } from "lucide-react";
import { fetchRecentAnnouncements, type ClassAnnouncement } from "@/services/announcements";
import type { ThptCourse } from "@/services/thpt-courses-public";
import { dayMonth } from "@/lib/parent-format";

/**
 * "Sắp tới": phụ huynh cần nhìn về phía trước để sắp xếp đưa đón và nhắc con — các khối khác của trang đều
 * nhìn lại quá khứ. Hai nguồn có thật trong hệ thống: lịch học hằng tuần của khoá con đã vào, và việc thầy
 * nhắn cho hôm nay. Chưa có ngày kiểm tra trong DB nên KHÔNG bịa mục "bài kiểm tra sắp tới".
 */
interface Slot {
  date: Date;
  course: string;
  start: string;
  end: string;
  location: string;
}

/** Các buổi học trong 14 ngày tới (weekday 1..7 = Thứ 2..Chủ nhật), buổi hôm nay chỉ tính khi chưa kết thúc. */
export function upcomingSlots(courses: ThptCourse[], now: Date, limit = 3): Slot[] {
  const out: Slot[] = [];
  for (let i = 0; i < 14; i++) {
    const day = new Date(now.getFullYear(), now.getMonth(), now.getDate() + i);
    const weekday = day.getDay() === 0 ? 7 : day.getDay();
    for (const c of courses) {
      for (const s of c.schedules) {
        if (s.weekday !== weekday) continue;
        const [h, m] = s.end_time.split(":").map(Number);
        const end = new Date(day.getFullYear(), day.getMonth(), day.getDate(), h, m);
        if (end.getTime() < now.getTime()) continue;
        out.push({ date: day, course: c.name, start: s.start_time, end: s.end_time, location: s.location });
      }
    }
  }
  return out
    .sort((a, b) => a.date.getTime() - b.date.getTime() || a.start.localeCompare(b.start))
    .slice(0, limit);
}

const WEEK = 7 * 24 * 60 * 60 * 1000;

export default function ParentUpcoming({ classId, courses }: { classId: number; courses: ThptCourse[] }) {
  const [task, setTask] = useState<ClassAnnouncement | null>(null);
  const [now] = useState(() => new Date());

  useEffect(() => {
    let cancelled = false;
    fetchRecentAnnouncements(classId, "today_task", 1)
      .then((rows) => {
        if (!cancelled) setTask(rows[0] ?? null);
      })
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [classId]);

  const slots = upcomingSlots(courses, now);
  const freshTask = task && now.getTime() - new Date(task.createdAt).getTime() <= WEEK ? task : null;
  if (slots.length === 0 && !freshTask) return null;

  return (
    <section className="mb-6 rounded-2xl border border-white/10 bg-panel p-5">
      <h2 className="flex items-center gap-2 font-display text-lg font-semibold text-white">
        <CalendarClock size={18} className="text-cyan-300" aria-hidden /> Sắp tới
      </h2>
      {slots.length > 0 && (
        <ul className="mt-3 space-y-2">
          {slots.map((s) => (
            <li key={`${s.date.toISOString()}-${s.start}-${s.course}`}>
              <p className="font-semibold text-white">{dayMonth(s.date)}</p>
              <p className="parent-copy text-slate-300">
                Học {s.start}–{s.end} · {s.course}
                {s.location ? ` · ${s.location}` : ""}
              </p>
            </li>
          ))}
        </ul>
      )}
      {freshTask && (
        <div className="mt-4 rounded-xl border border-cyan-400/25 bg-cyan-400/[.06] p-3">
          <p className="text-slate-400">Thầy nhắn con</p>
          <p className="parent-copy mt-0.5 whitespace-pre-wrap text-white">{freshTask.body}</p>
        </div>
      )}
    </section>
  );
}
