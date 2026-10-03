"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { CheckCircle2, CircleAlert, X } from "lucide-react";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import { useToast } from "@/components/ui/Toast";
import type { ExamQuestion, QuestionResponse } from "@/features/exams/types";
import { emptyResponses, isAnswered } from "@/features/exams/types";
import {
  GATE_LEVEL_LABELS,
  formatGateWhen,
  tierMeta,
  type GateQuestion,
  type GateResult,
  type GateStart,
  type RankGate,
} from "@/features/rank/types";
import { answerGateQuiz, startGateQuiz } from "@/services/rank";

type Phase = "loading" | "error" | "intro" | "running" | "result";

/** QuestionCard cần đủ shape ExamQuestion; ở chế độ làm bài nó không đọc `answer`/`explanation`, nên điền giá trị rỗng. */
function toExamQuestion(q: GateQuestion): ExamQuestion {
  if (q.type === "multiple_choice") return { type: "multiple_choice", question: q.question, options: q.options, answer: -1, explanation: "" };
  if (q.type === "true_false") {
    return { type: "true_false", question: q.question, statements: q.statements.map((s) => ({ text: s.text, answer: false })), explanation: "" };
  }
  return { type: "short_answer", question: q.question, answer: "", explanation: "" };
}

/**
 * Thi thăng hạng thích ứng (rank_gate_start / rank_gate_answer — migration 20261003100000).
 * Khung chép từ FixQuizModal. Khác: mỗi câu gửi lên server rồi mới nhận câu sau (server chọn độ khó và chấm),
 * KHÔNG hiện đúng/sai trong lúc thi (đây là bài đo, không phải bài luyện), không đồng hồ đếm ngược.
 * Quy tắc: N1 một câu/màn, D2 đích chạm ≥ 44px, D3 nút chính ở đáy trong tầm ngón cái, L3 phần thưởng chỉ hiện
 * ở màn kết quả, L4 lời phản hồi hướng việc tiếp theo, M4 trạng thái có icon + chữ, B4 không chuyển động giữa bài.
 */
