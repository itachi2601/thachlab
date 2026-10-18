"use client";

import { useLayoutEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { ChevronDown, ChevronUp, Database, PencilLine, Repeat, Sparkles, Trash2, Undo2 } from "lucide-react";
import QuestionBankPickerModal, { normalizeQuestionText } from "@/components/admin/QuestionBankPickerModal";
import { useToast } from "@/components/ui/Toast";
import type {
  ExamQuestion,
  MultipleChoiceQuestion,
  QuestionForm,
  ShortAnswerQuestion,
  TrueFalseQuestion,
} from "@/features/exams/types";
import { classifyQuestionTagsBatched } from "@/services/ai-classify";
import { editableToHtml, htmlToEditable, questionTextForAi } from "@/services/exam-question-text";
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

/** Ô một ý/phương án: tự giãn theo nội dung nên công thức dài không bị cắt; Enter không xuống dòng (ý luôn là một dòng). */
function AutoText({
  value,
  onChange,
  placeholder,
}: {
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
}) {
  const ref = useRef<HTMLTextAreaElement>(null);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${el.scrollHeight}px`;
  }, [value]);
  return (
    <textarea
      ref={ref}
      rows={1}
      value={value}
      onChange={(e) => onChange(e.target.value.replace(/\n/g, " "))}
      onKeyDown={(e) => {
        if (e.key === "Enter") e.preventDefault();
      }}
      placeholder={placeholder}
      className={`${inputCls} resize-none overflow-hidden font-mono text-xs leading-5`}
    />
  );
}

export default function ExamDraftEditor({
  bundle,
  onChange,
  topicOptions = [],
  aiTopicCandidates = [],
  grade = null,
  renderPreview,
}: {
  bundle: LessonBundle;
  onChange: (next: LessonBundle) => void;
  /** Tên yêu cầu cần đạt trong danh mục — gợi ý cho ô "Chủ đề câu này". */
  topicOptions?: string[];
  /** YCCĐ của đúng bài đang chọn — danh mục đóng cho AI gắn nhãn (hẹp hơn topicOptions). */
  aiTopicCandidates?: string[];
  /** Khối để lọc Ngân hàng câu hỏi khi "Thêm câu"/"Đổi câu khác" — null thì ẩn 2 nút đó. */
  grade?: string | null;
  /** Vẽ câu đúng như học sinh thấy (thẻ xem trước) — mỗi câu hiện thẻ này, nút "Sửa" mở ô sửa ngay dưới nó. */
  renderPreview: (q: ExamQuestion, index: number) => ReactNode;
}) {
  const toast = useToast();
  // Câu đang mở ô sửa (một câu một lúc) — nằm ở đây, không ở thẻ, để đi theo câu khi đổi chỗ/xoá.
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  const [aiBusy, setAiBusy] = useState(false);
  const [aiProgress, setAiProgress] = useState<{ done: number; total: number } | null>(null);
  const questions = bundle.exam.questions;
  // "add": mở bảng chọn nhiều câu để thêm cuối đề. { index }: đang thay đúng 1 câu tại vị trí đó.
  const [bankPicker, setBankPicker] = useState<{ mode: "add" } | { mode: "swap"; index: number } | null>(null);
  const excludeTexts = useMemo(
    () => new Set(questions.map((q) => normalizeQuestionText(q.question))),
    [questions],
  );

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
    if (openIndex === index) setOpenIndex(target);
    else if (openIndex === target) setOpenIndex(index);
  }
  function remove(index: number) {
    setQuestions(questions.filter((_, k) => k !== index));
    if (openIndex === index) setOpenIndex(null);
    else if (openIndex !== null && openIndex > index) setOpenIndex(openIndex - 1);
  }

  const aiTargets = questions
    .map((_, i) => i)
    .filter(
      (i) =>
        !(questions[i].topic ?? "").trim() || !questions[i].form || !questions[i].difficulty,
    );
  const aiAvailable = aiTopicCandidates.length > 0 && aiTargets.length > 0;

  async function runAutoTag() {
    if (!aiAvailable || aiBusy) return;
    setAiBusy(true);
    try {
      const items = aiTargets.map((i) => ({ index: i, text: questionTextForAi(questions[i]) }));
      const results = await classifyQuestionTagsBatched(aiTopicCandidates, items, (done, total) => setAiProgress({ done, total }));
      let next = questions;
      for (const r of results) {
        next = next.map((q, i) =>
          i === r.index
            ? {
                ...q,
                topic: r.topic ?? q.topic,
                form: r.form ?? q.form,
                // AI gợi ý độ khó khi câu chưa có — gắn tay đè lên (difficultySource: "gv")
                // sẽ không bị AI ghi đè lại lần sau vì aiTargets chỉ nhắm câu còn thiếu.
                difficulty: q.difficulty ? q.difficulty : (r.difficulty ?? q.difficulty),
                difficultySource: q.difficulty ? q.difficultySource : r.difficulty ? "ai" : q.difficultySource,
              }
            : q,
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
      setAiProgress(null);
    }
  }

  const incomplete = questions.filter((q) => problems(q).length > 0).length;

  return (
    <div className="space-y-4">
      {/* Tên đề + Thời gian do khối cha (ExamSection) giữ — một chỗ duy nhất, không lặp lại ở đây
          (thầy báo 10/10/2026: trước đây hai nơi cùng có 2 ô này nên phải điền hai lần). */}
      <div className="grid gap-3 sm:grid-cols-2">
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
          Đã chọn <b className="text-white">{questions.length}</b> câu
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
            className="ml-auto inline-flex items-center gap-1 rounded-lg bg-primary/20 px-2 py-1 text-[12px] font-semibold text-primary hover:bg-primary/30 disabled:opacity-50"
          >
            <Sparkles size={12} /> {aiBusy ? `Đang phân loại… ${aiProgress ? `${aiProgress.done}/${aiProgress.total} câu` : ""}` : `AI gắn nhãn (${aiTargets.length} câu)`}
          </button>
        )}
      </div>

      <div className="space-y-4">
        {questions.map((q, i) => (
          <QuestionCardEditor
            key={i}
            index={i}
            total={questions.length}
            q={q}
            preview={renderPreview(q, i)}
            open={openIndex === i}
            onToggle={() => setOpenIndex(openIndex === i ? null : i)}
            onChange={(next) => update(i, next)}
            topicOptions={topicOptions}
            onRemove={() => remove(i)}
            onMove={(delta) => move(i, delta)}
            onSwap={grade ? () => setBankPicker({ mode: "swap", index: i }) : undefined}
          />
        ))}
      </div>

      <div className="flex flex-wrap gap-2">
        {(Object.keys(TYPE_LABELS) as EditableType[]).map((type) => (
          <button
            key={type}
            type="button"
            onClick={() => {
              setQuestions([...questions, newQuestion(type)]);
              setOpenIndex(questions.length);
            }}
            className="admin-chip"
          >
            + {TYPE_LABELS[type]}
          </button>
        ))}
        {grade && (
          <button type="button" onClick={() => setBankPicker({ mode: "add" })} className="admin-chip">
            <Database size={14} /> + Thêm từ ngân hàng câu hỏi
          </button>
        )}
      </div>

      <QuestionBankPickerModal
        open={bankPicker !== null}
        onClose={() => setBankPicker(null)}
        grade={grade}
        excludeTexts={excludeTexts}
        mode={bankPicker?.mode ?? "add"}
        initialQtype={bankPicker?.mode === "swap" ? questions[bankPicker.index]?.type : undefined}
        onConfirm={(picked) => {
          if (bankPicker?.mode === "swap") {
            update(bankPicker.index, picked[0]);
            toast("success", "Đã đổi câu.");
          } else {
            setQuestions([...questions, ...picked]);
            toast("success", `Đã thêm ${picked.length} câu.`);
          }
          setBankPicker(null);
        }}
      />
    </div>
  );
}

function QuestionCardEditor({
  q,
  index,
  total,
  preview,
  open,
  onToggle,
  onChange,
  topicOptions,
  onRemove,
  onMove,
  onSwap,
}: {
  q: ExamQuestion;
  index: number;
  total: number;
  /** Thẻ xem trước của câu (vẽ ở ExamSection). */
  preview: ReactNode;
  open: boolean;
  onToggle: () => void;
  onChange: (next: ExamQuestion) => void;
  topicOptions: string[];
  onRemove: () => void;
  onMove: (delta: number) => void;
  /** Mở bảng Ngân hàng câu hỏi để thay câu này bằng câu khác — undefined khi chưa rõ khối. */
  onSwap?: () => void;
}) {
  const issues = problems(q);
  const type = q.type === "essay" ? "short_answer" : q.type;
  // Bản của câu lúc bấm "Sửa" — để "Hoàn tác câu này" đưa về đúng bản đó (ô nhập React không nhận Cmd+Z).
  const [snapshot, setSnapshot] = useState<string | null>(null);
  const changed = open && snapshot !== null && snapshot !== JSON.stringify(q);
  const btn = "inline-flex items-center gap-1 rounded-lg px-2 py-1.5 text-xs font-semibold text-slate-300 hover:bg-white/10 hover:text-white disabled:opacity-30";

  return (
    <article id={`exam-q-${index}`} className="space-y-2">
      {preview}
      <div className="flex flex-wrap items-center gap-1">
        <button
          type="button"
          onClick={() => {
            if (!open) setSnapshot(JSON.stringify(q));
            onToggle();
          }}
          className={`${btn} ${open ? "bg-primary/20 text-primary" : ""}`}
        >
          <PencilLine size={14} /> {open ? "Xong" : "Sửa"}
        </button>
        {changed && (
          <button
            type="button"
            onClick={() => onChange(JSON.parse(snapshot as string) as ExamQuestion)}
            className={btn}
            title="Bỏ mọi thay đổi của câu này kể từ lúc bấm Sửa"
          >
            <Undo2 size={14} /> Hoàn tác câu này
          </button>
        )}
        {onSwap && (
          <button type="button" onClick={onSwap} className={btn} title="Đổi câu khác từ ngân hàng câu hỏi">
            <Repeat size={14} /> Đổi câu
          </button>
        )}
        <button type="button" onClick={() => onMove(-1)} disabled={index === 0} className={btn} aria-label="Đưa lên">
          <ChevronUp size={14} />
        </button>
        <button type="button" onClick={() => onMove(1)} disabled={index === total - 1} className={btn} aria-label="Đưa xuống">
          <ChevronDown size={14} />
        </button>
        <button type="button" onClick={onRemove} className={`${btn} ml-auto text-red-300 hover:text-red-200`}>
          <Trash2 size={14} /> Xóa
        </button>
      </div>

      {open && (
    <div
      className={`space-y-3 rounded-2xl border p-4 ${
        issues.length ? "border-amber-500/40 bg-amber-500/[.04]" : "border-white/10 bg-white/[.03]"
      }`}
    >
      <label className="flex items-center gap-2 text-xs font-semibold text-slate-400">
        Loại câu
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
      </label>

      {issues.length > 0 && <p className="text-[12px] text-amber-300">Còn thiếu: {issues.join(" · ")}</p>}

      <textarea
        value={htmlToEditable(q.question)}
        onChange={(e) => onChange({ ...q, question: editableToHtml(e.target.value) })}
        rows={2}
        placeholder="Nội dung câu hỏi — công thức viết trong $…$"
        className={`${inputCls} font-mono text-xs`}
      />
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
              <AutoText
                value={htmlToEditable(option).replace(/\n/g, " ")}
                onChange={(v) => {
                  const options = [...q.options];
                  options[i] = v;
                  onChange({ ...q, options });
                }}
                placeholder={`Phương án ${LETTERS[i]}`}
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
              <AutoText
                value={htmlToEditable(s.text).replace(/\n/g, " ")}
                onChange={(v) => {
                  const statements = q.statements.map((st, k) => (k === i ? { ...st, text: v } : st));
                  onChange({ ...q, statements });
                }}
                placeholder="Nội dung ý"
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
        value={htmlToEditable(q.explanation)}
        onChange={(e) => onChange({ ...q, explanation: editableToHtml(e.target.value) })}
        rows={2}
        placeholder="Lời giải cho học sinh xem sau khi nộp"
        className={`${inputCls} font-mono text-xs`}
      />

      <div className="grid gap-2 sm:grid-cols-2">
        <label className="text-[12px] font-semibold text-slate-400">
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
        <label className="text-[12px] font-semibold text-slate-400">
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
    </div>
      )}
    </article>
  );
}
