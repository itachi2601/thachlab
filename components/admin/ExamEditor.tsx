"use client";

import { useState } from "react";
import type { Exam, MultipleChoiceQuestion } from "@/features/exams/types";
import LaTexEditor from "@/components/admin/LaTexEditor";
import { getSupabase } from "@/services/supabase";
import { useToast } from "@/components/ui/Toast";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const LETTERS = ["A", "B", "C", "D"];

function newQuestion(): MultipleChoiceQuestion {
  return { type: "multiple_choice", question: "", options: ["", "", "", ""], answer: 0, explanation: "" };
}

function QuestionEditor({
  q,
  onChange,
  onRemove,
  index,
}: {
  q: MultipleChoiceQuestion;
  onChange: (q: MultipleChoiceQuestion) => void;
  onRemove: () => void;
  index: number;
}) {
  return (
    <div className="space-y-3 rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-primary">Câu {index + 1}</span>
        <button type="button" onClick={onRemove} className="text-xs text-red-300 hover:text-red-200">
          Xóa câu
        </button>
      </div>

      <LaTexEditor
        value={q.question}
        onChange={(html) => onChange({ ...q, question: html })}
        placeholder="Nội dung câu hỏi (LaTeX, AZOTA, hoặc HTML)"
      />

      <div className="space-y-2">
        {q.options.map((opt, oi) => (
          <div key={oi} className="flex items-center gap-2">
            <button
              type="button"
              title="Chọn làm đáp án đúng"
              onClick={() => onChange({ ...q, answer: oi })}
              className={`h-8 w-8 shrink-0 rounded-lg text-sm font-semibold ${
                q.answer === oi ? "bg-emerald-500 text-white" : "bg-white/10 text-slate-400 hover:bg-white/20"
              }`}
            >
              {LETTERS[oi]}
            </button>
            <input
              value={opt}
              onChange={(e) => {
                const options = [...q.options];
                options[oi] = e.target.value;
                onChange({ ...q, options });
              }}
              placeholder={`Đáp án ${LETTERS[oi]}`}
              className={inputCls}
            />
          </div>
        ))}
        <p className="text-xs text-slate-500">
          Bấm vào chữ cái để chọn đáp án đúng (đang chọn: {LETTERS[q.answer]})
        </p>
      </div>

      <textarea
        value={q.explanation}
        onChange={(e) => onChange({ ...q, explanation: e.target.value })}
        placeholder="Lời giải (hiện sau khi học sinh làm sai — không bắt buộc)"
        rows={2}
        className={inputCls}
      />
    </div>
  );
}

export default function ExamEditor({
  exam,
  initialQuestions,
  initialTitle,
  cncBank,
  onDone,
}: {
  exam: Exam | null; // null = tạo mới
  initialQuestions?: MultipleChoiceQuestion[]; // prefill từ Import LaTeX
  initialTitle?: string; // prefill title từ Import
  cncBank: { key: string; label: string }; // ngân hàng câu hỏi CNC đang sửa
  onDone: () => void;
}) {
  const toast = useToast();
  const [title, setTitle] = useState(exam?.title ?? initialTitle ?? cncBank.label);
  const [questions, setQuestions] = useState<MultipleChoiceQuestion[]>(
    (exam?.questions as MultipleChoiceQuestion[] | undefined) ?? initialQuestions ?? [],
  );
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function save() {
    if (!title.trim()) {
      setError("Ngân hàng cần có tiêu đề.");
      return;
    }
    if (questions.length === 0) {
      setError("Ngân hàng cần ít nhất 1 câu hỏi.");
      return;
    }
    setBusy(true);
    setError("");
    const payload = {
      title: title.trim(),
      duration_minutes: 20,
      topic: "CNC",
      difficulty: "" as const,
      questions,
      published: false,
      cnc_key: cncBank.key,
    };
    const supabase = getSupabase();
    if (exam) {
      const { error } = await supabase.from("exams").update(payload).eq("id", exam.id);
      if (error) {
        setBusy(false);
        setError(error.message);
        return;
      }
    } else {
      const { error } = await supabase.from("exams").upsert(payload, { onConflict: "cnc_key" });
      if (error) {
        setBusy(false);
        setError(error.message ?? "Không lưu được ngân hàng câu hỏi.");
        return;
      }
    }
    setBusy(false);
    toast("success", "Đã lưu ngân hàng câu hỏi.");
    onDone();
  }

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-orange-400/20 bg-orange-500/5 p-4">
        <p className="text-xs font-bold uppercase tracking-wide text-orange-300">Ngân hàng câu hỏi CNC</p>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder={cncBank.label}
          className={`${inputCls} mt-2 text-lg font-bold`}
        />
      </div>

      <div className="space-y-4">
        {questions.map((q, qi) => (
          <QuestionEditor
            key={qi}
            index={qi}
            q={q}
            onChange={(nq) => setQuestions((prev) => prev.map((p, i) => (i === qi ? nq : p)))}
            onRemove={() => setQuestions((prev) => prev.filter((_, i) => i !== qi))}
          />
        ))}
      </div>

      <button
        type="button"
        onClick={() => setQuestions((prev) => [...prev, newQuestion()])}
        className="rounded-full border border-dashed border-white/20 px-4 py-2 text-sm text-slate-300 hover:border-primary hover:text-white"
      >
        + Thêm câu hỏi
      </button>

      {error && <p className="text-sm text-red-400">{error}</p>}

      <div className="flex flex-wrap gap-3">
        <button
          onClick={save}
          disabled={busy}
          className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark disabled:opacity-50"
        >
          Lưu ngân hàng câu hỏi
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
