"use client";

import QuestionCard from "@/components/exams/QuestionCard";
import { useAuth } from "@/components/auth/AuthProvider";
import Badge from "@/components/ui/Badge";
import { isAnswered, type ExamQuestionPublic, type QuestionResponse } from "@/features/exams/types";

function formatClock(totalSeconds: number) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

/**
 * Màn sau khi nộp khi server CHƯA mở đáp án (đề đánh giá: chưa đủ 3 lượt nộp và chưa đạt điểm đạt —
 * submit_exam_attempt trả answers_revealed = false). Hiện điểm + đúng/sai từng câu (per_question) và chính
 * câu hỏi cùng đáp án em đã chọn; ẩn đáp án đúng và lời giải. Không tự chấm lại ở máy (không có đáp án).
 */
export default function ExamDoneLocked({
  title,
  questions,
  responses,
  perQuestion,
  score10,
  correctCount,
  usedSeconds,
}: {
  title: string;
  questions: ExamQuestionPublic[];
  responses: QuestionResponse[];
  perQuestion: { earned: number; max: number; is_correct: boolean }[];
  score10: number;
  correctCount: number;
  usedSeconds: number;
}) {
  const { profile } = useAuth();
  return (
    <div className="mx-auto max-w-3xl">
      <div className="rounded-2xl border border-line bg-panel p-6 text-center">
        <p className="text-sm text-muted">
          {profile?.full_name}
          {profile?.class_name && ` · Lớp ${profile.class_name}`}
          {` · ${title} · ${formatClock(usedSeconds)}`}
        </p>
        <p className="mt-3 font-display text-5xl font-bold text-ink">{score10.toFixed(2)}</p>
        <p className="mt-1 text-base text-ink">
          Đúng {correctCount}/{questions.length} câu
        </p>
        <p className="mt-3 text-sm text-muted">Đáp án sẽ hiện sau 3 lượt làm hoặc khi đạt điểm.</p>
      </div>

      <h2 className="mb-4 mt-8 font-display text-xl font-semibold text-ink">Kết quả từng câu</h2>
      <div className="space-y-4">
        {questions.map((q, i) => {
          const g = perQuestion[i];
          const answered = isAnswered(q, responses[i]);
          let label = "Sai";
          let tone: "success" | "warning" | "error" | "neutral" = "error";
          if (q.type === "essay" || (g && g.max === 0)) {
            label = "Thầy chấm";
            tone = "neutral";
          } else if (!answered) {
            label = "Bỏ qua";
            tone = "neutral";
          } else if (g && g.earned >= g.max) {
            label = "Đúng";
            tone = "success";
          } else if (g && g.earned > 0) {
            label = "Đúng một phần";
            tone = "warning";
          }
          return (
            <div key={i}>
              <div className="mb-1">
                <Badge tone={tone}>{label}</Badge>
              </div>
              <QuestionCard index={i + 1} question={q} response={responses[i]} />
            </div>
          );
        })}
      </div>
    </div>
  );
}
