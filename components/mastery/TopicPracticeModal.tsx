"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { X } from "lucide-react";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import type { PracticePick } from "@/services/lessons";
import { fetchExamsFull, savePracticeSession } from "@/services/lessons";
import type { Exam, QuestionResponse } from "@/features/exams/types";
import { emptyResponses, gradeExam, isAnswered, pickRandom } from "@/features/exams/types";

type Phase = "loading" | "empty" | "intro" | "running" | "done";

const COUNT = 10;

/**
 * "Luyện 10 câu phần này" từ thẻ mastery (components/mastery/LessonMasteryCard.tsx) — bốc tối đa
 * 10 câu cùng YCCĐ (khớp theo tên `topicName`, đúng cách `exams.questions[].topic` được gắn khi
 * đăng đề) từ CHÍNH các đề đã gắn vào bài học đang xem (`examIds`, học sinh đã có quyền đọc qua
 * cách trang bài học vẫn dùng — không cần RLS/RPC mới cho `question_bank`).
 *
 * Cố tình TÁI DÙNG plumbing "luyện tập" hiện có thay vì viết luồng mới:
 * - `fetchExamsFull` (services/lessons.ts) — đúng hàm PracticeSession.tsx đang dùng để tải câu hỏi.
 * - `gradeExam`/`emptyResponses`/`isAnswered`/`pickRandom` (features/exams/types.ts).
 * - `savePracticeSession` (services/lessons.ts) — ghi practice_sessions + practice_question_results,
 *   NHỜ VẬY lượt luyện này cũng tự động tính vào 10 lượt gần nhất của lần tính mastery kế tiếp.
 * - `QuestionCard` — cùng UI trả lời câu hỏi với ExamRunner/PracticeSession/FixQuizModal.
 *
 * KHÔNG dùng `rank_fix_quiz_start`/`FixQuizModal` (components/rank/FixQuizModal.tsx): hàm đó cần
 * một `exam_result_id` có thật + mùa rank đang mở + đề là nguồn RP, và bốc theo topic TẦNG BÀI
 * (coalesce parent_id) chứ không theo đúng YCCĐ — không khớp ngữ cảnh "cuối bài học"/"sau khi nộp
 * luyện tập" (không phải lúc nào cũng có exam_result). Không dùng select thẳng `question_bank` lọc
 * `topic_id` vì RLS bảng đó chỉ mở cho học sinh qua đúng 1 policy hẹp gắn với `tutoring_needs`
 * đang mở — nới thêm sẽ phạm luật "không nới RLS".
 */
export default function TopicPracticeModal({
  lessonId,
  examIds,
  topicName,
  onClose,
  onFinished,
}: {
  lessonId: number;
  examIds: number[];
  topicName: string;
  onClose: () => void;
  onFinished?: () => void;
}) {
  const { session } = useAuth();
  const toast = useToast();
  const reduceMotion = useReducedMotion();
  const [phase, setPhase] = useState<Phase>("loading");
  const [picks, setPicks] = useState<PracticePick[]>([]);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [cur, setCur] = useState(0);
  const [saving, setSaving] = useState(false);
  const [result, setResult] = useState<{ score10: number; correctCount: number; total: number } | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const metas = await fetchExamsFull(examIds);
        if (cancelled) return;
        const pool: PracticePick[] = [];
        for (const id of examIds) {
          const exam = metas.get(id) as Exam | undefined;
          if (!exam) continue;
          exam.questions.forEach((question, qi) => {
            if (question.type === "essay") return;
            if ((question.topic ?? "").trim() !== topicName.trim()) return;
            pool.push({ question, examId: exam.id, sourceIndex: qi });
          });
        }
        const chosen = pickRandom(pool, Math.min(COUNT, pool.length));
        setPicks(chosen);
        setResponses(emptyResponses(chosen.map((p) => p.question)));
        setPhase(chosen.length === 0 ? "empty" : "intro");
      } catch {
        if (!cancelled) setPhase("empty");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [examIds, topicName]);

  const questions = picks.map((p) => p.question);
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
    if (!session || picks.length === 0) return;
    setSaving(true);
    try {
      const summary = gradeExam(questions, responses);
      await savePracticeSession({
        studentId: session.user.id,
        lessonId,
        itemId: null,
        picks,
        responses,
        score10: summary.score10,
        correctCount: summary.correctCount,
        durationSeconds: 0,
        timedOut: false,
        clientToken: crypto.randomUUID(),
      });
      setResult({ score10: summary.score10, correctCount: summary.correctCount, total: questions.length });
      setPhase("done");
      onFinished?.();
    } catch {
      toast("error", "Chưa lưu được kết quả, thử lại nhé.");
    } finally {
      setSaving(false);
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
            <h2 className="font-display text-lg font-semibold text-white">Luyện thêm: {topicName}</h2>
            <button type="button" onClick={onClose} aria-label="Đóng" className="text-slate-400 hover:text-white">
              <X size={18} />
            </button>
          </div>

          {phase === "loading" && <p className="text-sm text-slate-400">Đang soạn câu hỏi…</p>}

          {phase === "empty" && (
            <div className="space-y-4">
              <p className="text-sm text-slate-300">
                Chưa có đủ câu hỏi cho yêu cầu này trong các đề của bài học. Hãy hỏi thầy/cô nhé.
              </p>
              <Button variant="outline" onClick={onClose} className="w-full">
                Đóng
              </Button>
            </div>
          )}

          {phase === "intro" && (
            <div className="space-y-4">
              <p className="text-sm text-slate-300">
                <strong className="text-white">{topicName}</strong> · {questions.length} câu bốc ngẫu nhiên từ
                các đề của bài học.
              </p>
              <p className="text-xs text-slate-500">Làm xong sẽ tính vào mức độ thành thạo của em ở phần này.</p>
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
                  <Button onClick={submit} disabled={saving}>
                    {saving ? "Đang nộp…" : "Nộp bài"}
                  </Button>
                )}
              </div>
            </div>
          )}

          {phase === "done" && result && (
            <div className="space-y-4">
              <div
                className={`rounded-xl border p-4 text-center ${
                  result.correctCount === result.total
                    ? "border-emerald-500/40 bg-emerald-500/10"
                    : "border-amber-500/40 bg-amber-500/10"
                }`}
              >
                <p className="text-3xl font-bold text-white">{result.score10.toFixed(2)}</p>
                <p className="mt-1 text-sm text-slate-300">
                  Đúng {result.correctCount}/{result.total} câu
                </p>
              </div>
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
