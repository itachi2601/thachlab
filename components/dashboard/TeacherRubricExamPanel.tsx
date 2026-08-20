"use client";

import { useCallback, useEffect, useState } from "react";
import { ClipboardList, Send, UserRound } from "lucide-react";
import RubricExamForm from "@/components/lessons/RubricExamForm";
import { RUBRIC_BY_MACHINE, gradeRubricExam, type RubricLevel } from "@/services/cnc-rubric";
import {
  fetchRubricExamAttemptsByCourse,
  fetchRubricExamAttemptsForStudent,
  submitTeacherRubricGrade,
  type RubricExamAttempt,
  type RubricExamMachine,
} from "@/services/cnc-rubric-exam";
import { fetchCncLearningRecords } from "@/services/cnc-learning-records";

type Student = { id: string; name: string; className: string };
const machines: { id: RubricExamMachine; label: string }[] = [
  { id: "tien", label: "Tiện CNC" },
  { id: "phay", label: "Phay CNC" },
];

export default function TeacherRubricExamPanel({ courseId, students }: { courseId: number; students: Student[] }) {
  const [machine, setMachine] = useState<RubricExamMachine>("tien");
  const [studentId, setStudentId] = useState("");
  const [levels, setLevels] = useState<Record<string, RubricLevel | undefined>>({});
  const [zeroTolerance, setZeroTolerance] = useState<Record<number, boolean>>({});
  const [notes, setNotes] = useState("");
  const [selfAttempt, setSelfAttempt] = useState<RubricExamAttempt | null>(null);
  const [checklistNote, setChecklistNote] = useState("");
  const [courseAttempts, setCourseAttempts] = useState<RubricExamAttempt[]>([]);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  const rubric = RUBRIC_BY_MACHINE[machine];

  const loadCourseAttempts = useCallback(() => {
    fetchRubricExamAttemptsByCourse(courseId, machine).then(setCourseAttempts).catch(() => setCourseAttempts([]));
  }, [courseId, machine]);
  useEffect(() => { loadCourseAttempts(); }, [loadCourseAttempts]);

  const resetForm = useCallback(() => {
    setLevels({});
    setZeroTolerance({});
    setNotes("");
    setSelfAttempt(null);
    setChecklistNote("");
    setSaved(false);
    setError("");
  }, []);

  function chooseStudent(id: string) {
    setStudentId(id);
    resetForm();
    if (!id) return;
    setLoading(true);
    const lessonId = machine === "tien" ? "lesson-5" : "lesson-6";
    Promise.all([
      fetchRubricExamAttemptsForStudent(courseId, id, machine),
      fetchCncLearningRecords(courseId, id),
    ])
      .then(([rows, records]) => {
        const self = rows.find((row) => row.role === "self") ?? null;
        const teacher = rows.find((row) => row.role === "teacher") ?? null;
        setSelfAttempt(self);
        if (teacher) {
          setLevels(teacher.item_levels);
          setZeroTolerance(teacher.zero_tolerance_confirmed);
          setNotes(teacher.notes);
        }
        const checklistRecord = records.find((row) => row.lesson_id === lessonId && row.assessment_id === "checklist");
        setChecklistNote(checklistRecord ? `Điểm checklist chấm chéo gia công: ${checklistRecord.best_score ?? 0}/10` : "Chưa có điểm checklist chấm chéo gia công.");
      })
      .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được bài thi của học sinh."))
      .finally(() => setLoading(false));
  }

  function chooseMachine(next: RubricExamMachine) {
    setMachine(next);
    setStudentId("");
    resetForm();
  }

  async function submit() {
    if (!studentId) return;
    setBusy(true);
    setError("");
    setSaved(false);
    try {
      const result = gradeRubricExam(rubric, levels, zeroTolerance);
      await submitTeacherRubricGrade({
        courseId, studentId, machine, itemLevels: levels as Record<string, RubricLevel>,
        zeroToleranceConfirmed: zeroTolerance, kyThuatScore: result.groupScores[rubric.gateGroupId] ?? 0,
        thanhPhanScore: result.groupScores[rubric.gatedGroupId] ?? 0, totalScore: result.totalScore,
        xepLoai: result.xepLoai, notes,
      });
      setSaved(true);
      loadCourseAttempts();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không lưu được điểm chấm.");
    } finally {
      setBusy(false);
    }
  }

  function studentName(id: string) { return students.find((item) => item.id === id)?.name ?? "Học sinh"; }
  const allLevelsChosen = rubric.groups.every((group) => group.criteria.every((criterion) => levels[criterion.id]));

  return <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 sm:p-6">
    <div>
      <p className="text-xs font-bold uppercase tracking-[.16em] text-violet-300">Rubric thi thực hành tổng hợp</p>
      <h3 className="mt-1 font-display text-2xl font-bold text-white">Lập trình → Mô phỏng → Cài đặt → Gia công</h3>
      <p className="mt-1 text-sm text-slate-500">Chấm chính thức theo rubric E/G/P/F. Học sinh có thể đã tự đánh giá trước — điểm dưới đây do giảng viên chấm mới là điểm chính thức, ghi vào Bài 6/7.</p>
    </div>

    <div className="mt-4 flex gap-2">{machines.map((item) => <button key={item.id} onClick={() => chooseMachine(item.id)} className={`rounded-xl border px-4 py-2 text-sm font-bold ${machine === item.id ? "border-blue-400/40 bg-blue-500/10 text-blue-200" : "border-white/10 text-slate-400"}`}>{item.label}</button>)}</div>

    <label className="mt-4 flex flex-col gap-1.5 text-sm text-slate-300">
      <span className="flex items-center gap-1.5 font-bold"><UserRound size={16} /> Chọn học sinh</span>
      <select value={studentId} onChange={(event) => chooseStudent(event.target.value)} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white">
        <option value="">— Chọn học sinh —</option>
        {students.map((item) => <option key={item.id} value={item.id}>{item.name} · {item.className}</option>)}
      </select>
    </label>

    {loading && <p className="mt-4 text-sm text-slate-500">Đang tải bài thi…</p>}

    {!loading && studentId && <div className="mt-5">
      <RubricExamForm
        rubric={rubric}
        levels={levels}
        onLevelChange={(criterionId, level) => { setLevels((current) => ({ ...current, [criterionId]: level })); setSaved(false); }}
        zeroToleranceConfirmed={zeroTolerance}
        onZeroToleranceChange={(index, confirmed) => { setZeroTolerance((current) => ({ ...current, [index]: confirmed })); setSaved(false); }}
        notes={notes}
        onNotesChange={(value) => { setNotes(value); setSaved(false); }}
        referenceLevels={selfAttempt?.item_levels}
        referenceLabel="SV tự chọn"
        criterionNotes={checklistNote ? { "cai-dat": checklistNote } : undefined}
      />
      {error && <p className="cnc-checklist-error">{error}</p>}
      <button type="button" disabled={busy || !allLevelsChosen} onClick={submit} className="cnc-submit">
        <Send size={16} /> {busy ? "Đang lưu…" : `Lưu điểm chính thức cho ${studentName(studentId)}`}
      </button>
      {saved && <div className="cnc-result passed">Đã lưu điểm chính thức và cập nhật vào Bài 6/7.</div>}
    </div>}

    <div className="mt-6">
      <div className="mb-3 flex items-center gap-2 text-sm font-bold text-white"><ClipboardList size={16} />Đã chấm chính thức ({courseAttempts.filter((row) => row.role === "teacher").length})</div>
      <div className="overflow-x-auto"><table className="w-full min-w-[520px] text-left text-sm"><thead><tr className="border-b border-white/10 text-xs uppercase text-slate-500"><th className="p-3">Học sinh</th><th className="p-3">Vai trò</th><th className="p-3">Điểm</th><th className="p-3">Xếp loại</th></tr></thead><tbody>
        {courseAttempts.map((item) => <tr key={item.id} className="border-b border-white/5">
          <td className="p-3"><strong className="text-white">{studentName(item.student_id)}</strong></td>
          <td className="p-3"><span className={`rounded-full px-2 py-0.5 text-[10px] font-bold ${item.role === "teacher" ? "bg-blue-500/10 text-blue-300" : "bg-violet-500/10 text-violet-300"}`}>{item.role === "teacher" ? "Chính thức" : "SV tự đánh giá"}</span></td>
          <td className="p-3 font-mono text-slate-300">{item.total_score.toFixed(2)}/10</td>
          <td className={`p-3 font-bold ${item.xep_loai.startsWith("Không đạt") ? "text-red-300" : "text-emerald-300"}`}>{item.xep_loai}</td>
        </tr>)}
        {!courseAttempts.length && <tr><td colSpan={4} className="p-8 text-center text-slate-500">Chưa có bài thi nào cho ca máy này.</td></tr>}
      </tbody></table></div>
    </div>
  </section>;
}
