"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, Eye, Sparkles, Trash2 } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import { useToast } from "@/components/ui/Toast";
import type {
  ExamQuestion,
  MultipleChoiceQuestion,
  QuestionForm,
  ShortAnswerQuestion,
  TrueFalseQuestion,
} from "@/features/exams/types";
import { classifyQuestionTags } from "@/services/ai-classify";
import { questionTextForAi } from "@/services/exam-question-text";
import type { Difficulty, LessonBundle } from "@/services/lesson-import";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const LETTERS = ["A", "B", "C", "D"];

type EditableType = "multiple_choice" | "true_false" | "short_answer";

const TYPE_LABELS: Record<EditableType, string> = {
  multiple_choice: "Trắc nghiệm A–D",
  true_false: "Đúng / Sai (4 ý)",
  short_answer: "Trả lời ngắn",
};

/** Đổi loại câu nhưng giữ lại đề bài và lời giải đã có. */
function changeType(q: ExamQuestion, type: EditableType): ExamQuestion {
  const base = { question: q.question, explanation: q.explanation, topic: q.topic, form: q.form };
  if (type === "multiple_choice")
    return { ...base, type, options: ["", "", "", ""], answer: -1 } as MultipleChoiceQuestion;
  if (type === "true_false")
    return {
      ...base,
      type,
      statements: [0, 1, 2, 3].map(() => ({ text: "", answer: false })),
    } as TrueFalseQuestion;
  return { ...base, type, answer: "" } as ShortAnswerQuestion;
}

function newQuestion(type: EditableType): ExamQuestion {
  return changeType({ type: "short_answer", question: "", answer: "", explanation: "" }, type);
}

/** Chỗ còn thiếu của một câu — hiện ngay trên thẻ câu đó, không đợi lúc bấm Đăng. */
function problems(q: ExamQuestion): string[] {
  const out: string[] = [];
  if (!q.question.trim()) out.push("chưa có nội dung câu hỏi");
  if (q.type === "multiple_choice") {
    if (q.options.some((o) => !o.trim())) out.push("còn phương án để trống");
    if (q.answer < 0 || q.answer > 3) out.push("chưa chọn đáp án đúng");
  } else if (q.type === "true_false") {
    if (q.statements.some((s) => !s.text.trim())) out.push("còn ý để trống");
  } else if (q.type === "short_answer") {
    const a = q.answer.trim();
    if (!a) out.push("chưa có đáp án");
    else if (a.length > 4) out.push(`đáp án "${a}" dài quá 4 ký tự`);
  }
  if (!q.explanation.trim()) out.push("chưa có lời giải");
  return out;
}

