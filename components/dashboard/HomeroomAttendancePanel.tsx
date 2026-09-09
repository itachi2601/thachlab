"use client";

import { useCallback, useEffect, useState } from "react";
import {
  AlertTriangle,
  CalendarCheck,
  Check,
  CheckCheck,
  Clock3,
  Copy,
  Grid3x3,
  LockKeyhole,
  NotebookPen,
  Plus,
  RefreshCw,
  Search,
  Trash2,
  UserCheck,
  Users,
} from "lucide-react";
import {
  closeAttendanceSession,
  createAttendanceSession,
  deleteAttendanceSession,
  fetchAttendanceRecords,
  fetchAttendanceSessions,
  setAttendanceRecord,
  setAttendanceRecordBonus,
  setAttendanceRecordNote,
  updateAttendanceSessionNote,
  type AttendanceRecord,
  type AttendanceSession,
  type AttendanceStatus,
} from "@/services/course-attendance";

type Student = { id: string; name: string; className: string };

const statusMeta: Record<AttendanceStatus, { label: string; code: string; style: string; active: string }> = {
  present: { label: "Có mặt", code: "C", style: "text-emerald-300", active: "border-emerald-400/50 bg-emerald-500/15 text-emerald-200" },
  late: { label: "Đi trễ", code: "T", style: "text-amber-300", active: "border-amber-400/50 bg-amber-500/15 text-amber-200" },
  excused: { label: "Vắng có phép", code: "VP", style: "text-blue-300", active: "border-blue-400/50 bg-blue-500/15 text-blue-200" },
  absent: { label: "Vắng không phép", code: "V", style: "text-red-300", active: "border-red-400/50 bg-red-500/15 text-red-200" },
};

