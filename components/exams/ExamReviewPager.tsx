"use client";

import { useState, type ReactNode } from "react";
import {
  groupQuestionIndexesByType,
  questionStatus,
  QUESTION_STATUS_LABELS,
  QUESTION_TYPE_LABELS,
  type ExamQuestion,
  type QuestionResponse,
  type QuestionStatus,
} from "@/features/exams/types";
import QuestionCard from "@/components/exams/QuestionCard";

/** Ô số trong bảng câu hỏi — cùng tông màu với thẻ trạng thái của QuestionCard. */
const NAV_DOT: Record<QuestionStatus, string> = {
  correct: "border-emerald-500/60 bg-emerald-500/15 text-emerald-200 hover:border-emerald-400",
  partial: "border-amber-500/60 bg-amber-500/15 text-amber-200 hover:border-amber-400",
  wrong: "border-red-500/60 bg-red-500/15 text-red-200 hover:border-red-400",
  skipped: "border-white/15 text-slate-400 hover:border-white/30",
  manual: "border-violet-400/60 bg-violet-500/15 text-violet-200 hover:border-violet-300",
};

interface Props {
  questions: ExamQuestion[];
  responses: QuestionResponse[];
  /** Nội dung phụ hiện phía trên câu hỏi đang xem (nhãn chủ đề, nút "Ôn ngay"…). */
  renderAbove?: (index: number) => ReactNode;
}

/**
 * Xem lại bài làm giống lúc làm bài: bảng câu hỏi ghim trên đầu, mỗi lần chỉ
 * hiện 1 câu — dễ lần theo câu sai hơn là cuộn qua một danh sách dài.
 */
export default function ExamReviewPager({ questions, responses, renderAbove }: Props) {
  const firstWrong = questions.findIndex((q, i) => questionStatus(q, responses[i]) !== "correct");
  const [cur, setCur] = useState(firstWrong >= 0 ? firstWrong : 0);
  const [paletteOpen, setPaletteOpen] = useState(true);
  const lastIndex = questions.length - 1;

  function goTo(idx: number) {
    setCur(Math.min(lastIndex, Math.max(0, idx)));
  }

  return (
    <div>
      <div className="sticky top-16 z-30 mb-6 rounded-2xl border border-white/10 bg-panel/95 px-5 py-3 backdrop-blur-md">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <span className="text-sm text-slate-400">
            Câu <span className="font-semibold text-white">{cur + 1}</span>/{questions.length}
          </span>
          <button
            type="button"
            onClick={() => setPaletteOpen((v) => !v)}
            className="rounded-full border border-white/15 px-3 py-1 text-xs font-semibold text-slate-300 hover:border-white/30"
          >
            {paletteOpen ? "Ẩn bảng câu" : "Bảng câu hỏi"}
          </button>
        </div>

        {paletteOpen && (
          <div className="mt-3 max-h-[30vh] space-y-2 overflow-y-auto border-t border-white/10 pt-3">
            {groupQuestionIndexesByType(questions).map((section) => (
              <div key={section.type}>
                <div className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
                  {QUESTION_TYPE_LABELS[section.type]} · {section.indices.length} câu
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {section.indices.map((i) => {
                    const status = questionStatus(questions[i], responses[i]);
                    const title = `Câu ${i + 1} · ${QUESTION_STATUS_LABELS[status]}`;
                    return (
                      <button
                        key={i}
                        type="button"
                        onClick={() => goTo(i)}
                        title={title}
                        className={`flex h-8 w-8 items-center justify-center rounded-lg border text-xs font-bold transition-colors sm:h-9 sm:w-9 ${NAV_DOT[status]} ${
                          i === cur ? "ring-2 ring-white/70" : ""
                        }`}
                      >
                        {i + 1}
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-[11px] text-slate-500">
          <span className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded border border-emerald-500/60 bg-emerald-500/15" />
            Đúng
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded border border-amber-500/60 bg-amber-500/15" />
            Đúng một phần
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded border border-red-500/60 bg-red-500/15" />
            Sai
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded border border-white/15" />
            Bỏ qua
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded border border-violet-400/60 bg-violet-500/15" />
            Thầy chấm
          </span>
        </div>
      </div>

      {renderAbove?.(cur)}
      <QuestionCard index={cur + 1} question={questions[cur]} response={responses[cur]} review />

      <div className="mt-6 flex flex-wrap items-center gap-2">
        <button
          type="button"
          disabled={cur === 0}
          onClick={() => goTo(cur - 1)}
          className="rounded-xl border border-white/15 px-4 py-2 text-sm text-slate-300 hover:border-white/30 disabled:opacity-40"
        >
          ← Câu trước
        </button>
        <button
          type="button"
          disabled={cur === lastIndex}
          onClick={() => goTo(cur + 1)}
          className="ml-auto rounded-xl bg-primary px-5 py-2 text-sm font-semibold text-white hover:bg-primary-dark disabled:opacity-40"
        >
          Câu sau →
        </button>
      </div>
    </div>
  );
}
