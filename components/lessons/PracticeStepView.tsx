"use client";

import { useMemo, useState } from "react";
import { CheckCircle2, CircleAlert, RotateCcw } from "lucide-react";
import QuestionCard from "@/components/exams/QuestionCard";
import Html from "@/components/exams/ContentHtml";
import { emptyResponses, isAnswered, type QuestionResponse } from "@/features/exams/types";
import { distractorHints, isFullyCorrect, pickKey, similarCandidates } from "@/features/lessons/practice-step";
import type { PracticePick } from "@/services/lessons";

/** Kết quả LẦN ĐẦU của một câu — thứ duy nhất được lưu vào practice_question_results. */
export interface StepItem {
  pick: PracticePick;
  response: QuestionResponse;
  correct: boolean;
}

interface Slot {
  pick: PracticePick;
  /** Câu sai được xếp lại cuối phiên: làm lại 1 lần, không tính điểm lần 2. */
  retry: boolean;
}

/**
 * Luyện tập "Từng câu" (kiểu Duolingo): chọn → Kiểm tra → hiện ngay đúng/sai, đáp án, lời giải và (nếu câu có
 * distractorNotes) lý do phương án em chọn sai. Sai → "Làm câu tương tự" (cùng chủ đề, cùng mức, chưa dùng trong
 * phiên, chèn ngay sau); câu sai còn được xếp lại cuối phiên. Không đồng hồ, không "tim", không trừ gì — chỉ
 * một chuỗi đúng nhỏ ở góc.
 *
 * State phiên (picks, lưu điểm, thang mức) vẫn do PracticeSession giữ; view này chỉ báo `onFinish(items)` với kết
 * quả lần đầu theo thứ tự câu đã hiện. Tách chunk + LazyErrorBoundary ở PracticeSession (đợt tối ưu tốc độ).
 *
 * Quy tắc thiết kế: N1 một câu/màn · C2 cột đọc ≈ 65 ký tự (max-w-xl) · M4 đúng/sai có icon + chữ (không chỉ màu) ·
 * L1 phản hồi tức thì kèm giải thích vì sao sai · L3 chuỗi đúng nhỏ, không phần thưởng giữa bài · L4 lời phản hồi
 * hướng việc tiếp theo · D2 nút ≥ 44px · D3 "Tiếp" ở cuối khối trong tầm ngón cái, "Kết thúc" xa ngón cái ·
 * B2 một nút nổi mỗi màn · B4 không chuyển động.
 */
