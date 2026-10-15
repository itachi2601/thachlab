"use client";

import { useEffect, useState } from "react";
import { getSupabase } from "@/services/supabase";

/**
 * "Nhịp học 7 ngày" — con có tự mở web học không, ngày nào. Một hàng 7 ô (T2…CN) + ba con số.
 * Không xếp hạng, không so với bạn (P-nhạy địa vị); ô trống là "chưa học", không tô đỏ (không phán xét).
 * Nguồn: lesson_progress (mục bài học xong), practice_sessions (lượt luyện), exam_results (bài làm) —
 * cả ba phụ huynh đã đọc được.
 */

export interface WeekDay {
  /** yyyy-mm-dd theo giờ máy. */
  date: string;
  lessons: number;
  practices: number;
  exams: number;
}

const WD = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"];

function ymd(d: Date) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

export function lastSevenDays(): WeekDay[] {
  const days: WeekDay[] = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    days.push({ date: ymd(d), lessons: 0, practices: 0, exams: 0 });
  }
  return days;
}

export function WeekRhythmView({ days }: { days: WeekDay[] }) {
  const active = days.filter((d) => d.lessons + d.practices + d.exams > 0).length;
  const sum = (k: "lessons" | "practices" | "exams") => days.reduce((n, d) => n + d[k], 0);
  return (
    <section className="mb-6 rounded-2xl border border-line bg-panel p-5">
      <h2 className="font-display text-lg font-bold text-ink">Con tự học 7 ngày qua</h2>
      <p className="parent-copy mt-1 text-ink">
        Con mở web học <b className="parent-num">{active}/7</b> ngày.
      </p>
      <ol className="mt-3 grid grid-cols-7 gap-1.5" aria-label="Các ngày con có học trên web">
        {days.map((d) => {
          const n = d.lessons + d.practices + d.exams;
          const wd = WD[new Date(`${d.date}T12:00:00`).getDay()];
          return (
            <li key={d.date} className="text-center">
              <span className="block text-[15px] font-semibold text-muted">{wd}</span>
              <span
                className={`mt-1 flex h-11 items-center justify-center rounded-lg border text-base font-bold tabular-nums ${
                  n > 0 ? "border-primary bg-primary text-white" : "border-line bg-surface-2 text-muted"
                }`}
                aria-label={n > 0 ? `${wd}: ${n} việc` : `${wd}: chưa học`}
              >
                {n > 0 ? "✓" : "·"}
              </span>
            </li>
          );
        })}
      </ol>
      <ul className="mt-4 space-y-1 text-ink">
        <li>
          Học xong <b className="parent-num">{sum("lessons")}</b> mục bài học (lý thuyết, bài tập mẫu)
        </li>
        <li>
          Luyện tập <b className="parent-num">{sum("practices")}</b> lượt
        </li>
        <li>
          Làm <b className="parent-num">{sum("exams")}</b> bài kiểm tra
        </li>
      </ul>
    </section>
  );
}

export default function ParentWeekRhythm({ studentId }: { studentId: string }) {
  const [days, setDays] = useState<WeekDay[] | null>(null);
  useEffect(() => {
    let cancelled = false;
    const base = lastSevenDays();
    const since = new Date(`${base[0].date}T00:00:00`).toISOString();
    const supabase = getSupabase();
    Promise.all([
      supabase.from("lesson_progress").select("done_at").eq("user_id", studentId).gte("done_at", since),
      supabase.from("practice_sessions").select("created_at").eq("student_id", studentId).gte("created_at", since),
      supabase.from("exam_results").select("created_at").eq("student_id", studentId).gte("created_at", since),
    ])
      .then(([lp, ps, er]) => {
        if (cancelled) return;
        const byDate = new Map(base.map((d) => [d.date, d]));
        const add = (iso: string | null, k: "lessons" | "practices" | "exams") => {
          const d = iso ? byDate.get(ymd(new Date(iso))) : undefined;
          if (d) d[k] += 1;
        };
        for (const r of lp.data ?? []) add(r.done_at, "lessons");
        for (const r of ps.data ?? []) add(r.created_at, "practices");
        for (const r of er.data ?? []) add(r.created_at, "exams");
        setDays(base);
      })
      .catch(() => !cancelled && setDays(base));
    return () => {
      cancelled = true;
    };
  }, [studentId]);
  if (days === null) return <div className="mb-6 h-48 rounded-2xl border border-line bg-panel" aria-busy="true" />;
  return <WeekRhythmView days={days} />;
}
