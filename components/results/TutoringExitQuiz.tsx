"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { X } from "lucide-react";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import TheoryReviewStep from "@/components/results/TheoryReviewStep";
import { useToast } from "@/components/ui/Toast";
import type { ExamQuestion, QuestionResponse } from "@/features/exams/types";
import { emptyResponses, gradeExam, isAnswered, pickRandom } from "@/features/exams/types";
import { fetchBankQuestions, toExamQuestion, type BankQuestion } from "@/services/question-bank";
import {
  EXIT_QUIZ_PASS_PCT,
  EXIT_QUIZ_QUESTION_COUNT,
  EXIT_QUIZ_THEORY_COUNT,
  EXIT_COOLDOWN_HOURS,
  WINDOW_QUIZ_MIX,
  WINDOW_QUIZ_PASS_PCT,
  WINDOW_QUIZ_QUESTION_COUNT,
  fetchSeenQuestionIds,
  fetchTheoryItem,
  fetchTopicFamilyIds,
  logExitAttempt,
  needLabel,
  type ExitWindow,
  type TutoringNeed,
} from "@/services/tutoring";

type Phase = "loading" | "empty" | "review" | "intro" | "running" | "result";

/**
 * Bài cuối buổi (có `exitWindow`): 10 câu cơ cấu 4 dễ / 4 trung bình / 2 khó, ưu tiên câu em chưa gặp,
 * đạt từ 70%, chỉ làm được trong cửa sổ trợ giảng mở. Lượt này được tính vào điểm phụ đạo của trợ giảng.
 */
function pickWindowQuestions(pool: BankQuestion[], seen: Set<number>): BankQuestion[] {
  const fresh = (list: BankQuestion[]) => [
    ...pickRandom(list.filter((q) => !seen.has(q.id)), list.length),
    ...pickRandom(list.filter((q) => seen.has(q.id)), list.length),
  ];
  const levels = ["de", "trung-binh", "kho"] as const;
  const byLevel = new Map(levels.map((lv) => [lv, fresh(pool.filter((q) => q.difficulty === lv))]));
  const picked: BankQuestion[] = [];
  const taken = new Set<number>();
  const take = (q: BankQuestion) => {
    picked.push(q);
    taken.add(q.id);
  };
  for (const lv of levels) (byLevel.get(lv) ?? []).slice(0, WINDOW_QUIZ_MIX[lv]).forEach(take);
  // Thiếu câu ở mức nào thì bù từ phần còn lại (câu chưa gặp trước, kể cả chưa phân loại mức).
  if (picked.length < WINDOW_QUIZ_QUESTION_COUNT) {
    const rest = fresh(pool.filter((q) => !taken.has(q.id)));
    rest.slice(0, WINDOW_QUIZ_QUESTION_COUNT - picked.length).forEach(take);
  }
  return pickRandom(picked, picked.length);
}

const DIFFICULTY_RANK: Record<string, number> = { de: 0, "trung-binh": 1, "": 1, kho: 2 };

/**
 * Bài tự kiểm tra thoát phụ đạo: phần ĐẦU (dễ) lấy từ bộ Kiểm tra nhanh của bài lý thuyết — đúng những câu em vừa
 * xem lại — phần SAU lấy các câu khác trong ngân hàng của chủ đề, xếp dễ → khó. Bài chưa có bộ Kiểm tra nhanh
 * (hoặc ngân hàng ít câu) thì phần thiếu bù từ ngân hàng như cũ.
 */
function pickSelfQuizQuestions(pool: BankQuestion[], theory: BankQuestion[]): { picked: BankQuestion[]; easyCount: number } {
  const easy = pickRandom(
    theory.filter((q) => q.qtype !== "essay"),
    EXIT_QUIZ_THEORY_COUNT,
  );
  const taken = new Set(easy.map((q) => q.id));
  const others = pickRandom(
    pool.filter((q) => !taken.has(q.id)),
    EXIT_QUIZ_QUESTION_COUNT - easy.length,
  ).sort((a, b) => (DIFFICULTY_RANK[a.difficulty] ?? 1) - (DIFFICULTY_RANK[b.difficulty] ?? 1));
  return { picked: [...easy, ...others], easyCount: easy.length };
}

/**
 * Bài ~20 câu bốc ngẫu nhiên từ ngân hàng đúng chủ đề em đang cần phụ đạo — đạt từ 80%
 * thì DB (trigger) tự gỡ mục khỏi tutoring_needs, không cần chờ trợ giảng. Xem
 * docs/supabase-migration-tutoring-exit-quiz.sql.
 */
