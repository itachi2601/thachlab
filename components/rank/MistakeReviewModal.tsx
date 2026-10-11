"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { X, Sparkles, CheckCircle2, XCircle, ArrowRight, ArrowLeft } from "lucide-react";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import { useToast } from "@/components/ui/Toast";
import type { ExamQuestion, QuestionResponse } from "@/features/exams/types";
import { emptyResponses, isAnswered } from "@/features/exams/types";
import {
  startMistakeReviewQuiz,
  submitMistakeReviewQuiz,
  type MistakeQuizStart,
  type MistakeQuizSubmitResult,
} from "@/services/mistakes";
import ContentHtml from "@/components/exams/ContentHtml";

interface MistakeReviewModalProps {
  onClose: () => void;
  onFinished?: () => void;
}

export default function MistakeReviewModal({ onClose, onFinished }: MistakeReviewModalProps) {
  const reduceMotion = useReducedMotion();
  const toast = useToast();

  const [loading, setLoading] = useState(true);
  const [quizStart, setQuizStart] = useState<MistakeQuizStart | null>(null);
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [cur, setCur] = useState(0);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<MistakeQuizSubmitResult | null>(null);

  useEffect(() => {
    let cancelled = false;
    startMistakeReviewQuiz(5)
      .then((data) => {
        if (cancelled) return;
        if (!data.ok || !data.questions || data.questions.length === 0) {
          setQuizStart({ ok: false, attempt_id: 0, total: 0, questions: [] });
          setLoading(false);
          return;
        }
        setQuizStart(data);
        const mappedQuestions: ExamQuestion[] = data.questions.map((q) => {
          if (q.type === "multiple_choice") {
            return {
              type: "multiple_choice",
              question: q.question,
              options: q.options || [],
              answer: 0,
              explanation: "",
            };
          }
          if (q.type === "true_false") {
            return {
              type: "true_false",
              question: q.question,
              statements: (q.statements || []).map((s) => ({ text: s.text, answer: true })),
              explanation: "",
            };
          }
          return {
            type: "short_answer",
            question: q.question,
            answer: "",
            explanation: "",
          };
        });
        setQuestions(mappedQuestions);
        setResponses(emptyResponses(mappedQuestions));
        setLoading(false);
      })
      .catch((err) => {
        if (cancelled) return;
        toast("error", err instanceof Error ? err.message : "Không tải được bài ôn tập");
        setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [toast]);

  const total = questions.length;
  const answeredCount = questions.filter((q, i) => isAnswered(q, responses[i])).length;

  async function handleSubmit() {
    if (!quizStart || submitting) return;
    setSubmitting(true);
    try {
      const respMap: Record<string, unknown> = {};
      quizStart.questions.forEach((q, i) => {
        respMap[q.mistake_id.toString()] = responses[i];
      });

      const res = await submitMistakeReviewQuiz(quizStart.attempt_id, respMap);
      setResult(res);
      onFinished?.();
    } catch (err) {
      toast("error", err instanceof Error ? err.message : "Lỗi khi nộp bài ôn");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-3 sm:p-4"
    >
      <div className="relative flex max-h-[90vh] w-full max-w-2xl flex-col rounded-3xl border border-line bg-panel shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-line px-5 py-4 sm:px-6">
          <div className="flex items-center gap-2.5">
            <span className="flex h-8 w-8 items-center justify-center rounded-xl bg-amber-500/10 text-amber-500">
              <Sparkles className="h-4 w-4" />
            </span>
            <div>
              <h2 className="text-base font-semibold text-ink">Xoá bẫy Vật lí (Ôn câu sai)</h2>
              <p className="text-xs text-muted">Lặp lại ngắt quãng để khắc sâu bài học</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Đóng"
            className="flex h-11 w-11 items-center justify-center rounded-full text-muted hover:bg-panel-soft hover:text-ink"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-5 py-5 sm:px-6">
          {loading ? (
            <div className="flex h-48 items-center justify-center text-sm text-muted">
              Đang chuẩn bị câu hỏi đến hạn ôn…
            </div>
          ) : !quizStart?.ok || total === 0 ? (
            <div className="flex flex-col items-center justify-center py-10 text-center">
              <span className="mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-500/10 text-emerald-500">
                <CheckCircle2 className="h-6 w-6" />
              </span>
              <h3 className="text-base font-semibold text-ink">Chưa có câu nào đến hạn ôn!</h3>
              <p className="mt-1 max-w-sm text-xs text-muted">
                Em đã xử lý sạch sẽ các câu sai cần ôn đợt này. Hãy tiếp tục làm bài kiểm tra và quay lại khi đến lịch nhé.
              </p>
              <Button type="button" variant="primary" onClick={onClose} className="mt-5 min-h-11 px-6">
                Tuyệt vời, quay lại
              </Button>
            </div>
          ) : result ? (
            /* Result View */
            <div className="space-y-6">
              <div className="rounded-2xl border border-line bg-panel-soft p-5 text-center">
                <p className="text-xs font-medium uppercase tracking-wider text-muted">Kết quả phiên ôn tập</p>
                <div className="mt-2 text-3xl font-bold text-ink">
                  Đúng {result.correct} / {result.total} câu
                </div>
                {result.rp_awarded > 0 && (
                  <div className="mt-2.5 inline-flex items-center gap-1.5 rounded-full bg-amber-500/10 px-3.5 py-1 text-xs font-semibold text-amber-500">
                    <Sparkles className="h-3.5 w-3.5" />
                    +{result.rp_awarded} RP thưởng nỗ lực
                  </div>
                )}
              </div>

              {/* Review details */}
              <div className="space-y-4">
                <h4 className="text-sm font-semibold text-ink">Chi tiết từng câu:</h4>
                {result.results.map((r, i) => {
                  const q = questions[i];
                  return (
                    <div
                      key={r.mistake_id}
                      className={`rounded-2xl border p-4 text-xs ${
                        r.correct
                          ? "border-emerald-500/30 bg-emerald-500/5"
                          : "border-rose-500/30 bg-rose-500/5"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        {r.correct ? (
                          <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                        ) : (
                          <XCircle className="h-4 w-4 text-rose-500" />
                        )}
                        <span className="font-semibold text-ink">Câu {i + 1}: {r.correct ? "Chính xác" : "Chưa đúng"}</span>
                      </div>
                      <div className="mt-2.5 text-ink">
                        <ContentHtml html={q.question} />
                      </div>
                      {r.explanation && (
                        <div className="mt-3 rounded-xl border border-line bg-panel p-3 text-[13px] text-muted">
                          <strong className="text-ink">Giải thích: </strong>
                          <ContentHtml html={r.explanation} />
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            /* Quiz Active View */
            <div className="space-y-5">
              <div className="flex items-center justify-between text-xs text-muted">
                <span>
                  Câu <strong className="text-ink">{cur + 1}</strong> / {total}
                </span>
                <span>
                  Đã làm: <strong className="text-ink">{answeredCount}</strong>/{total}
                </span>
              </div>

              <div className="h-1.5 w-full overflow-hidden rounded-full bg-line">
                <div
                  className="h-full bg-primary transition-all duration-300"
                  style={{ width: `${((cur + 1) / total) * 100}%` }}
                />
              </div>

              <AnimatePresence mode="wait">
                <motion.div
                  key={cur}
                  initial={reduceMotion ? { opacity: 1 } : { opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={reduceMotion ? { opacity: 0 } : { opacity: 0, x: -10 }}
                  transition={{ duration: 0.2 }}
                >
                  <QuestionCard
                    index={cur + 1}
                    question={questions[cur]}
                    response={responses[cur]}
                    onChange={(val) => {
                      const next = [...responses];
                      next[cur] = val;
                      setResponses(next);
                    }}
                  />
                </motion.div>
              </AnimatePresence>
            </div>
          )}
        </div>

        {/* Footer */}
        {!loading && quizStart?.ok && !result && total > 0 && (
          <div className="flex items-center justify-between border-t border-line px-5 py-4 sm:px-6">
            <Button
              type="button"
              variant="outline"
              disabled={cur === 0}
              onClick={() => setCur((c) => Math.max(0, c - 1))}
              className="min-h-11 px-4 text-xs font-semibold"
            >
              <ArrowLeft className="mr-1.5 h-4 w-4" /> Câu trước
            </Button>

            {cur < total - 1 ? (
              <Button
                type="button"
                variant="primary"
                onClick={() => setCur((c) => Math.min(total - 1, c + 1))}
                className="min-h-11 px-4 text-xs font-semibold"
              >
                Câu sau <ArrowRight className="ml-1.5 h-4 w-4" />
              </Button>
            ) : (
              <Button
                type="button"
                variant="primary"
                disabled={submitting}
                onClick={handleSubmit}
                className="min-h-11 px-5 text-xs font-semibold"
              >
                {submitting ? "Đang chấm…" : "Nộp bài ôn"}
              </Button>
            )}
          </div>
        )}

        {result && (
          <div className="flex justify-end border-t border-line px-5 py-4 sm:px-6">
            <Button type="button" variant="primary" onClick={onClose} className="min-h-11 px-6 text-xs font-semibold">
              Hoàn thành
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
