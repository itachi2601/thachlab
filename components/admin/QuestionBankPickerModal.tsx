"use client";

import { useEffect, useMemo, useState } from "react";
import { Search, X } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtmlLazy";
import { useToast } from "@/components/ui/Toast";
import { DIFFICULTY_LABELS, QUESTION_FORM_LABELS, type Difficulty, type ExamQuestion } from "@/features/exams/types";
import { TYPE_SHORT } from "@/features/lessons/types";
import { fetchQuestionTopics, lessonTopics, outcomesOf, type QuestionTopic } from "@/services/analytics";
import { fetchBankQuestions, toExamQuestion, type BankQuestion } from "@/services/question-bank";

const inputCls =
  "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const selectCls = `${inputCls} bg-panel`;

/** Chuẩn hoá nội dung câu để so trùng — bỏ thẻ HTML, khoảng trắng thừa, không phân biệt hoa/thường. */
export function normalizeQuestionText(html: string): string {
  return html
    .replace(/<img[^>]*alt="([^"]*)"[^>]*>/g, " $1 ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

export interface QuestionBankPickerModalProps {
  open: boolean;
  onClose: () => void;
  /** Khối để lọc ngân hàng ("10"/"11"/"12"/"9") — không mở được nếu chưa rõ khối. */
  grade: string | null;
  /** Nội dung câu (đã chuẩn hoá qua normalizeQuestionText) đang có sẵn trong đề — loại khỏi danh sách để khỏi chọn trùng. */
  excludeTexts: Set<string>;
  /** "add": chọn nhiều câu để thêm vào cuối đề. "swap": bấm 1 câu là thay ngay, đóng luôn. */
  mode: "add" | "swap";
  /** Khi mode=swap: lọc sẵn theo loại câu đang thay cho hợp lý (thầy vẫn đổi lại được). */
  initialQtype?: ExamQuestion["type"];
  onConfirm: (questions: ExamQuestion[]) => void;
}

/** Bảng chọn câu từ Ngân hàng câu hỏi — dùng chung để "Thêm câu" (nhiều câu) và
 * "Đổi câu khác" (một câu) ngay tại trang Đăng đề, sau khi đã xem/soạn xong đề. */
