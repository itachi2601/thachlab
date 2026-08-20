"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertTriangle, ClipboardCheck, Copy, LockKeyhole, Plus, RefreshCw, Users } from "lucide-react";
import {
  closeChecklistSession,
  createChecklistSession,
  fetchChecklistAttempts,
  fetchChecklistSessions,
  type ChecklistAttempt,
  type ChecklistLessonId,
  type ChecklistSession,
} from "@/services/cnc-checklist";

type Student = { id: string; name: string; className: string };
const machines: { id: ChecklistLessonId; label: string }[] = [
  { id: "lesson-4-turn", label: "Cài đặt dao – máy tiện" },
  { id: "lesson-4-mill", label: "Cài đặt dao – máy phay" },
  { id: "lesson-5", label: "Gia công tiện" },
  { id: "lesson-6", label: "Gia công phay" },
];

export default function TeacherChecklistPanel({ courseId, students }: { courseId: number; students: Student[] }) {
  const [lessonId, setLessonId] = useState<ChecklistLessonId>("lesson-4-turn");
  const [sessions, setSessions] = useState<ChecklistSession[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [attempts, setAttempts] = useState<ChecklistAttempt[]>([]);
  const [creating, setCreating] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const now = new Date();
  const [title, setTitle] = useState("Ca chấm thực hành");
  const [startsAt, setStartsAt] = useState(new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16));

  const selected = sessions.find((item) => item.id === selectedId) ?? null;
  const load = useCallback(() => fetchChecklistSessions(courseId, lessonId).then((rows) => {
    setSessions(rows);
    setSelectedId((current) => rows.some((item) => item.id === current) ? current : rows[0]?.id ?? null);
  }).catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được phiên chấm.")), [courseId, lessonId]);
  useEffect(() => { void load(); }, [load]);
  useEffect(() => { if (!selectedId) { setAttempts([]); return; } void fetchChecklistAttempts(courseId, { sessionId: selectedId }).then(setAttempts).catch(() => setAttempts([])); }, [courseId, selectedId]);

  async function createSession() {
    setBusy(true); setError("");
    try {
      const item = await createChecklistSession({ courseId, lessonId, title, startsAt, durationMinutes: 90 });
      setSessions((current) => [item, ...current]);
      setSelectedId(item.id);
      setCreating(false);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không mở được phiên chấm.");
    } finally { setBusy(false); }
  }

  function studentName(id: string) { return students.find((item) => item.id === id)?.name ?? "Học sinh"; }

  return <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 sm:p-6">
    <div className="flex flex-wrap items-start justify-between gap-4">
      <div>
        <p className="text-xs font-bold uppercase tracking-[.16em] text-violet-300">Chấm chéo checklist thực hành</p>
        <h3 className="mt-1 font-display text-2xl font-bold text-white">Phiên chấm thực hành</h3>
        <p className="mt-1 text-sm text-slate-500">Mở phiên theo ca máy để học sinh đã qua checklist chấm chéo cho bạn; mục trọng yếu vẫn cần giáo viên xác nhận qua tab Năng lực.</p>
      </div>
      <button onClick={() => setCreating((value) => !value)} className="inline-flex items-center gap-2 rounded-xl bg-orange-500 px-4 py-2.5 text-sm font-bold text-white"><Plus size={17} />Mở phiên chấm</button>
    </div>

    <div className="mt-4 flex gap-2">{machines.map((item) => <button key={item.id} onClick={() => setLessonId(item.id)} className={`rounded-xl border px-4 py-2 text-sm font-bold ${lessonId === item.id ? "border-blue-400/40 bg-blue-500/10 text-blue-200" : "border-white/10 text-slate-400"}`}>{item.label}</button>)}</div>

    {creating && <div className="mt-5 grid gap-3 rounded-2xl border border-orange-400/20 bg-orange-500/5 p-4 sm:grid-cols-[1fr_1fr_auto]">
      <input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Tên ca chấm" className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white" />
      <input type="datetime-local" value={startsAt} onChange={(event) => setStartsAt(event.target.value)} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white" />
      <button disabled={busy || !title.trim()} onClick={createSession} className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold text-white disabled:opacity-40">Mở phiên</button>
    </div>}
    {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}

    <div className="mt-5 grid gap-5 lg:grid-cols-[.75fr_1.4fr]">
      <div>
        <div className="mb-3 flex items-center justify-between"><strong className="text-sm text-white">Các phiên đã mở</strong><button aria-label="Làm mới" onClick={() => void load()} className="text-slate-400"><RefreshCw size={16} /></button></div>
        <div className="space-y-2">
          {sessions.map((item) => <button key={item.id} onClick={() => setSelectedId(item.id)} className={`w-full rounded-xl border p-3 text-left ${selectedId === item.id ? "border-violet-400/40 bg-violet-500/10" : "border-white/5 bg-white/[.02]"}`}>
            <div className="flex justify-between gap-2"><strong className="text-sm text-white">{item.title}</strong><span className={item.status === "open" ? "text-xs font-bold text-emerald-300" : "text-xs text-slate-500"}>{item.status === "open" ? "Đang mở" : "Đã khóa"}</span></div>
            <small className="mt-1 block text-slate-500">{new Date(item.starts_at).toLocaleString("vi-VN")}</small>
          </button>)}
          {!sessions.length && <p className="rounded-xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">Chưa có phiên chấm cho ca máy này.</p>}
        </div>
      </div>
      <div>
        {selected ? <>
          <div className="rounded-2xl border border-violet-400/20 bg-gradient-to-br from-violet-500/10 to-blue-500/5 p-5">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div><small className="font-bold uppercase tracking-wider text-violet-300">Mã phiên chấm</small><div className="mt-1 flex items-center gap-3"><strong className="font-mono text-4xl tracking-[.18em] text-white">{selected.code}</strong><button onClick={() => navigator.clipboard.writeText(selected.code)} className="text-violet-300"><Copy size={18} /></button></div></div>
              <div className="text-right text-sm text-slate-400"><p className="flex items-center justify-end gap-2"><Users size={15} />{attempts.length} lượt đã chấm</p><p className="mt-1 flex items-center justify-end gap-2"><ClipboardCheck size={15} />Đóng {new Date(selected.closes_at).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })}</p></div>
            </div>
            {selected.status === "open" && <button onClick={async () => { await closeChecklistSession(selected.id); await load(); }} className="mt-4 inline-flex items-center gap-2 rounded-full border border-white/10 px-4 py-2 text-xs font-bold text-slate-300"><LockKeyhole size={14} />Khóa phiên</button>}
          </div>
          <div className="mt-4 overflow-x-auto"><table className="w-full min-w-[560px] text-left text-sm"><thead><tr className="border-b border-white/10 text-xs uppercase text-slate-500"><th className="p-3">Học sinh</th><th className="p-3">Người chấm</th><th className="p-3">Điểm</th><th className="p-3">Kết quả</th></tr></thead><tbody>
            {attempts.map((item) => <tr key={item.id} className="border-b border-white/5">
              <td className="p-3"><strong className="text-white">{studentName(item.student_id)}</strong></td>
              <td className="p-3 text-slate-400">{item.grader_id ? studentName(item.grader_id) : "—"} <span className={`ml-1.5 rounded-full px-2 py-0.5 text-[10px] font-bold ${item.grader_role === "teacher" ? "bg-blue-500/10 text-blue-300" : "bg-violet-500/10 text-violet-300"}`}>{item.grader_role === "teacher" ? "GV" : "Bạn học"}</span></td>
              <td className="p-3 font-mono text-slate-300">{item.score.toFixed(1)}/{item.total}</td>
              <td className={`p-3 font-bold ${item.passed ? "text-emerald-300" : "text-amber-300"}`}>{item.passed ? "Đạt" : "Chưa đạt"}{!item.critical_ok || !item.zero_tolerance_ok ? <span className="ml-1.5 inline-flex items-center gap-1 text-red-300"><AlertTriangle size={12} />vi phạm mốc chặn</span> : null}</td>
            </tr>)}
            {!attempts.length && <tr><td colSpan={4} className="p-8 text-center text-slate-500">Chưa có lượt chấm nào trong phiên này.</td></tr>}
          </tbody></table></div>
        </> : <div className="grid min-h-72 place-items-center rounded-2xl border border-dashed border-white/10 text-sm text-slate-500"><ClipboardCheck size={30} /><span className="mt-2">Chọn hoặc mở một phiên chấm.</span></div>}
      </div>
    </div>
  </section>;
}
