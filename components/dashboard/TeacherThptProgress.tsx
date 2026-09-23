"use client";

import { useEffect, useMemo, useState } from "react";
import type { ClassStudent } from "@/services/classes";
import { expandClassIdsByGrade, fetchClasses } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { fetchChapters, fetchLessonItems, fetchLessons } from "@/services/lessons";
import type { Lesson, LessonItem } from "@/features/lessons/types";
import { dominantStatus, STATUS_LABELS, type ActivityStatus } from "@/features/progress/types";
import {
  fetchClassLearningProgress,
  fetchPendingEssays,
  gradeEssayAnswer,
  type ItemProgress,
  type PendingEssay,
} from "@/services/progress";
import { useToast } from "@/components/ui/Toast";

const STATUS_TONE: Record<ActivityStatus, string> = {
  not_started: "text-slate-500",
  in_progress: "text-cyan-300",
  submitted: "text-slate-300",
  completed_not_passed: "text-amber-300",
  passed: "text-emerald-300",
  pending_grading: "text-violet-300",
};

const FILTER_OPTIONS: { value: ActivityStatus | "all"; label: string }[] = [
  { value: "all", label: "Tất cả trạng thái" },
  { value: "not_started", label: STATUS_LABELS.not_started },
  { value: "in_progress", label: STATUS_LABELS.in_progress },
  { value: "completed_not_passed", label: STATUS_LABELS.completed_not_passed },
  { value: "pending_grading", label: STATUS_LABELS.pending_grading },
  { value: "passed", label: STATUS_LABELS.passed },
];

function StatusCell({ items }: { items: ItemProgress[] }) {
  if (items.length === 0) return <span className="text-slate-600">—</span>;
  const statuses = items
    .map((i) => i.theory?.status ?? i.practice?.status ?? i.graded?.status)
    .filter((s): s is ActivityStatus => !!s);
  const status = dominantStatus(statuses.length ? statuses : ["not_started"]) ?? "not_started";
  return <span className={`font-semibold ${STATUS_TONE[status]}`}>{STATUS_LABELS[status]}</span>;
}

