"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertTriangle, CalendarCheck, Check, Clock3, Grid3x3, NotebookPen, Plus, RefreshCw, Search, ShieldCheck, UserCheck, Users, XCircle } from "lucide-react";
import {
  createAttendanceSession,
  fetchAttendanceRecords,
  fetchAttendanceSessions,
  setAttendanceRecord,
  updateAttendanceSessionNote,
  type AttendanceStatus,
  type ThptAttendanceRecord,
  type ThptAttendanceSession,
} from "@/services/class-attendance";
import type { ClassStudent } from "@/services/classes";

const statusMeta: Record<AttendanceStatus, { label: string; code: string; style: string; active: string; icon: typeof UserCheck }> = {
  present: { label: "Có mặt", code: "C", style: "text-emerald-300", active: "border-emerald-400/50 bg-emerald-500/15 text-emerald-200", icon: UserCheck },
  late: { label: "Đi trễ", code: "T", style: "text-amber-300", active: "border-amber-400/50 bg-amber-500/15 text-amber-200", icon: Clock3 },
  excused: { label: "Vắng có phép", code: "VP", style: "text-blue-300", active: "border-blue-400/50 bg-blue-500/15 text-blue-200", icon: ShieldCheck },
  absent: { label: "Vắng không phép", code: "V", style: "text-red-300", active: "border-red-400/50 bg-red-500/15 text-red-200", icon: XCircle },
};

