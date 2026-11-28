"use client";

// Màn chấm thi thực hành tổng hợp CNC (Tiện/Phay) của giảng viên — thiết kế cho điện thoại cầm tay
// đứng cạnh máy (28/11/2026). Chuẩn chung với bảng điểm SV: mọi phép tính, tên tiêu chí, chữ xếp loại
// lấy từ services/cnc-rubric.ts (gradeRubricExam, buildCncGradeRow). Luồng:
//   1. Danh sách SV (tìm tên, lọc Chưa chấm / Chưa gửi) → chạm một SV.
//   2. Mỗi tiêu chí 4 nút E/G/P/F to (một chạm), mô tả mức hiện dưới; lỗi loại trực tiếp là nút "Vi phạm"
//      (mặc định không vi phạm). Thanh dưới cùng luôn thấy tổng điểm + xếp loại + "Lưu & SV tiếp".
//   3. Nháp tự lưu trên máy theo từng SV (mất mạng giữa giờ thi không mất điểm đã bấm).
//   4. "Gửi điểm cho SV": ghi cnc_grades (trang /lop-hoc/cnc/bang-diem/) + chuông thông báo từng SV riêng.

import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, ChevronLeft, ChevronRight, Search, Send } from "lucide-react";
import {
  RUBRIC_BY_MACHINE,
  RUBRIC_LEVELS,
  RUBRIC_LEVEL_LABEL,
  RUBRIC_LEVEL_PCT,
  buildCncGradeRow,
  cncGradeNotificationBody,
  confirmedToViolations,
  gradeRubricExam,
  isRubricComplete,
  parseCncGradeDetail,
  rubricGradeShort,
  rubricMaxScore,
  violationsToConfirmed,
  type RubricLevel,
} from "@/services/cnc-rubric";
import {
  fetchRubricExamAttemptsByCourse,
  submitTeacherRubricGrade,
  type RubricExamAttempt,
  type RubricExamMachine,
} from "@/services/cnc-rubric-exam";
import { fetchCourseCncGrades, publishCncGrade, type CourseCncGrade } from "@/services/cnc-grades";
import type { CncLearningRecord } from "@/services/cnc-learning-records";

type Student = { id: string; name: string; className: string; records?: CncLearningRecord[] };
type Levels = Record<string, RubricLevel | undefined>;
type Draft = { levels: Levels; violated: Record<number, boolean>; notes: string; ts: number };
type Filter = "all" | "todo" | "unsent";

const MACHINES: { id: RubricExamMachine; label: string }[] = [
  { id: "tien", label: "Tiện CNC" },
  { id: "phay", label: "Phay CNC" },
];

// Nút đã chọn tô đặc + chữ trắng (đặt bằng style vì nền sáng đổi .text-white thành mực tối):
// nhìn lướt cả cột cũng thấy mức nào đã chấm, kể cả dưới nắng xưởng.
const LEVEL_SOLID: Record<RubricLevel, string> = { E: "#059669", G: "#2563eb", P: "#d97706", F: "#dc2626" };
const SOLID_ON = (color: string) => ({ background: color, borderColor: color, color: "#fff" });

const fmt = (x: number) => (Math.round(x * 100) / 100).toString().replace(".", ",");
const draftKey = (courseId: number, machine: string, studentId: string) => `cnc-cham:${courseId}:${machine}:${studentId}`;

// Lỗi Supabase (PostgrestError) là object thường, không phải Error — vẫn lấy được .message.
const errText = (cause: unknown, fallback: string) =>
  cause instanceof Error ? cause.message : (cause as { message?: string } | null)?.message || fallback;

function readDraft(key: string): Draft | null {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as Draft) : null;
  } catch {
    return null;
  }
}

