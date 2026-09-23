"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { X } from "lucide-react";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import { useToast } from "@/components/ui/Toast";
import type { QuestionResponse } from "@/features/exams/types";
import { emptyResponses, gradeExam, isAnswered } from "@/features/exams/types";
import type { FixQuizResult, FixQuizStart, FixableTopic } from "@/features/rank/types";
import { startFixQuiz, submitFixQuiz } from "@/services/rank";

type Phase = "loading" | "error" | "intro" | "running" | "result";

/**
 * Sửa sai để nhận RP: bài ngắn bốc từ ngân hàng cùng chủ đề, loại câu đã gặp trong đề gốc
 * (RPC rank_fix_quiz_start chọn câu và kiểm điều kiện phía DB). Chấm ở client như mọi đề khác,
 * DB tính pct/đạt và cộng RP theo tỉ lệ chủ đề đã sửa (rank_fix_quiz_submit).
 */
export default function FixQuizModal({
  resultId,
  topic,
  onClose,
  onDone,
}: {
  resultId: number;
  topic: FixableTopic;
  onClose: () => void;
  onDone: (result: FixQuizResult) => void;
}) {
  const toast = useToast();
  const reduceMotion = useReducedMotion();
  const [phase, setPhase] = useState<Phase>("loading");
  const [quiz, setQuiz] = useState<FixQuizStart | null>(null);
  const [errorMsg, setErrorMsg] = useState("");
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [cur, setCur] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<(FixQuizResult & { correct: number; total: number }) | null>(null);

  useEffect(() => {
    let cancelled = false;
    startFixQuiz(resultId, topic.topicId)
      .then((q) => {
        if (cancelled) return;
        setQuiz(q);
        setResponses(emptyResponses(q.questions));
        setPhase(q.questions.length === 0 ? "error" : "intro");
        if (q.questions.length === 0) setErrorMsg("Ngân hàng chưa đủ câu tương đương cho chủ đề này.");
      })
      .catch((e) => {
        if (cancelled) return;
        setErrorMsg(e instanceof Error ? e.message : "Chưa mở được bài sửa sai.");
        setPhase("error");
      });
    return () => {
      cancelled = true;
    };
  }, [resultId, topic.topicId]);

  const questions = quiz?.questions ?? [];
  const lastIndex = questions.length - 1;
  const answeredCount = questions.filter((q, i) => isAnswered(q, responses[i])).length;

  function setResponse(i: number, r: QuestionResponse) {
    setResponses((prev) => {
      const next = [...prev];
      next[i] = r;
      return next;
    });
  }

  async function submit() {
    if (!quiz) return;
    setSubmitting(true);
    try {
      const summary = gradeExam(questions, responses);
      const r = await submitFixQuiz(quiz.attemptId, summary.correctCount);
      setResult({ ...r, correct: summary.correctCount, total: questions.length });
      setPhase("result");
      if (r.rpDelta > 0) toast("success", `+${r.rpDelta} RP sửa sai!`);
      onDone(r);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa nộp được, thử lại nhé.");
    } finally {
      setSubmitting(false);
    }
  }

  const wide = phase === "running";

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-100 flex items-center justify-center bg-black/60 px-4 py-6 backdrop-blur-sm"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: reduceMotion ? 0 : 0.15 }}
        onClick={onClose}
        role="presentation"
      >
        <motion.div
          className={`max-h-[90vh] w-full overflow-y-auto rounded-2xl border border-white/10 bg-panel p-5 shadow-2xl sm:p-6 ${
            wide ? "max-w-2xl" : "max-w-sm"
          }`}
          initial={{ opacity: 0, scale: reduceMotion ? 1 : 0.96, y: reduceMotion ? 0 : 8 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: reduceMotion ? 1 : 0.96, y: reduceMotion ? 0 : 8 }}
          transition={{ duration: reduceMotion ? 0 : 0.18, ease: "easeOut" }}
          onClick={(e) => e.stopPropagation()}
          role="dialog"
          aria-modal="true"
        >
          <div className="mb-3 flex items-start justify-between gap-3">
            <h2 className="font-display text-lg font-semibold text-white">Sửa sai để nhận RP</h2>
            <button type="button" onClick={onClose} aria-label="Đóng" className="text-slate-400 hover:text-white">
              <X size={18} />
            </button>
          </div>

          {phase === "loading" && <p className="text-sm text-slate-400">Đang soạn câu hỏi tương đương…</p>}

          {phase === "error" && (
            <div className="space-y-4">
              <p className="text-sm text-slate-300">{errorMsg}</p>
              <Button variant="outline" onClick={onClose} className="w-full">
                Đóng
              </Button>
            </div>
          )}

          {phase === "intro" && quiz && (
            <div className="space-y-4">
              <p className="text-sm text-slate-300">
                <strong className="text-white">{quiz.topicName}</strong> · {quiz.total} câu · cần đạt từ {quiz.passPct}% · còn{" "}
                {quiz.attemptsLeft} lượt.
              </p>
              <p className="text-xs text-slate-500">
                Câu hỏi khác với đề em đã làm, cùng chủ đề. Đạt là chủ đề này được tính đã sửa.
              </p>
              <Button onClick={() => setPhase("running")} className="w-full">
                Bắt đầu
              </Button>
            </div>
          )}

          {phase === "running" && (
            <div className="space-y-4">
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-semibold text-white">
                  Câu {cur + 1}/{questions.length}
                </p>
                <p className="text-xs text-slate-500">
                  Đã trả lời {answeredCount}/{questions.length}
                </p>
              </div>
              <QuestionCard index={cur + 1} question={questions[cur]} response={responses[cur]} onChange={(r) => setResponse(cur, r)} />
              <div className="flex items-center justify-between gap-2">
                <Button variant="outline" onClick={() => setCur((i) => Math.max(0, i - 1))} disabled={cur === 0}>
                  Câu trước
                </Button>
                {cur < lastIndex ? (
                  <Button onClick={() => setCur((i) => Math.min(lastIndex, i + 1))}>Câu tiếp</Button>
                ) : (
                  <Button onClick={submit} disabled={submitting}>
                    {submitting ? "Đang nộp…" : "Nộp bài"}
                  </Button>
                )}
              </div>
            </div>
          )}

          {phase === "result" && result && (
            <div className="space-y-4">
              <div
                className={`rounded-xl border p-4 text-center ${
                  result.passed ? "border-emerald-500/40 bg-emerald-500/10" : "border-amber-500/40 bg-amber-500/10"
                }`}
              >
                <p className="text-3xl font-bold text-white">{result.pct}%</p>
                <p className="mt-1 text-sm text-slate-300">
                  Đúng {result.correct}/{result.total} câu
                </p>
              </div>
              {result.passed ? (
                <p className="text-sm text-emerald-200">
                  Đã sửa xong chủ đề này ({result.fixedTopics}/{result.wrongTopics} chủ đề của bài).
                  {result.rpDelta > 0 ? ` +${result.rpDelta} RP.` : " RP sửa sai của bài này đã nhận đủ."}
                </p>
              ) : (
                <p className="text-sm text-amber-200">Chưa đạt — ôn lại rồi thử lượt khác nhé.</p>
              )}
              <Button variant="outline" onClick={onClose} className="w-full">
                Đóng
              </Button>
            </div>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
