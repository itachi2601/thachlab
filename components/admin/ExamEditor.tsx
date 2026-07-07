"use client";

import { useState } from "react";
import type {
  Exam,
  ExamQuestion,
  MultipleChoiceQuestion,
  ShortAnswerQuestion,
  TrueFalseQuestion,
} from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-[#3B82F6] focus:outline-none";
const LETTERS = ["A", "B", "C", "D"];
const TF_LABELS = ["a)", "b)", "c)", "d)"];

function newQuestion(type: ExamQuestion["type"]): ExamQuestion {
  if (type === "multiple_choice")
    return {
      type,
      question: "",
      options: ["", "", "", ""],
      answer: 0,
      explanation: "",
    };
  if (type === "true_false")
    return {
      type,
      question: "",
      statements: Array.from({ length: 4 }, () => ({
        text: "",
        answer: true,
      })),
      explanation: "",
    };
  return { type, question: "", answer: "", explanation: "" };
}

const TYPE_LABELS: Record<ExamQuestion["type"], string> = {
  multiple_choice: "Trắc nghiệm A/B/C/D",
  true_false: "Đúng / Sai (4 ý)",
  short_answer: "Trả lời ngắn",
};

function QuestionEditor({
  q,
  onChange,
  onRemove,
  index,
}: {
  q: ExamQuestion;
  onChange: (q: ExamQuestion) => void;
  onRemove: () => void;
  index: number;
}) {
  return (
    <div className="space-y-3 rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-[#3B82F6]">
          Câu {index + 1} · {TYPE_LABELS[q.type]}
        </span>
        <button
          type="button"
          onClick={onRemove}
          className="text-xs text-red-300 hover:text-red-200"
        >
          Xóa câu
        </button>
      </div>

      <textarea
        value={q.question}
        onChange={(e) => onChange({ ...q, question: e.target.value })}
        placeholder="Nội dung câu hỏi"
        rows={2}
        className={inputCls}
      />

      {q.type === "multiple_choice" && (
        <div className="space-y-2">
          {(q as MultipleChoiceQuestion).options.map((opt, oi) => (
            <div key={oi} className="flex items-center gap-2">
              <button
                type="button"
                title="Chọn làm đáp án đúng"
                onClick={() =>
                  onChange({ ...q, answer: oi } as MultipleChoiceQuestion)
                }
                className={`h-8 w-8 shrink-0 rounded-lg text-sm font-semibold ${
                  (q as MultipleChoiceQuestion).answer === oi
                    ? "bg-emerald-500 text-white"
                    : "bg-white/10 text-slate-400 hover:bg-white/20"
                }`}
              >
                {LETTERS[oi]}
              </button>
              <input
                value={opt}
                onChange={(e) => {
                  const options = [
                    ...(q as MultipleChoiceQuestion).options,
                  ];
                  options[oi] = e.target.value;
                  onChange({ ...q, options } as MultipleChoiceQuestion);
                }}
                placeholder={`Đáp án ${LETTERS[oi]}`}
                className={inputCls}
              />
            </div>
          ))}
          <p className="text-xs text-slate-500">
            Bấm vào chữ cái để chọn đáp án đúng (đang chọn:{" "}
            {LETTERS[(q as MultipleChoiceQuestion).answer]})
          </p>
        </div>
      )}

      {q.type === "true_false" && (
        <div className="space-y-2">
          {(q as TrueFalseQuestion).statements.map((st, si) => (
            <div key={si} className="flex items-center gap-2">
              <span className="w-6 shrink-0 text-sm text-slate-400">
                {TF_LABELS[si]}
              </span>
              <input
                value={st.text}
                onChange={(e) => {
                  const statements = [...(q as TrueFalseQuestion).statements];
                  statements[si] = { ...st, text: e.target.value };
                  onChange({ ...q, statements } as TrueFalseQuestion);
                }}
                placeholder={`Ý ${TF_LABELS[si]}`}
                className={inputCls}
              />
              <button
                type="button"
                onClick={() => {
                  const statements = [...(q as TrueFalseQuestion).statements];
                  statements[si] = { ...st, answer: !st.answer };
                  onChange({ ...q, statements } as TrueFalseQuestion);
                }}
                className={`w-16 shrink-0 rounded-lg px-2 py-1.5 text-xs font-semibold ${
                  st.answer
                    ? "bg-emerald-500/80 text-white"
                    : "bg-red-500/80 text-white"
                }`}
              >
                {st.answer ? "Đúng" : "Sai"}
              </button>
            </div>
          ))}
        </div>
      )}

      {q.type === "short_answer" && (
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-400">Đáp án:</span>
          <input
            value={(q as ShortAnswerQuestion).answer}
            onChange={(e) =>
              onChange({
                ...q,
                answer: e.target.value.replace(/[^0-9,.\-]/g, "").slice(0, 4),
              } as ShortAnswerQuestion)
            }
            placeholder="vd -1,5"
            className={`${inputCls} w-32 font-mono`}
          />
          <span className="text-xs text-slate-500">
            tối đa 4 ký tự: số, dấu trừ, dấu phẩy
          </span>
        </div>
      )}

      <textarea
        value={q.explanation}
        onChange={(e) => onChange({ ...q, explanation: e.target.value })}
        placeholder="Lời giải (hiện sau khi học sinh nộp bài — không bắt buộc)"
        rows={2}
        className={inputCls}
      />
    </div>
  );
}

export default function ExamEditor({
  exam,
  onDone,
}: {
  exam: Exam | null; // null = tạo mới
  onDone: () => void;
}) {
  const [title, setTitle] = useState(exam?.title ?? "");
  const [duration, setDuration] = useState(exam?.duration_minutes ?? 45);
  const [questions, setQuestions] = useState<ExamQuestion[]>(
    exam?.questions ?? [],
  );
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function save(publish: boolean) {
    if (!title.trim()) {
      setError("Đề cần có tiêu đề.");
      return;
    }
    if (questions.length === 0) {
      setError("Đề cần ít nhất 1 câu hỏi.");
      return;
    }
    setBusy(true);
    setError("");
    const payload = {
      title: title.trim(),
      duration_minutes: duration,
      questions,
      published: publish,
    };
    const supabase = getSupabase();
    const { error } = exam
      ? await supabase.from("exams").update(payload).eq("id", exam.id)
      : await supabase.from("exams").insert(payload);
    setBusy(false);
    if (error) {
      setError(error.message);
      return;
    }
    onDone();
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center gap-3">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Tiêu đề đề kiểm tra"
          className={`${inputCls} flex-1 min-w-60`}
        />
        <label className="flex items-center gap-2 text-sm text-slate-400">
          Thời gian
          <input
            type="number"
            min={1}
            max={180}
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value))}
            className={`${inputCls} w-20 text-center`}
          />
          phút
        </label>
      </div>

      <div className="space-y-4">
        {questions.map((q, qi) => (
          <QuestionEditor
            key={qi}
            index={qi}
            q={q}
            onChange={(nq) =>
              setQuestions((prev) => prev.map((p, i) => (i === qi ? nq : p)))
            }
            onRemove={() =>
              setQuestions((prev) => prev.filter((_, i) => i !== qi))
            }
          />
        ))}
      </div>

      <div className="flex flex-wrap gap-2">
        {(
          ["multiple_choice", "true_false", "short_answer"] as const
        ).map((t) => (
          <button
            key={t}
            type="button"
            onClick={() => setQuestions((prev) => [...prev, newQuestion(t)])}
            className="rounded-full border border-dashed border-white/20 px-4 py-2 text-sm text-slate-300 hover:border-[#3B82F6] hover:text-white"
          >
            + {TYPE_LABELS[t]}
          </button>
        ))}
      </div>

      {error && <p className="text-sm text-red-400">{error}</p>}

      <div className="flex flex-wrap gap-3">
        <button
          onClick={() => save(true)}
          disabled={busy}
          className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#1D4ED8] disabled:opacity-50"
        >
          Lưu &amp; đăng đề
        </button>
        <button
          onClick={() => save(false)}
          disabled={busy}
          className="rounded-full border border-white/15 px-5 py-2.5 text-sm font-semibold text-slate-200 hover:border-white/30 disabled:opacity-50"
        >
          Lưu nháp
        </button>
        <button
          onClick={onDone}
          disabled={busy}
          className="rounded-full px-5 py-2.5 text-sm text-slate-400 hover:text-white"
        >
          Hủy
        </button>
      </div>
    </div>
  );
}
