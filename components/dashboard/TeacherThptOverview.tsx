"use client";

import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, ArrowRight, CalendarCheck, GraduationCap, Users } from "lucide-react";
import type { ClassStudent } from "@/services/classes";
import { fetchClassExamResults, type ClassExamResult } from "@/services/class-results";
import { fetchAttendanceRecords, fetchAttendanceSessions, type ThptAttendanceRecord } from "@/services/class-attendance";

export default function TeacherThptOverview({
  classId,
  students,
  onOpenTab,
  onOpenStudent,
}: {
  classId: number;
  students: ClassStudent[];
  onOpenTab: (tab: "gradebook" | "attendance") => void;
  onOpenStudent: (id: string) => void;
}) {
  const [results, setResults] = useState<ClassExamResult[]>([]);
  const [attendance, setAttendance] = useState<ThptAttendanceRecord[]>([]);
  const [sessionCount, setSessionCount] = useState(0);

  const studentIds = useMemo(() => students.map((item) => item.id), [students]);

  useEffect(() => {
    let cancelled = false;
    fetchClassExamResults(studentIds).then((rows) => { if (!cancelled) setResults(rows); }).catch(() => undefined);
    return () => { cancelled = true; };
  }, [studentIds]);

  useEffect(() => {
    let cancelled = false;
    fetchAttendanceSessions(classId)
      .then(async (sessions) => {
        const rows = (await Promise.all(sessions.map((session) => fetchAttendanceRecords(session.id).catch(() => [])))).flat();
        if (cancelled) return;
        setSessionCount(sessions.length);
        setAttendance(rows);
      })
      .catch(() => undefined);
    return () => { cancelled = true; };
  }, [classId]);

  const scoreByStudent = useMemo(() => {
    const map = new Map<string, number[]>();
    for (const row of results) {
      const list = map.get(row.student_id) ?? [];
      list.push(Number(row.score));
      map.set(row.student_id, list);
    }
    return map;
  }, [results]);

  const attendanceRateByStudent = useMemo(() => {
    const map = new Map<string, number>();
    if (!sessionCount) return map;
    for (const student of students) {
      const own = attendance.filter((row) => row.student_id === student.id);
      const attended = own.filter((row) => row.status === "present" || row.status === "late").length;
      map.set(student.id, Math.round((attended / sessionCount) * 100));
    }
    return map;
  }, [attendance, sessionCount, students]);

  const classAverage = useMemo(() => {
    if (results.length === 0) return 0;
    const sum = results.reduce((total, row) => total + Number(row.score), 0);
    return Math.round((sum / results.length) * 10) / 10;
  }, [results]);

  const attendanceAverage = useMemo(() => {
    if (attendanceRateByStudent.size === 0) return null;
    const values = [...attendanceRateByStudent.values()];
    return Math.round(values.reduce((a, b) => a + b, 0) / values.length);
  }, [attendanceRateByStudent]);

  const concern = useMemo(() => {
    return students
      .map((student) => {
        const scores = scoreByStudent.get(student.id) ?? [];
        const avg = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : null;
        const rate = attendanceRateByStudent.get(student.id);
        const reasons: string[] = [];
        if (avg === null) reasons.push("Chưa làm bài kiểm tra nào");
        else if (avg < 5) reasons.push(`Điểm trung bình ${avg.toFixed(1)}`);
        if (rate !== undefined && rate < 75) reasons.push(`Đi học ${rate}%`);
        return { student, reasons };
      })
      .filter((item) => item.reasons.length > 0)
      .slice(0, 8);
  }, [students, scoreByStudent, attendanceRateByStudent]);

  return (
    <div className="space-y-5">
      <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <Metric icon={<Users size={18} />} value={String(students.length)} label="Học sinh" tone="blue" />
        <Metric icon={<GraduationCap size={18} />} value={results.length ? classAverage.toFixed(1) : "—"} label="Điểm trung bình lớp" tone="violet" />
        <Metric icon={<CalendarCheck size={18} />} value={sessionCount && attendanceAverage !== null ? `${attendanceAverage}%` : "—"} label="Tham dự trung bình" tone="emerald" />
        <Metric icon={<AlertTriangle size={18} />} value={String(concern.length)} label="Học sinh cần quan tâm" tone="amber" />
      </section>

      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div className="mb-4 flex items-center gap-2 text-amber-300">
          <AlertTriangle size={18} />
          <h3 className="font-display text-lg font-bold text-white">Học sinh cần quan tâm</h3>
        </div>
        {concern.length ? (
          <div className="space-y-2">
            {concern.map((item) => (
              <button
                key={item.student.id}
                onClick={() => onOpenStudent(item.student.id)}
                className="flex w-full items-center justify-between rounded-xl border border-red-400/10 bg-red-500/5 p-3 text-left"
              >
                <div>
                  <strong className="text-sm text-white">{item.student.full_name}</strong>
                  <small className="mt-1 block text-red-200/70">{item.reasons.join(" · ")}</small>
                </div>
                <ArrowRight size={16} className="text-red-300" />
              </button>
            ))}
          </div>
        ) : (
          <Empty text="Chưa có học sinh thuộc nhóm cần quan tâm." />
        )}
      </section>

      <section className="grid gap-3 sm:grid-cols-2">
        <button
          onClick={() => onOpenTab("gradebook")}
          className="flex items-center justify-between rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-left hover:border-white/30"
        >
          <span>
            <strong className="block text-lg text-white">Xem bảng điểm</strong>
            <small className="text-slate-400">{results.length} lượt làm bài của lớp</small>
          </span>
          <ArrowRight size={18} className="text-blue-300" />
        </button>
        <button
          onClick={() => onOpenTab("attendance")}
          className="flex items-center justify-between rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-left hover:border-white/30"
        >
          <span>
            <strong className="block text-lg text-white">Điểm danh buổi học</strong>
            <small className="text-slate-400">Mở phiên điểm danh mới</small>
          </span>
          <ArrowRight size={18} className="text-blue-300" />
        </button>
      </section>
    </div>
  );
}

function Metric({ icon, value, label, tone }: { icon: React.ReactNode; value: string; label: string; tone: string }) {
  const styles: Record<string, string> = {
    blue: "border-blue-500/20 bg-blue-500/8 text-blue-300",
    violet: "border-violet-500/20 bg-violet-500/8 text-violet-300",
    emerald: "border-emerald-500/20 bg-emerald-500/8 text-emerald-300",
    amber: "border-amber-500/20 bg-amber-500/8 text-amber-300",
  };
  return (
    <div className={`rounded-2xl border p-5 ${styles[tone]}`}>
      <div className="flex items-center gap-2">
        {icon}
        <span className="text-xs font-semibold uppercase tracking-wider">{label}</span>
      </div>
      <strong className="mt-3 block text-3xl text-white">{value}</strong>
    </div>
  );
}

function Empty({ text }: { text: string }) {
  return <p className="rounded-xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">{text}</p>;
}
