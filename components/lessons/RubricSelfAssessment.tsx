"use client";

import { useCallback, useEffect, useState } from "react";
import { Award, ClipboardList, Send } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import RubricExamForm from "@/components/lessons/RubricExamForm";
import { RUBRIC_BY_MACHINE, gradeRubricExam, type RubricLevel } from "@/services/cnc-rubric";
import {
  fetchMyRubricExamAttempts,
  submitSelfRubricAssessment,
  type RubricExamAttempt,
} from "@/services/cnc-rubric-exam";
import { fetchCncLearningRecords } from "@/services/cnc-learning-records";

export default function RubricSelfAssessment({ machine, courseId }: { machine: "tien" | "phay"; courseId?: number }) {
  const { session } = useAuth();
  const rubric = RUBRIC_BY_MACHINE[machine];
  const [attempts, setAttempts] = useState<RubricExamAttempt[] | null>(null);
  const [levels, setLevels] = useState<Record<string, RubricLevel | undefined>>({});
  const [zeroTolerance, setZeroTolerance] = useState<Record<number, boolean>>({});
  const [notes, setNotes] = useState("");
  const [checklistNote, setChecklistNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  const load = useCallback(() => {
    if (!courseId) { setAttempts([]); return; }
    fetchMyRubricExamAttempts(courseId, machine)
      .then((rows) => {
        setAttempts(rows);
        const self = rows.find((row) => row.role === "self");
        if (self) {
          setLevels(self.item_levels);
          setZeroTolerance(self.zero_tolerance_confirmed);
          setNotes(self.notes);
        }
      })
      .catch((cause) => { setAttempts([]); setError(cause instanceof Error ? cause.message : "Không tải được phiếu tự đánh giá."); });
    if (session?.user.id) {
      const lessonId = machine === "tien" ? "lesson-5" : "lesson-6";
      fetchCncLearningRecords(courseId, session?.user.id)
        .then((rows) => {
          const record = rows.find((row) => row.lesson_id === lessonId && row.assessment_id === "checklist");
          setChecklistNote(record ? `Điểm checklist chấm chéo gia công: ${record.best_score ?? 0}/10` : "Chưa có điểm checklist chấm chéo gia công.");
        })
        .catch(() => setChecklistNote(""));
    }
  }, [courseId, machine, session?.user.id]);
  useEffect(() => { load(); }, [load]);

  async function submit() {
    if (!courseId || !session?.user.id) return;
    setBusy(true);
    setError("");
    setSaved(false);
    try {
      const result = gradeRubricExam(rubric, levels, zeroTolerance);
      await submitSelfRubricAssessment({
        courseId, studentId: session.user.id, machine, itemLevels: levels as Record<string, RubricLevel>,
        zeroToleranceConfirmed: zeroTolerance, kyThuatScore: result.groupScores[rubric.gateGroupId] ?? 0,
        thanhPhanScore: result.groupScores[rubric.gatedGroupId] ?? 0, totalScore: result.totalScore,
        xepLoai: result.xepLoai, notes,
      });
      setSaved(true);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không lưu được phiếu tự đánh giá.");
    } finally {
      setBusy(false);
    }
  }

  if (attempts === null) return <div className="cnc-checklist-locked"><ClipboardList size={19} /><div><strong>Đang tải phiếu tự đánh giá…</strong></div></div>;

  const teacherAttempt = attempts.find((row) => row.role === "teacher") ?? null;
  const allLevelsChosen = rubric.groups.every((group) => group.criteria.every((criterion) => levels[criterion.id]));

  return <div className="cnc-rubric-self">
    <p className="cnc-checklist-hint">
      Tự đánh giá bài thi thực hành tổng hợp (lập trình → mô phỏng → cài đặt dao/phôi → gia công) theo đúng tiêu chí giảng viên sẽ dùng để chấm chính thức. Đây là phần tự phản hồi — điểm chính thức do giảng viên chấm lại.
    </p>

    {teacherAttempt && <div className={`cnc-checklist-congratulations ${teacherAttempt.xep_loai.startsWith("Không đạt") ? "cnc-checklist-warn" : ""}`}>
      <Award size={22} />
      <p>Điểm chính thức từ giảng viên: <b>{teacherAttempt.total_score.toFixed(2)}/10</b> — {teacherAttempt.xep_loai}{teacherAttempt.notes ? ` · "${teacherAttempt.notes}"` : ""}</p>
    </div>}

    <RubricExamForm
      rubric={rubric}
      levels={levels}
      onLevelChange={(criterionId, level) => { setLevels((current) => ({ ...current, [criterionId]: level })); setSaved(false); }}
      zeroToleranceConfirmed={zeroTolerance}
      onZeroToleranceChange={(index, confirmed) => { setZeroTolerance((current) => ({ ...current, [index]: confirmed })); setSaved(false); }}
      notes={notes}
      onNotesChange={(value) => { setNotes(value); setSaved(false); }}
      criterionNotes={checklistNote ? { "cai-dat": checklistNote } : undefined}
    />

    {error && <p className="cnc-checklist-error">{error}</p>}
    <button type="button" className="cnc-submit" disabled={!courseId || busy || !allLevelsChosen} onClick={submit}>
      <Send size={16} /> {busy ? "Đang lưu…" : "Lưu phiếu tự đánh giá"}
    </button>
    {saved && <div className="cnc-result passed">Đã lưu phiếu tự đánh giá.</div>}
  </div>;
}
