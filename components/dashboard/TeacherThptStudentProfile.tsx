"use client";

import { useEffect, useMemo, useState } from "react";
import { Search } from "lucide-react";
import { fetchCttcStudentIds, removeStudentFromClass, type ClassStudent } from "@/services/classes";
import { fetchClassExamResults, type ClassExamResult } from "@/services/class-results";
import { fetchAttendanceRecords, fetchAttendanceSessions, type ThptAttendanceSession } from "@/services/class-attendance";

const STATUS_LABEL: Record<string, string> = { present: "Có mặt", late: "Đi trễ", excused: "Vắng có phép", absent: "Vắng không phép" };

export default function TeacherThptStudentProfile({
  classId,
  students,
  selectedId,
  onSelect,
  onRemoved,
}: {
  classId: number;
  students: ClassStudent[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  onRemoved?: () => void;
}) {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState<ClassExamResult[]>([]);
  const [sessions, setSessions] = useState<ThptAttendanceSession[]>([]);
  const [attendanceByStudent, setAttendanceByStudent] = useState<Map<string, Map<number, string>>>(new Map());
  const [cttcIds, setCttcIds] = useState<Set<string>>(new Set());
  const [removing, setRemoving] = useState(false);

  const studentIds = useMemo(() => students.map((item) => item.id), [students]);

  useEffect(() => {
    fetchClassExamResults(studentIds).then(setResults).catch(() => setResults([]));
  }, [studentIds]);

  useEffect(() => {
    fetchCttcStudentIds(studentIds).then(setCttcIds).catch(() => setCttcIds(new Set()));
  }, [studentIds]);

  useEffect(() => {
    let cancelled = false;
    fetchAttendanceSessions(classId)
      .then(async (rows) => {
        const records = await Promise.all(rows.map((session) => fetchAttendanceRecords(session.id).catch(() => [])));
        if (cancelled) return;
        setSessions(rows);
        const map = new Map<string, Map<number, string>>();
        records.flat().forEach((record) => {
          const inner = map.get(record.student_id) ?? new Map<number, string>();
          inner.set(record.session_id, record.status);
          map.set(record.student_id, inner);
        });
        setAttendanceByStudent(map);
      })
      .catch(() => undefined);
    return () => { cancelled = true; };
  }, [classId]);

  async function handleRemove() {
    if (!selected) return;
    if (!window.confirm(`Gỡ "${selected.full_name}" khỏi lớp này? Học sinh sẽ mất quyền xem nội dung/đề của lớp.`)) return;
    setRemoving(true);
    try {
      await removeStudentFromClass(selected.id, classId);
      onRemoved?.();
    } catch (error) {
      window.alert(error instanceof Error ? error.message : "Không gỡ được học sinh khỏi lớp.");
    } finally {
      setRemoving(false);
    }
  }

  const visibleStudents = students.filter((item) => item.full_name.toLocaleLowerCase("vi-VN").includes(search.trim().toLocaleLowerCase("vi-VN")));
  const selected = students.find((item) => item.id === selectedId) ?? null;
  const selectedResults = results.filter((row) => row.student_id === selectedId).sort((a, b) => Date.parse(b.created_at) - Date.parse(a.created_at));
  const selectedAttendance = selectedId ? attendanceByStudent.get(selectedId) ?? new Map<number, string>() : new Map<number, string>();

  return (
    <div className="grid gap-4 lg:grid-cols-[280px_1fr]">
      <aside className="rounded-2xl border border-white/10 bg-[#0B1020] p-3">
        <div className="mb-3 flex items-center gap-2 rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2">
          <Search size={15} className="text-slate-500" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Tìm học sinh…"
            className="w-full bg-transparent text-sm text-white placeholder:text-slate-500 focus:outline-none"
          />
        </div>
        <div className="max-h-[60vh] space-y-1 overflow-y-auto">
          {visibleStudents.map((student) => (
            <button
              key={student.id}
              onClick={() => onSelect(student.id)}
              className={`block w-full rounded-xl px-3 py-2.5 text-left text-sm ${
                selectedId === student.id ? "bg-blue-600 text-white" : "text-slate-300 hover:bg-white/5"
              }`}
            >
              <strong className="block">
                {student.full_name}
                {cttcIds.has(student.id) && (
                  <span className="ml-1.5 rounded-full bg-amber-500/20 px-1.5 py-0.5 text-[10px] font-bold text-amber-300">
                    CTTC
                  </span>
                )}
              </strong>
              <small className="opacity-70">{student.class_name || "Chưa cập nhật lớp"}</small>
            </button>
          ))}
          {!visibleStudents.length && <p className="p-3 text-center text-sm text-slate-500">Không tìm thấy học sinh.</p>}
        </div>
      </aside>

      {!selected ? (
        <div className="grid min-h-72 place-items-center rounded-2xl border border-dashed border-white/10 text-sm text-slate-500">
          Chọn một học sinh để xem hồ sơ.
        </div>
      ) : (
        <div className="space-y-4">
          <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h3 className="font-display text-xl font-bold text-white">{selected.full_name}</h3>
                <p className="mt-1 text-sm text-slate-400">Lớp: {selected.class_name || "Chưa cập nhật"}</p>
              </div>
              <button
                type="button"
                onClick={handleRemove}
                disabled={removing}
                className="shrink-0 rounded-xl border border-red-500/30 px-3 py-2 text-xs font-bold text-red-300 hover:bg-red-500/10 disabled:opacity-50"
              >
                {removing ? "Đang gỡ…" : "Xóa khỏi lớp"}
              </button>
            </div>
            {cttcIds.has(selected.id) && (
              <p className="mt-3 rounded-xl border border-amber-500/25 bg-amber-500/[.06] p-3 text-xs text-amber-200">
                Học sinh này cũng có tài khoản CTTC (học CNC/tiện phay) — có thể đã bị gán nhầm
                vào lớp THPT này. Bấm &quot;Xóa khỏi lớp&quot; nếu đúng vậy.
              </p>
            )}
          </section>

          <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
            <h4 className="font-display text-lg font-bold text-white">Lịch sử làm bài kiểm tra</h4>
            {selectedResults.length ? (
              <div className="mt-3 space-y-2">
                {selectedResults.map((row) => (
                  <div key={row.id} className="flex items-center justify-between rounded-xl bg-white/[.02] p-3">
                    <div>
                      <strong className="text-sm text-white">{row.exams?.title ?? `Đề #${row.exam_id}`}</strong>
                      <small className="mt-1 block text-slate-500">{new Date(row.created_at).toLocaleString("vi-VN")}</small>
                    </div>
                    <span className="font-mono text-lg font-bold text-white">{Number(row.score).toLocaleString("vi-VN")}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="mt-3 text-sm text-slate-500">Chưa làm bài kiểm tra nào.</p>
            )}
          </section>

          <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
            <h4 className="font-display text-lg font-bold text-white">Điểm danh</h4>
            {sessions.length ? (
              <div className="mt-3 space-y-2">
                {sessions.map((session) => {
                  const status = selectedAttendance.get(session.id);
                  return (
                    <div key={session.id} className="flex items-center justify-between rounded-xl bg-white/[.02] p-3 text-sm">
                      <span className="text-slate-300">{session.title} · {new Date(session.starts_at).toLocaleDateString("vi-VN")}</span>
                      <span className="font-semibold text-white">{status ? STATUS_LABEL[status] : "Chưa điểm danh"}</span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="mt-3 text-sm text-slate-500">Lớp chưa có buổi điểm danh nào.</p>
            )}
          </section>
        </div>
      )}
    </div>
  );
}