export default function ExamDraftEditor({
  bundle,
  onChange,
  topicOptions = [],
  aiTopicCandidates = [],
}: {
  bundle: LessonBundle;
  onChange: (next: LessonBundle) => void;
  /** Tên yêu cầu cần đạt trong danh mục — gợi ý cho ô "Chủ đề câu này". */
  topicOptions?: string[];
  /** YCCĐ của đúng bài đang chọn — danh mục đóng cho AI gắn nhãn (hẹp hơn topicOptions). */
  aiTopicCandidates?: string[];
}) {
  const toast = useToast();
  const [aiBusy, setAiBusy] = useState(false);
  const questions = bundle.exam.questions;

  function setExam(patch: Partial<LessonBundle["exam"]>) {
    onChange({ ...bundle, exam: { ...bundle.exam, ...patch } });
  }
  function setQuestions(next: ExamQuestion[]) {
    setExam({ questions: next });
  }
  function update(index: number, next: ExamQuestion) {
    setQuestions(questions.map((q, i) => (i === index ? next : q)));
  }
  function move(index: number, delta: number) {
    const target = index + delta;
    if (target < 0 || target >= questions.length) return;
    const next = [...questions];
    [next[index], next[target]] = [next[target], next[index]];
    setQuestions(next);
  }

  const aiTargets = questions
    .map((_, i) => i)
    .filter((i) => !(questions[i].topic ?? "").trim() || !questions[i].form);
  const aiAvailable = aiTopicCandidates.length > 0 && aiTargets.length > 0;

  async function runAutoTag() {
    if (!aiAvailable || aiBusy) return;
    setAiBusy(true);
    try {
      const items = aiTargets.map((i) => ({ index: i, text: questionTextForAi(questions[i]) }));
      const results = await classifyQuestionTags(aiTopicCandidates, items);
      let next = questions;
      for (const r of results) {
        next = next.map((q, i) =>
          i === r.index ? { ...q, topic: r.topic ?? q.topic, form: r.form ?? q.form } : q,
        );
      }
      setQuestions(next);
      toast(
        results.length > 0 ? "success" : "error",
        results.length > 0
          ? `AI đã gắn nhãn cho ${results.length}/${aiTargets.length} câu.`
          : "AI không gắn được nhãn nào — thử lại hoặc gắn tay.",
      );
    } catch (e) {
      toast("error", e instanceof Error ? e.message : String(e));
    } finally {
      setAiBusy(false);
    }
  }

  const incomplete = questions.filter((q) => problems(q).length > 0).length;

  return (
    <div className="space-y-4">
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <label className="text-xs font-semibold text-slate-400">
          Tên đề
          <input
            value={bundle.exam.title}
            onChange={(e) => setExam({ title: e.target.value })}
            className={`${inputCls} mt-1`}
          />
        </label>
        <label className="text-xs font-semibold text-slate-400">
          Thời gian (phút)
          <input
            type="number"
            min={5}
            max={180}
            value={bundle.exam.duration_minutes ?? 45}
            onChange={(e) => setExam({ duration_minutes: Number(e.target.value) })}
            className={`${inputCls} mt-1`}
          />
        </label>
        <label className="text-xs font-semibold text-slate-400">
          Chủ đề chung
          <input
            value={bundle.exam.topic ?? ""}
            onChange={(e) => setExam({ topic: e.target.value })}
            placeholder="vd: Chuyển động biến đổi đều"
            className={`${inputCls} mt-1`}
          />
        </label>
        <label className="text-xs font-semibold text-slate-400">
          Mức độ
          <select
            value={bundle.exam.difficulty ?? ""}
            onChange={(e) => setExam({ difficulty: e.target.value as Difficulty })}
            className={`${inputCls} mt-1 bg-panel`}
          >
            <option value="">Chưa phân loại</option>
            <option value="de">Dễ</option>
            <option value="trung-binh">Trung bình</option>
            <option value="kho">Khó</option>
          </select>
        </label>
      </div>

      <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400">
        <span>
          {questions.length} câu
          {incomplete > 0 ? (
            <span className="text-amber-300"> · {incomplete} câu còn thiếu, xem viền vàng bên dưới</span>
          ) : (
            <span className="text-emerald-300"> · đã đủ đáp án và lời giải</span>
          )}
        </span>
        {aiAvailable && (
          <button
            type="button"
            onClick={runAutoTag}
            disabled={aiBusy}
            className="ml-auto inline-flex items-center gap-1 rounded-lg bg-primary/20 px-2 py-1 text-[11px] font-semibold text-primary hover:bg-primary/30 disabled:opacity-50"
          >
            <Sparkles size={12} /> {aiBusy ? "Đang phân loại…" : `AI gắn nhãn (${aiTargets.length} câu)`}
          </button>
        )}
      </div>

      <div className="space-y-3">
        {questions.map((q, i) => (
          <QuestionCardEditor
            key={i}
            index={i}
            total={questions.length}
            q={q}
            onChange={(next) => update(i, next)}
            topicOptions={topicOptions}
            onRemove={() => setQuestions(questions.filter((_, k) => k !== i))}
            onMove={(delta) => move(i, delta)}
          />
        ))}
      </div>

      <div className="flex flex-wrap gap-2">
        {(Object.keys(TYPE_LABELS) as EditableType[]).map((type) => (
          <button
            key={type}
            type="button"
            onClick={() => setQuestions([...questions, newQuestion(type)])}
            className="admin-chip"
          >
            + {TYPE_LABELS[type]}
          </button>
        ))}
      </div>
    </div>
  );
}

