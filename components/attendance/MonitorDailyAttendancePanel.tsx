"use client";

import { useCallback, useEffect, useState } from "react";
import { CalendarCheck, Check, History, Loader2, Search, UserX } from "lucide-react";
import { fetchCourseEnrollments } from "@/services/course-enrollments";
import {
  MONITOR_ROLE_LABEL,
  fetchDailyAttendance,
  fetchDailyAttendanceOn,
  submitDailyAttendance,
  vnToday,
  weekRange,
  type AbsentEntry,
  type DailyAttendance,
  type MonitorRole,
} from "@/services/homeroom-shcn";

type Classmate = { id: string; name: string };

const dateFormat = new Intl.DateTimeFormat("vi-VN", { weekday: "short", day: "2-digit", month: "2-digit" });

function formatDate(value: string) {
  return dateFormat.format(new Date(`${value}T00:00:00`));
}

/**
 * Điểm danh nhanh cho lớp trưởng/lớp phó: mặc định cả lớp có mặt, chỉ tick bạn vắng.
 * Chỉ nhập/sửa được trong ngày hôm nay — RLS chặn ngày cũ, giao diện cũng không mở form ngày cũ.
 */
export default function MonitorDailyAttendancePanel({ courseId, role }: { courseId: number; role: MonitorRole }) {
  const today = vnToday();
  const [classmates, setClassmates] = useState<Classmate[]>([]);
  const [absent, setAbsent] = useState<Map<string, string>>(new Map());
  const [headcount, setHeadcount] = useState<number | null>(null);
  const [saved, setSaved] = useState<DailyAttendance | null>(null);
  const [history, setHistory] = useState<DailyAttendance[]>([]);
  const [search, setSearch] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  /** Đưa bản ghi hôm nay (nếu lớp trưởng đã nộp) trở lại form để sửa tiếp. */
  const applySaved = useCallback((row: DailyAttendance | null) => {
    setSaved(row);
    if (!row) return;
    setAbsent(new Map(row.absentees.map((item) => [item.student_id ?? item.full_name, item.reason])));
    setHeadcount(row.headcount);
  }, []);

  useEffect(() => {
    let cancelled = false;
    const range = weekRange(today);
    Promise.all([
      fetchCourseEnrollments(courseId),
      fetchDailyAttendanceOn(courseId, today),
      fetchDailyAttendance(courseId, range.from, range.to).catch(() => []),
    ])
      .then(([rows, row, week]) => {
        if (cancelled) return;
        const active = rows
          .filter((item) => item.status === "active")
          .map((item) => ({ id: item.student_id, name: item.profiles?.full_name || "Sinh viên" }));
        setClassmates(active);
        setHistory(week);
        applySaved(row);
        if (!row) setHeadcount(active.length);
        setError("");
      })
      .catch((cause) => {
        if (!cancelled) setError(cause instanceof Error ? cause.message : "Không tải được danh sách lớp.");
      });
    return () => { cancelled = true; };
  }, [courseId, today, applySaved]);

  function toggleAbsent(studentId: string) {
    setAbsent((current) => {
      const next = new Map(current);
      if (next.has(studentId)) next.delete(studentId);
      else next.set(studentId, "");
      return next;
    });
  }

  async function save() {
    setBusy(true);
    setMessage("");
    setError("");
    try {
      const absentees: AbsentEntry[] = [...absent].map(([studentId, reason]) => ({
        student_id: classmates.some((item) => item.id === studentId) ? studentId : null,
        full_name: classmates.find((item) => item.id === studentId)?.name ?? studentId,
        reason,
      }));
      await submitDailyAttendance({ courseId, date: today, headcount: headcount ?? classmates.length, absentees });
      const range = weekRange(today);
      applySaved(await fetchDailyAttendanceOn(courseId, today));
      setHistory(await fetchDailyAttendance(courseId, range.from, range.to).catch(() => []));
      setMessage(`Đã nộp điểm danh ngày ${formatDate(today)}.`);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không nộp được điểm danh.");
    } finally {
      setBusy(false);
    }
  }

  const visible = classmates.filter((item) =>
    item.name.toLocaleLowerCase("vi-VN").includes(search.trim().toLocaleLowerCase("vi-VN")),
  );
  const total = headcount ?? classmates.length;
  const present = Math.max(0, total - absent.size);

  return (
    <section className="rounded-2xl border border-orange-400/20 bg-orange-500/[.04] p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-bold uppercase tracking-[.16em] text-orange-300">{MONITOR_ROLE_LABEL[role]}</p>
          <h3 className="mt-1 flex items-center gap-2 font-display text-xl font-bold text-white">
            <CalendarCheck size={19} className="text-orange-300" />Điểm danh ngày {formatDate(today)}
          </h3>
          <p className="mt-1 text-xs text-slate-400">
            Mặc định cả lớp có mặt — chỉ tick bạn vắng và ghi lý do. Chỉ nhập/sửa được trong ngày hôm nay.
          </p>
        </div>
        <div className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2 text-right">
          <strong className="block text-lg text-white">{present}/{total}</strong>
          <small className="text-xs text-slate-500">Có mặt · {absent.size} vắng</small>
        </div>
      </div>

      {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}
      {message && <p className="mt-3 rounded-xl bg-emerald-500/10 p-3 text-sm text-emerald-200">{message}</p>}
      {saved && (
        <p className="mt-3 text-xs text-slate-500">
          Đã nộp lúc {new Date(saved.updated_at).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })} — sửa lại rồi bấm nộp nếu có thay đổi.
        </p>
      )}

      <label className="mt-4 flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-slate-400">
        Sĩ số lớp
        <input
          type="number"
          min={0}
          value={headcount ?? ""}
          onChange={(event) => setHeadcount(event.target.value === "" ? null : Math.max(0, Number(event.target.value)))}
          className="w-20 rounded-lg border border-white/10 bg-[#080d1d] px-2 py-1.5 text-sm font-bold text-white"
        />
        <span className="font-normal normal-case text-slate-500">(mặc định lấy theo danh sách lớp: {classmates.length})</span>
      </label>

      <div className="mt-3 flex items-center gap-2 rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2">
        <Search size={15} className="text-slate-500" />
        <input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Tìm bạn trong lớp…"
          className="w-full bg-transparent text-sm text-white placeholder:text-slate-500 focus:outline-none"
        />
      </div>

      <div className="mt-3 grid gap-2 sm:grid-cols-2">
        {visible.map((mate) => {
          const isAbsent = absent.has(mate.id);
          return (
            <div key={mate.id} className={`rounded-xl border p-3 ${isAbsent ? "border-red-400/30 bg-red-500/5" : "border-white/10 bg-black/15"}`}>
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" checked={isAbsent} onChange={() => toggleAbsent(mate.id)} className="h-4 w-4 accent-red-500" />
                <span className={isAbsent ? "font-bold text-red-200" : "text-white"}>{mate.name}</span>
                {isAbsent && <UserX size={14} className="ml-auto text-red-300" />}
              </label>
              {isAbsent && (
                <input
                  value={absent.get(mate.id) ?? ""}
                  onChange={(event) => setAbsent((current) => new Map(current).set(mate.id, event.target.value))}
                  placeholder="Lý do (ốm, có phép, không phép…)"
                  className="mt-2 w-full rounded-lg border border-white/10 bg-[#080d1d] px-2 py-1.5 text-xs text-white placeholder:text-slate-600"
                />
              )}
            </div>
          );
        })}
        {!visible.length && (
          <p className="sm:col-span-2 rounded-xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">
            {classmates.length ? "Không tìm thấy bạn nào phù hợp." : "Danh sách lớp trống — nhờ thầy/cô nhập danh sách lớp trước."}
          </p>
        )}
      </div>

      <button
        disabled={busy || !classmates.length}
        onClick={() => void save()}
        className="mt-4 inline-flex items-center gap-2 rounded-xl bg-orange-600 px-5 py-2.5 text-sm font-bold text-white disabled:opacity-40"
      >
        {busy ? <Loader2 size={16} className="animate-spin" /> : <Check size={16} />}
        {saved ? "Cập nhật điểm danh hôm nay" : "Nộp điểm danh hôm nay"}
      </button>

      {history.length > 0 && (
        <div className="mt-5 border-t border-white/10 pt-4">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-slate-400">
            <History size={14} />Tuần này đã nộp
          </div>
          <div className="mt-2 flex flex-wrap gap-2">
            {history.map((row) => (
              <span key={row.id} className="rounded-full border border-white/10 bg-black/20 px-3 py-1 text-xs text-slate-300">
                {formatDate(row.attendance_date)}: {row.present_count}/{row.headcount}
                {row.absentees.length > 0 && <span className="text-red-300"> · {row.absentees.length} vắng</span>}
              </span>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
