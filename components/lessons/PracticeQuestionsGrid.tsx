"use client";

import { useEffect, useState } from "react";
import QuestionCard from "@/components/exams/QuestionCard";
import { emptyResponses, type Exam } from "@/features/exams/types";
import { TYPE_SHORT } from "@/features/lessons/types";
import { fetchExamsFull } from "@/services/lessons";

/** Lưới câu hỏi để tự luyện: bấm 1 câu để xem đáp án + lời giải ngay, không tính giờ, không chấm điểm. */
export default function PracticeQuestionsGrid({
  examIds,
  color = "#F59E0B",
}: {
  examIds: number[];
  color?: string;
}) {
  const [exams, setExams] = useState<Exam[] | null>(null);
  const [openKey, setOpenKey] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetchExamsFull(examIds).then((metas) =>
      setExams(examIds.map((id) => metas.get(id)).filter((e): e is Exam => !!e)),
    );
  }, [examIds]);

  function toggle(key: string) {
    setOpenKey((current) => {
      const next = new Set(current);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  if (!exams) return <p className="text-sm text-slate-400">Đang tải câu hỏi…</p>;
  if (exams.length === 0)
    return <p className="text-sm text-slate-400">Chưa có đề luyện tập.</p>;

  return (
    <div className="space-y-5">
      {exams.map((exam) => (
        <div key={exam.id} className="space-y-3">
          {exams.length > 1 && (
            <p className="text-xs font-bold uppercase tracking-wide" style={{ color }}>
              {exam.title}
            </p>
          )}
          <div className="flex flex-wrap gap-2">
            {exam.questions.map((q, qi) => {
              const key = `${exam.id}-${qi}`;
              const active = openKey.has(key);
              return (
                <button
                  key={key}
                  type="button"
                  onClick={() => toggle(key)}
                  className="flex min-w-16 flex-col items-center gap-0.5 rounded-xl border px-3 py-2 text-xs font-semibold transition-colors"
                  style={
                    active
                      ? { borderColor: color, backgroundColor: `${color}26`, color }
                      : { borderColor: "rgba(255,255,255,0.1)", color: "#94A3B8" }
                  }
                >
                  <span>CÂU {qi + 1}</span>
                  <span className="text-[10px] font-bold uppercase opacity-80">
                    {TYPE_SHORT[q.type] ?? ""}
                  </span>
                </button>
              );
            })}
          </div>
          <div className="space-y-3">
            {exam.questions.map((q, qi) => {
              const key = `${exam.id}-${qi}`;
              if (!openKey.has(key)) return null;
              const response = emptyResponses(exam.questions)[qi];
              return (
                <QuestionCard
                  key={key}
                  index={qi + 1}
                  question={q}
                  response={response}
                  review
                  selfCheck
                />
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