export default function GateQuizModal({
  tierCode,
  gate,
  onClose,
  onDone,
}: {
  tierCode: string;
  /** Điều kiện của bậc kế (từ rank_status_of) — hiện ở màn giới thiệu. */
  gate: RankGate;
  onClose: () => void;
  /** Gọi sau khi chốt lượt để trang tải lại trạng thái (đỗ → bậc đổi ngay). */
  onDone: (result: GateResult) => void;
}) {
  const toast = useToast();
  const reduceMotion = useReducedMotion();
  const [phase, setPhase] = useState<Phase>("loading");
  const [start, setStart] = useState<GateStart | null>(null);
  const [errorMsg, setErrorMsg] = useState("");
  const [question, setQuestion] = useState<GateQuestion | null>(null);
  const [index, setIndex] = useState(0);
  const [response, setResponse] = useState<QuestionResponse>(null);
  const [sending, setSending] = useState(false);
  const [result, setResult] = useState<GateResult | null>(null);

  useEffect(() => {
    let cancelled = false;
    startGateQuiz(tierCode)
      .then((s) => {
        if (cancelled) return;
        setStart(s);
        setQuestion(s.question);
        setIndex(s.index);
        setResponse(emptyResponses([toExamQuestion(s.question)])[0]);
        setPhase("intro");
      })
      .catch((e) => {
        if (cancelled) return;
        setErrorMsg(e instanceof Error ? e.message : "Chưa mở được bài thi thăng hạng.");
        setPhase("error");
      });
    return () => {
      cancelled = true;
    };
  }, [tierCode]);

  const exam = question ? toExamQuestion(question) : null;
  const total = start?.total ?? 0;
  const canSend = !!exam && isAnswered(exam, response) && !sending;
  const targetName = tierMeta(tierCode).name;

  async function send() {
    if (!question || !start || !canSend) return;
    setSending(true);
    try {
      const out = await answerGateQuiz(start.attemptId, response, question.qid);
      if (out.done) {
        setResult(out.result);
        setPhase("result");
        onDone(out.result);
      } else {
        setQuestion(out.next);
        setIndex(out.index);
        setResponse(emptyResponses([toExamQuestion(out.next)])[0]);
      }
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa gửi được câu trả lời, thử lại nhé.");
    } finally {
      setSending(false);
    }
  }

  const running = phase === "running";
  const pctDone = total > 0 ? Math.round((index / total) * 100) : 0;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-100 flex items-center justify-center bg-black/60 px-3 py-4 backdrop-blur-sm sm:px-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: reduceMotion ? 0 : 0.15 }}
        // Đang làm bài: bấm ra ngoài không đóng (tránh mất câu đang chọn); dùng nút X.
        onClick={running ? undefined : onClose}
        role="presentation"
      >
        <motion.div
          className={`flex max-h-[92vh] w-full flex-col rounded-2xl border border-white/10 bg-panel shadow-2xl ${running ? "max-w-2xl" : "max-w-sm"}`}
          initial={{ opacity: 0, scale: reduceMotion ? 1 : 0.96, y: reduceMotion ? 0 : 8 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: reduceMotion ? 1 : 0.96, y: reduceMotion ? 0 : 8 }}
          transition={{ duration: reduceMotion ? 0 : 0.18, ease: "easeOut" }}
          onClick={(e) => e.stopPropagation()}
          role="dialog"
          aria-modal="true"
          aria-label={`Thi thăng hạng lên ${targetName}`}
        >
          <div className="flex shrink-0 items-start justify-between gap-3 px-4 pt-4 sm:px-6 sm:pt-5">
            <h2 className="font-display text-lg font-semibold text-white">Thi thăng hạng · {targetName}</h2>
            <button
              type="button"
              onClick={onClose}
              aria-label={running ? "Tạm dừng, em vào thi tiếp sau" : "Đóng"}
              className="-mr-2 -mt-1 flex h-11 w-11 items-center justify-center rounded-full text-slate-400 hover:bg-white/5 hover:text-white"
            >
              <X size={20} />
            </button>
          </div>

          <div className="min-h-0 flex-1 overflow-y-auto px-4 pb-4 pt-2 sm:px-6">
            {phase === "loading" && <p className="text-base text-slate-300">Đang soạn bài thi…</p>}

            {phase === "error" && <p className="text-base leading-relaxed text-slate-200">{errorMsg}</p>}

            {phase === "intro" && start && (
              <div className="space-y-3 text-base leading-relaxed text-slate-200">
                <p>
                  <strong className="text-white">{start.total} câu</strong>, độ khó tự điều chỉnh theo bài làm của em: đúng thì câu sau khó hơn, sai thì dễ hơn.
                </p>
                <ul className="list-disc space-y-1 pl-5 text-slate-300">
                  <li>Cần đúng từ {start.passPct}% số câu.</li>
                  {(gate.min_hard_correct ?? 0) > 0 && <li>Đúng ít nhất {gate.min_hard_correct} câu mức Khó.</li>}
                  {gate.min_level && <li>Kết thúc ở mức {GATE_LEVEL_LABELS[gate.min_level]} trở lên.</li>}
                  <li>Không giới hạn thời gian. Đã trả lời thì không sửa được.</li>
                  <li>
                    Chưa đạt thì không mất RP, thi lại sau {gate.cooldown_hours ?? 48} giờ.
                  </li>
                </ul>
                {start.index > 0 && <p className="text-sm text-cyan-300">Em đang làm dở — tiếp tục từ câu {start.index + 1}.</p>}
              </div>
            )}

            {running && exam && question && (
              <div className="space-y-3">
                <div>
                  <p className="text-sm font-semibold text-slate-200">
                    Câu {index + 1}/{total}
                  </p>
                  <div
                    className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-white/10"
                    role="progressbar"
                    aria-valuemin={0}
                    aria-valuemax={total}
                    aria-valuenow={index}
                    aria-label="Tiến độ bài thi"
                  >
                    <div className="h-full rounded-full bg-primary" style={{ width: `${pctDone}%` }} />
                  </div>
                </div>
                <QuestionCard key={question.qid} index={index + 1} question={exam} response={response} onChange={setResponse} />
              </div>
            )}

            {phase === "result" && result && <GateResultView result={result} gate={gate} />}
          </div>

          <div className="shrink-0 border-t border-white/10 px-4 py-3 sm:px-6">
            {phase === "loading" && null}
            {(phase === "error" || phase === "result") && (
              <Button variant="outline" onClick={onClose} className="min-h-11 w-full">
                Đóng
              </Button>
            )}
            {phase === "intro" && (
              <Button onClick={() => setPhase("running")} className="min-h-11 w-full">
                {start && start.index > 0 ? "Tiếp tục thi" : "Bắt đầu thi"}
              </Button>
            )}
            {running && (
              <Button onClick={send} disabled={!canSend} className="min-h-11 w-full">
                {sending ? "Đang gửi…" : index + 1 >= total ? "Trả lời và nộp bài" : "Trả lời"}
              </Button>
            )}
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

