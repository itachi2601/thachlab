"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import QuestionCard from "@/components/exams/QuestionCard";
import { emptyResponses, isAnswered, type ExamQuestion, type QuestionResponse } from "@/features/exams/types";

/**
 * Trợ giảng xem đề thầy gửi bằng đúng giao diện của giáo viên (ExamRunner teacherView): mỗi câu hiện sẵn đáp án đúng,
 * lời giải và lý do của MỌI phương án sai (QuestionCard selfCheck). Muốn tự làm trước thì bấm "Tự làm thử câu này":
 * chọn xong bấm "Xem đáp án" thấy điểm câu đó cùng lý do mọi phương án sai. Hết đề → sang trang Chữa bài của đề cho lớp đó.
 * Không đồng hồ, không lưu điểm, không ghi exam_results — đây là xem trước, không phải bài nộp.
 */
export default function TaPreviewRunner({
  title,
  examId,
  classId,
  questions,
}: {
  title: string;
  examId: number;
  classId: number;
  questions: ExamQuestion[];
}) {
  const router = useRouter();
  const [cur, setCur] = useState(0);
  const [responses, setResponses] = useState<QuestionResponse[]>(() => emptyResponses(questions));
  // Câu TA chọn tự làm thử: chưa lộ đáp án tới khi bấm "Xem đáp án". Còn lại mặc định hiện như giao diện giáo viên.
  const [trying, setTrying] = useState<Set<number>>(new Set());
  const [revealed, setRevealed] = useState<Set<number>>(new Set());

  const q = questions[cur];
  const isTrying = trying.has(cur);
  const shown = !isTrying || revealed.has(cur);
  const isLast = cur === questions.length - 1;
  const canReveal = isAnswered(q, responses[cur]);

  const reveal = () => setRevealed((s) => new Set(s).add(cur));
  const tryThis = () => {
    setResponses((rs) => rs.map((x, i) => (i === cur ? emptyResponses([q])[0] : x)));
    setRevealed((s) => { const n = new Set(s); n.delete(cur); return n; });
    setTrying((s) => new Set(s).add(cur));
  };
  const next = () => {
    if (isLast) router.push(`/tro-giang/chua-bai?exam=${examId}&class=${classId}`);
    else setCur(cur + 1);
  };

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs text-slate-400">Xem trước · {title}</p>
        <p className="text-sm text-slate-300">
          Câu <b className="text-white">{cur + 1}</b>/{questions.length}
        </p>
        <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-white/10" aria-hidden>
          <div className="h-full bg-primary" style={{ width: `${((cur + (shown ? 1 : 0)) / questions.length) * 100}%` }} />
        </div>
      </div>

      <QuestionCard
        key={cur}
        index={cur + 1}
        question={q}
        response={responses[cur]}
        review={shown}
        selfCheck={!isTrying}
        showAllNotes
        onChange={shown ? undefined : (r) => setResponses((rs) => rs.map((x, i) => (i === cur ? r : x)))}
      />

      <div className="flex gap-2">
        {cur > 0 && (
          <button type="button" onClick={() => setCur(cur - 1)} className="min-h-12 rounded-xl border border-white/15 px-4 font-semibold text-white">
            ← Trước
          </button>
        )}
        {!shown ? (
          <button
            type="button"
            onClick={reveal}
            disabled={!canReveal}
            className="min-h-12 flex-1 rounded-xl bg-primary px-5 font-semibold text-white disabled:opacity-40"
          >
            {canReveal ? "Xem đáp án" : "Chọn đáp án để xem"}
          </button>
        ) : (
          <button type="button" onClick={next} className="min-h-12 flex-1 rounded-xl bg-primary px-5 font-semibold text-white">
            {isLast ? "Xong — xem phân tích lớp →" : "Câu sau →"}
          </button>
        )}
      </div>
      {!isTrying && (
        <button type="button" onClick={tryThis} className="min-h-11 text-sm text-slate-300 underline">
          Tự làm thử câu này
        </button>
      )}
      {isTrying && !shown && (
        <button type="button" onClick={reveal} className="min-h-11 text-sm text-slate-400 underline">
          Bỏ qua, chỉ xem đáp án
        </button>
      )}
    </div>
  );
}
