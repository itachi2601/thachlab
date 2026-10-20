"use client";

import { useEffect, useMemo, useState } from "react";
import { ExternalLink } from "lucide-react";
import { fetchChapters, fetchLessonItems, fetchLessons } from "@/services/lessons";
import { AVCN_SUBJECT_CODE } from "@/services/classes";
import { isItemLive, type Lesson, type LessonItem } from "@/features/lessons/types";
import { dominantStatus, STATUS_LABELS, type ActivityStatus } from "@/features/progress/types";
import { fetchClassLearningProgress, type ItemProgress } from "@/services/progress";
import TeacherAvcnExamAnalysis from "@/components/dashboard/TeacherAvcnExamAnalysis";

type Student = { id: string; name: string; className: string };

const STATUS_TONE: Record<ActivityStatus, string> = {
  not_started: "text-muted",
  in_progress: "text-cyan-600",
  submitted: "text-ink",
  completed_not_passed: "text-amber-600",
  passed: "text-emerald-600",
  pending_grading: "text-violet-600",
};

function statusOf(p: ItemProgress | undefined): ActivityStatus | undefined {
  return p?.theory?.status ?? p?.practice?.status ?? p?.graded?.status;
}

function StatusCell({ items }: { items: ItemProgress[] }) {
  if (items.length === 0) return <span className="text-muted">—</span>;
  const statuses = items.map(statusOf).filter((s): s is ActivityStatus => !!s);
  const status = dominantStatus(statuses.length ? statuses : ["not_started"]) ?? "not_started";
  return <span className={`font-semibold ${STATUS_TONE[status]}`}>{STATUS_LABELS[status]}</span>;
}

/**
 * Tab Tổng quan / Bảng điểm của lớp học phần AVCN: lấy thẳng các bài học môn 'avcn'
 * đang có trên web (/lop-hoc/avcn) và tiến độ thật của từng sinh viên trong lớp.
 */
