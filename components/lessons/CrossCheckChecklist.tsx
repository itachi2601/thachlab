"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertTriangle, Check, ClipboardCheck, Clock3, RefreshCw, UserRound } from "lucide-react";
import {
  cncChecklistConfig,
  type PracticalChecklistLessonId,
} from "@/components/lessons/CncCourseWorkspace";
import {
  fetchChecklistSessions,
  fetchCourseClassmates,
  submitChecklistResult,
  startChecklistAttempt,
  type ChecklistSession,
  type Classmate,
} from "@/services/cnc-checklist";

export default function CrossCheckChecklist({ machine, lessonId, courseId }: { machine: "tiện" | "phay"; lessonId: PracticalChecklistLessonId; courseId?: number }) {
  const [sessions, setSessions] = useState<ChecklistSession[] | null>(null);
  const [classmates, setClassmates] = useState<Classmate[] | null>(null);
  const [loadError, setLoadError] = useState("");
  const [targetId, setTargetId] = useState("");
  const [checked, setChecked] = useState<Record<string, boolean>>({});
  const [zeroToleranceClear, setZeroToleranceClear] = useState<Record<number, boolean>>({});
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<{ passed: boolean; score: number; studentName: string } | null>(null);
  const [startedAt,setStartedAt]=useState("");
  const [now,setNow]=useState(Date.now());

  const config = cncChecklistConfig[lessonId];
  const sections = config.sections;
  const zeroTolerance = config.zeroTolerance;
  const items = sections.flatMap((section) => section.items);
  const score = items.reduce((total, item) => total + (checked[item.id] ? item.score : 0), 0);
  const criticalOk = items.filter((item) => item.critical).every((item) => checked[item.id]);
  const zeroToleranceOk = zeroTolerance.every((_, index) => zeroToleranceClear[index]);
  const passed = score >= 8 && criticalOk && zeroToleranceOk;

  const load = useCallback(() => {
    if (!courseId) { setSessions([]); setClassmates([]); return; }
    setLoadError("");
    fetchChecklistSessions(courseId, lessonId)
      .then((rows) => setSessions(rows.filter((row) => row.status === "open")))
      .catch((cause) => { setSessions([]); setLoadError(cause instanceof Error ? cause.message : "Không tải được phiên chấm."); });
    fetchCourseClassmates(courseId)
      .then(setClassmates)
      .catch((cause) => { setClassmates([]); setLoadError(cause instanceof Error ? cause.message : "Không tải được danh sách bạn học."); });
  }, [courseId, lessonId]);
  useEffect(() => { load(); }, [load]);
  useEffect(()=>{const timer=window.setInterval(()=>setNow(Date.now()),1000);return()=>window.clearInterval(timer)},[]);

  const openSession = sessions?.[0] ?? null;
  const target = (classmates ?? []).find((item) => item.student_id === targetId) ?? null;
  const remaining=startedAt?Math.max(0,240-Math.floor((now-Date.parse(startedAt))/1000)):240;

  async function chooseTarget(studentId:string){setTargetId(studentId);setResult(null);setStartedAt("");setError("");if(!studentId||!courseId||!openSession)return;try{const start=await startChecklistAttempt({courseId,code:openSession.code,studentId,lessonId});setStartedAt(start.started_at);setNow(Date.now())}catch(cause){setError(cause instanceof Error?cause.message:"Không thể bắt đầu lượt checklist.")}}

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

  if (sessions === null || classmates === null) return <div className="cnc-checklist-locked"><ClipboardCheck size={19} /><div><strong>Đang tải phiên chấm…</strong></div></div>;

  if (!openSession) {
    return <div className="cnc-checklist-locked">
      <ClipboardCheck size={19} />
      <div>
        <strong>Chưa có phiên chấm chéo nào đang mở</strong>
        <p>Hỏi giáo viên mở "Phiên chấm thực hành" cho ca máy {machine} hiện tại, sau đó bấm làm mới.</p>
        {loadError && <p className="cnc-checklist-error">{loadError}</p>}
      </div>
      <button type="button" onClick={load} className="cnc-checklist-refresh"><RefreshCw size={15} /> Làm mới</button>
    </div>;
  }

  return <div className="cnc-cross-check">
    <div className="cnc-checklist-rules">
      <span><ClipboardCheck size={17} /><b>Phiên đang mở: {openSession.title}</b></span>
      <span><AlertTriangle size={17} /><b>Ngưỡng đạt: 8/10 điểm</b></span>
      <p>Chỉ có hiệu lực trong khung 06:30–11:00. Mỗi lượt phải kéo dài tối thiểu 4 phút trước khi nộp.</p>
    </div>

    {loadError && <p className="cnc-checklist-error">{loadError}</p>}

    {classmates.length === 0 ? (
      <div className="cnc-checklist-locked">
        <UserRound size={19} />
        <div>
          <strong>Không có bạn học nào để chọn</strong>
          <p>Không tìm thấy bạn học nào khác đang hoạt động (trạng thái “active”) trong khóa học này. Kiểm tra lại danh sách ghi danh của khóa học hoặc bấm làm mới.</p>
        </div>
        <button type="button" onClick={load} className="cnc-checklist-refresh"><RefreshCw size={15} /> Làm mới</button>
      </div>
    ) : <>
      <label className="cnc-cross-check-picker">
        <span><UserRound size={16} /> Đang chấm cho</span>
        <select value={targetId} onChange={(event) => void chooseTarget(event.target.value)}>
          <option value="">— Chọn bạn học —</option>
          {classmates.map((item) => <option key={item.student_id} value={item.student_id}>{item.full_name} · {item.class_name}</option>)}
        </select>
      </label>

      {!target && <p className="cnc-checklist-hint">Chọn 1 bạn học ở trên để bắt đầu chấm.</p>}
    </>}

    {target && <>
      <div className="cnc-checklist-rules"><span><Clock3 size={17}/><b>{remaining>0?`Có thể nộp sau ${Math.floor(remaining/60)}:${String(remaining%60).padStart(2,"0")}`:"Đã đủ thời gian tối thiểu 4 phút"}</b></span><p>Thời gian được tính từ máy chủ khi bắt đầu chấm cho {target.full_name}.</p></div>
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
      <button type="button" disabled={busy||remaining>0||!startedAt} onClick={submit} className="cnc-submit">{busy ? "Đang nộp…" : remaining>0?`Chờ đủ 4 phút (${Math.floor(remaining/60)}:${String(remaining%60).padStart(2,"0")})`:`Nộp kết quả chấm cho ${target.full_name}`}</button>
    </>}

    {result && <div className={`cnc-checklist-congratulations ${result.passed ? "" : "cnc-checklist-warn"}`}>
      <Check size={25} />
      <p>Đã nộp kết quả cho {result.studentName}: {result.score.toFixed(1)}/10 — {result.passed ? "Đạt" : "Chưa đạt"}.</p>
    </div>}
  </div>;
}
