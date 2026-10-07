"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import SimilarBankPractice from "@/components/lessons/SimilarBankPractice";
import type { LessonWorkedQuestion } from "@/features/lessons/types";

/** Dạng có cấu trúc: đề + mô phỏng → (HS chọn) phân tích đề → (HS chọn) lời giải đầy đủ → làm bài tương tự.
 *  Bản cũ có `hints_html` (gợi ý theo tầng) vẫn hiển thị như trước. Dạng cũ chỉ có body_html ở dưới. */
function StructuredBody({ q, color }: { q: LessonWorkedQuestion; color: string }) {
  const hints = q.hints_html ?? [];
  const [shown, setShown] = useState(0);
  const [analysed, setAnalysed] = useState(false);
  const [solved, setSolved] = useState(false);
  const hasAnalysis = !!q.analysis_html;
  return (
    <div className="space-y-3">
      <ContentHtml html={q.problem_html ?? ""} className="block leading-relaxed" />
      <p className="text-xs text-slate-400">
        {hasAnalysis ? "Tự thử giải trên giấy trước, kẹt thì mở phân tích đề." : "Tự thử giải trên giấy trước, kẹt thì mở từng gợi ý."}
      </p>
      {hasAnalysis && analysed && (
        <div className="rounded-lg border border-white/10 p-3">
          <p className="mb-1 text-xs font-semibold" style={{ color }}>
            Phân tích đề
          </p>
          <ContentHtml html={q.analysis_html ?? ""} className="block leading-relaxed" />
        </div>
      )}
      {!hasAnalysis &&
        hints.slice(0, shown).map((h, i) => (
          <div key={i} className="rounded-lg border border-white/10 p-3">
            <p className="mb-1 text-xs font-semibold" style={{ color }}>
              Gợi ý {i + 1}/{hints.length}
            </p>
            <ContentHtml html={h} className="block leading-relaxed" />
          </div>
        ))}
      <div className="flex flex-wrap gap-2">
        {hasAnalysis && !analysed && (
          <button type="button" className="lesson-btn-ghost" onClick={() => setAnalysed(true)}>
            Phân tích đề
          </button>
        )}
        {!hasAnalysis && shown < hints.length && (
          <button type="button" className="lesson-btn-ghost" onClick={() => setShown((n) => n + 1)}>
            Gợi ý {shown + 1}/{hints.length}
          </button>
        )}
        {!solved && (
          <button type="button" className="lesson-btn-ghost" onClick={() => setSolved(true)}>
            Xem lời giải đầy đủ
          </button>
        )}
      </div>
      {solved && (
        <>
          <ContentHtml html={q.solution_html ?? ""} className="block leading-relaxed" />
          {q.topic_id ? <SimilarBankPractice topicId={q.topic_id} form={q.form} color={color} /> : null}
        </>
      )}
    </div>
  );
}

/** Các "dạng bài" (bài tập mẫu): hàng thu/mở, tên dạng hiện rõ, lời giải mở ngay dưới hàng đó. */
export default function WorkedQuestionsGrid({
  questions,
  color = "#8B5CF6",
}: {
  questions: LessonWorkedQuestion[];
  color?: string;
}) {
  const [openIdx, setOpenIdx] = useState<Set<number>>(() => new Set(questions.length ? [0] : []));

  function toggle(idx: number) {
    setOpenIdx((current) => {
      const next = new Set(current);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  }

  if (questions.length === 0) return null;

  return (
    <div className="lesson-worked">
      {questions.map((q, idx) => {
        const open = openIdx.has(idx);
        return (
          <div key={idx} className="lesson-worked-row">
            <button
              type="button"
              onClick={() => toggle(idx)}
              aria-expanded={open}
              className="lesson-worked-head"
            >
              <span
                className="lesson-worked-num"
                style={open ? { borderColor: color, color } : undefined}
              >
                {idx + 1}
              </span>
              <span className="lesson-worked-label">{q.label || `Ví dụ ${idx + 1}`}</span>
              <ChevronDown size={16} className={open ? "rotate-180" : ""} />
            </button>
            {open && (
              <div className="lesson-worked-body">
                {q.problem_html && q.solution_html ? (
                  <StructuredBody q={q} color={color} />
                ) : (
                  <ContentHtml html={q.body_html} className="block leading-relaxed" />
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
