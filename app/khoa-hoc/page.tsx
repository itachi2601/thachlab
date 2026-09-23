"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { CalendarDays, MapPin, Users, Wallet } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { supabaseConfigured } from "@/services/supabase";
import {
  fetchPublicCourses,
  formatDate,
  WEEKDAY_LABEL,
  type ThptCourse,
} from "@/services/thpt-courses";

function isFull(course: ThptCourse) {
  return course.capacity !== null && course.taken >= course.capacity;
}

function ScheduleList({ course }: { course: ThptCourse }) {
  return (
    <ul className="mt-3 space-y-1.5 text-sm text-slate-300">
      {course.schedules.length === 0 ? (
        <li className="text-slate-500">Lịch học sẽ thông báo sau.</li>
      ) : (
        course.schedules.map((s) => (
          <li key={`${s.weekday}-${s.start_time}`} className="flex items-center gap-2">
            <CalendarDays size={15} className="shrink-0 text-blue-300" />
            <span className="font-semibold text-white">{WEEKDAY_LABEL[s.weekday]}</span>
            <span>
              {s.start_time}–{s.end_time}
            </span>
            {s.location && (
              <span className="flex items-center gap-1 text-slate-400">
                <MapPin size={13} /> {s.location}
              </span>
            )}
          </li>
        ))
      )}
    </ul>
  );
}

function CourseCard({ course }: { course: ThptCourse }) {
  const full = isFull(course);
  const started = course.starts_at ? new Date(course.starts_at) < new Date(new Date().toDateString()) : false;
  return (
    <article className="flex flex-col rounded-3xl border border-white/10 bg-panel p-6">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-bold uppercase tracking-[.14em] text-blue-300">Khối {course.className}</p>
          <h2 className="mt-1 font-display text-xl font-bold text-white">{course.name}</h2>
          <p className="text-xs text-slate-500">Năm học {course.school_year}</p>
        </div>
        {full && (
          <span className="shrink-0 rounded-full bg-red-500/15 px-3 py-1 text-xs font-bold text-red-300">
            Đã đủ chỗ
          </span>
        )}
      </div>

      {course.description && <p className="mt-3 text-sm text-slate-300">{course.description}</p>}

      <ScheduleList course={course} />

      <div className="mt-4 space-y-1 text-xs text-slate-400">
        {course.starts_at && (
          <p>
            {started ? "Đã khai giảng" : "Khai giảng"} {formatDate(course.starts_at)}
            {course.ends_at ? ` · kết thúc ${formatDate(course.ends_at)}` : ""}
          </p>
        )}
        {course.fee_note && (
          <p className="flex items-center gap-1.5">
            <Wallet size={13} /> {course.fee_note}
          </p>
        )}
      </div>

      {started && !full && (
        <p className="mt-3 rounded-xl border border-amber-500/25 bg-amber-500/[.06] px-3 py-2 text-xs text-amber-100/90">
          Lớp đã học được một phần. Đăng ký lúc này sẽ được xếp buổi phụ đạo bù bài trước khi vào lớp chính thức.
        </p>
      )}

      <div className="mt-5 flex-1" />
      <Link
        href={full ? "#" : `/khoa-hoc/dang-ky/?id=${course.id}`}
        aria-disabled={full}
        className={`mt-2 inline-flex items-center justify-center gap-2 rounded-xl py-3 text-sm font-bold ${
          full ? "pointer-events-none bg-white/5 text-slate-500" : "bg-primary text-white hover:bg-primary-dark"
        }`}
      >
        <Users size={16} /> {full ? "Đã đủ chỗ" : "Đăng ký học"}
      </Link>
    </article>
  );
}

/** Lớp học nhiều buổi/tuần (vd 12L1: 1 buổi A + 1 buổi B) — gộp các khoá cùng pair_key
 * vào MỘT thẻ, chia rõ theo buổi, để khỏi nhầm thành nhiều lớp riêng biệt. */
