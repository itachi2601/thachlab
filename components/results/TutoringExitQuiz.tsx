"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { X } from "lucide-react";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import { useToast } from "@/components/ui/Toast";
import type { ExamQuestion, QuestionResponse } from "@/features/exams/types";
import { emptyResponses, gradeExam, isAnswered, pickRandom } from "@/features/exams/types";
import { fetchBankQuestions, toExamQuestion, type BankQuestion } from "@/services/question-bank";
import {
  EXIT_QUIZ_PASS_PCT,
  EXIT_QUIZ_QUESTION_COUNT,
  MAX_EXIT_ATTEMPTS,
  logExitAttempt,
  needLabel,
  type TutoringNeed,
} from "@/services/tutoring";

type Phase = "loading" | "empty" | "intro" | "running" | "result";

/**
 * Bài ~20 câu bốc ngẫu nhiên từ ngân hàng đúng chủ đề em đang cần phụ đạo — đạt từ 80%
 * thì DB (trigger) tự gỡ mục khỏi tutoring_needs, không cần chờ trợ giảng. Xem
 * docs/supabase-migration-tutoring-exit-quiz.sql.
 */
export default function TutoringExitQuiz({
  need,
  studentId,
  attemptsUsed,
  onClose,
  onCleared,
}: {
  need: TutoringNeed;
  studentId: string;
  attemptsUsed: number;
  onClose: () => void;
  onCleared: () => void;
}) {
  const toast = useToast();
  const reduceMotion = useReducedMotion();
  const [phase, setPhase] = useState<Phase>("loading");
  const [bankIds, setBankIds] = useState<number[]>([]);
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [cur, setCur] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<{ pct: number; passed: boolean; correct: number; total: number } | null>(null);

  const attemptsLeft = Math.max(0, MAX_EXIT_ATTEMPTS - attemptsUsed);

  useEffect(() => {
    let cancelled = false;
    const form = need.form === "ly_thuyet" || need.form === "bai_tap" ? need.form : undefined;
    fetchBankQuestions({ topicIds: [need.topicId], form, includeArchived: false })
      .then((rows) => {
        if (cancelled) return;
        const pool = rows.filter((r) => r.qtype !== "essay");
        const picked: BankQuestion[] = pickRandom(pool, EXIT_QUIZ_QUESTION_COUNT);
        setBankIds(picked.map((b) => b.id));
        const examQuestions = picked.map(toExamQuestion);
        setQuestions(examQuestions);
        setResponses(emptyResponses(examQuestions));
        setPhase(examQuestions.length === 0 ? "empty" : "intro");
      })
      .catch(() => {
        if (!cancelled) setPhase("empty");
      });
    return () => {
      cancelled = true;
    };
  }, [need.topicId, need.form]);

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
    setSubmitting(true);
    try {
      const summary = gradeExam(questions, responses);
      const attempt = await logExitAttempt({
        tutoringNeedId: need.id,
        studentId,
        questionIds: bankIds,
        total: questions.length,
        correct: summary.correctCount,
      });
      setResult({ pct: attempt.pct, passed: attempt.passed, correct: summary.correctCount, total: questions.length });
      setPhase("result");
      if (attempt.passed) {
        toast("success", `Đạt ${attempt.pct}% — đã gỡ khỏi danh sách cần phụ đạo!`);
        onCleared();
      }
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
            <h2 className="font-display text-lg font-semibold text-white">Tự kiểm tra thoát phụ đạo</h2>
            <button type="button" onClick={onClose} aria-label="Đóng" className="text-slate-400 hover:text-white">
              <X size={18} />
            </button>
          </div>

          {phase === "loading" && <p className="text-sm text-slate-400">Đang soạn câu hỏi…</p>}

          {phase === "empty" && (
            <div className="space-y-4">
              <p className="text-sm text-slate-300">
                Ngân hàng câu hỏi chưa có câu nào cho <strong className="text-white">{needLabel(need)}</strong>. Em
                đăng ký buổi phụ đạo bên dưới nhé.
              </p>
              <Button variant="outline" onClick={onClose} className="w-full">
                Đóng
              </Button>
            </div>
          )}

          {phase === "intro" && (
            <div className="space-y-4">
              <p className="text-sm text-slate-300">
                <strong className="text-white">{needLabel(need)}</strong> · {questions.length} câu · cần đạt từ{" "}
                {EXIT_QUIZ_PASS_PCT}% · còn {attemptsLeft} lượt.
              </p>
              <p className="text-xs text-slate-500">Câu hỏi lấy ngẫu nhiên từ ngân hàng, mỗi lượt một bộ khác nhau.</p>
              <Button onClick={() => setPhase("running")} className="w-full">
                Bắt đầu làm bài
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

              <QuestionCard
                index={cur + 1}
                question={questions[cur]}
                response={responses[cur]}
                onChange={(r) => setResponse(cur, r)}
              />

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
                <p className="text-sm text-emerald-200">Đạt yêu cầu — chủ đề này đã được gỡ khỏi danh sách cần phụ đạo.</p>
              ) : (
                <p className="text-sm text-amber-200">
                  {attemptsLeft - 1 > 0
                    ? `Chưa đạt ${EXIT_QUIZ_PASS_PCT}% — em còn ${attemptsLeft - 1} lượt, ôn lại rồi thử tiếp nhé.`
                    : "Đã hết lượt tự kiểm tra cho chủ đề này — em đăng ký buổi phụ đạo bên dưới nhé."}
                </p>
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
