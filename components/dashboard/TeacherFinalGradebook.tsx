"use client";

import { useEffect, useMemo, useState } from "react";
import { Calculator, CalendarCheck, Search } from "lucide-react";
import { fetchAttendanceRecords, fetchAttendanceSessions, type AttendanceRecord } from "@/services/course-attendance";
import { fetchRubricExamAttemptsByCourse, type RubricExamAttempt } from "@/services/cnc-rubric-exam";
import { fetchCourseGradeOverrides, setCourseGradeOverride, type CourseGradeOverride } from "@/services/course-grade-overrides";
import { CNC_ASSESSMENT_PLAN } from "@/services/cnc-progress";
import type { CncLearningRecord } from "@/services/cnc-learning-records";
import { fetchStudentCodes } from "@/services/student-profile";

type FinalGradeStudent = { id: string; name: string; className: string; records: CncLearningRecord[] };
function activityCount(records: CncLearningRecord[]) {
  return Object.entries(CNC_ASSESSMENT_PLAN).reduce((total, [lessonId, ids]) => total + ids.filter((id) => id !== "rubric-exam").reduce((sum, id) => {
    const record = records.find((item) => item.lesson_id === lessonId && item.assessment_id === id);
    return sum + (id === "checklist-practice" ? (record?.attempt_count ?? 0) : record?.completed ? 1 : 0);
  }, 0), 0);
}

function rubricScore(attempts: RubricExamAttempt[], studentId: string, machine: "tien" | "phay", role: "self" | "teacher") {
  return attempts.find((attempt) => attempt.student_id === studentId && attempt.machine === machine && attempt.role === role)?.total_score ?? null;
}