export default function TeacherAvcnProgress({ students }: { students: Student[] }) {
  const studentIds = useMemo(() => students.map((s) => s.id), [students]);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [lessonId, setLessonId] = useState<number | null>(null);
  const [items, setItems] = useState<LessonItem[]>([]);
  const [progress, setProgress] = useState<Map<string, Map<number, ItemProgress>>>(new Map());
  const [filter, setFilter] = useState<ActivityStatus | "all">("all");
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    void (async () => {
      try {
        const [chapters, all] = await Promise.all([fetchChapters(), fetchLessons(true)]);
        const ids = new Set(chapters.filter((c) => c.subjectCode === AVCN_SUBJECT_CODE).map((c) => c.id));
        const scoped = all.filter((l) => ids.has(l.chapter_id));
        setLessons(scoped);
        // Mặc định mở bài đã đăng đầu tiên: bài nháp chưa có SV nào làm.
        setLessonId((scoped.find((l) => l.published) ?? scoped[0])?.id ?? null);
      } finally {
        setLoaded(true);
      }
    })();
  }, []);

  useEffect(() => {
    void (async () => {
      if (lessonId === null) return setItems([]);
      try {
        setItems((await fetchLessonItems(lessonId)).filter(isItemLive));
      } catch {
        setItems([]);
      }
    })();
  }, [lessonId]);

  useEffect(() => {
    void (async () => {
      if (items.length === 0 || studentIds.length === 0) return setProgress(new Map());
      setLoading(true);
      try {
        setProgress(await fetchClassLearningProgress(studentIds, items));
      } catch {
        setProgress(new Map());
      } finally {
        setLoading(false);
      }
    })();
  }, [items, studentIds]);

  const theory = items.filter((i) => i.kind === "ly_thuyet");
  const practice = items.filter((i) => i.kind === "luyen_tap");
  const graded = items.filter((i) => i.kind === "kiem_tra" || i.kind === "bai_tap_ve_nha");

  const rowFor = (id: string, group: LessonItem[]) => {
    const map = progress.get(id);
    return map ? group.map((i) => map.get(i.id)).filter((p): p is ItemProgress => !!p) : [];
  };
  const lastActivity = (id: string) => {
    const dates = [...(progress.get(id)?.values() ?? [])].map((p) => p.lastActivityAt).filter((d): d is string => !!d);
    return dates.length ? dates.reduce((a, b) => (Date.parse(b) > Date.parse(a) ? b : a)) : null;
  };
  const overall = (id: string): ActivityStatus => {
    const statuses = [...(progress.get(id)?.values() ?? [])].map(statusOf).filter((s): s is ActivityStatus => !!s);
    return dominantStatus(statuses) ?? "not_started";
  };

  const rows = filter === "all" ? students : students.filter((s) => overall(s.id) === filter);
  const counts = students.reduce<Record<string, number>>((acc, s) => {
    const k = overall(s.id);
    acc[k] = (acc[k] ?? 0) + 1;
    return acc;
  }, {});
  const active = lessons.find((l) => l.id === lessonId);

  if (loaded && lessons.length === 0) {
    return <p className="rounded-2xl border border-dashed border-line p-6 text-sm text-muted">Môn Anh văn chuyên ngành chưa có bài học nào trên web.</p>;
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <select aria-label="Bài học" value={lessonId ?? ""} onChange={(e) => setLessonId(e.target.value ? Number(e.target.value) : null)} className="rounded-xl border border-line-strong bg-panel-deep px-3 py-2 text-sm font-semibold text-ink">
          {lessons.map((l) => (
            <option key={l.id} value={l.id}>
              {l.title}
              {l.published ? "" : " (chưa đăng)"}
            </option>
          ))}
        </select>
        <select aria-label="Trạng thái" value={filter} onChange={(e) => setFilter(e.target.value as ActivityStatus | "all")} className="rounded-xl border border-line-strong bg-panel-deep px-3 py-2 text-sm text-ink">
          <option value="all">Tất cả trạng thái</option>
          {(Object.keys(STATUS_LABELS) as ActivityStatus[]).map((k) => (
            <option key={k} value={k}>
              {STATUS_LABELS[k]}
            </option>
          ))}
        </select>
        {active && (
          <a href={`/lop-hoc/bai/?id=${active.id}`} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 rounded-xl border border-line-strong px-3 py-2 text-sm font-bold text-ink hover:bg-surface-2">
            <ExternalLink size={15} /> Xem bài trên web
          </a>
        )}
        {loading && <span className="text-xs text-muted">Đang tải…</span>}
      </div>

      {students.length > 0 && items.length > 0 && (
        <p className="text-sm text-muted">
          {students.length} sinh viên · đạt {counts.passed ?? 0} · đang học {(counts.in_progress ?? 0) + (counts.submitted ?? 0)} · chưa đạt {counts.completed_not_passed ?? 0} · chưa bắt đầu {counts.not_started ?? 0}
        </p>
      )}

      {items.length === 0 ? (
        <p className="text-sm text-muted">Bài này chưa có mục học liệu nào.</p>
      ) : rows.length === 0 ? (
        <p className="text-sm text-muted">Không có sinh viên nào khớp bộ lọc.</p>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-line">
          <table className="w-full min-w-175 text-left text-sm">
            <thead className="bg-surface-2 text-muted">
              <tr>
                <th className="px-4 py-3 font-medium">Sinh viên</th>
                <th className="px-4 py-3 font-medium">Bài đọc / từ vựng</th>
                <th className="px-4 py-3 font-medium">Luyện tập</th>
                <th className="px-4 py-3 font-medium">Đề kiểm tra</th>
                <th className="px-4 py-3 font-medium">Hoạt động gần nhất</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line text-ink">
              {rows.map((s) => {
                const last = lastActivity(s.id);
                return (
                  <tr key={s.id}>
                    <td className="px-4 py-3 font-semibold">{s.name}</td>
                    <td className="px-4 py-3"><StatusCell items={rowFor(s.id, theory)} /></td>
                    <td className="px-4 py-3"><StatusCell items={rowFor(s.id, practice)} /></td>
                    <td className="px-4 py-3"><StatusCell items={rowFor(s.id, graded)} /></td>
                    <td className="px-4 py-3 text-muted">{last ? new Date(last).toLocaleString("vi-VN") : "—"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      <TeacherAvcnExamAnalysis
        examIds={items.filter((i) => i.kind === "luyen_tap" || i.kind === "kiem_tra").flatMap((i) => i.exam_ids ?? [])}
        studentIds={studentIds}
      />
    </div>
  );
}
