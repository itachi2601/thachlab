"use client";

import type { ExamQuestion, QuestionResponse } from "@/features/exams/types";
import { gradeQuestion } from "@/features/exams/types";
import Html from "@/components/exams/ContentHtml";

const LETTERS = ["A", "B", "C", "D"];
const TF_LABELS = ["a)", "b)", "c)", "d)"];

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
  const graded = review && !selfCheck && q.type !== "essay" ? gradeQuestion(q, r) : null;
  const border = !review
    ? "border-white/10"
    : selfCheck
      ? "border-white/10"
      : !graded
        ? "border-violet-400/20 bg-violet-500/5"
      : graded.earned === graded.max
        ? "border-emerald-500/30 bg-emerald-500/5"
        : graded.earned > 0
          ? "border-amber-500/30 bg-amber-500/5"
          : "border-red-500/30 bg-red-500/5";

  return (
    <div className={`rounded-2xl border bg-[#0B1020] p-5 ${border}`}>
      <p className="exam-content font-medium text-slate-100">
        <span className="mr-1 font-semibold text-primary">Câu {index}.</span>
        <Html html={q.question} />
      </p>

      {q.type === "multiple_choice" && (
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          {q.options.map((opt, oi) => {
            const picked = r === oi;
            let cls =
              "border-white/10 bg-white/5 text-slate-300 hover:border-white/25";
            if (review) {
              cls =
                oi === q.answer
                  ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-200"
                  : picked
                    ? "border-red-500/50 bg-red-500/10 text-red-200"
                    : "border-white/5 text-slate-400";
            } else if (picked) {
              cls = "border-primary bg-primary/15 text-white";
            }
            return (
              <button
                key={oi}
                type="button"
                disabled={review}
                onClick={() => onChange?.(picked ? null : oi)}
                className={`flex items-start gap-2 rounded-xl border px-3 py-2.5 text-left text-sm transition-colors ${cls}`}
              >
                <span className="font-semibold">{LETTERS[oi]}.</span>
                <Html html={opt} />
                {review && oi === q.answer && <span className="ml-auto">✓</span>}
              </button>
            );
          })}
        </div>
      )}

      {q.type === "true_false" && (
        <div className="mt-4 space-y-2">
          {q.statements.map((st, si) => {
            const picks = Array.isArray(r) ? r : [];
            const pick = picks[si] ?? null;
            return (
              <div
                key={si}
                className="flex flex-wrap items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm"
              >
                <span className="font-semibold text-slate-400">
                  {TF_LABELS[si]}
                </span>
                <Html html={st.text} className="flex-1 text-slate-300" />
                <span className="ml-auto flex gap-1">
                  {([true, false] as const).map((val) => {
                    const chosen = pick === val;
                    let cls = chosen
                      ? "bg-primary text-white"
                      : "bg-white/10 text-slate-400 hover:bg-white/20";
                    if (review) {
                      if (val === st.answer)
                        cls = "bg-emerald-500/80 text-white";
                      else if (chosen) cls = "bg-red-500/80 text-white";
                      else cls = "bg-white/10 text-slate-500";
                    }
                    return (
                      <button
                        key={String(val)}
                        type="button"
                        disabled={review}
                        onClick={() => {
                          const next = [
                            ...(Array.isArray(r)
                              ? r
                              : [null, null, null, null]),
                          ];
                          next[si] = chosen ? null : val;
                          onChange?.(next);
                        }}
                        className={`rounded-lg px-3 py-1 text-xs font-semibold transition-colors ${cls}`}
                      >
                        {val ? "Đúng" : "Sai"}
                      </button>
                    );
                  })}
                </span>
              </div>
            );
          })}
        </div>
      )}

      {q.type === "short_answer" && (
        <div className="mt-4">
          {review ? (
            <p className="text-sm">
              {!selfCheck && (
                <>
                  <span className="text-slate-400">Trả lời của em: </span>
                  <span className="font-mono font-semibold text-white">
                    {typeof r === "string" && r.trim() !== "" ? r : "—"}
                  </span>
                </>
              )}
              <span className={`text-slate-400 ${selfCheck ? "" : "ml-4"}`}>Đáp án: </span>
              <span className="font-mono font-semibold text-emerald-300">
                {q.answer}
              </span>
            </p>
          ) : (
            <input
              value={typeof r === "string" ? r : ""}
              onChange={(e) => {
                const v = e.target.value
                  .replace(/[^0-9,.\-]/g, "")
                  .slice(0, 4);
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
              {q.suggestedAnswer && <div className="rounded-xl border border-violet-400/20 bg-violet-500/5 p-3 text-sm text-slate-300"><span className="font-semibold text-violet-300">Đáp án gợi ý: </span>{q.suggestedAnswer}</div>}
              {q.gradingGuide && <div className="rounded-xl border border-white/10 p-3 text-sm text-slate-400"><span className="font-semibold text-white">Hướng dẫn chấm: </span>{q.gradingGuide}</div>}
            </>
          ) : (
            <textarea value={typeof r === "string" ? r : ""} onChange={(e) => onChange?.(e.target.value)} rows={7} placeholder="Nhập bài làm tự luận…" className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm leading-6 text-white placeholder:text-slate-500 focus:border-primary focus:outline-none" />
          )}
        </div>
      )}

      {review && !selfCheck && graded && (
        <p className="mt-3 text-xs text-slate-400">
          Điểm câu này:{" "}
          <span className="font-semibold text-white">
            {graded.earned.toLocaleString("vi-VN")}/
            {graded.max.toLocaleString("vi-VN")}
          </span>
        </p>
      )}

      {review && q.explanation && (
        <div className="mt-3 rounded-xl border border-white/10 bg-white/5 p-3 text-sm text-slate-300">
          <span className="font-semibold text-cyan">Lời giải: </span>
          <Html html={q.explanation} />
        </div>
      )}
    </div>
  );
}