export default function TeacherFinalGradebook({ courseId, students }: { courseId: number; students: FinalGradeStudent[] }) {
  const [attempts, setAttempts] = useState<RubricExamAttempt[]>([]);
  const [attendance, setAttendance] = useState<AttendanceRecord[]>([]);
  const [sessionCount, setSessionCount] = useState(0);
  const [overrides, setOverrides] = useState<CourseGradeOverride[]>([]);
  const [saving, setSaving] = useState("");
  const [studentCodes, setStudentCodes] = useState<Map<string,string>>(new Map());
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      Promise.all([fetchRubricExamAttemptsByCourse(courseId, "tien"), fetchRubricExamAttemptsByCourse(courseId, "phay")]).then((rows) => rows.flat()),
      fetchAttendanceSessions(courseId).then(async (sessions) => ({ sessions, records: (await Promise.all(sessions.map((session) => fetchAttendanceRecords(session.id)))).flat() })),
      fetchCourseGradeOverrides(courseId).catch(() => []),
    ]).then(([rubricRows, attendanceData, overrideRows]) => {
      if (cancelled) return;
      setAttempts(rubricRows);
      setAttendance(attendanceData.records);
      setSessionCount(attendanceData.sessions.length);
      setOverrides(overrideRows);
      setError("");
    }).catch((cause) => { if (!cancelled) setError(cause instanceof Error ? cause.message : "Không tải được dữ liệu tổng kết điểm."); });
    return () => { cancelled = true; };
  }, [courseId]);
  useEffect(() => { fetchStudentCodes(students.map((student)=>student.id)).then(setStudentCodes).catch(()=>setStudentCodes(new Map())); }, [students]);

  const rows = useMemo(() => students.map((student) => {
    const override = (key: string, fallback: number | null) => overrides.find((item) => item.student_id === student.id && item.grade_key === key)?.score ?? fallback;
    const process = activityCount(student.records);
    const turnSelf = override("rubric:tien:self", rubricScore(attempts, student.id, "tien", "self"));
    const turnTeacher = override("rubric:tien:teacher", rubricScore(attempts, student.id, "tien", "teacher"));
    const millSelf = override("rubric:phay:self", rubricScore(attempts, student.id, "phay", "self"));
    const millTeacher = override("rubric:phay:teacher", rubricScore(attempts, student.id, "phay", "teacher"));
    const ownAttendance = attendance.filter((record) => record.student_id === student.id);
    const attended = ownAttendance.filter((record) => record.status === "present" || record.status === "late").length;
    const attendanceScore = override("attendance", sessionCount ? 10 * attended / sessionCount : 0) ?? 0;
    const sourceBonus = ownAttendance.reduce((sum, record) => sum + record.bonus_points, 0);
    const bonus = override("bonus", sourceBonus) ?? 0;
    const total = Math.min(10, Math.max(0, (turnTeacher ?? 0) * .45 + (millTeacher ?? 0) * .45 + attendanceScore * .1 + bonus));
    return { ...student, studentCode: studentCodes.get(student.id) ?? "", process, turnSelf, turnTeacher, millSelf, millTeacher, attendanceScore, bonus, total };
  }).filter((student) => `${student.name} ${student.className} ${student.studentCode}`.toLocaleLowerCase("vi-VN").includes(query.trim().toLocaleLowerCase("vi-VN"))), [students, attempts, attendance, sessionCount, overrides, studentCodes, query]);

  async function save(studentId: string, gradeKey: string, value: number) {
    const key = `${studentId}:${gradeKey}`;
    const score = gradeKey === "bonus" ? Math.min(10, Math.max(-10, value)) : Math.min(10, Math.max(0, value));
    setSaving(key); setError("");
    try {
      await setCourseGradeOverride(courseId, studentId, gradeKey, score);
      setOverrides((current) => [...current.filter((item) => !(item.student_id === studentId && item.grade_key === gradeKey)), { course_id: courseId, student_id: studentId, grade_key: gradeKey, score, updated_at: new Date().toISOString() }]);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Không lưu được điểm chỉnh sửa."); }
    finally { setSaving(""); }
  }

  return <div className="space-y-5">
    <section className="rounded-2xl border border-cyan-400/15 bg-gradient-to-r from-cyan-500/10 to-blue-500/5 p-5">
      <div className="flex items-center gap-2"><Calculator size={20} className="text-cyan-300"/><h3 className="font-display text-xl font-bold text-white">Tổng kết điểm học phần</h3></div>
      <p className="mt-2 text-sm text-slate-400">Công thức: <b className="text-white">Thi Tiện GV 45%</b> + <b className="text-white">Thi Phay GV 45%</b> + <b className="text-emerald-300">Chuyên cần 10%</b> + <b className="text-amber-300">điểm cộng/trừ</b>. Tổng điểm giới hạn trong thang 0–10.</p><p className="mt-1 text-xs text-cyan-200">Quá trình hiển thị số bài đã đạt và số lượt checklist tự chấm, dùng làm căn cứ cộng/trừ điểm. Điểm tự chấm chỉ để đối chiếu.</p>
      <div className="mt-4 flex items-center gap-2 rounded-xl border border-white/10 bg-black/15 px-3 py-2"><Search size={15} className="text-slate-500"/><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Tìm sinh viên theo tên hoặc lớp…" className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500"/></div>
      {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}
    </section>

    <section className="overflow-auto rounded-2xl border border-white/10 bg-[#0B1020]">
      <table className="min-w-[1450px] border-collapse text-sm">
        <thead className="sticky top-0 z-20 bg-[#111a2e] text-xs text-slate-300"><tr>
          <th className="sticky left-0 z-30 min-w-56 border-b border-r border-white/10 bg-[#111a2e] p-3 text-left">Sinh viên</th>
          <th className="border-b border-white/10 p-3 text-center">MSSV</th>
          <th className="border-b border-l border-white/10 p-3 text-center text-blue-200">Tổng lượt QT</th>
          <th className="border-b border-white/10 p-3 text-center text-violet-200">Tiện · Tự chấm</th><th className="border-b border-white/10 p-3 text-center text-orange-200">Tiện · GV</th>
          <th className="border-b border-white/10 p-3 text-center text-violet-200">Phay · Tự chấm</th><th className="border-b border-white/10 p-3 text-center text-orange-200">Phay · GV</th>
          <th className="border-b border-white/10 p-3 text-center text-emerald-200"><span className="inline-flex items-center gap-1"><CalendarCheck size={13}/>Chuyên cần</span></th>
          <th className="border-b border-white/10 p-3 text-center text-amber-200">Cộng / trừ</th>
          <th className="border-b border-l border-white/10 p-3 text-center text-cyan-200">Tổng kết</th>
        </tr></thead>
        <tbody>{rows.map((student) => <tr key={student.id} className="hover:bg-white/[.02]">
          <td className="sticky left-0 z-10 border-b border-r border-white/5 bg-[#0B1020] p-3"><strong className="block text-white">{student.name}</strong><small className="text-slate-500">{student.className}</small></td>
          <td className="border-b border-white/5 p-3 text-center font-mono text-slate-300">{student.studentCode||"—"}</td>
          <CountCell value={student.process} strong/><EditableGradeCell key={`ts:${student.turnSelf}`} value={student.turnSelf} busy={saving===`${student.id}:rubric:tien:self`} onSave={(value)=>save(student.id,"rubric:tien:self",value)}/><EditableGradeCell key={`tt:${student.turnTeacher}`} value={student.turnTeacher} official busy={saving===`${student.id}:rubric:tien:teacher`} onSave={(value)=>save(student.id,"rubric:tien:teacher",value)}/><EditableGradeCell key={`ms:${student.millSelf}`} value={student.millSelf} busy={saving===`${student.id}:rubric:phay:self`} onSave={(value)=>save(student.id,"rubric:phay:self",value)}/><EditableGradeCell key={`mt:${student.millTeacher}`} value={student.millTeacher} official busy={saving===`${student.id}:rubric:phay:teacher`} onSave={(value)=>save(student.id,"rubric:phay:teacher",value)}/><EditableGradeCell key={`a:${student.attendanceScore}`} value={sessionCount ? student.attendanceScore : null} attendance busy={saving===`${student.id}:attendance`} onSave={(value)=>save(student.id,"attendance",value)}/><EditableGradeCell key={`b:${student.bonus}`} value={student.bonus} bonus busy={saving===`${student.id}:bonus`} onSave={(value)=>save(student.id,"bonus",value)}/><GradeCell value={student.total} total/>
        </tr>)}{!rows.length && <tr><td colSpan={10} className="p-10 text-center text-slate-500">Không có sinh viên phù hợp.</td></tr>}</tbody>
      </table>
    </section>
  </div>;
}

