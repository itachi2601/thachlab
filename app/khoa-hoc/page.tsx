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

function seatsLabel(course: ThptCourse) {
  if (course.capacity === null) return `${course.taken} đã đăng ký`;
  const left = Math.max(course.capacity - course.taken, 0);
  return left === 0 ? "Đã đủ chỗ" : `Còn ${left}/${course.capacity} chỗ`;
}

function CourseCard({ course }: { course: ThptCourse }) {
  const full = course.capacity !== null && course.taken >= course.capacity;
  const started = course.starts_at ? new Date(course.starts_at) < new Date(new Date().toDateString()) : false;
  return (
    <article className="flex flex-col rounded-3xl border border-white/10 bg-[#0B1020] p-6">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-bold uppercase tracking-[.14em] text-blue-300">Khối {course.className}</p>
          <h2 className="mt-1 font-display text-xl font-bold text-white">{course.name}</h2>
          <p className="text-xs text-slate-500">Năm học {course.school_year}</p>
        </div>
        <span
          className={`shrink-0 rounded-full px-3 py-1 text-xs font-bold ${
            full ? "bg-red-500/15 text-red-300" : "bg-emerald-500/15 text-emerald-300"
          }`}
        >
          {seatsLabel(course)}
        </span>
      </div>

      {course.description && <p className="mt-3 text-sm text-slate-300">{course.description}</p>}

      <ul className="mt-4 space-y-1.5 text-sm text-slate-300">
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
          full ? "pointer-events-none bg-white/5 text-slate-500" : "bg-[#2563EB] text-white hover:bg-primary-dark"
        }`}
      >
        <Users size={16} /> {full ? "Đã đủ chỗ" : "Đăng ký học"}
      </Link>
    </article>
  );
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
    return [...m.entries()];
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
            {byClass.map(([className, list]) => (
              <section key={className}>
                <h2 className="mb-4 font-display text-lg font-bold text-slate-200">Khối {className}</h2>
                <div className="grid gap-5 md:grid-cols-2">
                  {list.map((course) => (
                    <CourseCard key={course.id} course={course} />
                  ))}
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
