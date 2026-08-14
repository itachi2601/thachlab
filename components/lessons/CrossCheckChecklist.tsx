"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertTriangle, Check, ClipboardCheck, RefreshCw, UserRound } from "lucide-react";
import {
  turningChecklistSections,
  millingChecklistSections,
  turningZeroTolerance,
  millingZeroTolerance,
} from "@/components/lessons/CncCourseWorkspace";
import {
  fetchChecklistSessions,
  fetchCourseClassmates,
  submitChecklistResult,
  type ChecklistSession,
  type Classmate,
} from "@/services/cnc-checklist";

export default function CrossCheckChecklist({ machine, lessonId, courseId }: { machine: "tiện" | "phay"; lessonId: "lesson-4-turn" | "lesson-4-mill"; courseId?: number }) {
  const [sessions, setSessions] = useState<ChecklistSession[] | null>(null);
  const [classmates, setClassmates] = useState<Classmate[]>([]);
  const [targetId, setTargetId] = useState("");
  const [checked, setChecked] = useState<Record<string, boolean>>({});
  const [zeroToleranceClear, setZeroToleranceClear] = useState<Record<number, boolean>>({});
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<{ passed: boolean; score: number; studentName: string } | null>(null);

  const sections = machine === "tiện" ? turningChecklistSections : millingChecklistSections;
  const zeroTolerance = machine === "tiện" ? turningZeroTolerance : millingZeroTolerance;
  const items = sections.flatMap((section) => section.items);
  const score = items.reduce((total, item) => total + (checked[item.id] ? item.score : 0), 0);
  const criticalOk = items.filter((item) => item.critical).every((item) => checked[item.id]);
  const zeroToleranceOk = zeroTolerance.every((_, index) => zeroToleranceClear[index]);
  const passed = score >= 8 && criticalOk && zeroToleranceOk;

  const load = useCallback(() => {
    if (!courseId) { setSessions([]); return; }
    fetchChecklistSessions(courseId, lessonId).then((rows) => setSessions(rows.filter((row) => row.status === "open"))).catch(() => setSessions([]));
    fetchCourseClassmates(courseId).then(setClassmates).catch(() => setClassmates([]));
  }, [courseId, lessonId]);
  useEffect(() => { load(); }, [load]);

  const openSession = sessions?.[0] ?? null;
  const target = classmates.find((item) => item.student_id === targetId) ?? null;

  async function submit() {
    if (!courseId || !openSession || !target) return;
    setBusy(true);
    setError("");
    try {
      const outcome = await submitChecklistResult({
        courseId, code: openSession.code, studentId: target.student_id, lessonId,
        itemResults: checked, score, criticalOk, zeroToleranceOk, passed,
      });
      setResult({ passed: outcome.passed, score: outcome.score, studentName: target.full_name });
      setChecked({});
      setZeroToleranceClear({});
      setTargetId("");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không nộp được kết quả chấm.");
    } finally {
      setBusy(false);
    }
  }

  if (sessions === null) return <div className="cnc-checklist-locked"><ClipboardCheck size={19} /><div><strong>Đang tải phiên chấm…</strong></div></div>;

  if (!openSession) {
    return <div className="cnc-checklist-locked">
      <ClipboardCheck size={19} />
      <div>
        <strong>Chưa có phiên chấm chéo nào đang mở</strong>
        <p>Hỏi giáo viên mở "Phiên chấm thực hành" cho ca máy {machine} hiện tại, sau đó bấm làm mới.</p>
      </div>
      <button type="button" onClick={load} className="cnc-checklist-refresh"><RefreshCw size={15} /> Làm mới</button>
    </div>;
  }

  return <div className="cnc-cross-check">
    <div className="cnc-checklist-rules">
      <span><ClipboardCheck size={17} /><b>Phiên đang mở: {openSession.title}</b></span>
      <span><AlertTriangle size={17} /><b>Ngưỡng đạt: 8/10 điểm</b></span>
      <p>Chọn bạn học bạn đang quan sát và chấm chéo, đánh dấu đúng các bước bạn ấy đã thực hiện chính xác.</p>
    </div>

    <label className="cnc-cross-check-picker">
      <span><UserRound size={16} /> Đang chấm cho</span>
      <select value={targetId} onChange={(event) => { setTargetId(event.target.value); setResult(null); }}>
        <option value="">— Chọn bạn học —</option>
        {classmates.map((item) => <option key={item.student_id} value={item.student_id}>{item.full_name} · {item.class_name}</option>)}
      </select>
    </label>

    {!target && <p className="cnc-checklist-hint">Chọn 1 bạn học ở trên để bắt đầu chấm.</p>}

    {target && <>
      <div className="cnc-operation-checklist">
        {sections.map((section) => <section key={section.id}>
          <header><h4>{section.title}</h4><b>{section.maxScore.toFixed(1)} điểm</b></header>
          {section.items.map((item) => <label key={item.id} className={`${checked[item.id] ? "checked" : ""} ${item.critical ? "critical" : ""}`}>
            <input type="checkbox" checked={Boolean(checked[item.id])} onChange={(event) => setChecked((current) => ({ ...current, [item.id]: event.target.checked }))} />
            <i><Check size={14} /></i>
            <span><strong>{item.critical && <AlertTriangle size={14} />} {item.id}. {item.label}</strong><small>{item.note}</small></span>
            <b>+{item.score.toFixed(1)}</b>
          </label>)}
        </section>)}
      </div>
      <section className="cnc-zero-tolerance">
        <header><AlertTriangle size={20} /><div><strong>Lỗi loại trực tiếp (Zero-tolerance)</strong><p>Xác nhận bạn học không vi phạm đầy đủ {zeroTolerance.length} điều kiện dưới đây.</p></div></header>
        {zeroTolerance.map((item, index) => <label key={item}>
          <input type="checkbox" checked={Boolean(zeroToleranceClear[index])} onChange={(event) => setZeroToleranceClear((current) => ({ ...current, [index]: event.target.checked }))} />
          <i><Check size={13} /></i><span><b>{index + 1}</b>{item}</span>
        </label>)}
      </section>
      <div className={`cnc-checklist-score ${passed ? "passed" : ""}`}>
        <div><small>TỔNG ĐIỂM THỰC HÀNH</small><strong>{score.toFixed(1)}<span>/10.0</span></strong></div>
        <div className="cnc-checklist-status"><b>{passed ? "ĐẠT" : "CHƯA ĐẠT"}</b></div>
      </div>
      {error && <p className="cnc-checklist-error">{error}</p>}
      <button type="button" disabled={busy} onClick={submit} className="cnc-submit">{busy ? "Đang nộp…" : `Nộp kết quả chấm cho ${target.full_name}`}</button>
    </>}

    {result && <div className={`cnc-checklist-congratulations ${result.passed ? "" : "cnc-checklist-warn"}`}>
      <Check size={25} />
      <p>Đã nộp kết quả cho {result.studentName}: {result.score.toFixed(1)}/10 — {result.passed ? "Đạt" : "Chưa đạt"}.</p>
    </div>}
  </div>;
}