function EssayGradingQueue({ studentIds, onGraded }: { studentIds: string[]; onGraded: () => void }) {
  const toast = useToast();
  const [pending, setPending] = useState<PendingEssay[] | null>(null);
  const [scores, setScores] = useState<Record<string, string>>({});
  const [busyKey, setBusyKey] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      if (studentIds.length === 0) {
        setPending([]);
        return;
      }
      try {
        setPending(await fetchPendingEssays(studentIds));
      } catch {
        setPending([]);
      }
    })();
  }, [studentIds]);

  if (!pending || pending.length === 0) return null;

  async function submit(item: PendingEssay) {
    const key = `${item.examResultId}-${item.questionIndex}`;
    const raw = scores[key];
    const earned = raw ? Number(raw) : NaN;
    if (Number.isNaN(earned) || earned < 0) {
      toast("error", "Nhập điểm hợp lệ (từ 0)");
      return;
    }
    setBusyKey(key);
    const res = await gradeEssayAnswer(item.examResultId, item.questionIndex, earned, 1);
    setBusyKey(null);
    if (!res.ok) {
      toast("error", `Chấm lỗi: ${res.message}`);
      return;
    }
    toast("success", "Đã chấm.");
    setPending((cur) => (cur ?? []).filter((p) => p !== item));
    onGraded();
  }

  return (
    <div className="space-y-3 rounded-2xl border border-violet-500/30 bg-violet-500/5 p-4">
      <p className="text-sm font-bold text-violet-300">Cần chấm ({pending.length})</p>
      <div className="space-y-3">
        {pending.map((item) => {
          const key = `${item.examResultId}-${item.questionIndex}`;
          return (
            <div key={key} className="rounded-xl border border-white/10 bg-panel p-3">
              <p className="text-xs text-slate-400">
                <b className="text-white">{item.studentName}</b> · {item.examTitle} · câu {item.questionIndex + 1} ·{" "}
                {new Date(item.submittedAt).toLocaleString("vi-VN")}
              </p>
              <p className="mt-2 text-sm text-slate-200">{item.question || "(không đọc được đề câu này)"}</p>
              <p className="mt-2 rounded-lg bg-white/5 p-2 text-sm text-slate-300">
                {item.answer || <span className="text-slate-500">(bỏ trống)</span>}
              </p>
              <div className="mt-2 flex items-center gap-2">
                <input
                  type="number"
                  min={0}
                  max={1}
                  step={0.05}
                  placeholder="Điểm (0–1)"
                  value={scores[key] ?? ""}
                  onChange={(e) => setScores((s) => ({ ...s, [key]: e.target.value }))}
                  className="w-28 rounded-lg border border-white/10 bg-white/5 px-2 py-1.5 text-sm text-white"
                />
                <button
                  type="button"
                  onClick={() => submit(item)}
                  disabled={busyKey === key}
                  className="rounded-lg bg-violet-600 px-3 py-1.5 text-xs font-bold text-white hover:bg-violet-500 disabled:opacity-50"
                >
                  {busyKey === key ? "Đang lưu…" : "Chấm"}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function TeacherThptProgress({ classId, students }: { classId: number; students: ClassStudent[] }) {
  const studentIds = useMemo(() => students.map((s) => s.id), [students]);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [lessonId, setLessonId] = useState<number | null>(null);
  const [items, setItems] = useState<LessonItem[]>([]);
  const [progressByStudent, setProgressByStudent] = useState<Map<string, Map<number, ItemProgress>>>(new Map());
  const [statusFilter, setStatusFilter] = useState<ActivityStatus | "all">("all");
  const [loading, setLoading] = useState(false);
  const [essayNonce, setEssayNonce] = useState(0);

  useEffect(() => {
    void (async () => {
      const [classes, chapters, allLessons] = await Promise.all([
        fetchClasses(),
        fetchChapters(),
        fetchLessons(true),
      ]);
      const visibleClassIds = expandClassIdsByGrade([classId], classes);
      const chapterIds = new Set(chapters.filter((ch) => visibleTo(ch.classIds, visibleClassIds)).map((ch) => ch.id));
      const scoped = allLessons.filter((l) => chapterIds.has(l.chapter_id) && l.published);
      setLessons(scoped);
      setLessonId((cur) => (cur !== null && scoped.some((l) => l.id === cur) ? cur : (scoped[0]?.id ?? null)));
    })();
  }, [classId]);

  useEffect(() => {
    void (async () => {
      if (lessonId === null) {
        setItems([]);
        return;
      }
      try {
        setItems(await fetchLessonItems(lessonId));
      } catch {
        setItems([]);
      }
    })();
  }, [lessonId]);

  useEffect(() => {
    void (async () => {
      if (items.length === 0 || studentIds.length === 0) {
        setProgressByStudent(new Map());
        return;
      }
      setLoading(true);
      try {
        setProgressByStudent(await fetchClassLearningProgress(studentIds, items));
      } catch {
        setProgressByStudent(new Map());
      } finally {
        setLoading(false);
      }
    })();
  }, [items, studentIds, essayNonce]);

  const theoryItems = items.filter((i) => i.kind === "ly_thuyet");
  const practiceItems = items.filter((i) => i.kind === "luyen_tap");
  const gradedItems = items.filter((i) => i.kind === "kiem_tra" || i.kind === "bai_tap_ve_nha");

  function rowFor(studentId: string, group: LessonItem[]): ItemProgress[] {
    const map = progressByStudent.get(studentId);
    if (!map) return [];
    return group.map((i) => map.get(i.id)).filter((p): p is ItemProgress => !!p);
  }

  function lastActivityFor(studentId: string): string | null {
    const map = progressByStudent.get(studentId);
    if (!map) return null;
    const dates = [...map.values()].map((p) => p.lastActivityAt).filter((d): d is string => !!d);
    if (dates.length === 0) return null;
    return dates.reduce((a, b) => (Date.parse(b) > Date.parse(a) ? b : a));
  }

  function overallStatus(studentId: string): ActivityStatus {
    const map = progressByStudent.get(studentId);
    if (!map) return "not_started";
    const statuses = [...map.values()]
      .map((p) => p.theory?.status ?? p.practice?.status ?? p.graded?.status)
      .filter((s): s is ActivityStatus => !!s);
    return dominantStatus(statuses) ?? "not_started";
  }

  const filteredStudents =
    statusFilter === "all" ? students : students.filter((s) => overallStatus(s.id) === statusFilter);

  return (
    <div className="space-y-4">
      <EssayGradingQueue studentIds={studentIds} onGraded={() => setEssayNonce((n) => n + 1)} />

      <div className="flex flex-wrap items-center gap-3">
        <select
          value={lessonId ?? ""}
          onChange={(e) => setLessonId(e.target.value ? Number(e.target.value) : null)}
          className="rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white focus:border-primary focus:outline-none"
        >
          {lessons.length === 0 && <option value="">Chưa có bài học nào</option>}
          {lessons.map((l) => (
            <option key={l.id} value={l.id}>
              {l.title}
            </option>
          ))}
        </select>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value as ActivityStatus | "all")}
          className="rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white focus:border-primary focus:outline-none"
        >
          {FILTER_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
        {loading && <span className="text-xs text-slate-500">Đang tải…</span>}
      </div>

      {items.length === 0 ? (
        <p className="text-sm text-slate-400">Bài này chưa có mục học liệu nào.</p>
      ) : filteredStudents.length === 0 ? (
        <p className="text-sm text-slate-400">Không có học sinh nào khớp bộ lọc.</p>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-white/10">
          <table className="w-full min-w-175 text-left text-sm">
            <thead className="bg-white/5 text-slate-400">
              <tr>
                <th className="px-4 py-3 font-medium">Học sinh</th>
                <th className="px-4 py-3 font-medium">Lý thuyết</th>
                <th className="px-4 py-3 font-medium">Luyện tập</th>
                <th className="px-4 py-3 font-medium">Đề kiểm tra</th>
                <th className="px-4 py-3 font-medium">Hoạt động gần nhất</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-300">
              {filteredStudents.map((s) => {
                const last = lastActivityFor(s.id);
                return (
                  <tr key={s.id}>
                    <td className="px-4 py-3 text-white">{s.full_name}</td>
                    <td className="px-4 py-3">
                      <StatusCell items={rowFor(s.id, theoryItems)} />
                    </td>
                    <td className="px-4 py-3">
                      <StatusCell items={rowFor(s.id, practiceItems)} />
                    </td>
                    <td className="px-4 py-3">
                      <StatusCell items={rowFor(s.id, gradedItems)} />
                    </td>
                    <td className="px-4 py-3 text-slate-400">
                      {last ? new Date(last).toLocaleString("vi-VN") : "—"}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