function PairedCourseCard({ pairKey, className, slots }: { pairKey: string; className: string; slots: [string, ThptCourse[]][] }) {
  return (
    <article className="flex flex-col rounded-3xl border border-blue-400/25 bg-panel p-6 md:col-span-2">
      <p className="text-xs font-bold uppercase tracking-[.14em] text-blue-300">Khối {className} · học nhiều buổi/tuần</p>
      <h2 className="mt-1 font-display text-xl font-bold text-white">Vật lí {pairKey}</h2>
      <p className="mt-2 text-sm text-slate-400">
        Chọn 1 khung giờ ở mỗi buổi bên dưới — đăng ký 2 lần (1 lần ở buổi này, 1 lần ở buổi kia) để đủ lịch tuần.
      </p>

      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        {slots.map(([slot, options]) => (
          <div key={slot} className="rounded-2xl border border-white/10 bg-white/[.03] p-4">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Buổi {slot}</p>
            <ul className="mt-2 space-y-3">
              {options.map((course) => {
                const full = isFull(course);
                return (
                  <li key={course.id} className="rounded-xl border border-white/10 p-3">
                    <ScheduleList course={course} />
                    <Link
                      href={full ? "#" : `/khoa-hoc/dang-ky/?id=${course.id}`}
                      aria-disabled={full}
                      className={`mt-3 flex items-center justify-center gap-1.5 rounded-lg py-2 text-xs font-bold ${
                        full ? "pointer-events-none bg-white/5 text-slate-500" : "bg-primary text-white hover:bg-primary-dark"
                      }`}
                    >
                      <Users size={13} /> {full ? "Đã đủ chỗ" : `Đăng ký buổi ${slot}`}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </div>
    </article>
  );
}

type DisplayItem =
  | { kind: "single"; course: ThptCourse }
  | { kind: "paired"; pairKey: string; className: string; slots: [string, ThptCourse[]][] };

function groupForDisplay(list: ThptCourse[]): DisplayItem[] {
  const paired = new Map<string, ThptCourse[]>();
  const items: DisplayItem[] = [];
  for (const course of list) {
    if (course.pair_key) {
      paired.set(course.pair_key, [...(paired.get(course.pair_key) ?? []), course]);
    } else {
      items.push({ kind: "single", course });
    }
  }
  for (const [pairKey, courses] of paired) {
    const bySlot = new Map<string, ThptCourse[]>();
    for (const c of courses) {
      const slot = c.pair_slot ?? "?";
      bySlot.set(slot, [...(bySlot.get(slot) ?? []), c]);
    }
    const slots = [...bySlot.entries()].sort((a, b) => a[0].localeCompare(b[0]));
    items.push({ kind: "paired", pairKey, className: courses[0].className, slots });
  }
  return items;
}

export default function KhoaHocPage() {
  const [courses, setCourses] = useState<ThptCourse[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!supabaseConfigured) return;
    fetchPublicCourses()
      .then(setCourses)
      .catch((e: unknown) => {
        setCourses([]);
        setError(e instanceof Error ? e.message : "Chưa tải được danh sách khoá học.");
      });
  }, []);

  const byClass = useMemo(() => {
    const m = new Map<string, ThptCourse[]>();
    for (const c of courses ?? []) {
      const list = m.get(c.className) ?? [];
      list.push(c);
      m.set(c.className, list);
    }
    return [...m.entries()].map(([className, list]) => [className, groupForDisplay(list)] as const);
  }, [courses]);

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pb-24 pt-28 lg:px-8">
        <header className="max-w-2xl">
          <p className="text-xs font-bold uppercase tracking-[.16em] text-blue-300">Đăng ký học</p>
          <h1 className="mt-2 font-display text-3xl font-bold text-white">Lớp Vật lí đang mở</h1>
          <p className="mt-3 text-slate-400">
            Chọn lớp đúng khối và lịch học phù hợp. Phụ huynh có thể đăng ký cho con; học sinh đã có tài khoản tự đăng
            ký. Giáo viên duyệt xong là vào lớp, học phí đóng tại trung tâm.
          </p>
        </header>

        {!supabaseConfigured ? (
          <p className="mt-10 text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : courses === null ? (
          <p className="mt-10 text-slate-400">Đang tải…</p>
        ) : error ? (
          <p className="mt-10 text-red-300">{error}</p>
        ) : courses.length === 0 ? (
          <p className="mt-10 rounded-2xl border border-dashed border-white/10 p-8 text-center text-slate-500">
            Chưa có lớp nào đang mở đăng ký. Quay lại sau hoặc liên hệ trực tiếp.
          </p>
        ) : (
          <div className="mt-10 space-y-10">
            {byClass.map(([className, items]) => (
              <section key={className}>
                <h2 className="mb-4 font-display text-lg font-bold text-slate-200">Khối {className}</h2>
                <div className="grid gap-5 md:grid-cols-2">
                  {items.map((item) =>
                    item.kind === "single" ? (
                      <CourseCard key={item.course.id} course={item.course} />
                    ) : (
                      <PairedCourseCard key={item.pairKey} pairKey={item.pairKey} className={item.className} slots={item.slots} />
                    ),
                  )}
                </div>
              </section>
            ))}
          </div>
        )}
      </main>
      <Footer />
    </>
  );
}
