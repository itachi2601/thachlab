"use client";

import { Flag } from "lucide-react";
import QuestionCard from "@/components/exams/QuestionCard";
import {
  isAnswered,
  questionSeconds,
  type ExamQuestion,
  type QuestionResponse,
} from "@/features/exams/types";

function formatClock(totalSeconds: number) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

/**
 * Màn hình đang làm 1 phiên luyện tập — tách khỏi components/lessons/PracticeSession.tsx và tải
 * qua `next/dynamic({ ssr: false })` vì học sinh KHÔNG thấy màn này lúc mới mở bài học (chỉ hiện
 * sau khi bấm "Bắt đầu luyện N câu" ở màn chọn số câu), giống PracticeDoneView.tsx — phần "không
 * cần thiết ngay khi trang vừa mount" theo đúng mục tiêu đợt tối ưu tốc độ lần 4
 * (perf4/RESULT.md). Kéo theo QuestionCard nên tách riêng có ý nghĩa (chunk lớn nhất trong 2 màn
 * running/done). KHÔNG đổi logic đếm giờ/lưu đáp án — state (cur, flags, secondsLeft, responses)
 * vẫn do PracticeSession sở hữu, component này thuần hiển thị + gọi ngược qua props.
 */
export default function PracticeRunningView({
  questions,
  responses,
  cur,
  flags,
  secondsLeft,
  color,
  onAnswer,
  onSetCur,
  onToggleFlag,
  onConfirmSubmit,
}: {
  questions: ExamQuestion[];
  responses: QuestionResponse[];
  cur: number;
  flags: Set<number>;
  secondsLeft: number;
  color: string;
  onAnswer: (r: QuestionResponse) => void;
  onSetCur: (updater: number | ((i: number) => number)) => void;
  onToggleFlag: (idx: number) => void;
  onConfirmSubmit: () => void;
}) {
  const q = questions[cur];
  const answeredCount = questions.filter((item, i) => isAnswered(item, responses[i])).length;

  return (
    <div className="space-y-4 rounded-2xl border border-white/10 bg-panel p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <span className="text-sm text-slate-400">
          Câu <span className="font-semibold text-white">{cur + 1}</span>/{questions.length} ·
          đã làm{" "}
          <span className="font-semibold text-white">
            {answeredCount}/{questions.length}
          </span>
        </span>
        <span
          className={`font-mono text-lg font-semibold ${
            secondsLeft <= 30 ? "text-red-400" : "text-cyan"
          }`}
        >
          {formatClock(secondsLeft)}
        </span>
        <button
          type="button"
          onClick={onConfirmSubmit}
          className="rounded-full px-4 py-1.5 text-sm font-bold text-white"
          style={{ backgroundColor: color }}
        >
          Nộp bài
        </button>
      </div>

      <div className="flex flex-wrap gap-1.5">
        {questions.map((item, i) => {
          const done = isAnswered(item, responses[i]);
          const flagged = flags.has(i);
          return (
            <button
              key={i}
              type="button"
              onClick={() => onSetCur(i)}
              title={`Câu ${i + 1}${flagged ? " · đã đánh dấu" : ""}`}
              className={`h-9 w-9 rounded-lg border text-xs font-bold transition-colors ${
                i === cur ? "ring-2 ring-white/70" : ""
              }`}
              style={{
                borderColor: flagged ? "#FBBF24" : done ? color : "rgba(255,255,255,0.12)",
                backgroundColor: done ? `${color}33` : "transparent",
                color: done ? "#FFFFFF" : flagged ? "#FBBF24" : "#94A3B8",
              }}
            >
              {i + 1}
            </button>
          );
        })}
      </div>

      <QuestionCard index={cur + 1} question={q} response={responses[cur]} onChange={onAnswer} />

      <div className="flex flex-wrap items-center gap-2">
        <button
          type="button"
          disabled={cur === 0}
          onClick={() => onSetCur((i) => Math.max(0, i - 1))}
          className="rounded-xl border border-white/15 px-4 py-2 text-sm text-slate-300 hover:border-white/30 disabled:opacity-40"
        >
          ← Câu trước
        </button>
        <button
          type="button"
          onClick={() => onToggleFlag(cur)}
          className={`inline-flex items-center gap-1.5 rounded-xl border px-4 py-2 text-sm font-semibold ${
            flags.has(cur)
              ? "border-amber-400/60 bg-amber-400/10 text-amber-300"
              : "border-white/15 text-slate-300 hover:border-white/30"
          }`}
        >
          <Flag size={14} />
          {flags.has(cur) ? "Bỏ đánh dấu" : "Đánh dấu xem lại"}
        </button>
        {cur < questions.length - 1 ? (
          <button
            type="button"
            onClick={() => onSetCur((i) => Math.min(questions.length - 1, i + 1))}
            className="rounded-xl px-4 py-2 text-sm font-bold text-white"
            style={{ backgroundColor: color }}
          >
            Câu sau →
          </button>
        ) : (
          <button
            type="button"
            onClick={onConfirmSubmit}
            className="rounded-xl px-4 py-2 text-sm font-bold text-white"
            style={{ backgroundColor: color }}
          >
            Nộp bài
          </button>
        )}
        <span className="text-xs text-slate-500">
          Câu này {questionSeconds(q)} giây trong tổng thời lượng
        </span>
      </div>
    </div>
  );
}
