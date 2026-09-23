"use client";

/**
 * components/home/TeachingSchedule.tsx
 *
 * Thời khoá biểu trong tuần — lấy trực tiếp từ các khoá công khai (thpt_courses)
 * mà giáo viên mở ở Dashboard THPT, cùng nguồn dữ liệu với /khoa-hoc. Vẽ dạng
 * lưới ngày × giờ thật (vị trí và chiều cao của mỗi lớp tỉ lệ với khung giờ học)
 * thay vì liệt kê chữ, để nhìn là biết ngay lớp nào học lúc nào trong tuần.
 */

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { supabaseConfigured } from "@/services/supabase";
import { fetchPublicCourses, WEEKDAY_LABEL, type ThptCourse } from "@/services/thpt-courses";

const WEEKDAYS = [1, 2, 3, 4, 5, 6, 7];
const PX_PER_HOUR = 64;
const DEFAULT_START_HOUR = 7;
const DEFAULT_END_HOUR = 22;

interface Slot {
  course: ThptCourse;
  weekday: number;
  startMinutes: number;
  endMinutes: number;
  start: string;
  end: string;
}

function toMinutes(t: string): number {
  const [h, m] = t.split(":").map(Number);
  return h * 60 + m;
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

  const slots: Slot[] = (courses ?? []).flatMap((course) =>
    course.schedules.map((s) => ({
      course,
      weekday: s.weekday,
      startMinutes: toMinutes(s.start_time),
      endMinutes: toMinutes(s.end_time),
      start: s.start_time,
      end: s.end_time,
    })),
  );

  const startHour = Math.min(DEFAULT_START_HOUR, ...slots.map((s) => Math.floor(s.startMinutes / 60)));
  const endHour = Math.max(DEFAULT_END_HOUR, ...slots.map((s) => Math.ceil(s.endMinutes / 60)));
  const dayStartMinutes = startHour * 60;
  const totalHeight = (endHour - startHour) * PX_PER_HOUR;
  const hourMarks = Array.from({ length: endHour - startHour + 1 }, (_, i) => startHour + i);

  return (
    <section id="lich-day" className="scroll-mt-20 border-t border-line py-20 lg:py-28">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="max-w-2xl">
          <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Lịch dạy</p>
          <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Thời khoá biểu trong tuần
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Các lớp Vật lý đang mở đăng ký. Bấm vào một lớp trên lịch để xem chi tiết và đăng ký.
          </p>
        </Reveal>

        {courses === null ? (
          <p className="mt-10 text-sm text-muted">Đang tải lịch…</p>
        ) : (
          <div className="mt-10 overflow-x-auto rounded-2xl border border-line">
            <div style={{ minWidth: 56 + WEEKDAYS.length * 96 }}>
              {/* Hàng tiêu đề: tên ngày */}
              <div className="grid" style={{ gridTemplateColumns: `56px repeat(${WEEKDAYS.length}, 1fr)` }}>
                <div className="sticky left-0 border-b border-line bg-panel" />
                {WEEKDAYS.map((d) => (
                  <div key={d} className="border-b border-l border-line bg-panel px-2 py-2.5 text-center">
                    <p className="font-mono text-xs font-semibold uppercase tracking-wide text-cyan-300">
                      {WEEKDAY_LABEL[d]}
                    </p>
                  </div>
                ))}
              </div>

              {/* Thân lưới: cột giờ + 7 cột ngày, mỗi lớp đặt đúng theo khung giờ */}
              <div className="grid" style={{ gridTemplateColumns: `56px repeat(${WEEKDAYS.length}, 1fr)` }}>
                <div className="sticky left-0 z-10 border-r border-line bg-panel" style={{ height: totalHeight }}>
                  {hourMarks.map((h) => (
                    <p
                      key={h}
                      className="absolute right-1.5 -translate-y-1/2 text-[11px] tabular-nums text-muted"
                      style={{ top: (h - startHour) * PX_PER_HOUR }}
                    >
                      {h}g
                    </p>
                  ))}
                </div>
                {WEEKDAYS.map((d) => (
                  <div key={d} className="relative border-l border-line" style={{ height: totalHeight }}>
                    {hourMarks.map((h) => (
                      <div
                        key={h}
                        className="absolute inset-x-0 border-t border-line/60"
                        style={{ top: (h - startHour) * PX_PER_HOUR }}
                      />
                    ))}
                    {slots
                      .filter((s) => s.weekday === d)
                      .map((s) => {
                        const top = ((s.startMinutes - dayStartMinutes) / 60) * PX_PER_HOUR;
                        const height = Math.max(((s.endMinutes - s.startMinutes) / 60) * PX_PER_HOUR, 40);
                        return (
                          <Link
                            key={`${s.course.id}-${s.start}`}
                            href={`/khoa-hoc/dang-ky/?id=${s.course.id}`}
                            className="absolute inset-x-1 overflow-hidden rounded-lg border border-cyan-300/30 bg-cyan-400/10 px-1.5 py-1 text-[11px] leading-tight transition hover:border-cyan-300 hover:bg-cyan-400/20"
                            style={{ top, height }}
                          >
                            <span className="block truncate font-semibold text-ink">{s.course.name}</span>
                            <span className="mt-0.5 block tabular-nums text-muted">
                              {s.start}–{s.end}
                            </span>
                          </Link>
                        );
                      })}
                  </div>
                ))}
              </div>
            </div>
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