function QuestionCardEditor({
  q,
  index,
  total,
  onChange,
  topicOptions,
  onRemove,
  onMove,
}: {
  q: ExamQuestion;
  index: number;
  total: number;
  onChange: (next: ExamQuestion) => void;
  topicOptions: string[];
  onRemove: () => void;
  onMove: (delta: number) => void;
}) {
  const [preview, setPreview] = useState(false);
  const issues = problems(q);
  const type = q.type === "essay" ? "short_answer" : q.type;

  return (
    <article
      className={`space-y-3 rounded-2xl border p-4 ${
        issues.length ? "border-amber-500/40 bg-amber-500/[.04]" : "border-white/10 bg-white/[.03]"
      }`}
    >
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="text-sm font-bold text-blue-300">Câu {index + 1}</span>
          <select
            value={type}
            onChange={(e) => onChange(changeType(q, e.target.value as EditableType))}
            className="rounded-lg border border-white/10 bg-panel px-2 py-1 text-xs text-slate-300"
          >
            {(Object.keys(TYPE_LABELS) as EditableType[]).map((t) => (
              <option key={t} value={t}>
                {TYPE_LABELS[t]}
              </option>
            ))}
          </select>
        </div>
        <div className="flex items-center gap-1 text-slate-400">
          <button type="button" onClick={() => setPreview((v) => !v)} title="Xem như học sinh thấy" className="rounded p-1 hover:text-white">
            <Eye size={14} />
          </button>
          <button type="button" onClick={() => onMove(-1)} disabled={index === 0} className="rounded p-1 hover:text-white disabled:opacity-30">
            <ChevronUp size={14} />
          </button>
          <button type="button" onClick={() => onMove(1)} disabled={index === total - 1} className="rounded p-1 hover:text-white disabled:opacity-30">
            <ChevronDown size={14} />
          </button>
          <button type="button" onClick={onRemove} className="rounded p-1 text-red-300 hover:text-red-200">
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      {issues.length > 0 && <p className="text-[11px] text-amber-300">Còn thiếu: {issues.join(" · ")}</p>}

      <textarea
        value={q.question}
        onChange={(e) => onChange({ ...q, question: e.target.value })}
        rows={2}
        placeholder="Nội dung câu hỏi — công thức viết trong $…$"
        className={`${inputCls} font-mono text-xs`}
      />
      {preview && (
        <div className="rounded-xl border border-white/10 bg-black/30 p-3">
          <ContentHtml html={q.question} className="block text-sm text-slate-200" />
        </div>
      )}

      {q.type === "multiple_choice" && (
        <div className="space-y-2">
          {q.options.map((option, i) => (
            <div key={i} className="flex items-start gap-2">
              <button
                type="button"
                onClick={() => onChange({ ...q, answer: i })}
                title="Đánh dấu đây là đáp án đúng"
                className={`mt-0.5 h-8 w-8 shrink-0 rounded-lg text-sm font-bold ${
                  q.answer === i ? "bg-emerald-500 text-white" : "bg-white/10 text-slate-400 hover:bg-white/20"
                }`}
              >
                {LETTERS[i]}
              </button>
              <input
                value={option}
                onChange={(e) => {
                  const options = [...q.options];
                  options[i] = e.target.value;
                  onChange({ ...q, options });
                }}
                placeholder={`Phương án ${LETTERS[i]}`}
                className={`${inputCls} font-mono text-xs`}
              />
            </div>
          ))}
        </div>
      )}

      {q.type === "true_false" && (
        <div className="space-y-2">
          {q.statements.map((s, i) => (
            <div key={i} className="grid gap-2 sm:grid-cols-[28px_minmax(0,1fr)_auto]">
              <span className="pt-2 text-sm font-bold text-slate-500">{String.fromCharCode(97 + i)})</span>
              <input
                value={s.text}
                onChange={(e) => {
                  const statements = q.statements.map((st, k) => (k === i ? { ...st, text: e.target.value } : st));
                  onChange({ ...q, statements });
                }}
                placeholder="Nội dung ý"
                className={`${inputCls} font-mono text-xs`}
              />
              <button
                type="button"
                onClick={() => {
                  const statements = q.statements.map((st, k) => (k === i ? { ...st, answer: !st.answer } : st));
                  onChange({ ...q, statements });
                }}
                className={`rounded-xl px-4 py-2 text-xs font-bold ${
                  s.answer ? "bg-emerald-500/15 text-emerald-300" : "bg-red-500/15 text-red-300"
                }`}
              >
                {s.answer ? "Đúng" : "Sai"}
              </button>
            </div>
          ))}
        </div>
      )}

      {q.type === "short_answer" && (
        <label className="block text-xs font-semibold text-amber-200">
          Đáp án (tối đa 4 ký tự, dùng dấu phẩy thập phân)
          <input
            value={q.answer}
            onChange={(e) => onChange({ ...q, answer: e.target.value })}
            placeholder="vd: 2,5"
            className={`${inputCls} mt-1 max-w-[160px]`}
          />
        </label>
      )}

      <textarea
        value={q.explanation}
        onChange={(e) => onChange({ ...q, explanation: e.target.value })}
        rows={2}
        placeholder="Lời giải cho học sinh xem sau khi nộp"
        className={`${inputCls} font-mono text-xs`}
      />

      <div className="grid gap-2 sm:grid-cols-2">
        <label className="text-[11px] font-semibold text-slate-400">
          Chủ đề câu này (để thống kê chỗ hổng)
          <input
            value={q.topic ?? ""}
            onChange={(e) => onChange({ ...q, topic: e.target.value })}
            list={topicOptions.length ? "exam-draft-topic-options" : undefined}
            placeholder="vd: Nêu được định nghĩa từ trường"
            className={`${inputCls} mt-1`}
          />
          {topicOptions.length > 0 && index === 0 && (
            <datalist id="exam-draft-topic-options">
              {topicOptions.map((n) => (
                <option key={n} value={n} />
              ))}
            </datalist>
          )}
        </label>
        <label className="text-[11px] font-semibold text-slate-400">
          Dạng
          <select
            value={q.form ?? ""}
            onChange={(e) => onChange({ ...q, form: e.target.value as QuestionForm | "" })}
            className={`${inputCls} mt-1 bg-panel`}
          >
            <option value="">Chưa phân loại</option>
            <option value="ly_thuyet">Lý thuyết</option>
            <option value="bai_tap">Bài tập</option>
          </select>
        </label>
      </div>
    </article>
  );
}
