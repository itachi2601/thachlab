"use client";

import { useEffect, useRef, useState } from "react";
import { ChevronDown } from "lucide-react";
import type { ExamQuestion, QuestionResponse, QuestionStatus } from "@/features/exams/types";
import {
  gradeQuestion,
  questionStatus,
  QUESTION_STATUS_LABELS,
} from "@/features/exams/types";
import Html from "@/components/exams/ContentHtml";
import Badge from "@/components/ui/Badge";

const LETTERS = ["A", "B", "C", "D"];
const TF_LABELS = ["a)", "b)", "c)", "d)"];

const STATUS_PILL: Record<QuestionStatus, string> = {
  correct: "bg-emerald-500/15 text-emerald-300",
  partial: "bg-amber-500/15 text-amber-300",
  wrong: "bg-red-500/15 text-red-300",
  skipped: "bg-slate-500/20 text-slate-400",
  manual: "bg-violet-500/15 text-violet-300",
};

// Viền cho biết kết quả; nền vẫn là nền thẻ để hai chế độ sáng/tối đều đọc được.
const CARD_TONE: Record<QuestionStatus, string> = {
  correct: "border-emerald-500/40",
  partial: "border-amber-500/40",
  wrong: "border-red-500/40",
  skipped: "border-white/10",
  manual: "border-violet-400/30",
};

/**
 * Hiệu ứng "nảy" nhẹ (scale 1 → 1.015 → 1, 0.16s) mỗi khi phương án VỪA được
 * chọn — trước dùng framer-motion `animate={{ scale: [1,1.015,1] }}`, nay đổi
 * sang CSS thuần: bật class `.is-pulsing` trong 160ms rồi tự tắt.
 */
function usePickPulse(active: boolean): boolean {
  const [pulsing, setPulsing] = useState(false);
  const wasActive = useRef(active);

  useEffect(() => {
    if (active && !wasActive.current) {
      setPulsing(true);
      const timer = window.setTimeout(() => setPulsing(false), 160);
      wasActive.current = active;
      return () => window.clearTimeout(timer);
    }
    wasActive.current = active;
  }, [active]);

  return pulsing;
}

function OptionButton({
  picked,
  review,
  className,
  onClick,
  children,
}: {
  picked: boolean;
  review: boolean;
  className: string;
  onClick: () => void;
  children: React.ReactNode;
}) {
  const pulsing = usePickPulse(picked && !review);
  return (
    <button
      type="button"
      disabled={review}
      onClick={onClick}
      className={`${className} ${review ? "" : "active:scale-[0.98] motion-reduce:active:scale-100"} ${
        pulsing ? "animate-pick-pulse" : ""
      } transition-transform duration-150`}
    >
      {children}
    </button>
  );
}

interface Props {
  index: number; // số thứ tự hiển thị (1-based)
  question: ExamQuestion;
  response: QuestionResponse;
  onChange?: (r: QuestionResponse) => void; // undefined = chế độ xem lại
  review?: boolean;
  /** Xem đáp án để tự đối chiếu (không tính là một lần làm bài) — bỏ điểm/số câu đúng, không tô đỏ. */
  selfCheck?: boolean;
}

