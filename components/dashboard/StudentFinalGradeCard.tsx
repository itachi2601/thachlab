"use client";

import { useEffect, useMemo, useState } from "react";
import { Award, CalendarCheck, ClipboardCheck, Info } from "lucide-react";
import { fetchMyAttendance } from "@/services/course-attendance";
import { fetchCourseGradeOverrides, type CourseGradeOverride } from "@/services/course-grade-overrides";
import { fetchRubricExamAttemptsForStudent, type RubricExamAttempt } from "@/services/cnc-rubric-exam";
import { CNC_ASSESSMENT_PLAN } from "@/services/cnc-progress";
import type { CncLearningRecord } from "@/services/cnc-learning-records";

function activityCount(records: CncLearningRecord[]) {
  return Object.entries(CNC_ASSESSMENT_PLAN).reduce((total, [lessonId, ids]) => total + ids.filter((id) => id !== "rubric-exam").reduce((sum, id) => {
    const record = records.find((item) => item.lesson_id === lessonId && item.assessment_id === id);
    return sum + (id === "checklist-practice" ? (record?.attempt_count ?? 0) : record?.completed ? 1 : 0);
  }, 0), 0);
}

function attemptScore(attempts: RubricExamAttempt[], machine: "tien" | "phay", role: "self" | "teacher") {
  return attempts.find((attempt) => attempt.machine === machine && attempt.role === role)?.total_score ?? null;
}