function EditableGradeCell({ value, onSave, busy, official, attendance, bonus }: { value: number | null; onSave: (value: number) => void; busy: boolean; official?: boolean; attendance?: boolean; bonus?: boolean }) {
  function commit(input: HTMLInputElement) { if (input.value.trim() === "" || Number.isNaN(input.valueAsNumber)) return; onSave(input.valueAsNumber); }
  return <td className="border-b border-white/5 p-2 text-center"><input aria-label="Sửa điểm" type="number" min={bonus?-10:0} max={10} step={.01} disabled={busy} defaultValue={value === null ? "" : value.toFixed(2)} onBlur={(event) => commit(event.currentTarget)} onKeyDown={(event) => { if (event.key === "Enter") event.currentTarget.blur(); }} className={`w-20 rounded-lg border border-white/10 bg-black/20 px-2 py-1.5 text-center font-mono font-bold outline-none focus:border-cyan-400/60 disabled:opacity-50 ${bonus ? "text-amber-300" : attendance ? "text-emerald-300" : official ? "text-orange-200" : "text-slate-300"}`}/></td>;
}

function CountCell({ value, strong }: { value: number; strong?: boolean }) {
  return <td className={`border-b border-white/5 p-3 text-center font-mono font-bold ${strong ? "bg-blue-500/5 text-blue-200" : "text-slate-300"}`}>{value}</td>;
}

function GradeCell({ value, strong, official, attendance, total }: { value: number | null; strong?: boolean; official?: boolean; attendance?: boolean; total?: boolean }) {
  const text = value === null ? "—" : value.toFixed(2);
  const tone = total ? "bg-cyan-500/10 text-cyan-200 text-base" : attendance ? "text-emerald-300" : official ? "text-orange-200" : strong ? "text-blue-200" : "text-slate-300";
  return <td className={`border-b border-white/5 p-3 text-center font-mono font-bold ${tone}`}>{text}</td>;
}
