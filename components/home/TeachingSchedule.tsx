"use client";

/**
 * components/home/TeachingSchedule.tsx
 *
 * Lịch dạy trong tuần — lấy trực tiếp từ các khoá công khai (thpt_courses) mà
 * giáo viên mở ở Dashboard THPT, cùng nguồn dữ liệu với /khoa-hoc. Khách xem
 * lịch ngay tại trang chủ, không cần qua trang riêng mới thấy khối nào có lớp,
 * ngày nào rảnh mới đăng ký được.
 */

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, CalendarDays } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { supabaseConfigured } from "@/services/supabase";
import { fetchPublicCourses, WEEKDAY_LABEL, type ThptCourse } from "@/services/thpt-courses";

const WEEKDAYS = [1, 2, 3, 4, 5, 6, 7];

interface DaySlot {
  course: ThptCourse;
  start: string;
  end: string;
}

export default function TeachingSchedule() {
  const [courses, setCourses] = useState<ThptCourse[] | null>(null);

  useEffect(() => {
    if (!supabaseConfigured) return;
    fetchPublicCourses()
      .then(setCourses)
      .catch(() => setCourses([]));
  }, []);

  if (!supabaseConfigured) return null;
  if (courses !== null && courses.length === 0) return null;

  const byWeekday = new Map<number, DaySlot[]>();
  for (const course of courses ?? []) {
    for (const s of course.schedules) {
      const list = byWeekday.get(s.weekday) ?? [];
      list.push({ course, start: s.start_time, end: s.end_time });
      byWeekday.set(s.weekday, list);
    }
  }
  for (const list of byWeekday.values()) list.sort((a, b) => a.start.localeCompare(b.start));

  return (
    <section id="lich-day" className="scroll-mt-20 border-t border-line py-20 lg:py-28">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="max-w-2xl">
          <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Lịch dạy</p>
          <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Lịch học trong tuần
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Các lớp Vật lý đang mở đăng ký, xếp theo ngày trong tuần. Bấm vào một lớp để xem chi tiết và đăng ký.
          </p>
        </Reveal>

        {courses === null ? (
          <p className="mt-10 text-sm text-muted">Đang tải lịch…</p>
        ) : (
          <div className="mt-10 grid gap-px overflow-hidden rounded-2xl border border-line bg-line sm:grid-cols-2 lg:grid-cols-7">
            {WEEKDAYS.map((weekday) => {
              const slots = byWeekday.get(weekday) ?? [];
              return (
                <div key={weekday} className="min-h-[9rem] bg-panel p-3">
                  <p className="font-mono text-xs font-semibold uppercase tracking-wide text-cyan-300">
                    {WEEKDAY_LABEL[weekday]}
                  </p>
                  <div className="mt-2 space-y-2">
                    {slots.length === 0 ? (
                      <p className="text-xs text-muted">—</p>
                    ) : (
                      slots.map(({ course, start, end }) => (
                        <Link
                          key={`${course.id}-${start}`}
                          href={`/khoa-hoc/dang-ky/?id=${course.id}`}
                          className="block rounded-lg border border-line px-2.5 py-2 text-xs leading-snug transition hover:border-cyan-300/50"
                        >
                          <span className="block font-semibold text-ink">{course.name}</span>
                          <span className="mt-0.5 flex items-center gap-1 text-muted">
                            <CalendarDays size={11} className="shrink-0 text-cyan-300" />
                            {start}–{end}
                          </span>
                        </Link>
                      ))
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        <div className="mt-6">
          <Link
            href="/khoa-hoc"
            className="inline-flex items-center gap-1.5 text-sm font-semibold text-cyan-300 transition hover:text-cyan-200"
          >
            Xem đầy đủ các lớp và đăng ký học <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </section>
  );
}
