"use client";

import { useEffect, useState } from "react";
import ChapterMasteryRadar from "@/components/results/ChapterMasteryRadar";
import { buildCourseRadar, fetchClassQuestionActivity, fetchCurriculumMeta } from "@/services/class-insights";
import type { ChapterLessonMastery } from "@/services/mastery";

export type RadarData = { current: ChapterLessonMastery[]; prev: ChapterLessonMastery[] | null };

/**
 * "Con nắm bài tới đâu" — sơ đồ mạng nhện cho phụ huynh, kèm hai câu đọc sẵn (vững nhất / cần thêm).
 * Thầy chốt 15/10/2026 đưa radar sang trang phụ huynh (trước đó P17 để "không biểu đồ"): bù lại bằng
 * số % ghi ngay trên đỉnh và câu chữ đọc sẵn phía trên, để phụ huynh không phải tự đọc hình (P6, P19).
 * Dữ liệu dựng ở máy như trang hồ sơ của giáo viên (buildCourseRadar) — phụ huynh đã có quyền đọc
 * exam_question_results / practice_question_results của con, không cần RPC hay migration mới.
 */
export default function ParentRadar({ studentId, demo }: { studentId: string; demo?: RadarData }) {
  const [data, setData] = useState<RadarData | null | undefined>(demo);

  useEffect(() => {
    if (demo) return;
    let cancelled = false;
    Promise.all([fetchClassQuestionActivity([studentId]), fetchCurriculumMeta()])
      .then(([rows, meta]) => {
        if (cancelled) return;
        const current = buildCourseRadar(rows, meta);
        const prev = buildCourseRadar(rows, meta, new Date(Date.now() - 30 * 86400e3));
        setData(
          current.some((r) => r.pct !== null)
            ? { current, prev: prev.some((r) => r.pct !== null) ? prev : null }
            : null,
        );
      })
      .catch(() => !cancelled && setData(null));
    return () => {
      cancelled = true;
    };
  }, [studentId, demo]);

  if (data === undefined) {
    return (
      <div className="mb-6 h-[320px] rounded-2xl border border-line bg-panel" aria-busy="true" aria-label="Đang tải…" />
    );
  }
  if (data === null) return null;

  const done = data.current.filter((r) => r.pct !== null && r.answeredCount >= 4);
  const best = [...done].sort((a, b) => (b.pct ?? 0) - (a.pct ?? 0))[0];
  const weak = [...done].sort((a, b) => (a.pct ?? 0) - (b.pct ?? 0))[0];

  return (
    <section className="mb-6">
      <h2 className="font-display text-lg font-bold text-ink">Con nắm bài tới đâu</h2>
      <p className="parent-copy mt-1 text-muted">
        Mỗi đỉnh là một bài học. Số trong vòng tròn là phần trăm câu con làm đúng ở bài đó; càng ra xa tâm càng vững.
        Mục tiêu là 80%.
      </p>
      {best && weak && best.lessonId !== weak.lessonId && (
        <ul className="parent-copy mt-3 space-y-1 text-ink">
          <li>
            Vững nhất: <b>{best.lessonTitle}</b> — {best.pct}%.
          </li>
          <li>
            Cần thêm nhất: <b>{weak.lessonTitle}</b> — {weak.pct}%.
          </li>
        </ul>
      )}
      <div className="mt-3">
        <ChapterMasteryRadar studentId={studentId} courseData={data} viewer="parent" />
      </div>
    </section>
  );
}