export default function TutoringExitQuiz({
  need,
  studentId,
  exitWindow,
  onClose,
  onCleared,
}: {
  need: TutoringNeed;
  studentId: string;
  /** Có thì đây là bài kiểm tra cuối buổi do trợ giảng mở (xem pickWindowQuestions). */
  exitWindow?: ExitWindow;
  onClose: () => void;
  onCleared: () => void;
}) {
  const toast = useToast();
  const reduceMotion = useReducedMotion();
  const [phase, setPhase] = useState<Phase>("loading");
  const [bankIds, setBankIds] = useState<number[]>([]);
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [easyCount, setEasyCount] = useState(0);
  const [cur, setCur] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<{ pct: number; passed: boolean; correct: number; total: number } | null>(null);

  const passPct = exitWindow ? WINDOW_QUIZ_PASS_PCT : EXIT_QUIZ_PASS_PCT;
  const theoryHref = need.lessonId ? `/lop-hoc/bai/?id=${need.lessonId}#secondary-stage-ly_thuyet` : null;

  useEffect(() => {
    let cancelled = false;
    const form = need.form === "ly_thuyet" || need.form === "bai_tap" ? need.form : undefined;
    Promise.all([
      fetchTopicFamilyIds(need.topicId).then((topicIds) =>
        Promise.all([
          fetchBankQuestions({ topicIds, form, includeArchived: false }),
          // Bộ Kiểm tra nhanh của bài lý thuyết (bài tự kiểm tra thoát phụ đạo lấy làm phần dễ).
          exitWindow || !need.lessonId
            ? Promise.resolve<BankQuestion[]>([])
            : fetchTheoryItem(need.lessonId)
                .then((t) =>
                  t && t.examIds.length > 0
                    ? fetchBankQuestions({ topicIds, sourceExamIds: t.examIds, includeArchived: false })
                    : [],
                )
                .catch(() => [] as BankQuestion[]),
        ]),
      ),
      exitWindow ? fetchSeenQuestionIds(studentId, need.id).catch(() => new Set<number>()) : Promise.resolve(null),
    ])
      .then(([[rows, theoryRows], seen]) => {
        if (cancelled) return;
        const pool = rows.filter((r) => r.qtype !== "essay");
        let picked: BankQuestion[];
        let easy = 0;
        if (seen) {
          picked = pickWindowQuestions(pool, seen);
        } else {
          ({ picked, easyCount: easy } = pickSelfQuizQuestions(pool, theoryRows));
        }
        setEasyCount(easy);
        setBankIds(picked.map((b) => b.id));
        const examQuestions = picked.map(toExamQuestion);
        setQuestions(examQuestions);
        setResponses(emptyResponses(examQuestions));
        // Tự kiểm tra: xem lại lý thuyết trước (bước này tự bỏ qua nếu chủ đề không có bài lý thuyết).
        setPhase(examQuestions.length === 0 ? "empty" : exitWindow ? "intro" : "review");
      })
      .catch(() => {
        if (!cancelled) setPhase("empty");
      });
    return () => {
      cancelled = true;
    };
  }, [need.topicId, need.form, need.id, need.lessonId, studentId, exitWindow]);

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
        windowId: exitWindow?.id,
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

  const wide = phase === "running" || phase === "review";

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
          className={`max-h-[90vh] w-full overflow-y-auto rounded-2xl border border-line bg-panel p-5 shadow-2xl sm:p-6 ${
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
            <h2 className="font-display text-lg font-semibold text-ink">
              {exitWindow ? "Kiểm tra cuối buổi phụ đạo" : "Tự kiểm tra thoát phụ đạo"}
            </h2>
            <button type="button" onClick={onClose} aria-label="Đóng" className="text-muted hover:text-primary">
              <X size={18} />
            </button>
          </div>

          {phase === "loading" && <p className="text-sm text-muted">Đang soạn câu hỏi…</p>}

          {phase === "empty" && (
            <div className="space-y-4">
              <p className="text-sm text-ink">
                Ngân hàng câu hỏi chưa có câu nào cho <strong className="text-ink">{needLabel(need)}</strong>. Em
                đăng ký buổi phụ đạo bên dưới nhé.
              </p>
              <Button variant="outline" onClick={onClose} className="w-full">
                Đóng
              </Button>
            </div>
          )}

          {phase === "review" && <TheoryReviewStep need={need} onReady={() => setPhase("intro")} />}

          {phase === "intro" && (
            <div className="space-y-4">
              <p className="text-sm text-ink">
                <strong className="text-ink">{needLabel(need)}</strong> · {questions.length} câu · cần đạt từ{" "}
                {passPct}%.
              </p>
              <p className="text-xs text-slate-500">
                {exitWindow
                  ? "Em tự làm một mình, một lượt duy nhất cho chủ đề này trong buổi. Kết quả giúp thầy cô biết buổi phụ đạo có hiệu quả không."
                  : easyCount > 0
                    ? `${easyCount} câu đầu (dễ) lấy từ bộ Kiểm tra nhanh của bài em vừa xem lại; các câu sau lấy từ ngân hàng, xếp từ dễ đến khó.`
                    : "Câu hỏi lấy ngẫu nhiên từ ngân hàng, xếp từ dễ đến khó, mỗi lượt một bộ khác nhau."}
              </p>
              <Button onClick={() => setPhase("running")} className="w-full">
                Bắt đầu làm bài
              </Button>
            </div>
          )}

          {phase === "running" && (
            <div className="space-y-4">
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-semibold text-ink">
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
                <p className="text-3xl font-bold text-ink">{result.pct}%</p>
                <p className="mt-1 text-sm text-ink">
                  Đúng {result.correct}/{result.total} câu
                </p>
              </div>
              {result.passed ? (
                <p className="text-sm text-emerald-200">Đạt yêu cầu — chủ đề này đã được mở khoá. Em đã phục hồi!</p>
              ) : (
                <div className="space-y-2 text-sm text-amber-200">
                  <p>
                    {exitWindow
                      ? `Chưa đạt ${passPct}% — chưa sao cả. Em nhờ trợ giảng giảng lại phần còn vướng; chủ đề này vẫn còn trong danh sách của em.`
                      : `Chưa đạt ${passPct}% — chưa sao cả. Ôn lại đúng phần lý thuyết của chủ đề này, sau ${EXIT_COOLDOWN_HOURS} giờ em xem lại lý thuyết rồi thử lượt mới nhé.`}
                  </p>
                  {theoryHref && (
                    <a href={theoryHref} className="inline-block font-semibold text-primary underline-offset-2 hover:underline">
                      Ôn lại đoạn lý thuyết →
                    </a>
                  )}
                </div>
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