export default function QuestionCard({
  index,
  question: q,
  response: r,
  onChange,
  review = false,
  selfCheck = false,
}: Props) {
  const scored = review && !selfCheck;
  const status = scored ? questionStatus(q, r) : null;
  const graded = scored && q.type !== "essay" ? gradeQuestion(q, r) : null;
  const border = status ? CARD_TONE[status] : "border-white/10";

  return (
    <div className={`rounded-2xl border bg-panel p-5 ${border}`}>
      <div className="flex items-start gap-3">
        <p className="exam-content min-w-0 flex-1 font-medium text-white">
          <span className="mr-1 font-semibold text-primary">Câu {index}.</span>
          <Html html={q.question} />
        </p>
        {status && (
          <span className="shrink-0 text-right">
            <span
              className={`inline-block rounded-lg px-2.5 py-1 text-sm font-semibold ${STATUS_PILL[status]}`}
            >
              {QUESTION_STATUS_LABELS[status]}
            </span>
            {graded && graded.max > 0 && (
              <span className="mt-1 block font-mono text-xs text-slate-400">
                {graded.earned.toLocaleString("vi-VN")}/{graded.max.toLocaleString("vi-VN")} đ
              </span>
            )}
          </span>
        )}
      </div>

      {q.type === "multiple_choice" && (
        <div className={`mt-4 grid gap-2 ${review ? "" : "sm:grid-cols-2"}`}>
          {q.options.map((opt, oi) => {
            const picked = r === oi;
            const isAnswer = oi === q.answer;
            const showPick = picked && !selfCheck;
            let cls = "border-white/10 bg-white/5 text-slate-300 hover:border-white/25";
            let dot = "bg-slate-500/20 text-slate-300";
            if (review) {
              if (isAnswer) {
                cls = "border-emerald-500/50 bg-emerald-500/10 text-emerald-100";
                dot = "bg-emerald-500 text-white";
              } else if (showPick) {
                cls = "border-red-500/50 bg-red-500/10 text-red-100";
                dot = "bg-red-500 text-white";
              } else {
                cls = "border-white/5 text-slate-400";
                dot = "bg-slate-500/20 text-slate-500";
              }
            } else if (picked) {
              cls = "border-primary bg-primary/15 text-white";
              dot = "bg-primary text-white";
            }
            return (
              <OptionButton
                key={oi}
                picked={picked}
                review={review}
                onClick={() => onChange?.(picked ? null : oi)}
                className={`flex items-start gap-3 rounded-xl border px-3 py-2.5 text-left text-base transition-colors ${cls}`}
              >
                <span
                  className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-sm font-bold ${dot}`}
                >
                  {LETTERS[oi]}
                </span>
                <span className="min-w-0 flex-1">
                  <Html html={opt} />
                  {review && (isAnswer || showPick) && (
                    <span className="mt-1.5 flex flex-wrap gap-1.5">
                      {isAnswer && <Badge tone="success">✓ Đáp án đúng</Badge>}
                      {showPick && (
                        <Badge tone={isAnswer ? "success" : "error"}>
                          {isAnswer ? "✓ Bạn chọn" : "✗ Bạn chọn"}
                        </Badge>
                      )}
                    </span>
                  )}
                </span>
              </OptionButton>
            );
          })}
          {review && !selfCheck && r === null && (
            <p className="text-sm text-slate-500">Em đã bỏ qua câu này.</p>
          )}
        </div>
      )}

      {q.type === "true_false" && (
        <div className="mt-4 space-y-2">
          {q.statements.map((st, si) => {
            const picks = Array.isArray(r) ? r : [];
            const pick = picks[si] ?? null;
            const rightHere = review && !selfCheck && pick === st.answer;
            const wrongHere = review && !selfCheck && pick !== null && pick !== st.answer;
            return (
              <div
                key={si}
                className={`flex flex-wrap items-center gap-2 rounded-xl border px-3 py-2 text-base ${
                  wrongHere
                    ? "border-red-500/40 bg-red-500/5"
                    : rightHere
                      ? "border-emerald-500/40 bg-emerald-500/5"
                      : "border-white/10 bg-white/5"
                }`}
              >
                <span className="font-semibold text-slate-400">{TF_LABELS[si]}</span>
                <Html
                  html={st.text}
                  className="basis-[calc(100%-2.5rem)] text-slate-300 sm:basis-auto sm:flex-1"
                />
                <span className="ml-auto flex gap-1">
                  {([true, false] as const).map((val) => {
                    const chosen = pick === val;
                    let cls = chosen
                      ? "bg-primary text-white"
                      : "bg-slate-500/20 text-slate-400 hover:bg-slate-500/30";
                    if (review) {
                      if (val === st.answer) cls = "bg-emerald-500/80 text-white";
                      else if (chosen && !selfCheck) cls = "bg-red-500/80 text-white";
                      else cls = "bg-slate-500/20 text-slate-500";
                    }
                    return (
                      <button
                        key={String(val)}
                        type="button"
                        disabled={review}
                        onClick={() => {
                          const next = [
                            ...(Array.isArray(r) ? r : [null, null, null, null]),
                          ];
                          next[si] = chosen ? null : val;
                          onChange?.(next);
                        }}
                        className={`rounded-lg px-3 py-1 text-sm font-semibold transition-transform transition-colors duration-150 ${
                          review ? "" : "active:scale-[0.94] motion-reduce:active:scale-100"
                        } ${cls}`}
                      >
                        {review && chosen && !selfCheck ? "✓ " : ""}
                        {val ? "Đúng" : "Sai"}
                      </button>
                    );
                  })}
                </span>
                {review && !selfCheck && pick === null && <Badge tone="neutral">Bỏ qua</Badge>}
              </div>
            );
          })}
        </div>
      )}

      {q.type === "short_answer" && (
        <div className="mt-4">
          {review ? (
            <div className="flex flex-wrap items-center gap-2 text-base">
              {!selfCheck && (
                <span className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-3 py-1.5">
                  <span className="text-sm text-slate-400">Em trả lời</span>
                  <span className="font-mono font-semibold text-white">
                    {typeof r === "string" && r.trim() !== "" ? r : "—"}
                  </span>
                </span>
              )}
              <span className="inline-flex items-center gap-2 rounded-xl border border-emerald-500/40 bg-emerald-500/10 px-3 py-1.5">
                <span className="text-sm text-emerald-200/80">Đáp án</span>
                <span className="font-mono font-semibold text-emerald-300">{q.answer}</span>
              </span>
            </div>
          ) : (
            <input
              value={typeof r === "string" ? r : ""}
              onChange={(e) => {
                const v = e.target.value.replace(/[^0-9,.\-]/g, "").slice(0, 4);
                onChange?.(v);
              }}
              placeholder="Đáp án (tối đa 4 ký tự)"
              className="w-48 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 font-mono text-white placeholder:text-sm placeholder:text-slate-500 focus:border-primary focus:outline-none"
            />
          )}
        </div>
      )}

      {q.type === "essay" && (
        <div className="mt-4 space-y-3">
          {review ? (
            <>
              {!selfCheck && (
                <div className="rounded-xl border border-white/10 bg-white/5 p-3 text-sm text-slate-300">
                  <span className="font-semibold text-slate-400">Bài làm: </span>
                  {typeof r === "string" && r.trim() ? r : "—"}
                </div>
              )}
              {q.suggestedAnswer && (
                <div className="rounded-xl border border-violet-400/20 bg-violet-500/5 p-3 text-sm text-slate-300">
                  <span className="font-semibold text-violet-300">Đáp án gợi ý: </span>
                  {q.suggestedAnswer}
                </div>
              )}
              {q.gradingGuide && (
                <div className="rounded-xl border border-white/10 p-3 text-sm text-slate-400">
                  <span className="font-semibold text-white">Hướng dẫn chấm: </span>
                  {q.gradingGuide}
                </div>
              )}
            </>
          ) : (
            <textarea
              value={typeof r === "string" ? r : ""}
              onChange={(e) => onChange?.(e.target.value)}
              rows={7}
              placeholder="Nhập bài làm tự luận…"
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm leading-6 text-white placeholder:text-slate-500 focus:border-primary focus:outline-none"
            />
          )}
        </div>
      )}

      {review && q.explanation && (
        <details open={status !== "correct"} className="group mt-3">
          <summary className="flex cursor-pointer list-none items-center gap-1.5 text-sm font-semibold text-cyan">
            Xem giải thích chi tiết
            <ChevronDown size={16} className="transition-transform group-open:rotate-180" />
          </summary>
          <div className="mt-2 rounded-xl border border-white/10 bg-white/5 p-3 text-base text-slate-300">
            <Html html={q.explanation} />
          </div>
        </details>
      )}
    </div>
  );
}