export default function StudentFinalGradeCard({ courseId, studentId, records }: { courseId: number; studentId: string; records: CncLearningRecord[] }) {
  const [attempts, setAttempts] = useState<RubricExamAttempt[]>([]);
  const [attendance, setAttendance] = useState<Awaited<ReturnType<typeof fetchMyAttendance>>>([]);
  const [overrides, setOverrides] = useState<CourseGradeOverride[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      Promise.all([fetchRubricExamAttemptsForStudent(courseId, studentId, "tien"), fetchRubricExamAttemptsForStudent(courseId, studentId, "phay")]).then((rows) => rows.flat()),
      fetchMyAttendance(courseId, studentId),
      fetchCourseGradeOverrides(courseId).catch(() => []),
    ]).then(([rubricRows, attendanceRows, overrideRows]) => {
      if (cancelled) return;
      setAttempts(rubricRows);
      setAttendance(attendanceRows);
      setOverrides(overrideRows.filter((item) => item.student_id === studentId));
    }).catch(() => undefined).finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [courseId, studentId]);

  const grade = useMemo(() => {
    const override = (key: string, fallback: number | null) => overrides.find((item) => item.grade_key === key)?.score ?? fallback;
    const turnSelf = override("rubric:tien:self", attemptScore(attempts, "tien", "self"));
    const turnTeacher = override("rubric:tien:teacher", attemptScore(attempts, "tien", "teacher"));
    const millSelf = override("rubric:phay:self", attemptScore(attempts, "phay", "self"));
    const millTeacher = override("rubric:phay:teacher", attemptScore(attempts, "phay", "teacher"));
    const attended = attendance.filter((row) => row.status === "present" || row.status === "late").length;
    const attendanceScore = override("attendance", attendance.length ? 10 * attended / attendance.length : null);
    const sourceBonus = attendance.reduce((sum, row) => sum + row.bonus_points, 0);
    const bonus = override("bonus", sourceBonus) ?? 0;
    const complete = turnTeacher !== null && millTeacher !== null && attendanceScore !== null;
    const total = complete ? Math.min(10, Math.max(0, turnTeacher * .45 + millTeacher * .45 + attendanceScore * .1 + bonus)) : null;
    return { turnSelf, turnTeacher, millSelf, millTeacher, attendanceScore, bonus, total, processCount: activityCount(records) };
  }, [attempts, attendance, overrides, records]);

  if (loading) return <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-sm text-slate-500">Đang tải điểm tổng kết…</section>;
  const classification = grade.total === null ? "Chưa đủ dữ liệu" : grade.total >= 8.5 ? "Xuất sắc" : grade.total >= 7 ? "Khá" : grade.total >= 5 ? "Đạt" : "Chưa đạt";
  const tone = grade.total === null ? "border-slate-400/15 from-slate-500/10" : grade.total >= 8.5 ? "border-emerald-400/25 from-emerald-500/15" : grade.total >= 7 ? "border-blue-400/25 from-blue-500/15" : grade.total >= 5 ? "border-amber-400/25 from-amber-500/15" : "border-red-400/25 from-red-500/15";

  return <section className={`rounded-2xl border bg-gradient-to-r ${tone} to-[#0B1020] p-5 sm:p-6`}>
    <div className="flex flex-wrap items-start justify-between gap-4"><div><div className="flex items-center gap-2 text-cyan-200"><Award size={19}/><strong className="text-xs uppercase tracking-[.14em]">Kết quả học phần</strong></div><h2 className="mt-2 font-display text-xl font-bold text-white">Điểm tổng kết Gia công CNC</h2><p className="mt-1 text-xs text-slate-400">Tiện GV 45% + Phay GV 45% + Chuyên cần 10% + điểm cộng/trừ</p></div><div className="text-right"><strong className="font-mono text-4xl text-white">{grade.total === null ? "—" : grade.total.toFixed(2)}<small className="text-base text-slate-500">/10</small></strong><span className="mt-1 block text-sm font-bold text-cyan-200">{classification}</span></div></div>
    <div className="mt-5 grid gap-2 sm:grid-cols-2 xl:grid-cols-5">
      <GradePart label="Thi Tiện GV" value={grade.turnTeacher} contribution={grade.turnTeacher === null ? null : grade.turnTeacher * .45}/>
      <GradePart label="Thi Phay GV" value={grade.millTeacher} contribution={grade.millTeacher === null ? null : grade.millTeacher * .45}/>
      <GradePart label="Chuyên cần" value={grade.attendanceScore} contribution={grade.attendanceScore === null ? null : grade.attendanceScore * .1} icon={<CalendarCheck size={13}/>}/>
      <GradePart label="Cộng / trừ" value={grade.bonus} signed/>
      <div className="rounded-xl border border-white/10 bg-black/15 p-3"><span className="flex items-center gap-1 text-[10px] font-bold uppercase text-slate-500"><ClipboardCheck size={13}/>Quá trình</span><strong className="mt-1 block text-lg text-white">{grade.processCount} lượt</strong><small className="text-slate-500">Đạt bài / checklist tự chấm</small></div>
    </div>
    <div className="mt-3 flex items-start gap-2 rounded-xl bg-black/15 p-3 text-xs text-slate-400"><Info size={14} className="mt-0.5 shrink-0 text-cyan-300"/><p>{grade.total === null ? "Điểm tổng kết sẽ hiển thị khi đã có đủ điểm giáo viên chấm cho cả phần thi Tiện, phần thi Phay và dữ liệu chuyên cần." : `Điểm tự chấm để tham khảo: Tiện ${grade.turnSelf?.toFixed(2) ?? "—"} · Phay ${grade.millSelf?.toFixed(2) ?? "—"}. Điểm chính thức do giáo viên chấm.`}</p></div>
  </section>;
}

function GradePart({ label, value, contribution, icon, signed }: { label: string; value: number | null; contribution?: number | null; icon?: React.ReactNode; signed?: boolean }) {
  const shown = value === null ? "—" : signed && value > 0 ? `+${value.toFixed(2)}` : value.toFixed(2);
  return <div className="rounded-xl border border-white/10 bg-black/15 p-3"><span className="flex items-center gap-1 text-[10px] font-bold uppercase text-slate-500">{icon}{label}</span><strong className={`mt-1 block text-lg ${signed ? "text-amber-300" : "text-white"}`}>{shown}</strong>{contribution !== undefined && <small className="text-slate-500">Đóng góp {contribution === null ? "—" : contribution.toFixed(2)}</small>}</div>;
}