function GateResultView({ result, gate }: { result: GateResult; gate: RankGate }) {
  const hardNeeded = result.minHardCorrect > 0;
  const reasons: string[] = [];
  if (!result.passed) {
    if (result.pct < result.passPct) reasons.push(`đạt ${result.pct}% (cần từ ${result.passPct}%)`);
    if (result.hardCorrect < result.minHardCorrect) reasons.push(`đúng ${result.hardCorrect}/${result.minHardCorrect} câu Khó cần có`);
    if (reasons.length === 0) reasons.push(`chưa giữ được mức ${GATE_LEVEL_LABELS[result.minLevel]} ở cuối bài`);
  }
  const tone = result.passed ? "border-emerald-500/40 bg-emerald-500/10" : "border-amber-500/40 bg-amber-500/10";
  const Icon = result.passed ? CheckCircle2 : CircleAlert;
  return (
    <div className="space-y-3">
      <div className={`rounded-xl border p-4 text-center ${tone}`}>
        <p className="flex items-center justify-center gap-2 text-base font-semibold text-white">
          <Icon size={20} aria-hidden className={result.passed ? "text-emerald-300" : "text-amber-300"} />
          {result.passed ? "Em đã qua bài thi" : "Lần này chưa đạt"}
        </p>
        <p className="mt-1 text-3xl font-bold text-white">{result.pct}%</p>
        <p className="mt-1 text-base text-slate-200">
          Đúng {result.correct}/{result.total} câu
          {hardNeeded || result.hardCorrect > 0 ? ` · ${result.hardCorrect} câu Khó` : ""}
        </p>
      </div>

      {result.passed && result.promoted && (
        <p className="text-base leading-relaxed text-emerald-200">Em đã lên bậc mới. Xem huy hiệu ở trang xếp hạng.</p>
      )}
      {result.passed && !result.promoted && (
        <p className="text-base leading-relaxed text-slate-200">
          {result.missingTitles > 0
            ? `Bài thi đã xong. Em còn thiếu ${result.missingTitles} danh hiệu chuyên môn — luyện thêm ở bộ sưu tập là lên bậc ngay.`
            : "Bài thi đã xong. Bậc mới sẽ cập nhật sau ít giây — tải lại trang nếu chưa thấy."}
        </p>
      )}
      {!result.passed && (
        <>
          <p className="text-base leading-relaxed text-slate-200">
            {reasons.join("; ").replace(/^./, (c) => c.toUpperCase())}. Em không mất RP.
          </p>
          {result.weakTopics.length > 0 && (
            <p className="text-base leading-relaxed text-slate-200">
              Nên ôn trước: <b className="text-white">{result.weakTopics.map((w) => w.name).join("; ")}</b>.
            </p>
          )}
          {result.cooldownUntil && (
            <p className="text-sm text-slate-300">
              Thi lại được sau {formatGateWhen(result.cooldownUntil)} ({gate.cooldown_hours ?? 48} giờ kể từ lúc nộp).
            </p>
          )}
        </>
      )}
    </div>
  );
}