export default function TeacherThptAttendancePanel({ classId, students }: { classId: number; students: ClassStudent[] }) {
  const [view, setView] = useState<"live" | "summary">("live");
  const [sessions, setSessions] = useState<ThptAttendanceSession[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [records, setRecords] = useState<ThptAttendanceRecord[]>([]);
  const [allRecords, setAllRecords] = useState<ThptAttendanceRecord[]>([]);
  const [creating, setCreating] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [noteDraft, setNoteDraft] = useState("");
  const [title, setTitle] = useState("Buổi học");
  const [sessionDate, setSessionDate] = useState(() => new Date().toISOString().slice(0, 10));

  const selected = sessions.find((item) => item.id === selectedId) ?? null;

  const loadSessions = useCallback(
    () =>
      fetchAttendanceSessions(classId)
        .then((rows) => {
          setSessions(rows);
          setSelectedId((current) => (rows.some((item) => item.id === current) ? current : rows[0]?.id ?? null));
        })
        .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được phiên điểm danh.")),
    [classId],
  );
  useEffect(() => { void loadSessions(); }, [loadSessions]);

  useEffect(() => {
    let cancelled = false;
    Promise.all(sessions.map((session) => fetchAttendanceRecords(session.id).catch(() => []))).then((rows) => {
      if (!cancelled) setAllRecords(rows.flat());
    });
    return () => { cancelled = true; };
  }, [sessions]);

  useEffect(() => {
    if (!selectedId) { setRecords([]); return; }
    fetchAttendanceRecords(selectedId).then(setRecords).catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được kết quả điểm danh."));
  }, [selectedId]);

  useEffect(() => { setNoteDraft(selected?.note ?? ""); }, [selected?.id, selected?.note]);

  async function createSession() {
    setBusy(true);
    setError("");
    try {
      const item = await createAttendanceSession({ classId, title, sessionDate });
      setSessions((current) => [item, ...current]);
      setSelectedId(item.id);
      setCreating(false);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không mở được phiên điểm danh.");
    } finally {
      setBusy(false);
    }
  }

  async function mark(studentId: string, status: AttendanceStatus) {
    if (!selected) return;
    setBusy(true);
    try {
      await setAttendanceRecord(selected.id, studentId, status);
      setRecords(await fetchAttendanceRecords(selected.id));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không cập nhật được điểm danh.");
    } finally {
      setBusy(false);
    }
  }

  async function markRemainingPresent() {
    if (!selected) return;
    const unmarked = students.filter((student) => !records.some((record) => record.student_id === student.id));
    if (!unmarked.length) return;
    setBusy(true);
    try {
      await Promise.all(unmarked.map((student) => setAttendanceRecord(selected.id, student.id, "present")));
      setRecords(await fetchAttendanceRecords(selected.id));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không cập nhật được điểm danh.");
    } finally {
      setBusy(false);
    }
  }

  async function saveNote() {
    if (!selected || noteDraft === selected.note) return;
    try {
      await updateAttendanceSessionNote(selected.id, noteDraft);
      setSessions((current) => current.map((item) => (item.id === selected.id ? { ...item, note: noteDraft } : item)));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không lưu được ghi chú.");
    }
  }

  const presentCount = records.filter((item) => item.status === "present" || item.status === "late").length;
  const unmarkedCount = selected ? students.filter((student) => !records.some((record) => record.student_id === student.id)).length : 0;
  const visibleStudents = students.filter((student) => student.full_name.toLocaleLowerCase("vi-VN").includes(search.trim().toLocaleLowerCase("vi-VN")));

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap gap-2">
        <button onClick={() => setView("live")} className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view === "live" ? "border-blue-400/40 bg-blue-500/10 text-blue-200" : "border-white/10 text-slate-400"}`}>
          <CalendarCheck size={16} />Điểm danh trực tiếp
        </button>
        <button onClick={() => setView("summary")} className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view === "summary" ? "border-blue-400/40 bg-blue-500/10 text-blue-200" : "border-white/10 text-slate-400"}`}>
          <Grid3x3 size={16} />Tổng hợp điểm danh
        </button>
      </div>

      {view === "live" && (
        <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 sm:p-6">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-[.16em] text-blue-300">Điểm danh lớp học</p>
              <h3 className="mt-1 font-display text-2xl font-bold text-white">Buổi học</h3>
              <p className="mt-1 text-sm text-slate-500">Mở phiên theo buổi học rồi đánh dấu trực tiếp trên lớp.</p>
            </div>
            <button onClick={() => setCreating((value) => !value)} className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-bold text-white">
              <Plus size={17} />Mở phiên điểm danh
            </button>
          </div>

          {creating && (
            <div className="mt-5 grid gap-3 rounded-2xl border border-blue-400/20 bg-blue-500/5 p-4 sm:grid-cols-[1fr_1fr_auto]">
              <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Nội dung buổi học" className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white" />
              <input type="date" value={sessionDate} onChange={(e) => setSessionDate(e.target.value)} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white" />
              <button disabled={busy || !title.trim()} onClick={createSession} className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold text-white disabled:opacity-40">Mở phiên</button>
            </div>
          )}
          {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}

          <div className="mt-5 flex flex-wrap items-center gap-3">
            <select aria-label="Chọn buổi điểm danh" value={selectedId ?? ""} onChange={(e) => setSelectedId(Number(e.target.value))} className="min-w-64 flex-1 rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white sm:flex-none">
              <option value="" disabled>Chọn buổi điểm danh…</option>
              {sessions.map((item) => (
                <option key={item.id} value={item.id}>{item.title} · {new Date(item.starts_at).toLocaleDateString("vi-VN")}</option>
              ))}
            </select>
            <button aria-label="Làm mới" onClick={() => void loadSessions()} className="text-slate-400"><RefreshCw size={16} /></button>
            {!sessions.length && <p className="text-sm text-slate-500">Chưa có buổi điểm danh nào, hãy mở phiên đầu tiên.</p>}
          </div>

          {selected ? (
            <>
              <div className="mt-4 grid gap-4 lg:grid-cols-[1.3fr_1fr]">
                <div className="rounded-2xl border border-blue-400/20 bg-gradient-to-br from-blue-500/10 to-cyan-500/5 p-5">
                  <div className="flex flex-wrap items-center justify-between gap-4">
                    <div>
                      <small className="font-bold uppercase tracking-wider text-blue-300">{selected.title}</small>
                      <p className="mt-1 text-sm text-slate-400">{new Date(selected.starts_at).toLocaleDateString("vi-VN")}</p>
                    </div>
                    <div className="text-right text-sm text-slate-400">
                      <p className="flex items-center justify-end gap-2"><Users size={15} />{presentCount}/{students.length} đã điểm danh</p>
                    </div>
                  </div>
                  {unmarkedCount > 0 && (
                    <button disabled={busy} onClick={() => void markRemainingPresent()} className="mt-4 inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-4 py-2 text-xs font-bold text-emerald-200 disabled:opacity-40">
                      <Check size={14} />Đánh dấu {unmarkedCount} HS còn lại: Có mặt
                    </button>
                  )}
                </div>
                <div className="rounded-2xl border border-white/10 bg-white/[.02] p-5">
                  <div className="flex items-center gap-2 text-sm font-bold text-white"><NotebookPen size={16} className="text-violet-300" />Ghi chú buổi học</div>
                  <textarea value={noteDraft} onChange={(e) => setNoteDraft(e.target.value)} onBlur={saveNote} rows={4} placeholder="Ghi chú nhanh: nội dung dạy, học sinh xin nghỉ đột xuất…" className="mt-3 w-full resize-none rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2.5 text-sm text-white placeholder:text-slate-500 focus:outline-none" />
                </div>
              </div>

              <div className="mt-4 flex items-center gap-2 rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2">
                <Search size={15} className="text-slate-500" />
                <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Tìm học sinh…" className="w-full bg-transparent text-sm text-white placeholder:text-slate-500 focus:outline-none" />
              </div>
              <div className="mt-3 overflow-x-auto">
                <table className="w-full min-w-150 text-left text-sm">
                  <thead>
                    <tr className="border-b border-white/10 text-xs uppercase text-slate-500">
                      <th className="p-3">Học sinh</th>
                      <th className="p-3">Điểm danh</th>
                    </tr>
                  </thead>
                  <tbody>
                    {visibleStudents.map((student) => {
                      const record = records.find((item) => item.student_id === student.id);
                      return (
                        <tr key={student.id} className="border-b border-white/5">
                          <td className="p-3"><strong className="text-white">{student.full_name}</strong><small className="block text-slate-500">{student.class_name}</small></td>
                          <td className="p-3">
                            <select disabled={busy} value={record?.status ?? ""} onChange={(e) => void mark(student.id, e.target.value as AttendanceStatus)} className={`rounded-lg border bg-[#080d1d] px-2.5 py-1.5 text-xs font-bold disabled:opacity-40 border-white/10 ${record ? statusMeta[record.status].style : "text-slate-500"}`}>
                              <option value="" disabled>Chọn</option>
                              {Object.entries(statusMeta).map(([value, meta]) => (
                                <option key={value} value={value}>{meta.label}</option>
                              ))}
                            </select>
                          </td>
                        </tr>
                      );
                    })}
                    {!visibleStudents.length && (
                      <tr><td colSpan={2} className="p-6 text-center text-sm text-slate-500">Không tìm thấy học sinh phù hợp.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </>
          ) : (
            <div className="mt-5 grid min-h-56 place-items-center rounded-2xl border border-dashed border-white/10 text-sm text-slate-500">
              <CalendarCheck size={26} /><span className="mt-2">Chọn hoặc mở một phiên điểm danh.</span>
            </div>
          )}
        </section>
      )}

      {view === "summary" && <AttendanceMatrixSummary students={students} sessions={sessions} allRecords={allRecords} />}
    </div>
  );
}

