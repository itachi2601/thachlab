"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertTriangle, ChevronLeft, ChevronRight, ShieldCheck, UserCog, Users } from "lucide-react";
import {
  ABSENCE_ALERT_THRESHOLD,
  MONITOR_ROLE_LABEL,
  absenceTally,
  fetchDailyAttendance,
  fetchHomeroomMonitors,
  removeHomeroomMonitor,
  setHomeroomMonitor,
  shiftDate,
  vnToday,
  weekRange,
  type DailyAttendance,
  type HomeroomMonitor,
  type MonitorRole,
} from "@/services/homeroom-shcn";

type Student = { id: string; name: string; className: string };

const dayFormat = new Intl.DateTimeFormat("vi-VN", { weekday: "long", day: "2-digit", month: "2-digit" });
const shortFormat = new Intl.DateTimeFormat("vi-VN", { day: "2-digit", month: "2-digit" });

/**
 * Bảng theo dõi điểm danh hàng ngày do lớp trưởng nộp — GVCN xem trước tiết SHCN, kèm cảnh báo
 * sinh viên vắng nhiều và phần giao quyền điểm danh cho lớp trưởng/lớp phó.
 */
export default function HomeroomDailyReport({ courseId, students }: { courseId: number; students: Student[] }) {
  const [anchor, setAnchor] = useState(vnToday);
  const [rows, setRows] = useState<DailyAttendance[]>([]);
  const [monitors, setMonitors] = useState<HomeroomMonitor[]>([]);
  const [pickedStudent, setPickedStudent] = useState("");
  const [pickedRole, setPickedRole] = useState<MonitorRole>("lop_truong");
  const [error, setError] = useState("");
  const range = weekRange(anchor);

  const loadMonitors = useCallback(
    () =>
      fetchHomeroomMonitors(courseId)
        .then(setMonitors)
        .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được danh sách lớp trưởng.")),
    [courseId],
  );

  useEffect(() => { void loadMonitors(); }, [loadMonitors]);

  useEffect(() => {
    let cancelled = false;
    fetchDailyAttendance(courseId, range.from, range.to)
      .then((data) => { if (!cancelled) { setRows(data); setError(""); } })
      .catch((cause) => { if (!cancelled) setError(cause instanceof Error ? cause.message : "Không tải được điểm danh."); });
    return () => { cancelled = true; };
  }, [courseId, range.from, range.to]);

  async function assignMonitor() {
    if (!pickedStudent) return;
    try {
      await setHomeroomMonitor(courseId, pickedStudent, pickedRole);
      setPickedStudent("");
      await loadMonitors();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không giao được quyền điểm danh.");
    }
  }

  async function revokeMonitor(studentId: string) {
    try {
      await removeHomeroomMonitor(courseId, studentId);
      await loadMonitors();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không thu hồi được quyền điểm danh.");
    }
  }

  const alerts = absenceTally(rows).filter((item) => item.days.length >= ABSENCE_ALERT_THRESHOLD);
  const days = [...Array(7)].map((_, index) => shiftDate(range.from, index));

  return (
    <div className="space-y-5">
      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs font-bold uppercase tracking-[.16em] text-cyan-300">Lớp trưởng nộp hàng ngày</p>
            <h3 className="mt-1 font-display text-xl font-bold text-white">
              Điểm danh tuần {shortFormat.format(new Date(`${range.from}T00:00:00`))} – {shortFormat.format(new Date(`${range.to}T00:00:00`))}
            </h3>
          </div>
          <div className="flex items-center gap-2">
            <button aria-label="Tuần trước" onClick={() => setAnchor((value) => shiftDate(value, -7))} className="rounded-lg border border-white/10 p-2 text-slate-300 hover:bg-white/5"><ChevronLeft size={16} /></button>
            <button onClick={() => setAnchor(vnToday())} className="rounded-lg border border-white/10 px-3 py-2 text-xs font-bold text-slate-300 hover:bg-white/5">Tuần này</button>
            <button aria-label="Tuần sau" onClick={() => setAnchor((value) => shiftDate(value, 7))} className="rounded-lg border border-white/10 p-2 text-slate-300 hover:bg-white/5"><ChevronRight size={16} /></button>
          </div>
        </div>

        {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}

        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[620px] text-left text-sm">
            <thead>
              <tr className="border-b border-white/10 text-xs uppercase text-slate-500">
                <th className="p-3">Ngày</th>
                <th className="p-3">Sĩ số</th>
                <th className="p-3">Có mặt</th>
                <th className="p-3">Vắng</th>
                <th className="p-3">Giờ nộp</th>
              </tr>
            </thead>
            <tbody>
              {days.map((date) => {
                const row = rows.find((item) => item.attendance_date === date);
                return (
                  <tr key={date} className="border-b border-white/5">
                    <td className="p-3 capitalize text-slate-300">{dayFormat.format(new Date(`${date}T00:00:00`))}</td>
                    <td className="p-3 text-slate-300">{row?.headcount ?? "—"}</td>
                    <td className="p-3 font-bold text-emerald-300">{row?.present_count ?? "—"}</td>
                    <td className="p-3">
                      {!row ? <span className="text-slate-600">Chưa nộp</span>
                        : row.absentees.length === 0 ? <span className="text-emerald-300">Đủ</span>
                        : <span className="text-red-200">{row.absentees.map((item) => item.reason ? `${item.full_name} (${item.reason})` : item.full_name).join(", ")}</span>}
                    </td>
                    <td className="p-3 text-xs text-slate-500">{row ? new Date(row.updated_at).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }) : "—"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <Metric icon={<Users size={15} />} label="Ngày đã nộp" value={`${rows.length}/7`} />
          <Metric icon={<Users size={15} />} label="Vắng cả tuần" value={String(rows.reduce((sum, row) => sum + row.absentees.length, 0))} />
          <Metric icon={<AlertTriangle size={15} />} label={`Vắng ≥ ${ABSENCE_ALERT_THRESHOLD} buổi`} value={String(alerts.length)} danger />
        </div>
      </section>

      {alerts.length > 0 && (
        <section className="rounded-2xl border border-red-400/20 bg-red-500/[.05] p-5">
          <div className="flex items-center gap-2 text-sm font-bold text-red-200"><AlertTriangle size={17} />Cần nhắc nhở trong tiết sinh hoạt</div>
          <ul className="mt-3 space-y-2">
            {alerts.map((item) => (
              <li key={item.name} className="rounded-xl border border-red-400/15 bg-black/20 p-3 text-sm">
                <strong className="text-white">{item.name}</strong>
                <span className="ml-2 text-red-300">vắng {item.days.length} buổi</span>
                <p className="mt-1 text-xs text-slate-400">
                  {item.days.map((day) => shortFormat.format(new Date(`${day}T00:00:00`))).join(", ")}
                  {item.reasons.length > 0 && ` · ${[...new Set(item.reasons)].join("; ")}`}
                </p>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div className="flex items-center gap-2"><UserCog size={18} className="text-blue-300" /><h3 className="font-display text-lg font-bold text-white">Lớp trưởng / lớp phó</h3></div>
        <p className="mt-1 text-sm text-slate-500">Người được giao chỉ điểm danh cho lớp này và chỉ sửa được bản ghi trong ngày hôm nay.</p>

        <div className="mt-4 flex flex-wrap gap-2">
          <select aria-label="Chọn sinh viên" value={pickedStudent} onChange={(event) => setPickedStudent(event.target.value)} className="min-w-56 flex-1 rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white sm:flex-none">
            <option value="">Chọn sinh viên…</option>
            {students.filter((student) => !monitors.some((monitor) => monitor.student_id === student.id)).map((student) => (
              <option key={student.id} value={student.id}>{student.name}</option>
            ))}
          </select>
          <select aria-label="Chức vụ" value={pickedRole} onChange={(event) => setPickedRole(event.target.value as MonitorRole)} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white">
            {(Object.keys(MONITOR_ROLE_LABEL) as MonitorRole[]).map((role) => <option key={role} value={role}>{MONITOR_ROLE_LABEL[role]}</option>)}
          </select>
          <button disabled={!pickedStudent} onClick={() => void assignMonitor()} className="rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white disabled:opacity-40">Giao quyền điểm danh</button>
        </div>

        <div className="mt-4 space-y-2">
          {monitors.map((monitor) => (
            <div key={monitor.student_id} className="flex flex-wrap items-center justify-between gap-2 rounded-xl border border-white/5 bg-black/15 p-3">
              <div className="flex items-center gap-2 text-sm">
                <ShieldCheck size={15} className="text-emerald-300" />
                <strong className="text-white">{monitor.profiles?.full_name ?? students.find((item) => item.id === monitor.student_id)?.name ?? "Sinh viên"}</strong>
                <span className="rounded-full bg-blue-500/10 px-2 py-0.5 text-xs font-bold text-blue-200">{MONITOR_ROLE_LABEL[monitor.role]}</span>
              </div>
              <button onClick={() => void revokeMonitor(monitor.student_id)} className="rounded-lg border border-red-400/25 px-3 py-1.5 text-xs font-bold text-red-300 hover:bg-red-500/10">Thu hồi</button>
            </div>
          ))}
          {!monitors.length && <p className="rounded-xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">Chưa giao cho ai — lớp chưa điểm danh hàng ngày được.</p>}
        </div>
      </section>
    </div>
  );
}

function Metric({ icon, label, value, danger = false }: { icon: React.ReactNode; label: string; value: string; danger?: boolean }) {
  return (
    <div className={`rounded-xl border p-4 ${danger ? "border-red-400/15 bg-red-500/5 text-red-300" : "border-blue-400/10 bg-blue-500/5 text-blue-300"}`}>
      <div className="flex items-center gap-2 text-xs font-bold uppercase">{icon}{label}</div>
      <strong className="mt-2 block text-2xl text-white">{value}</strong>
    </div>
  );
}