export default function HomeroomAttendancePanel({ courseId, students }: { courseId: number; students: Student[] }) {
  const [view, setView] = useState<"live" | "summary">("live");
  const [sessions, setSessions] = useState<AttendanceSession[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [allRecords, setAllRecords] = useState<AttendanceRecord[]>([]);
  const [creating, setCreating] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [copied, setCopied] = useState(false);
  const [noteDraft, setNoteDraft] = useState("");
  const [bonusDrafts, setBonusDrafts] = useState<Record<string, string>>({});
  const [recordNoteDrafts, setRecordNoteDrafts] = useState<Record<string, string>>({});
  const [title, setTitle] = useState("Giáo dục đạo đức & phát triển nghề nghiệp");
  const [sessionDate, setSessionDate] = useState(() => new Date().toISOString().slice(0, 10));

  const selected = sessions.find((item) => item.id === selectedId) ?? null;

  const loadSessions = useCallback(
    () =>
      fetchAttendanceSessions(courseId)
        .then((rows) => {
          setSessions(rows);
          setSelectedId((current) => (rows.some((item) => item.id === current) ? current : rows[0]?.id ?? null));
        })
        .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được phiên điểm danh.")),
    [courseId],
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
  useEffect(() => { setBonusDrafts({}); setRecordNoteDrafts({}); }, [selectedId]);

  async function createSession() {
    setBusy(true);
    setError("");
    try {
      const item = await createAttendanceSession({
        courseId,
        title,
        startsAt: `${sessionDate}T07:00`,
        durationMinutes: 300,
        lateMinutes: 15,
      });
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

  async function saveStudentBonus(studentId: string) {
    if (!selected) return;
    const raw = bonusDrafts[studentId];
    if (raw === undefined) return;
    const value = Math.trunc(Number(raw)) || 0;
    try {
      await setAttendanceRecordBonus(selected.id, studentId, value);
      setRecords((current) => current.map((item) => (item.student_id === studentId ? { ...item, bonus_points: value } : item)));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không lưu được điểm nề nếp.");
    }
  }

  async function saveStudentNote(studentId: string) {
    if (!selected) return;
    const value = recordNoteDrafts[studentId];
    if (value === undefined) return;
    try {
      await setAttendanceRecordNote(selected.id, studentId, value);
      setRecords((current) => current.map((item) => (item.student_id === studentId ? { ...item, note: value } : item)));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không lưu được ghi chú.");
    }
  }

  async function removeSelectedSession() {
    if (!selected) return;
    const date = new Date(selected.starts_at).toLocaleDateString("vi-VN");
    if (!window.confirm(`Xóa buổi “${selected.title}” ngày ${date}?\n\nToàn bộ kết quả điểm danh trong buổi này cũng bị xóa. Không thể hoàn tác.`)) return;
    setBusy(true);
    setError("");
    try {
      await deleteAttendanceSession(selected.id);
      setRecords([]);
      await loadSessions();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không xóa được buổi điểm danh.");
    } finally {
      setBusy(false);
    }
  }

  function copyCode() {
    if (!selected) return;
    void navigator.clipboard.writeText(selected.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  const presentCount = records.filter((item) => item.status === "present" || item.status === "late").length;
  const unmarkedCount = selected ? students.filter((student) => !records.some((record) => record.student_id === student.id)).length : 0;
  const visibleStudents = students.filter((student) =>
    `${student.name} ${student.className}`.toLocaleLowerCase("vi-VN").includes(search.trim().toLocaleLowerCase("vi-VN")),
  );

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap gap-2">
        <button onClick={() => setView("live")} className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view === "live" ? "border-blue-400/40 bg-blue-500/10 text-blue-200" : "border-white/10 text-slate-400"}`}>
          <CalendarCheck size={16} />Điểm danh trực tiếp
        </button>
        <button onClick={() => setView("summary")} className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view === "summary" ? "border-blue-400/40 bg-blue-500/10 text-blue-200" : "border-white/10 text-slate-400"}`}>
          <Grid3x3 size={16} />Tổng hợp chuyên cần
        </button>
      </div>

      {view === "live" && (
        <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 sm:p-6">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-[.16em] text-blue-300">Lớp chủ nhiệm</p>
              <h3 className="mt-1 font-display text-2xl font-bold text-white">Điểm danh buổi học</h3>
              <p className="mt-1 text-sm text-slate-500">Mở buổi rồi đánh dấu trực tiếp, hoặc đọc mã 6 số cho học sinh tự điểm danh. Cột nề nếp cộng/trừ điểm rèn luyện từng buổi.</p>
            </div>
            <button onClick={() => setCreating((value) => !value)} className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-bold text-white">
              <Plus size={17} />Mở buổi điểm danh
            </button>
          </div>

          {creating && (
            <div className="mt-5 grid gap-3 rounded-2xl border border-blue-400/20 bg-blue-500/5 p-4 sm:grid-cols-[1fr_1fr_auto]">
              <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Nội dung buổi học" className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white" />
              <input type="date" value={sessionDate} onChange={(e) => setSessionDate(e.target.value)} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white" />
              <button disabled={busy || !title.trim()} onClick={createSession} className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold text-white disabled:opacity-40">Mở buổi</button>
            </div>
          )}
          {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}

          <div className="mt-5 flex flex-wrap items-center gap-3">
            <select aria-label="Chọn buổi điểm danh" value={selectedId ?? ""} onChange={(e) => setSelectedId(Number(e.target.value))} className="min-w-64 flex-1 rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white sm:flex-none">
              <option value="" disabled>Chọn buổi điểm danh…</option>
              {sessions.map((item) => (
                <option key={item.id} value={item.id}>{item.title} · {new Date(item.starts_at).toLocaleDateString("vi-VN")} · {item.status === "open" ? "Đang mở" : "Đã khóa"}</option>
              ))}
            </select>
            <button aria-label="Làm mới" onClick={() => void loadSessions()} className="text-slate-400"><RefreshCw size={16} /></button>
            {!sessions.length && <p className="text-sm text-slate-500">Chưa có buổi nào, hãy mở buổi đầu tiên.</p>}
          </div>

          {selected ? (
            <>
              <div className="mt-4 grid gap-4 lg:grid-cols-[1.3fr_1fr]">
                <div className="rounded-2xl border border-blue-400/20 bg-gradient-to-br from-blue-500/10 to-cyan-500/5 p-5">
                  <div className="flex flex-wrap items-center justify-between gap-4">
                    <div>
                      <small className="font-bold uppercase tracking-wider text-blue-300">Mã điểm danh</small>
                      <div className="mt-1 flex items-center gap-3">
                        <strong className="font-mono text-4xl tracking-[.18em] text-white">{selected.code}</strong>
                        <button onClick={copyCode} className="flex items-center gap-1 text-blue-300">
                          {copied ? (<><CheckCheck size={18} /><small className="text-xs font-bold">Đã chép</small></>) : <Copy size={18} />}
                        </button>
                      </div>
                    </div>
                    <div className="text-right text-sm text-slate-400">
                      <p className="flex items-center justify-end gap-2"><Users size={15} />{presentCount}/{students.length} đã điểm danh</p>
                      <p className="mt-1 flex items-center justify-end gap-2"><Clock3 size={15} />{selected.status === "open" ? `Đóng ${new Date(selected.closes_at).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })}` : "Đã khóa"}</p>
                    </div>
                  </div>
                  <div className="mt-4 flex flex-wrap items-center gap-2">
                    {selected.status === "open" && (
                      <button onClick={async () => { await closeAttendanceSession(selected.id); await loadSessions(); }} className="inline-flex items-center gap-2 rounded-full border border-white/10 px-4 py-2 text-xs font-bold text-slate-300">
                        <LockKeyhole size={14} />Khóa buổi
                      </button>
                    )}
                    {selected.status === "open" && unmarkedCount > 0 && (
                      <button disabled={busy} onClick={() => void markRemainingPresent()} className="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-4 py-2 text-xs font-bold text-emerald-200 disabled:opacity-40">
                        <Check size={14} />Đánh dấu {unmarkedCount} HS còn lại: Có mặt
                      </button>
                    )}
                    <button type="button" disabled={busy} onClick={() => void removeSelectedSession()} className="inline-flex items-center gap-1.5 rounded-full border border-red-400/25 px-3 py-2 text-xs font-bold text-red-300 hover:border-red-400/50 hover:bg-red-500/10 disabled:opacity-40">
                      <Trash2 size={13} />Xóa buổi mở nhầm
                    </button>
                  </div>
                </div>
                <div className="rounded-2xl border border-white/10 bg-white/[.02] p-5">
                  <div className="flex items-center gap-2 text-sm font-bold text-white"><NotebookPen size={16} className="text-violet-300" />Sổ đầu bài / ghi chú buổi</div>
                  <textarea value={noteDraft} onChange={(e) => setNoteDraft(e.target.value)} onBlur={saveNote} rows={4} placeholder="Nội dung dạy, xếp loại tiết, học sinh vi phạm / tuyên dương, HS xin nghỉ đột xuất…" className="mt-3 w-full resize-none rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2.5 text-sm text-white placeholder:text-slate-500 focus:outline-none" />
                </div>
              </div>

              <div className="mt-4 flex items-center gap-2 rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2">
                <Search size={15} className="text-slate-500" />
                <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Tìm học sinh theo tên hoặc lớp…" className="w-full bg-transparent text-sm text-white placeholder:text-slate-500 focus:outline-none" />
              </div>
              <div className="mt-3 overflow-x-auto">
                <table className="w-full min-w-[820px] text-left text-sm">
                  <thead>
                    <tr className="border-b border-white/10 text-xs uppercase text-slate-500">
                      <th className="p-3">Học sinh</th>
                      <th className="p-3">Giờ vào</th>
                      <th className="p-3">Điểm danh</th>
                      <th className="p-3">Nề nếp</th>
                      <th className="p-3">Ghi chú</th>
                    </tr>
                  </thead>
                  <tbody>
                    {visibleStudents.map((student) => {
                      const record = records.find((item) => item.student_id === student.id);
                      const bonusValue = bonusDrafts[student.id] ?? String(record?.bonus_points ?? 0);
                      const noteValue = recordNoteDrafts[student.id] ?? record?.note ?? "";
                      const bonusNum = Number(bonusValue) || 0;
                      return (
                        <tr key={student.id} className="border-b border-white/5">
                          <td className="p-3"><strong className="text-white">{student.name}</strong><small className="block text-slate-500">{student.className}</small></td>
                          <td className="p-3 text-slate-400">{record?.checked_in_at ? new Date(record.checked_in_at).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }) : "—"}</td>
                          <td className="p-3">
                            <select disabled={busy} value={record?.status ?? ""} onChange={(e) => void mark(student.id, e.target.value as AttendanceStatus)} className={`rounded-lg border bg-[#080d1d] px-2.5 py-1.5 text-xs font-bold disabled:opacity-40 border-white/10 ${record ? statusMeta[record.status].style : "text-slate-500"}`}>
                              <option value="" disabled>Chọn</option>
                              {Object.entries(statusMeta).map(([value, meta]) => (
                                <option key={value} value={value}>{meta.label}</option>
                              ))}
                            </select>
                          </td>
                          <td className="p-3">
                            <input
                              type="number"
                              step={1}
                              disabled={!record}
                              title={!record ? "Điểm danh trước khi chấm nề nếp" : ""}
                              value={bonusValue}
                              onChange={(e) => setBonusDrafts((current) => ({ ...current, [student.id]: e.target.value }))}
                              onBlur={() => void saveStudentBonus(student.id)}
                              className={`w-20 rounded-lg border bg-[#080d1d] px-2 py-1.5 text-xs font-bold disabled:cursor-not-allowed disabled:opacity-30 ${bonusNum > 0 ? "border-emerald-400/30 text-emerald-300" : bonusNum < 0 ? "border-red-400/30 text-red-300" : "border-white/10 text-slate-300"}`}
                            />
                          </td>
                          <td className="p-3">
                            <input
                              type="text"
                              disabled={!record}
                              title={!record ? "Điểm danh trước khi ghi chú" : ""}
                              value={noteValue}
                              onChange={(e) => setRecordNoteDrafts((current) => ({ ...current, [student.id]: e.target.value }))}
                              onBlur={() => void saveStudentNote(student.id)}
                              placeholder={record ? "Lý do vắng, vi phạm…" : "—"}
                              className="w-44 rounded-lg border border-white/10 bg-[#080d1d] px-2 py-1.5 text-xs text-white placeholder:text-slate-600 disabled:cursor-not-allowed disabled:opacity-30"
                            />
                          </td>
                        </tr>
                      );
                    })}
                    {!visibleStudents.length && (
                      <tr><td colSpan={5} className="p-6 text-center text-sm text-slate-500">Không tìm thấy học sinh phù hợp.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </>
          ) : (
            <div className="mt-5 grid min-h-56 place-items-center rounded-2xl border border-dashed border-white/10 text-sm text-slate-500">
              <CalendarCheck size={26} /><span className="mt-2">Chọn hoặc mở một buổi điểm danh.</span>
            </div>
          )}
        </section>
      )}

      {view === "summary" && <AttendanceMatrixSummary students={students} sessions={sessions} allRecords={allRecords} />}
    </div>
  );
}

function AttendanceMatrixSummary({ students, sessions, allRecords }: { students: Student[]; sessions: AttendanceSession[]; allRecords: AttendanceRecord[] }) {
  const orderedSessions = sessions.toSorted((a, b) => Date.parse(a.starts_at) - Date.parse(b.starts_at));
  const rows = students.map((student) => {
    const own = allRecords.filter((row) => row.student_id === student.id);
    const present = own.filter((row) => row.status === "present").length;
    const late = own.filter((row) => row.status === "late").length;
    const excused = own.filter((row) => row.status === "excused").length;
    const absent = own.filter((row) => row.status === "absent").length;
    const conduct = own.reduce((sum, row) => sum + (row.bonus_points ?? 0), 0);
    const rate = orderedSessions.length ? Math.min(100, Math.round(((present + late) / orderedSessions.length) * 100)) : 0;
    const cells = orderedSessions.map((session) => own.find((row) => row.session_id === session.id)?.status ?? null);
    return { ...student, present, late, excused, absent, conduct, rate, cells };
  });
  const classRate = orderedSessions.length && students.length
    ? Math.round((allRecords.filter((row) => row.status === "present" || row.status === "late").length / (orderedSessions.length * students.length)) * 100)
    : 0;
  const perfect = rows.filter((row) => orderedSessions.length > 0 && row.present === orderedSessions.length).length;
  const concern = rows.filter((row) => row.absent >= 2 || row.late >= 3 || (orderedSessions.length >= 3 && row.rate < 75)).length;

  return (
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
      <div className="flex items-center gap-2"><Grid3x3 size={19} className="text-blue-300" /><h3 className="font-display text-xl font-bold text-white">Tổng hợp chuyên cần & nề nếp</h3></div>
      <p className="mt-1 text-xs text-slate-500">Ký hiệu: <b className="text-emerald-300">C</b> Có mặt · <b className="text-amber-300">T</b> Đi trễ · <b className="text-blue-300">VP</b> Vắng có phép · <b className="text-red-300">V</b> Vắng không phép. Cột nề nếp là tổng điểm cộng/trừ rèn luyện các buổi.</p>
      <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryMetric icon={<CalendarCheck size={16} />} value={String(orderedSessions.length)} label="Buổi đã tổ chức" />
        <SummaryMetric icon={<Users size={16} />} value={orderedSessions.length ? `${classRate}%` : "—"} label="Chuyên cần trung bình" />
        <SummaryMetric icon={<UserCheck size={16} />} value={String(perfect)} label="Chuyên cần đầy đủ" />
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
                <th className="min-w-16 border-b border-white/10 p-2 text-center text-xs uppercase text-slate-400">Vắng</th>
                <th className="min-w-16 border-b border-white/10 p-2 text-center text-xs uppercase text-slate-400">Nề nếp</th>
                <th className="min-w-16 border-b border-white/10 p-2 text-center text-xs uppercase text-slate-400">Tỷ lệ</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id} className="group">
                  <td className="sticky left-0 z-10 border-b border-r border-white/5 bg-[#0B1020] p-3 group-hover:bg-[#10192a]">
                    <strong className="block text-sm text-white">{row.name}</strong>
                    <small className="text-slate-500">{row.className}</small>
                  </td>
                  {row.cells.map((status, index) => (
                    <td key={index} className="border-b border-white/5 p-1.5 text-center">
                      {status ? <span className={`inline-flex h-6 w-9 items-center justify-center rounded-md text-[11px] font-bold ${statusMeta[status].active}`}>{statusMeta[status].code}</span> : <span className="text-slate-700">–</span>}
                    </td>
                  ))}
                  <td className="border-b border-white/5 p-2 text-center text-xs font-bold text-slate-300">{row.absent + row.excused > 0 ? `${row.absent}${row.excused ? ` (+${row.excused}P)` : ""}` : "0"}</td>
                  <td className={`border-b border-white/5 p-2 text-center text-xs font-bold ${row.conduct > 0 ? "text-emerald-300" : row.conduct < 0 ? "text-red-300" : "text-slate-500"}`}>{row.conduct > 0 ? `+${row.conduct}` : row.conduct}</td>
                  <td className="border-b border-white/5 p-2 text-center">
                    <span className={`rounded-full px-2.5 py-1 text-xs font-bold ${row.rate >= 90 ? "bg-emerald-500/10 text-emerald-300" : row.rate >= 75 ? "bg-amber-500/10 text-amber-300" : "bg-red-500/10 text-red-300"}`}>
                      {row.rate}%
                    </span>
                  </td>
                </tr>
              ))}
              {!rows.length && <tr><td colSpan={orderedSessions.length + 4} className="p-8 text-center text-slate-500">Chưa có học sinh.</td></tr>}
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