export default function QuestionBankPickerModal({
  open,
  onClose,
  grade,
  excludeTexts,
  mode,
  initialQtype,
  onConfirm,
}: QuestionBankPickerModalProps) {
  const toast = useToast();
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [topicId, setTopicId] = useState<number | "">("");
  const [qtype, setQtype] = useState<ExamQuestion["type"] | "">(initialQtype ?? "");
  const [difficulty, setDifficulty] = useState<Difficulty | "all">("all");
  const [search, setSearch] = useState("");
  const [debounced, setDebounced] = useState("");
  const [items, setItems] = useState<BankQuestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [picked, setPicked] = useState<Set<number>>(new Set());

  // Mỗi lần bảng MỞ LẠI (không phải mỗi lần render) thì xoá bộ lọc/lựa chọn cũ —
  // "điều chỉnh state theo prop lúc render" (như Modal.tsx dùng chung), tránh setState
  // đồng bộ trong effect (react-hooks/set-state-in-effect).
  const [prevOpen, setPrevOpen] = useState(open);
  if (open && !prevOpen) {
    setPrevOpen(open);
    setPicked(new Set());
    setQtype(initialQtype ?? "");
    setTopicId("");
    setDifficulty("all");
    setSearch("");
  } else if (open !== prevOpen) {
    setPrevOpen(open);
  }

  useEffect(() => {
    const t = setTimeout(() => setDebounced(search), 300);
    return () => clearTimeout(t);
  }, [search]);

  useEffect(() => {
    if (!open || !grade) return;
    fetchQuestionTopics(grade)
      .then(setTopics)
      .catch(() => setTopics([]));
  }, [open, grade]);

  const parents = useMemo(
    () => lessonTopics(topics).sort((a, b) => a.sortOrder - b.sortOrder || a.name.localeCompare(b.name, "vi")),
    [topics],
  );

  useEffect(() => {
    if (!open || !grade) return;
    let cancelled = false;
    queueMicrotask(() => {
      if (!cancelled) setLoading(true);
    });
    fetchBankQuestions({
      grade,
      topicIds: topicId === "" ? undefined : [topicId],
      qtype: qtype || undefined,
      difficulty,
      search: debounced,
      limit: 100,
    })
      .then((rows) => {
        if (cancelled) return;
        setItems(rows.filter((r) => !excludeTexts.has(normalizeQuestionText(r.question.question))));
      })
      .catch((e) => {
        if (cancelled) return;
        toast("error", e instanceof Error ? e.message : String(e));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
    // excludeTexts đổi theo mỗi lần thêm/bớt câu trong đề — không cần lọc lại từ server, chỉ lọc khi tải mới.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, grade, topicId, qtype, difficulty, debounced]);

  if (!open) return null;

  function toggle(id: number) {
    if (mode === "swap") {
      const q = items.find((x) => x.id === id);
      if (q) onConfirm([toExamQuestion(q)]);
      return;
    }
    setPicked((s) => {
      const next = new Set(s);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function confirmAdd() {
    const chosen = items.filter((q) => picked.has(q.id));
    if (!chosen.length) return;
    onConfirm(chosen.map(toExamQuestion));
  }

  return (
    <div
      className="fixed inset-0 z-100 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm"
      onClick={onClose}
      role="presentation"
    >
      <div
        className="flex max-h-[85vh] w-full max-w-3xl flex-col rounded-2xl border border-white/10 bg-panel shadow-2xl"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <div className="flex items-center gap-2 border-b border-white/10 p-4">
          <span className="text-sm font-semibold text-white">
            {mode === "swap" ? "Đổi câu khác từ Ngân hàng câu hỏi" : "Thêm câu từ Ngân hàng câu hỏi"}
          </span>
          {mode === "swap" && <span className="text-xs text-slate-400">— bấm vào câu muốn dùng để thay ngay</span>}
          <button type="button" onClick={onClose} className="ml-auto rounded p-1 text-slate-400 hover:text-white" aria-label="Đóng">
            <X size={18} />
          </button>
        </div>

        {!grade ? (
          <p className="p-6 text-center text-sm text-slate-500">Chưa rõ khối (chọn Lớp ở mục 3) nên chưa lọc được ngân hàng.</p>
        ) : (
          <>
            <div className="flex flex-wrap items-center gap-2 border-b border-white/10 p-3">
              <select
                value={topicId}
                onChange={(e) => setTopicId(e.target.value ? Number(e.target.value) : "")}
                className={`${selectCls} max-w-[220px]`}
              >
                <option value="">— mọi chủ đề —</option>
                {parents.map((p) => (
                  <optgroup key={p.id} label={p.name}>
                    <option value={p.id}>{p.name} (cả bài)</option>
                    {outcomesOf(topics, p.id).map((o) => (
                      <option key={o.id} value={o.id}>
                        {o.name}
                      </option>
                    ))}
                  </optgroup>
                ))}
              </select>
              <select value={qtype} onChange={(e) => setQtype(e.target.value as ExamQuestion["type"] | "")} className={selectCls}>
                <option value="">Mọi dạng câu</option>
                <option value="multiple_choice">Trắc nghiệm A–D</option>
                <option value="true_false">Đúng / Sai</option>
                <option value="short_answer">Trả lời ngắn</option>
                <option value="essay">Tự luận</option>
              </select>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value as Difficulty | "all")}
                className={selectCls}
              >
                <option value="all">Mọi mức độ</option>
                <option value="de">Dễ</option>
                <option value="trung-binh">Trung bình</option>
                <option value="kho">Khó</option>
                <option value="">Chưa phân loại</option>
              </select>
              <label className="relative ml-auto">
                <Search size={14} className="pointer-events-none absolute left-2 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Tìm nội dung câu…"
                  className={`${inputCls} w-52 pl-7`}
                />
              </label>
            </div>

            <div className="flex-1 overflow-y-auto p-3">
              {loading ? (
                <p className="p-6 text-center text-sm text-slate-500">Đang tải…</p>
              ) : items.length === 0 ? (
                <p className="p-6 text-center text-sm text-slate-500">Không có câu nào khớp bộ lọc.</p>
              ) : (
                <ul className="space-y-2">
                  {items.map((q) => (
                    <li
                      key={q.id}
                      onClick={() => toggle(q.id)}
                      className={`cursor-pointer rounded-xl border p-3 text-sm transition ${
                        picked.has(q.id) ? "border-primary bg-primary/10" : "border-white/10 hover:border-white/25"
                      }`}
                    >
                      <div className="mb-1 flex flex-wrap items-center gap-2 text-[11px] text-slate-400">
                        <span className="rounded bg-white/10 px-1.5 text-slate-300">{TYPE_SHORT[q.qtype] ?? q.qtype}</span>
                        {q.topicName && <span className="rounded-full bg-white/10 px-2 py-0.5">{q.topicName}</span>}
                        {q.difficulty && <span>{DIFFICULTY_LABELS[q.difficulty]}</span>}
                        {q.form && <span className="text-blue-300">{QUESTION_FORM_LABELS[q.form]}</span>}
                      </div>
                      <ContentHtml html={q.question.question} className="text-slate-200" />
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {mode === "add" && (
              <div className="flex items-center gap-3 border-t border-white/10 p-3">
                <span className="text-xs text-slate-400">Đã chọn {picked.size} câu</span>
                <button
                  type="button"
                  onClick={confirmAdd}
                  disabled={picked.size === 0}
                  className="admin-btn admin-btn--primary ml-auto disabled:opacity-40"
                >
                  Thêm {picked.size || ""} câu vào đề
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