export default function TeacherRubricExamPanel({ courseId, students }: { courseId: number; students: Student[] }) {
  const [machine, setMachine] = useState<RubricExamMachine>("tien");
  const [attempts, setAttempts] = useState<RubricExamAttempt[]>([]);
  const [grades, setGrades] = useState<CourseCncGrade[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState<Filter>("all");
  const [activeId, setActiveId] = useState<string | null>(null);
  const [levels, setLevels] = useState<Levels>({});
  const [violated, setViolated] = useState<Record<number, boolean>>({});
  const [notes, setNotes] = useState("");
  const [dirty, setDirty] = useState(false);
  const [openDesc, setOpenDesc] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);

  const rubric = RUBRIC_BY_MACHINE[machine];
  const criteria = useMemo(() => rubric.groups.flatMap((g) => g.criteria), [rubric]);

  const [reloadKey, setReloadKey] = useState(0);
  useEffect(() => {
    let alive = true;
    Promise.all([
      fetchRubricExamAttemptsByCourse(courseId, machine).catch(() => [] as RubricExamAttempt[]),
      fetchCourseCncGrades(courseId, machine).catch(() => [] as CourseCncGrade[]),
    ]).then(([a, g]) => {
      if (!alive) return;
      setAttempts(a);
      setGrades(g);
      setLoaded(true);
    });
    return () => { alive = false; };
  }, [courseId, machine, reloadKey]);

  const byStudent = useMemo(() => {
    const map = new Map<string, { teacher?: RubricExamAttempt; self?: RubricExamAttempt; grade?: CourseCncGrade }>();
    for (const s of students) map.set(s.id, {});
    for (const a of attempts) {
      const e = map.get(a.student_id);
      if (e) e[a.role === "teacher" ? "teacher" : "self"] = a;
    }
    for (const g of grades) {
      const e = map.get(g.student_id);
      if (e) e.grade = g;
    }
    return map;
  }, [students, attempts, grades]);

  function statusOf(id: string) {
    const e = byStudent.get(id) ?? {};
    const unsent = Boolean(e.teacher && (!e.grade || new Date(e.grade.updated_at) < new Date(e.teacher.updated_at)));
    const total = e.teacher?.total_score ?? e.grade?.total;
    const grade = e.teacher
      ? rubricGradeShort(gradeRubricExam(rubric, e.teacher.item_levels, e.teacher.zero_tolerance_confirmed), true)
      : e.grade?.grade ?? null;
    return { scored: Boolean(e.teacher || e.grade), unsent, total, grade };
  }

  const sorted = useMemo(() => [...students].sort((a, b) => a.name.localeCompare(b.name, "vi")), [students]);
  const visible = sorted.filter((s) => {
    if (query && !s.name.toLowerCase().includes(query.trim().toLowerCase())) return false;
    const st = statusOf(s.id);
    if (filter === "todo") return !st.scored;
    if (filter === "unsent") return st.unsent;
    return true;
  });
  const scoredCount = sorted.filter((s) => statusOf(s.id).scored).length;
  const unsentIds = sorted.filter((s) => statusOf(s.id).unsent).map((s) => s.id);

  function openStudent(id: string) {
    const e = byStudent.get(id) ?? {};
    const draft = readDraft(draftKey(courseId, machine, id));
    const teacherTs = e.teacher ? new Date(e.teacher.updated_at).getTime() : 0;
    if (draft && draft.ts > teacherTs) {
      setLevels(draft.levels);
      setViolated(draft.violated);
      setNotes(draft.notes);
      setDirty(true);
    } else if (e.teacher) {
      setLevels(e.teacher.item_levels);
      setViolated(confirmedToViolations(rubric, e.teacher.zero_tolerance_confirmed));
      setNotes(e.teacher.notes ?? "");
      setDirty(false);
    } else if (e.grade) {
      // Điểm đã nạp từ file chấm offline: mở ra để xem/sửa, lưu lại thành bản chấm chính thức trên web.
      const parsed = parseCncGradeDetail(rubric, e.grade.detail);
      setLevels(parsed.levels);
      setViolated(parsed.violated);
      setNotes("");
      setDirty(false);
    } else {
      setLevels({});
      setViolated({});
      setNotes("");
      setDirty(false);
    }
    setOpenDesc(null);
    setMsg(null);
    setActiveId(id);
    window.scrollTo({ top: 0 });
  }

  // Nháp theo từng SV, ghi ngay khi bấm.
  useEffect(() => {
    if (!activeId || !dirty) return;
    try {
      localStorage.setItem(draftKey(courseId, machine, activeId), JSON.stringify({ levels, violated, notes, ts: Date.now() }));
    } catch { /* trình duyệt chặn lưu: vẫn chấm được, chỉ mất nháp */ }
  }, [activeId, dirty, levels, violated, notes, courseId, machine]);

  function chooseMachine(next: RubricExamMachine) {
    if (next === machine) return;
    setLoaded(false);
    setMachine(next);
    setActiveId(null);
    setMsg(null);
  }

  const result = gradeRubricExam(rubric, levels, violationsToConfirmed(rubric, violated));
  const complete = isRubricComplete(rubric, levels);
  const missing = criteria.filter((c) => !levels[c.id]).length;
  const gradeLabel = rubricGradeShort(result, complete);
  const bad = result.zeroToleranceFailed || (complete && result.totalScore < 5);

  const activeIndex = activeId ? visible.findIndex((s) => s.id === activeId) : -1;
  const activeStudent = students.find((s) => s.id === activeId);
  const selfLevels = activeId ? byStudent.get(activeId)?.self?.item_levels : undefined;
  const checklistNote = useMemo(() => {
    const rec = activeStudent?.records?.find((r) => r.lesson_id === (machine === "tien" ? "lesson-5" : "lesson-6") && r.assessment_id === "checklist");
    return rec ? `Checklist chấm chéo: ${rec.best_score ?? 0}/10` : "";
  }, [activeStudent, machine]);

  async function save(goNext: boolean) {
    if (!activeId || !complete) return;
    setBusy(true);
    setMsg(null);
    try {
      const saved = await submitTeacherRubricGrade({
        courseId, studentId: activeId, machine,
        itemLevels: levels as Record<string, RubricLevel>,
        zeroToleranceConfirmed: violationsToConfirmed(rubric, violated),
        kyThuatScore: result.groupScores[rubric.gateGroupId] ?? 0,
        thanhPhanScore: result.groupScores[rubric.gatedGroupId] ?? 0,
        totalScore: result.totalScore,
        xepLoai: result.xepLoai,
        notes,
      });
      try { localStorage.removeItem(draftKey(courseId, machine, activeId)); } catch { /* bỏ qua */ }
      setAttempts((cur) => [...cur.filter((a) => !(a.student_id === activeId && a.role === "teacher")), saved]);
      setDirty(false);
      const next = goNext ? visible.slice(activeIndex + 1).find((s) => !statusOf(s.id).scored) ?? visible[activeIndex + 1] : undefined;
      if (next) openStudent(next.id);
      else if (goNext) {
        setActiveId(null);
        setMsg({ ok: true, text: "Đã lưu. Bấm \"Gửi điểm cho SV\" khi chấm xong cả ca." });
      } else setMsg({ ok: true, text: "Đã lưu (chưa gửi SV)." });
    } catch (cause) {
      setMsg({ ok: false, text: `${errText(cause, "Không lưu được")} — điểm vẫn giữ nháp trên máy này, thử lại.` });
    } finally {
      setBusy(false);
    }
  }

  async function sendAll() {
    if (!unsentIds.length) return;
    if (!window.confirm(`Gửi điểm ${rubric.machine === "tien" ? "Tiện" : "Phay"} cho ${unsentIds.length} SV? Mỗi SV chỉ thấy điểm của mình (trang Bảng điểm + chuông thông báo).`)) return;
    setBusy(true);
    setMsg(null);
    let done = 0;
    const failed: string[] = [];
    for (const id of unsentIds) {
      const e = byStudent.get(id);
      if (!e?.teacher) continue;
      const row = buildCncGradeRow(rubric, e.teacher.item_levels, confirmedToViolations(rubric, e.teacher.zero_tolerance_confirmed));
      try {
        await publishCncGrade({ courseId, studentId: id, module: machine, row, body: cncGradeNotificationBody(rubric, row), isUpdate: Boolean(e.grade) });
        done++;
      } catch (cause) {
        failed.push(`${students.find((s) => s.id === id)?.name ?? id}: ${errText(cause, "lỗi")}`);
      }
      setMsg({ ok: true, text: `Đang gửi… ${done}/${unsentIds.length}` });
    }
    setReloadKey((k) => k + 1);
    setBusy(false);
    setMsg(failed.length
      ? { ok: false, text: `Đã gửi ${done} SV. Lỗi ${failed.length}: ${failed.join(" · ")}` }
      : { ok: true, text: `Đã gửi điểm cho ${done} SV.` });
  }

  // ----------------------------------------------------------------- MÀN CHẤM MỘT SV
  if (activeId && activeStudent) {
    return <section className="-mx-4 sm:mx-0 rounded-none sm:rounded-2xl border-y sm:border border-white/10 bg-panel pb-28">
      <header className="sticky top-0 z-20 flex items-center gap-1 border-b border-white/10 bg-panel-deep/95 px-2 py-2 backdrop-blur">
        <button type="button" onClick={() => setActiveId(null)} className="flex min-h-11 items-center gap-1 rounded-xl px-2 text-sm font-bold text-slate-300" aria-label="Về danh sách">
          <ChevronLeft size={20} />DS
        </button>
        <div className="min-w-0 flex-1 text-center">
          <p className="truncate text-base font-bold text-white">{activeStudent.name}</p>
          <p className="text-xs text-slate-500">{rubric.machine === "tien" ? "Tiện" : "Phay"} · {activeIndex + 1}/{visible.length}{dirty ? " · nháp trên máy" : ""}</p>
        </div>
        <button type="button" disabled={activeIndex <= 0} onClick={() => openStudent(visible[activeIndex - 1].id)} className="flex h-11 w-11 items-center justify-center rounded-xl text-slate-300 disabled:opacity-30" aria-label="SV trước"><ChevronLeft size={22} /></button>
        <button type="button" disabled={activeIndex < 0 || activeIndex >= visible.length - 1} onClick={() => openStudent(visible[activeIndex + 1].id)} className="flex h-11 w-11 items-center justify-center rounded-xl text-slate-300 disabled:opacity-30" aria-label="SV sau"><ChevronRight size={22} /></button>
      </header>

      <div className="space-y-5 px-3 pt-4 sm:px-5">
        {rubric.groups.map((group) => {
          const gated = group.id === rubric.gatedGroupId;
          return <div key={group.id} className="space-y-3">
            <div className="flex items-baseline justify-between">
              <h4 className="text-sm font-bold uppercase tracking-wide text-slate-400">{group.title}</h4>
              <span className="font-mono text-sm text-slate-300">{fmt(result.groupScores[group.id] ?? 0)} / {fmt(rubricMaxScore(rubric, group.id))}</span>
            </div>
            {gated && complete && !result.gatePassed && <p className="flex items-start gap-1.5 rounded-xl bg-amber-500/10 px-3 py-2 text-sm text-amber-200">
              <AlertTriangle size={16} className="mt-0.5 shrink-0" />Kỹ thuật dưới {fmt(rubric.gateThreshold)} điểm nên nhóm này tính 0.
            </p>}
            {group.criteria.map((c) => {
              const lv = levels[c.id];
              const ref = selfLevels?.[c.id];
              return <div key={c.id} className="rounded-2xl border border-white/10 bg-panel-deep p-3">
                <div className="mb-2 flex items-baseline justify-between gap-2">
                  <button type="button" onClick={() => setOpenDesc(openDesc === c.id ? null : c.id)} className="text-left text-[15px] font-bold text-white">
                    {c.short} <span className="text-xs font-normal text-slate-500">ⓘ</span>
                  </button>
                  <span className="shrink-0 text-xs text-slate-500">tối đa {fmt(c.maxScore)}</span>
                </div>
                <div className="grid grid-cols-4 gap-2" role="radiogroup" aria-label={c.short}>
                  {RUBRIC_LEVELS.map((level) => {
                    const on = lv === level;
                    return <button key={level} type="button" role="radio" aria-checked={on}
                      onClick={() => { setLevels((cur) => ({ ...cur, [c.id]: level })); setDirty(true); }}
                      style={on ? SOLID_ON(LEVEL_SOLID[level]) : undefined}
                      className={`relative flex min-h-14 flex-col items-center justify-center rounded-xl border text-center transition ${on ? "" : "border-white/10 text-slate-400"}`}>
                      <b className="text-xl leading-none">{level}</b>
                      <small className="mt-1 text-[11px] leading-none">{fmt(RUBRIC_LEVEL_PCT[level] * c.maxScore)}</small>
                      {ref === level && <span className="absolute right-1 top-1 rounded px-1 text-[9px] font-bold" style={{ background: "#7c3aed", color: "#fff" }}>SV</span>}
                    </button>;
                  })}
                </div>
                {(openDesc === c.id ? RUBRIC_LEVELS : lv ? [lv] : []).map((level) => <p key={level} className="mt-2 text-[13px] leading-snug text-slate-400">
                  <b className="text-slate-300">{level} · {RUBRIC_LEVEL_LABEL[level]}:</b> {c.descriptors[level]}
                </p>)}
                {c.id === "cai-dat" && checklistNote && <p className="mt-2 text-xs text-slate-500">{checklistNote}</p>}
              </div>;
            })}
          </div>;
        })}

        <div className="space-y-2">
          <h4 className="text-sm font-bold uppercase tracking-wide text-red-300">Lỗi loại trực tiếp — chạm nếu VI PHẠM</h4>
          {rubric.zeroToleranceShort.map((label, i) => {
            const on = Boolean(violated[i]);
            return <button key={label} type="button" aria-pressed={on} title={rubric.zeroTolerance[i]}
              onClick={() => { setViolated((cur) => ({ ...cur, [i]: !cur[i] })); setDirty(true); }}
              className={`flex min-h-12 w-full items-center gap-3 rounded-xl border px-3 text-left text-sm ${on ? "font-bold" : "border-white/10 text-slate-300"}`}
              style={on ? SOLID_ON("#dc2626") : undefined}>
              <span className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-md border ${on ? "border-white" : "border-white/20"}`}>{on ? "✕" : ""}</span>
              {label}
            </button>;
          })}
        </div>

        <label className="block">
          <span className="text-sm font-bold text-slate-300">Nhận xét (tuỳ chọn)</span>
          <textarea value={notes} rows={2} onChange={(e) => { setNotes(e.target.value); setDirty(true); }}
            className="mt-1 w-full rounded-xl border border-white/10 bg-panel-deep px-3 py-2 text-base text-white" placeholder="Ghi chú cho bài thi…" />
        </label>
        {msg && <p className={`rounded-xl px-3 py-2 text-sm ${msg.ok ? "bg-emerald-500/10 text-emerald-200" : "bg-red-500/10 text-red-200"}`}>{msg.text}</p>}
      </div>

      <div className="fixed inset-x-0 bottom-0 z-50 border-t border-white/10 bg-panel px-3 py-2 shadow-[0_-8px_24px_rgba(0,0,0,.18)]" style={{ paddingBottom: "max(0.5rem, env(safe-area-inset-bottom))" }}>
        <div className="mx-auto flex max-w-3xl items-center gap-3">
          <div className="min-w-0 flex-1">
            <p className="font-mono text-2xl font-bold leading-none text-white">{fmt(result.totalScore)}<span className="text-sm text-slate-500">/10</span></p>
            <p className={`truncate text-sm font-bold ${!complete ? "text-slate-500" : bad ? "text-red-300" : "text-emerald-300"}`}>{!complete ? `Còn ${missing} tiêu chí` : result.zeroToleranceFailed ? "Loại trực tiếp" : gradeLabel}</p>
          </div>
          <button type="button" disabled={busy || !complete} onClick={() => save(false)} className="min-h-12 rounded-xl border border-white/15 px-3 text-sm font-bold text-slate-200 disabled:opacity-40">Lưu</button>
          <button type="button" disabled={busy || !complete} onClick={() => save(true)} className="flex min-h-12 items-center gap-1 rounded-xl bg-blue-600 px-4 text-sm font-bold text-white disabled:opacity-40">
            {busy ? "Đang lưu…" : <>Lưu &amp; tiếp<ChevronRight size={18} /></>}
          </button>
        </div>
      </div>
    </section>;
  }

  // ----------------------------------------------------------------- DANH SÁCH SV
  return <section className="rounded-2xl border border-white/10 bg-panel p-4 sm:p-6">
    <p className="text-xs font-bold uppercase tracking-[.16em] text-violet-300">Chấm thi thực hành tổng hợp</p>
    <p className="mt-1 text-sm text-slate-500">Rubric E/G/P/F (100/75/50/0%). Kỹ thuật &lt; 3,5 thì Thành phần tính 0; vi phạm lỗi loại trực tiếp là Không đạt. Xếp loại: ≥8,5 Xuất sắc · ≥7 Khá · ≥5 Đạt.</p>

    <div className="mt-4 grid grid-cols-2 gap-2">{MACHINES.map((m) => <button key={m.id} type="button" onClick={() => chooseMachine(m.id)}
      className={`min-h-11 rounded-xl border text-sm font-bold ${machine === m.id ? "border-blue-400/40 bg-blue-500/10 text-blue-200" : "border-white/10 text-slate-400"}`}>{m.label}</button>)}</div>

    <div className="mt-4 flex flex-wrap items-center gap-3">
      <p className="flex-1 text-sm text-slate-300">Đã chấm <b className="text-white">{scoredCount}/{students.length}</b>{unsentIds.length ? <> · <b className="text-amber-200">{unsentIds.length} chưa gửi</b></> : null}</p>
      <button type="button" disabled={busy || !unsentIds.length} onClick={sendAll}
        style={{ background: "#059669", color: "#fff" }}
        className="flex min-h-11 items-center gap-2 rounded-xl px-4 text-sm font-bold disabled:opacity-40">
        <Send size={16} />Gửi điểm cho SV{unsentIds.length ? ` (${unsentIds.length})` : ""}
      </button>
    </div>
    {msg && <p className={`mt-3 rounded-xl px-3 py-2 text-sm ${msg.ok ? "bg-emerald-500/10 text-emerald-200" : "bg-red-500/10 text-red-200"}`}>{msg.text}</p>}

    <div className="mt-4 flex items-center gap-2 rounded-xl border border-white/10 bg-panel-deep px-3">
      <Search size={16} className="text-slate-500" />
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Tìm tên SV…" className="min-h-11 flex-1 bg-transparent text-base text-white outline-none" />
    </div>
    <div className="mt-2 flex gap-2">{([["all", "Tất cả"], ["todo", "Chưa chấm"], ["unsent", "Chưa gửi"]] as [Filter, string][]).map(([k, label]) =>
      <button key={k} type="button" onClick={() => setFilter(k)} className={`min-h-9 rounded-full border px-3 text-xs font-bold ${filter === k ? "border-blue-400/40 bg-blue-500/10 text-blue-200" : "border-white/10 text-slate-400"}`}>{label}</button>)}</div>

    <ul className="mt-3 divide-y divide-white/5">
      {!loaded && <li className="py-6 text-center text-sm text-slate-500">Đang tải…</li>}
      {loaded && !visible.length && <li className="py-6 text-center text-sm text-slate-500">Không có SV nào.</li>}
      {loaded && visible.map((s) => {
        const st = statusOf(s.id);
        const hasDraft = typeof window !== "undefined" && Boolean(readDraft(draftKey(courseId, machine, s.id)));
        const failed = st.grade?.startsWith("Không đạt");
        return <li key={s.id}>
          <button type="button" onClick={() => openStudent(s.id)} className="flex min-h-14 w-full items-center gap-3 py-2 text-left">
            <div className="min-w-0 flex-1">
              <p className="truncate text-[15px] font-bold text-white">{s.name}</p>
              <p className="text-xs text-slate-500">{s.className}{hasDraft ? " · có nháp" : ""}</p>
            </div>
            {st.scored ? <div className="text-right">
              <p className="font-mono text-base font-bold text-white">{fmt(st.total ?? 0)}</p>
              <p className={`text-xs font-bold ${failed ? "text-red-300" : "text-emerald-300"}`}>{st.grade}</p>
            </div> : <span className="text-xs text-slate-500">Chưa chấm</span>}
            {st.unsent && <span className="h-2.5 w-2.5 shrink-0 rounded-full bg-amber-400" title="Chưa gửi SV" />}
            <ChevronRight size={18} className="shrink-0 text-slate-500" />
          </button>
        </li>;
      })}
    </ul>
  </section>;
}