export default function PracticeStepView({
  initialPicks,
  bank,
  color,
  onFinish,
  onQuit,
}: {
  initialPicks: PracticePick[];
  /** Toàn bộ ngân hàng câu của mục luyện tập — nguồn của "Làm câu tương tự". */
  bank: PracticePick[];
  color: string;
  onFinish: (items: StepItem[]) => void;
  /** Thoát khi chưa làm câu nào. */
  onQuit: () => void;
}) {
  const [queue, setQueue] = useState<Slot[]>(() => initialPicks.map((pick) => ({ pick, retry: false })));
  const [pos, setPos] = useState(0);
  const [stage, setStage] = useState<"answering" | "feedback">("answering");
  const [response, setResponse] = useState<QuestionResponse>(() => emptyResponses([initialPicks[0].question])[0]);
  const [items, setItems] = useState<StepItem[]>([]);
  const [streak, setStreak] = useState(0);
  const [usedKeys, setUsedKeys] = useState<Set<string>>(() => new Set(initialPicks.map(pickKey)));
  const [lastCorrect, setLastCorrect] = useState(true);

  const slot = queue[pos];
  const q = slot.pick.question;
  const planned = queue.filter((s) => !s.retry).length;
  const retriesLeft = queue.slice(pos).filter((s) => s.retry).length;
  const isLast = pos >= queue.length - 1;
  const canCheck = stage === "answering" && isAnswered(q, response);

  const similar = useMemo(
    () => (stage === "feedback" && !slot.retry && !lastCorrect ? similarCandidates(bank, q, usedKeys) : []),
    [stage, slot.retry, lastCorrect, bank, q, usedKeys],
  );
  const hints = stage === "feedback" ? distractorHints(q, response) : [];

  function check() {
    if (!canCheck) return;
    const ok = isFullyCorrect(q, response);
    setLastCorrect(ok);
    if (!slot.retry) {
      setItems((prev) => [...prev, { pick: slot.pick, response, correct: ok }]);
      setStreak((s) => (ok ? s + 1 : 0));
      // Sai (hoặc đúng một phần) → xếp lại 1 lần ở cuối phiên.
      if (!ok) setQueue((prev) => [...prev, { pick: slot.pick, retry: true }]);
    }
    setStage("feedback");
  }

  function goTo(nextPos: number, nextQueue: Slot[]) {
    setPos(nextPos);
    setStage("answering");
    setResponse(emptyResponses([nextQueue[nextPos].pick.question])[0]);
  }

  function next() {
    if (isLast) {
      onFinish(items);
      return;
    }
    goTo(pos + 1, queue);
  }

  function addSimilar() {
    if (similar.length === 0) return;
    const chosen = similar[Math.floor(Math.random() * similar.length)];
    const nextQueue = [...queue.slice(0, pos + 1), { pick: chosen, retry: false }, ...queue.slice(pos + 1)];
    setQueue(nextQueue);
    setUsedKeys((prev) => new Set(prev).add(pickKey(chosen)));
    goTo(pos + 1, nextQueue);
  }

  function finishEarly() {
    if (items.length === 0) {
      onQuit();
      return;
    }
    if (confirm(`Kết thúc phiên ở đây? Em đã làm ${items.length} câu — các câu chưa làm sẽ không tính.`)) onFinish(items);
  }

  const doneFirst = items.length;
  const pct = planned > 0 ? Math.min(100, Math.round((doneFirst / planned) * 100)) : 0;

  return (
    <div className="mx-auto max-w-xl space-y-4 rounded-2xl border border-white/10 bg-panel p-4 sm:p-5">
      <div>
        <div className="flex items-center justify-between gap-2">
          <p className="text-sm font-semibold text-slate-200">
            {slot.retry ? (
              <>
                <RotateCcw size={14} className="mr-1 inline align-[-2px]" aria-hidden />
                Làm lại câu đã sai · còn {retriesLeft}
              </>
            ) : (
              <>
                Câu {Math.min(doneFirst + (stage === "answering" ? 1 : 0), planned)}/{planned}
              </>
            )}
          </p>
          <div className="flex items-center gap-1">
            {streak >= 2 && <span className="text-sm text-slate-300">Đúng liên tiếp {streak}</span>}
            <button
              type="button"
              onClick={finishEarly}
              className="min-h-11 rounded-lg px-3 text-sm text-slate-400 hover:text-slate-200"
            >
              Kết thúc
            </button>
          </div>
        </div>
        <div
          className="mt-1 h-1.5 overflow-hidden rounded-full bg-white/10"
          role="progressbar"
          aria-valuemin={0}
          aria-valuemax={planned}
          aria-valuenow={doneFirst}
          aria-label="Tiến độ phiên luyện"
        >
          <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: color }} />
        </div>
      </div>

      {slot.retry && stage === "answering" && (
        <p className="text-sm text-slate-300">Câu này em đã làm sai ở trên. Thử lại — lần này không tính điểm.</p>
      )}

      <QuestionCard
        key={`${pos}-${stage}`}
        index={pos + 1}
        question={q}
        response={response}
        onChange={stage === "answering" ? setResponse : undefined}
        review={stage === "feedback"}
      />

      {stage === "feedback" && (
        <div role="status" aria-live="polite" className="space-y-3">
          {lastCorrect ? (
            <p className="flex items-start gap-2 rounded-xl border border-emerald-500/40 bg-emerald-500/10 p-3 text-base text-emerald-100">
              <CheckCircle2 size={20} className="mt-0.5 shrink-0 text-emerald-300" aria-hidden />
              <span>{slot.retry ? "Đúng rồi — lần làm lại này không tính điểm." : "Đúng rồi."}</span>
            </p>
          ) : (
            <p className="flex items-start gap-2 rounded-xl border border-amber-500/40 bg-amber-500/10 p-3 text-base text-amber-100">
              <CircleAlert size={20} className="mt-0.5 shrink-0 text-amber-300" aria-hidden />
              <span>
                Chưa đúng. Xem đáp án và lời giải ở trên
                {slot.retry ? "." : ", rồi thử câu tương tự hoặc gặp lại câu này ở cuối phiên."}
              </span>
            </p>
          )}
          {hints.length > 0 && (
            <ul className="space-y-2 border-l-2 border-amber-400/60 pl-3 text-base leading-relaxed text-slate-200">
              {hints.map((h) => (
                <li key={h.label}>
                  <b className="text-white">Vì sao em chọn {h.label} chưa đúng:</b> <Html html={h.note} />
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      <div className="flex flex-col gap-2">
        {stage === "answering" ? (
          <button
            type="button"
            onClick={check}
            disabled={!canCheck}
            className="min-h-12 w-full rounded-full px-5 text-base font-bold text-white disabled:opacity-40"
            style={{ backgroundColor: color }}
          >
            Kiểm tra
          </button>
        ) : (
          <>
            {similar.length > 0 && (
              <button
                type="button"
                onClick={addSimilar}
                className="min-h-11 w-full rounded-full border border-white/20 px-5 text-base font-semibold text-slate-100 hover:border-white/40"
              >
                Làm câu tương tự
              </button>
            )}
            <button
              type="button"
              onClick={next}
              className="min-h-12 w-full rounded-full px-5 text-base font-bold text-white"
              style={{ backgroundColor: color }}
            >
              {isLast ? "Xem kết quả" : "Tiếp"}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
