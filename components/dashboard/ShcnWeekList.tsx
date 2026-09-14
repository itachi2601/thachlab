"use client";

import { useEffect, useState } from "react";
import { BookOpenCheck, ClipboardList, ExternalLink, Target, Users } from "lucide-react";
import { fetchWeeklySessions, weekRange, type WeeklySession } from "@/services/homeroom-shcn";
import { GDDD_DOCS_URL, selfStudyItems } from "@/lib/shcn/gddd-topics";

const dateFormat = new Intl.DateTimeFormat("vi-VN", { day: "2-digit", month: "2-digit" });

function formatDate(value: string) {
  return dateFormat.format(new Date(`${value}T00:00:00`));
}

/** Danh sách các tuần đã sinh hoạt, mới nhất trước — sinh viên xem lại nội dung đã phổ biến. */
export default function ShcnWeekList({ courseId }: { courseId: number }) {
  const [weeks, setWeeks] = useState<WeeklySession[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    fetchWeeklySessions(courseId)
      .then((rows) => { if (!cancelled) setWeeks(rows); })
      .catch((cause) => { if (!cancelled) { setWeeks([]); setError(cause instanceof Error ? cause.message : "Không tải được nội dung sinh hoạt."); } });
    return () => { cancelled = true; };
  }, [courseId]);

  if (weeks === null) return <p className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-sm text-slate-400">Đang tải nội dung sinh hoạt lớp…</p>;

  return (
    <div className="space-y-4">
      {error && <p className="rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}
      {!weeks.length && !error && (
        <p className="rounded-2xl border border-dashed border-white/10 bg-[#0B1020] p-10 text-center text-sm text-slate-500">
          Chưa có tuần sinh hoạt nào được đăng. Nội dung sẽ xuất hiện ở đây sau tiết sinh hoạt chủ nhiệm.
        </p>
      )}
      {weeks.map((week) => <WeekCard key={week.id} week={week} />)}
    </div>
  );
}

function WeekCard({ week }: { week: WeeklySession }) {
  const range = week.met_on ? weekRange(week.met_on) : null;
  const selfStudy = selfStudyItems(week.ethics_topic, week.ethics_taught);

  return (
    <article className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
      <header className="flex flex-wrap items-center justify-between gap-2 border-b border-white/10 pb-3">
        <h3 className="font-display text-lg font-bold text-white">
          Tuần {week.week_no}
          {range && <span className="ml-2 text-sm font-medium text-slate-500">({formatDate(range.from)} – {formatDate(range.to)})</span>}
        </h3>
        {week.met_on && (
          <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-bold text-emerald-300">
            Đã sinh hoạt: {formatDate(week.met_on)}
          </span>
        )}
      </header>

      {week.announcements.length > 0 && (
        <section className="mt-4">
          <div className="flex items-center gap-2 text-sm font-bold text-white"><ClipboardList size={16} className="text-blue-300" />Nội dung phổ biến</div>
          <ul className="mt-2 space-y-1.5">
            {week.announcements.map((item, index) => (
              <li key={index} className="flex gap-2 text-sm text-slate-300">
                <span className="text-slate-600">{index + 1}.</span>
                <span>
                  {item.tieu_de}
                  {item.ghi_chu && <em className="ml-1 not-italic text-slate-500">— {item.ghi_chu}</em>}
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {(week.ethics_topic || week.ethics_taught.length > 0) && (
        <section className="mt-4">
          <div className="flex items-center gap-2 text-sm font-bold text-white">
            <Target size={16} className="text-violet-300" />GDĐĐ &amp; PTNN{week.ethics_topic && ` — ${week.ethics_topic}`}
          </div>
          {week.ethics_taught.length > 0 && (
            <p className="mt-2 text-sm text-slate-300">
              <span className="font-semibold text-slate-400">Đã dạy: </span>{week.ethics_taught.join("; ")}
            </p>
          )}
          {selfStudy.length > 0 && (
            <p className="mt-1 text-sm text-slate-300">
              <span className="font-semibold text-slate-400">Tự đọc thêm: </span>{selfStudy.join("; ")}
            </p>
          )}
          <a href={GDDD_DOCS_URL} target="_blank" rel="noreferrer" className="mt-2 inline-flex items-center gap-1.5 text-xs font-bold text-cyan-300 hover:text-cyan-200">
            <BookOpenCheck size={14} />Xem toàn bộ tài liệu GDĐĐ &amp; PTNN<ExternalLink size={12} />
          </a>
        </section>
      )}

      {(week.headcount !== null || week.present_count !== null) && (
        <footer className="mt-4 flex items-center gap-2 border-t border-white/10 pt-3 text-xs text-slate-400">
          <Users size={14} />
          Sĩ số: {week.headcount ?? "—"} · Có mặt: {week.present_count ?? "—"}
        </footer>
      )}
    </article>
  );
}
