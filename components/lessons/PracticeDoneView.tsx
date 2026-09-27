"use client";

import {
  gradeExam,
  gradeQuestion,
  QUESTION_FORM_LABELS,
  type ExamQuestion,
  type QuestionResponse,
} from "@/features/exams/types";
import { derivePracticeStatus } from "@/features/progress/types";
import QuestionCard from "@/components/exams/QuestionCard";

/**
 * Màn hình sau khi nộp phiên luyện tập (điểm + xem lại từng câu) — tách khỏi
 * components/lessons/PracticeSession.tsx và tải qua `next/dynamic({ ssr: false })` vì học sinh
 * KHÔNG thấy màn này lúc mới mở bài học (chỉ hiện sau khi bấm "Nộp bài" trong 1 phiên luyện
 * tập), phần "không phải câu hỏi đang hiển thị ngay" theo đúng mục tiêu đợt tối ưu tốc độ lần 4
 * (perf4/RESULT.md). KHÔNG đổi logic chấm điểm/lưu phiên — component này thuần hiển thị, việc
 * ghi Supabase vẫn nằm trong PracticeSession.save().
 */
export default function PracticeDoneView({
  questions,
  responses,
  usedSeconds,
  saveState,
  passScore,
  onRetry,
  onNewSession,
  color,
}: {
  questions: ExamQuestion[];
  responses: QuestionResponse[];
  usedSeconds: number;
  saveState: "idle" | "saving" | "saved" | "failed";
  passScore: number | null;
  onRetry: () => void;
  onNewSession: () => void;
  color: string;
}) {
  const summary = gradeExam(questions, responses);
  const practiceStatus =
    saveState === "saved"
      ? derivePracticeStatus({ sessionCount: 1, bestScore10: summary.score10, passScore })
      : null;
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-white/10 bg-panel p-6 text-center">
        <p className="font-display text-4xl font-bold text-gradient">
          {summary.score10.toLocaleString("vi-VN")}
        </p>
        <p className="mt-2 text-sm text-slate-300">
          Đúng trọn vẹn {summary.correctCount}/{questions.length} câu · {formatClock(usedSeconds)}
        </p>
        {practiceStatus && passScore !== null && (
          <p
            className={`mt-2 inline-block rounded-full border px-3 py-1 text-xs font-bold ${
              practiceStatus.status === "passed"
                ? "border-emerald-500/40 bg-emerald-500/15 text-emerald-300"
                : "border-red-500/40 bg-red-500/15 text-red-300"
            }`}
          >
            {practiceStatus.label}
          </p>
        )}
        <p className="mt-2 text-xs text-slate-500">
          {saveState === "saving" && "Đang lưu…"}
          {saveState === "saved" && "✓ Đã ghi lại để thầy biết em cần ôn phần nào"}
          {saveState === "idle" && "Điểm luyện tập không tính vào bảng điểm"}
        </p>
        {saveState === "failed" && (
          <p className="mt-2 flex flex-col items-center gap-2 text-xs text-red-300">
            <span>Chưa lưu được kết quả luyện tập — kiểm tra mạng rồi thử lại.</span>
            <button
              type="button"
              onClick={onRetry}
              className="rounded-full border border-white/15 px-4 py-1.5 text-xs font-semibold text-white hover:border-white/30"
            >
              Thử lại
            </button>
          </p>
        )}
        <button
          type="button"
          onClick={onNewSession}
          className="mt-4 rounded-full px-5 py-2 text-sm font-bold text-white"
          style={{ backgroundColor: color }}
        >
          Luyện phiên mới
        </button>
      </div>

      <ol className="space-y-4">
        {questions.map((q, i) => {
          const g = gradeQuestion(q, responses[i]);
          const wrong = g.earned < g.max;
          const topicName = (q.topic ?? "").trim();
          const formLabel =
            q.form === "ly_thuyet" || q.form === "bai_tap" ? QUESTION_FORM_LABELS[q.form] : "";
          return (
            <li key={i}>
              {wrong && (topicName || formLabel) && (
                <div className="mb-2 flex flex-wrap items-center gap-2 text-xs">
                  {topicName && (
                    <span className="rounded-full bg-amber-500/15 px-2.5 py-1 font-semibold text-amber-300">
                      {topicName}
                    </span>
                  )}
                  {formLabel && (
                    <span className="rounded-full border border-white/15 px-2.5 py-1 text-slate-400">
                      {formLabel}
                    </span>
                  )}
                </div>
              )}
              <QuestionCard index={i + 1} question={q} response={responses[i]} review />
            </li>
          );
        })}
      </ol>
    </div>
  );
}

function formatClock(totalSeconds: number) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}
