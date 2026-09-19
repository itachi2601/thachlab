"use client";

import { useEffect, useState } from "react";
import QuestionCard from "@/components/exams/QuestionCard";
import {
  emptyResponses,
  gradeQuestion,
  isAnswered,
  type Exam,
  type ExamQuestion,
  type QuestionResponse,
} from "@/features/exams/types";
import { TYPE_SHORT } from "@/features/lessons/types";
import { fetchExamsFull } from "@/services/lessons";

interface Pick {
  key: string;
  question: ExamQuestion;
  examTitle: string;
}

type Status = "doing" | "checked" | "revealed";

/**
 * Bài tập mẫu: em chọn/nhập đáp án rồi bấm "Kiểm tra" thì web mới chấm đúng–sai
 * và mở lời giải chi tiết. Em nào chưa làm được thì bấm "Xem lời giải" — vẫn mở
 * lời giải nhưng không chấm, không tô đỏ.
 */
export default function SampleQuestionsGrid({
  examIds,
  color = "#8B5CF6",
}: {
  examIds: number[];
  color?: string;
}) {
  const [picks, setPicks] = useState<Pick[] | null>(null);
  const [responses, setResponses] = useState<Record<string, QuestionResponse>>({});
  const [status, setStatus] = useState<Record<string, Status>>({});
  const [open, setOpen] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    fetchExamsFull(examIds).then((metas) => {
      if (!alive) return;
      const flat: Pick[] = [];
      const seed: Record<string, QuestionResponse> = {};
      for (const id of examIds) {
        const exam = metas.get(id) as Exam | undefined;
        if (!exam) continue;
        const blanks = emptyResponses(exam.questions);
        exam.questions.forEach((question, qi) => {
          const key = `${id}-${qi}`;
          flat.push({ key, question, examTitle: exam.title });
          seed[key] = blanks[qi];
        });
      }
      setPicks(flat);
      setResponses(seed);
    });
    return () => {
      alive = false;
    };
  }, [examIds]);

  if (!picks) return <p className="text-sm text-slate-400">Đang tải bài tập mẫu…</p>;
  if (picks.length === 0) return null;

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        {picks.map((p, idx) => {
          const st = status[p.key];
          const active = open === p.key;
          const graded =
            st === "checked" && p.question.type !== "essay"
              ? gradeQuestion(p.question, responses[p.key])
              : null;
          const mark = graded
            ? graded.earned === graded.max
              ? "✓"
              : "✗"
            : st === "revealed"
              ? "👁"
              : "";
          const tone = graded
            ? graded.earned === graded.max
              ? "#34D399"
              : "#F87171"
            : color;
          return (
            <button
              key={p.key}
              type="button"
              onClick={() => setOpen(active ? null : p.key)}
              className="flex min-w-16 flex-col items-center gap-0.5 rounded-xl border px-3 py-2 text-xs font-semibold transition-colors"
              style={
                active || st
                  ? { borderColor: tone, backgroundColor: `${tone}26`, color: tone }
                  : { borderColor: "rgba(255,255,255,0.1)", color: "#94A3B8" }
              }
            >
              <span>
                BÀI {idx + 1} {mark}
              </span>
              <span className="text-[10px] font-bold uppercase opacity-80">
                {TYPE_SHORT[p.question.type] ?? "TL"}
              </span>
            </button>
          );
        })}
      </div>

      {picks.map((p, idx) => {
        if (open !== p.key) return null;
        const st = status[p.key] ?? "doing";
        const answered = isAnswered(p.question, responses[p.key]);
        return (
          <div key={p.key} className="space-y-3">
            <QuestionCard
              index={idx + 1}
              question={p.question}
              response={responses[p.key]}
              onChange={
                st === "doing"
                  ? (r) => setResponses((cur) => ({ ...cur, [p.key]: r }))
                  : undefined
              }
              review={st !== "doing"}
              selfCheck={st === "revealed"}
            />
            {st === "doing" ? (
              <div className="flex flex-wrap items-center gap-2">
                <button
                  type="button"
                  disabled={!answered}
                  onClick={() => setStatus((cur) => ({ ...cur, [p.key]: "checked" }))}
                  className="rounded-xl px-5 py-2 text-sm font-bold text-white disabled:opacity-40"
                  style={{ backgroundColor: color }}
                >
                  Kiểm tra
                </button>
                <button
                  type="button"
                  onClick={() => setStatus((cur) => ({ ...cur, [p.key]: "revealed" }))}
                  className="rounded-xl border border-white/15 px-4 py-2 text-sm text-slate-300 hover:border-white/30"
                >
                  Chưa làm được, xem lời giải
                </button>
                {!answered && (
                  <span className="text-xs text-slate-500">
                    Chọn đáp án trước rồi mới kiểm tra được.
                  </span>
                )}
              </div>
            ) : (
              <button
                type="button"
                onClick={() => {
                  setStatus((cur) => {
                    const next = { ...cur };
                    delete next[p.key];
                    return next;
                  });
                  setResponses((cur) => ({
                    ...cur,
                    [p.key]: emptyResponses([p.question])[0],
                  }));
                }}
                className="rounded-xl border border-white/15 px-4 py-2 text-sm text-slate-300 hover:border-white/30"
              >
                Làm lại bài này
              </button>
            )}
          </div>
        );
      })}
    </div>
  );
}
