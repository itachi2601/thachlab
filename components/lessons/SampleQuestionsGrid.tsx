"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ChevronDown } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
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
type LoadState = "loading" | "loaded" | "error";

/**
 * Bài tập mẫu: hàng thu/mở theo từng câu — bấm để mở, chọn/nhập đáp án rồi
 * bấm "Kiểm tra" thì web mới chấm đúng–sai và mở lời giải chi tiết ngay dưới
 * câu đó. Em nào chưa làm được thì bấm "Xem lời giải" — vẫn mở lời giải
 * nhưng không chấm, không tô đỏ.
 */
export default function SampleQuestionsGrid({
  examIds,
  color = "#8B5CF6",
}: {
  examIds: number[];
  color?: string;
}) {
  const { session } = useAuth();
  const [picks, setPicks] = useState<Pick[]>([]);
  const [loadState, setLoadState] = useState<LoadState>("loading");
  const [responses, setResponses] = useState<Record<string, QuestionResponse>>({});
  const [status, setStatus] = useState<Record<string, Status>>({});
  const [open, setOpen] = useState<string | null>(null);

  useEffect(() => {
    if (!session) return;
    let alive = true;
    void (async () => {
      setLoadState("loading");
      try {
        const metas = await fetchExamsFull(examIds);
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
        setLoadState("loaded");
      } catch {
        if (alive) setLoadState("error");
      }
    })();
    return () => {
      alive = false;
    };
  }, [examIds, session]);

  if (!session)
    return (
      <p className="text-sm text-slate-400">
        <Link href="/dang-nhap" className="font-semibold text-slate-200 underline underline-offset-2">
          Đăng nhập
        </Link>{" "}
        để làm bài tập mẫu tự chấm.
      </p>
    );
  if (loadState === "loading") return <p className="text-sm text-slate-400">Đang tải bài tập mẫu…</p>;
  if (loadState === "error")
    return <p className="text-sm text-slate-400">Không tải được bài tập mẫu. Thử tải lại trang.</p>;
  if (picks.length === 0) return null;

  return (
    <div className="lesson-sample">
      {picks.map((p, idx) => {
        const st = status[p.key] ?? "doing";
        const active = open === p.key;
        const graded =
          st === "checked" && p.question.type !== "essay"
            ? gradeQuestion(p.question, responses[p.key])
            : null;
        const mark = graded ? (graded.earned === graded.max ? "correct" : "wrong") : st === "revealed" ? "revealed" : null;
        const answered = isAnswered(p.question, responses[p.key]);

        return (
          <div key={p.key} className="lesson-sample-row">
            <button
              type="button"
              onClick={() => setOpen(active ? null : p.key)}
              aria-expanded={active}
              className="lesson-sample-head"
            >
              <span
                className="lesson-sample-num"
                style={active ? { borderColor: color, color } : undefined}
              >
                {idx + 1}
              </span>
              <span className="lesson-sample-label">
                Câu {idx + 1}
                <em>{TYPE_SHORT[p.question.type] ?? "Tự luận"}</em>
              </span>
              {mark && <i className={`lesson-sample-mark is-${mark}`} aria-hidden />}
              <ChevronDown size={16} className={active ? "rotate-180" : ""} />
            </button>
            {active && (
              <div className="lesson-sample-body">
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
                  <div className="lesson-sample-actions">
                    <button
                      type="button"
                      disabled={!answered}
                      onClick={() => setStatus((cur) => ({ ...cur, [p.key]: "checked" }))}
                      style={{ backgroundColor: color }}
                    >
                      Kiểm tra
                    </button>
                    <button
                      type="button"
                      className="is-ghost"
                      onClick={() => setStatus((cur) => ({ ...cur, [p.key]: "revealed" }))}
                    >
                      Chưa làm được, xem lời giải
                    </button>
                    {!answered && <span className="hint">Chọn đáp án trước rồi mới kiểm tra được.</span>}
                  </div>
                ) : (
                  <div className="lesson-sample-actions">
                    <button
                      type="button"
                      className="is-ghost"
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
                    >
                      Làm lại bài này
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
