"use client";

import { useEffect, useMemo, useState } from "react";
import { Eye } from "lucide-react";
import type { ClassStudent } from "@/services/classes";
import { fetchClassExamResults, type ClassExamResult } from "@/services/class-results";
import {
  EARLY_THRESHOLDS,
  computeEarlySignals,
  fetchClassQuestionActivity,
  type EarlySignal,
} from "@/services/class-insights";

const KIND_LABEL: Record<EarlySignal["kind"], string> = {
  inactive: "Lâu không vào",
  never_started: "Chưa bắt đầu",
  score_drop: "Điểm đang tụt",
  rushed: "Làm quá nhanh",
};

/**
 * Cảnh báo sớm theo hành vi — trước khi thành "cần phụ đạo". Ngưỡng ở EARLY_THRESHOLDS
 * (class-insights.ts), cần chỉnh theo dữ liệu lớp thật để tránh báo động giả.
 */
export default function TeacherThptEarlyWarning({
  students,
  onOpenStudent,
  onLoaded,
}: {
  students: ClassStudent[];
  onOpenStudent: (id: string) => void;
  onLoaded?: (signalStudentCount: number) => void;
}) {
  const studentIds = useMemo(() => students.map((s) => s.id), [students]);
  const [results, setResults] = useState<ClassExamResult[] | null>(null);
  const [last, setLast] = useState<Map<string, string> | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([fetchClassExamResults(studentIds).catch(() => []), fetchClassQuestionActivity(studentIds).catch(() => [])]).then(([res, rows]) => {
      if (cancelled) return;
      const m = new Map<string, string>();
      for (const r of rows) {
        const cur = m.get(r.student_id);
        if (!cur || r.created_at > cur) m.set(r.student_id, r.created_at);
      }
      setResults(res);
      setLast(m);
    });
    return () => { cancelled = true; };
  }, [studentIds]);

  const signals = useMemo(
    () => (results && last ? computeEarlySignals(studentIds, results, last) : []),
    [results, last, studentIds],
  );
  const byStudent = useMemo(() => {
    const m = new Map<string, EarlySignal[]>();
    for (const s of signals) m.set(s.studentId, [...(m.get(s.studentId) ?? []), s]);
    return [...m.entries()].sort((a, b) => b[1].length - a[1].length);
  }, [signals]);

  useEffect(() => {
    if (results && last) onLoaded?.(byStudent.length);
  }, [results, last, byStudent.length, onLoaded]);

  const nameOf = useMemo(() => new Map(students.map((s) => [s.id, s.full_name])), [students]);

  return (
    <section className="space-y-3">
      <div className="flex items-center gap-2">
        <Eye size={18} className="text-amber-300" />
        <h3 className="font-display text-lg font-bold text-white">Cần để ý sớm</h3>
      </div>
      <p className="text-xs leading-relaxed text-slate-400">
        Dấu hiệu hành vi, chưa phải kết luận: ≥{EARLY_THRESHOLDS.inactiveDays} ngày không hoạt động, điểm giảm 3 đề liên tiếp,
        hoặc làm xong rất nhanh mà điểm thấp. Nên hỏi thăm trước khi xếp phụ đạo.
      </p>
      {!results || !last ? (
        <p className="text-sm text-slate-400">Đang phân tích…</p>
      ) : byStudent.length === 0 ? (
        <p className="rounded-2xl border border-white/10 bg-panel p-4 text-sm text-emerald-300">Chưa thấy dấu hiệu đáng lo nào.</p>
      ) : (
        <ul className="max-h-[32rem] space-y-2 overflow-y-auto pr-1">
          {byStudent.map(([id, list]) => (
            <li key={id}>
              <button
                type="button"
                onClick={() => onOpenStudent(id)}
                className="w-full rounded-2xl border border-white/10 bg-panel p-4 text-left hover:bg-white/[.06]"
              >
                <p className="text-sm font-semibold text-white">{nameOf.get(id) ?? "—"}</p>
                <ul className="mt-1 space-y-0.5 text-xs text-slate-300">
                  {list.map((s, i) => (
                    <li key={i}><span className="text-amber-300">{KIND_LABEL[s.kind]}</span> · {s.text}</li>
                  ))}
                </ul>
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