function AttendanceMatrixSummary({ students, sessions, allRecords }: { students: ClassStudent[]; sessions: ThptAttendanceSession[]; allRecords: ThptAttendanceRecord[] }) {
  const orderedSessions = sessions.toSorted((a, b) => Date.parse(a.starts_at) - Date.parse(b.starts_at));
  const rows = students.map((student) => {
    const own = allRecords.filter((row) => row.student_id === student.id);
    const present = own.filter((row) => row.status === "present").length;
    const late = own.filter((row) => row.status === "late").length;
    const absent = own.filter((row) => row.status === "absent").length;
    const rate = orderedSessions.length ? Math.min(100, Math.round(((present + late) / orderedSessions.length) * 100)) : 0;
    const cells = orderedSessions.map((session) => own.find((row) => row.session_id === session.id)?.status ?? null);
    return { ...student, present, late, absent, rate, cells };
  });
  const classRate = orderedSessions.length && students.length
    ? Math.round((allRecords.filter((row) => row.status === "present" || row.status === "late").length / (orderedSessions.length * students.length)) * 100)
    : 0;
  const perfect = rows.filter((row) => orderedSessions.length > 0 && row.present === orderedSessions.length).length;
  const concern = rows.filter((row) => row.absent >= 2 || row.late >= 3 || (orderedSessions.length >= 3 && row.rate < 75)).length;

  return (
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
      <div className="flex items-center gap-2"><Grid3x3 size={19} className="text-blue-300" /><h3 className="font-display text-xl font-bold text-white">Tổng hợp điểm danh theo học sinh</h3></div>
      <p className="mt-1 text-xs text-slate-500">Ký hiệu: <b className="text-emerald-300">C</b> Có mặt · <b className="text-amber-300">T</b> Đi trễ · <b className="text-blue-300">VP</b> Vắng có phép · <b className="text-red-300">V</b> Vắng không phép</p>
      <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryMetric icon={<CalendarCheck size={16} />} value={String(orderedSessions.length)} label="Buổi đã tổ chức" />
        <SummaryMetric icon={<Users size={16} />} value={orderedSessions.length ? `${classRate}%` : "—"} label="Tham dự trung bình" />
        <SummaryMetric icon={<UserCheck size={16} />} value={String(perfect)} label="Chuyên cần" />
        <SummaryMetric icon={<AlertTriangle size={16} />} value={String(concern)} label="Cần nhắc nhở" danger />
      </div>
      {!orderedSessions.length ? (
        <p className="mt-4 rounded-xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">Chưa có buổi điểm danh nào.</p>
      ) : (
        <div className="mt-4 max-h-[70vh] overflow-auto rounded-xl border border-white/10">
          <table className="w-full min-w-max border-separate border-spacing-0 text-sm">
            <thead className="sticky top-0 z-20 bg-[#10192a]">
              <tr>
                <th className="sticky left-0 z-30 min-w-48 border-b border-r border-white/10 bg-[#10192a] p-3 text-left text-xs uppercase text-slate-400">Học sinh</th>
                {orderedSessions.map((session) => (
                  <th key={session.id} className="min-w-14 border-b border-white/10 p-2 text-center text-[11px] font-bold text-slate-400" title={session.title}>
                    {new Date(session.starts_at).toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" })}
                  </th>
                ))}
                <th className="min-w-16 border-b border-white/10 p-2 text-center text-xs uppercase text-slate-400">Tỷ lệ</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id} className="group">
                  <td className="sticky left-0 z-10 border-b border-r border-white/5 bg-[#0B1020] p-3 group-hover:bg-[#10192a]">
                    <strong className="block text-sm text-white">{row.full_name}</strong>
                    <small className="text-slate-500">{row.class_name}</small>
                  </td>
                  {row.cells.map((status, index) => (
                    <td key={index} className="border-b border-white/5 p-1.5 text-center">
                      {status ? <span className={`inline-flex h-6 w-9 items-center justify-center rounded-md text-[11px] font-bold ${statusMeta[status].active}`}>{statusMeta[status].code}</span> : <span className="text-slate-700">–</span>}
                    </td>
                  ))}
                  <td className="border-b border-white/5 p-2 text-center">
                    <span className={`rounded-full px-2.5 py-1 text-xs font-bold ${row.rate >= 90 ? "bg-emerald-500/10 text-emerald-300" : row.rate >= 75 ? "bg-amber-500/10 text-amber-300" : "bg-red-500/10 text-red-300"}`}>
                      {orderedSessions.length ? `${row.rate}%` : "—"}
                    </span>
                  </td>
                </tr>
              ))}
              {!rows.length && <tr><td colSpan={orderedSessions.length + 2} className="p-8 text-center text-slate-500">Chưa có học sinh.</td></tr>}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function SummaryMetric({ icon, value, label, danger = false }: { icon: React.ReactNode; value: string; label: string; danger?: boolean }) {
  return (
    <div className={`rounded-xl border p-4 ${danger ? "border-red-400/15 bg-red-500/5 text-red-300" : "border-blue-400/10 bg-blue-500/5 text-blue-300"}`}>
      <div className="flex items-center gap-2 text-xs font-bold uppercase">{icon}{label}</div>
      <strong className="mt-2 block text-2xl text-white">{value}</strong>
    </div>
  );
}
