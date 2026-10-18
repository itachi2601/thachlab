"use client";

import { useEffect, useMemo, useState } from "react";
import { ChevronDown, DoorOpen, Tv } from "lucide-react";
import type { ClassStudent } from "@/services/classes";
import { fetchClassExamResults, type ClassExamResult } from "@/services/class-results";
import { fetchAttendanceRecordsForSessions, fetchAttendanceSessions, type ThptAttendanceRecord, type ThptAttendanceSession } from "@/services/class-attendance";
import { fetchWrongestQuestions, type WrongestQuestion } from "@/services/analytics";
import { useAuth } from "@/components/auth/AuthProvider";

const noteKey = (classId: number) => `thachlab.gv.ghichu-vao-lop.${classId}`;

/**
 * "Vào lớp" — việc cần nhìn trong 10 phút đầu giờ: ai vắng/trễ buổi trước, câu sai nhiều nhất
 * của đề gần nhất (chiếu ngay), ai chưa nộp, và ghi chú giáo viên để lại cho buổi sau.
 * Ghi chú lưu trong trình duyệt này (localStorage), không đồng bộ giữa các máy.
 */
export default function TeacherThptClassroomMode({ classId, students }: { classId: number; students: ClassStudent[] }) {
  const { profile } = useAuth();
  const reviewBase = profile?.role === "tro_giang" ? "/tro-giang/chua-bai" : "/dashboard-thpt/chua-bai";
  const [showMissing, setShowMissing] = useState(false);
  const studentIds = useMemo(() => students.map((s) => s.id), [students]);
  const nameOf = useMemo(() => new Map(students.map((s) => [s.id, s.full_name])), [students]);

  const [open, setOpen] = useState(true);
  const [results, setResults] = useState<ClassExamResult[] | null>(null);
  const [session, setSession] = useState<ThptAttendanceSession | null>(null);
  const [records, setRecords] = useState<ThptAttendanceRecord[]>([]);
  const [wrongest, setWrongest] = useState<WrongestQuestion[] | null>(null);
  // Component được gắn key theo lớp nên chỉ cần đọc một lần khi mở.
  const [note, setNote] = useState(() => {
    try { return window.localStorage.getItem(noteKey(classId)) ?? ""; } catch { return ""; }
  });

  useEffect(() => {
    let cancelled = false;
    fetchClassExamResults(studentIds).then((r) => { if (!cancelled) setResults(r); }).catch(() => { if (!cancelled) setResults([]); });
    fetchAttendanceSessions(classId)
      .then(async (sessions) => {
        const latest = sessions[0] ?? null;
        const recs = latest ? await fetchAttendanceRecordsForSessions([latest.id]).catch(() => []) : [];
        if (cancelled) return;
        setSession(latest);
        setRecords(recs);
      })
      .catch(() => undefined);
    return () => { cancelled = true; };
  }, [classId, studentIds]);

  // Đề gần nhất = đề có lượt nộp mới nhất của lớp (results đã sắp mới → cũ).
  const latestExam = results?.[0] ? { id: results[0].exam_id, title: results[0].exams?.title ?? `Đề #${results[0].exam_id}` } : null;
  const latestExamId = latestExam?.id ?? null;

  useEffect(() => {
    if (!latestExamId) return;
    let cancelled = false;
    fetchWrongestQuestions(latestExamId, studentIds).then((w) => { if (!cancelled) setWrongest(w); }).catch(() => { if (!cancelled) setWrongest([]); });
    return () => { cancelled = true; };
  }, [latestExamId, studentIds]);

  const notSubmitted = useMemo(() => {
    if (!latestExamId || !results) return [];
    const done = new Set(results.filter((r) => r.exam_id === latestExamId).map((r) => r.student_id));
    return students.filter((s) => !done.has(s.id)).map((s) => s.full_name);
  }, [latestExamId, results, students]);

  const absent = records.filter((r) => r.status === "absent").map((r) => nameOf.get(r.student_id) ?? "—");
  const late = records.filter((r) => r.status === "late").map((r) => nameOf.get(r.student_id) ?? "—");
  const top = (wrongest ?? []).filter((q) => q.total >= 3).slice(0, 2);

  function saveNote(v: string) {
    setNote(v);
    try { window.localStorage.setItem(noteKey(classId), v); } catch { /* không lưu được thì thôi */ }
  }

  return (
    <section className="rounded-2xl border border-emerald-400/20 bg-emerald-500/[.05] p-5">
      <button type="button" onClick={() => setOpen((o) => !o)} className="flex w-full items-center gap-2 text-left" aria-expanded={open}>
        <DoorOpen size={18} className="text-emerald-300" />
        <h3 className="flex-1 font-display text-lg font-bold text-white">Vào lớp</h3>
        <ChevronDown size={16} className={`text-slate-400 transition-transform ${open ? "rotate-180" : ""}`} />
      </button>

      {open && (
        <div className="mt-4 space-y-4 text-sm text-slate-200">
          <div>
            <p className="mb-1 text-xs font-bold uppercase tracking-wide text-slate-400">
              {session ? `Buổi trước · ${session.title || session.session_date}` : "Điểm danh"}
            </p>
            {!session ? (
              <p className="text-slate-400">Lớp chưa có buổi điểm danh nào.</p>
            ) : (
              <>
                <p>Vắng ({absent.length}): {absent.length ? absent.join(", ") : "không ai"}</p>
                <p>Đi trễ ({late.length}): {late.length ? late.join(", ") : "không ai"}</p>
              </>
            )}
          </div>

          <div>
            <p className="mb-1 text-xs font-bold uppercase tracking-wide text-slate-400">
              {latestExam ? `Đề gần nhất · ${latestExam.title}` : "Đề gần nhất"}
            </p>
            {!latestExam ? (
              <p className="text-slate-400">Chưa có lượt nộp đề nào.</p>
            ) : (
              <>
                {top.length === 0 ? (
                  <p className="text-slate-400">{wrongest === null ? "Đang tải…" : "Chưa đủ dữ liệu câu sai (cần ≥3 lượt)."}</p>
                ) : (
                  <ul className="space-y-2">
                    {top.map((q) => (
                      <li key={q.questionIndex} className="flex flex-wrap items-center gap-3 rounded-xl bg-white/[.04] px-4 py-3">
                        <span className="min-w-0 flex-1">Câu {q.questionIndex + 1} · {q.topic} — sai {q.pct}% ({q.wrong}/{q.total})</span>
                        <a
                          href={`${reviewBase}?exam=${latestExam.id}&class=${classId}&q=${q.questionIndex}`}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1.5 rounded-full bg-primary px-3 py-1.5 text-xs font-semibold text-white hover:bg-primary-dark"
                        >
                          <Tv size={14} /> Chiếu
                        </a>
                      </li>
                    ))}
                  </ul>
                )}
                <p className="mt-2">
                  {notSubmitted.length === 0 ? (
                    "Đủ cả lớp đã nộp"
                  ) : (
                    <>
                      <strong>{notSubmitted.length}</strong> em chưa nộp{" "}
                      <button type="button" onClick={() => setShowMissing((v) => !v)} className="font-semibold text-blue-300 underline">
                        {showMissing ? "Ẩn danh sách" : "Xem danh sách"}
                      </button>
                      {showMissing && <span className="mt-1 block text-slate-400">{notSubmitted.join(", ")}</span>}
                    </>
                  )}
                </p>
              </>
            )}
          </div>

          <label className="block">
            <span className="mb-1 block text-xs font-bold uppercase tracking-wide text-slate-400">Ghi chú cho buổi sau (chỉ lưu trên máy này)</span>
            <textarea
              value={note}
              onChange={(e) => saveNote(e.target.value)}
              rows={2}
              placeholder="Ví dụ: tiết sau nhắc lại lực ma sát nghỉ…"
              className="w-full rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white focus:border-primary focus:outline-none"
            />
          </label>
        </div>
      )}
    </section>
  );
}
