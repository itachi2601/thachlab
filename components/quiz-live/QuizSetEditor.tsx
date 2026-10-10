"use client";

import { useMemo, useState } from "react";
import { ArrowDown, ArrowUp, Trash2 } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtmlLazy";
import { useToast } from "@/components/ui/Toast";
import { makeTypedQuestion, parseQuizText, quizQuestionIssue, type QuizQuestion } from "@/features/quiz-live/text";
import { quizErrorText } from "@/features/quiz-live/types";
import { fetchQuestionTopics, type QuestionTopic } from "@/services/analytics";
import { saveQuizSet, setToBank, type QuizSet } from "@/services/quiz-live";
import QuizBankPicker from "./QuizBankPicker";
import { OPTION_STYLE } from "./shared";

const field = "w-full rounded-xl border border-line-strong bg-surface-2 px-3 py-2.5 text-sm text-ink placeholder:text-muted focus:border-primary focus:outline-none";
const btn = "min-h-11 rounded-xl border border-line px-4 text-sm font-semibold text-ink hover:bg-surface-2";

const SAMPLE = `Câu 1. Đơn vị của lực trong SI là gì?
A. Jun
B. Niutơn *
C. Oát
D. Pascal
Giải thích: 1 N = 1 kg·m/s².

Câu 2. Vật rơi tự do thì gia tốc phụ thuộc vào gì?
A. Khối lượng vật
B. Hình dạng vật
C. Nơi đặt vật
Đáp án: C`;

/** Soạn bộ câu: 3 cách thêm — gõ từng câu, dán nhiều câu một lúc, hoặc lấy từ ngân hàng. Giữ đơn giản cho trợ giảng. */
export default function QuizSetEditor({
  initial,
  onBack,
  onSaved,
}: {
  initial: QuizSet | null;
  onBack: () => void;
  onSaved: (id: number, play: boolean) => void;
}) {
  const toast = useToast();
  const [id, setId] = useState<number | null>(initial?.id ?? null);
  const [title, setTitle] = useState(initial?.title ?? "");
  const [grade, setGrade] = useState(initial?.grade ?? "");
  const [qs, setQs] = useState<QuizQuestion[]>(initial?.questions ?? []);
  const [mode, setMode] = useState<"none" | "paste" | "bank">("none");
  const [pasteText, setPasteText] = useState("");
  const [saving, setSaving] = useState(false);
  const [bankOpen, setBankOpen] = useState(false);

  const parsed = useMemo(() => (pasteText.trim() ? parseQuizText(pasteText) : null), [pasteText]);
  const issues = qs.map(quizQuestionIssue);
  const problems = issues.filter(Boolean).length;
  const bankIds = useMemo(() => new Set(qs.map((q) => q.bank_id).filter((x): x is number => typeof x === "number")), [qs]);
  const typedCount = qs.filter((q) => !q.bank_id).length;

  const patch = (i: number, fn: (q: QuizQuestion) => QuizQuestion) => setQs((a) => a.map((q, k) => (k === i ? fn(q) : q)));
  const move = (i: number, d: -1 | 1) =>
    setQs((a) => {
      const j = i + d;
      if (j < 0 || j >= a.length) return a;
      const b = [...a];
      [b[i], b[j]] = [b[j], b[i]];
      return b;
    });

  function editTyped(i: number, change: Partial<{ question: string; options: string[]; explanation: string }>, correct?: number) {
    patch(i, (q) => {
      const t = { question: "", options: ["", "", "", ""], explanation: "", ...q.typed, ...change };
      return makeTypedQuestion(t, correct ?? q.typed?.correct ?? -1);
    });
  }

  async function save(play: boolean) {
    if (!title.trim()) return toast("warning", "Đặt tên cho bộ câu trước.");
    if (qs.length === 0) return toast("warning", "Bộ câu chưa có câu nào.");
    if (play && problems) return toast("warning", `Còn ${problems} câu chưa đủ (đáp án trống hoặc chưa chọn đáp án đúng).`);
    setSaving(true);
    try {
      const newId = await saveQuizSet(id, { title, grade, questions: qs });
      setId(newId);
      toast("success", "Đã lưu bộ câu");
      onSaved(newId, play);
    } catch (e) {
      toast("error", quizErrorText(e));
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-5">
      <button onClick={onBack} className="text-sm text-primary underline">← Danh sách bộ câu</button>
      <div className="grid gap-3 sm:grid-cols-[1fr_9rem]">
        <input aria-label="Tên bộ câu" className={field} placeholder="Tên bộ câu, ví dụ: Ôn nhanh Định luật Newton" maxLength={120} value={title} onChange={(e) => setTitle(e.target.value)} />
        <select aria-label="Khối" className={`${field} bg-panel`} value={grade} onChange={(e) => setGrade(e.target.value)}>
          <option value="">Khối: không rõ</option>
          {["9", "10", "11", "12"].map((g) => <option key={g} value={g}>Lớp {g}</option>)}
        </select>
      </div>

      <div className="flex flex-wrap gap-2">
        <button className={btn} onClick={() => setQs((a) => [...a, makeTypedQuestion({ question: "", options: ["", "", "", ""], explanation: "" }, -1)])}>+ Gõ một câu</button>
        <button className={btn} onClick={() => setMode(mode === "paste" ? "none" : "paste")}>Dán nhiều câu</button>
        <button className={btn} onClick={() => setBankOpen((v) => !v)}>Lấy từ ngân hàng</button>
      </div>

      {mode === "paste" && (
        <section className="space-y-3 rounded-2xl border border-line bg-surface-2 p-4">
          <p className="text-sm text-ink">Dán câu hỏi vào đây. Đánh dấu đáp án đúng bằng dấu <b>*</b> sau đáp án, hoặc thêm dòng <b>Đáp án: B</b>. Công thức viết trong $…$.</p>
          <textarea className={`${field} min-h-48 font-mono`} value={pasteText} onChange={(e) => setPasteText(e.target.value)} placeholder={SAMPLE} />
          {parsed && (
            <div className="space-y-1 text-sm">
              <p className="text-ink">Đọc được <b>{parsed.questions.length}</b> câu.</p>
              {parsed.warnings.map((w) => <p key={w} className="text-warn">⚠ {w}</p>)}
            </div>
          )}
          <button
            disabled={!parsed || parsed.questions.length === 0}
            className="min-h-11 rounded-xl bg-primary px-5 font-bold text-white disabled:opacity-40"
            onClick={() => { setQs((a) => [...a, ...(parsed?.questions ?? [])]); setPasteText(""); setMode("none"); }}
          >
            Thêm {parsed?.questions.length ?? 0} câu vào bộ
          </button>
        </section>
      )}

      {bankOpen && (
        <QuizBankPicker defaultGrade={grade} existingBankIds={bankIds} onAdd={(add) => setQs((a) => [...a, ...add])} onClose={() => setBankOpen(false)} />
      )}

      <ol className="space-y-3">
        {qs.map((q, i) => (
          <li key={i} className="rounded-2xl border border-line bg-panel p-4">
            <div className="mb-3 flex items-center justify-between gap-2">
              <span className="text-sm font-bold text-ink">
                Câu {i + 1} <span className="ml-1 font-normal text-muted">{q.bank_id ? "· từ ngân hàng" : "· tự gõ"}</span>
                {issues[i] && <span className="ml-2 text-xs font-semibold text-warn">⚠ {issues[i]}</span>}
              </span>
              <span className="flex gap-1">
                <IconBtn label="Lên" onClick={() => move(i, -1)}><ArrowUp size={16} /></IconBtn>
                <IconBtn label="Xuống" onClick={() => move(i, 1)}><ArrowDown size={16} /></IconBtn>
                <IconBtn label="Xoá câu" onClick={() => setQs((a) => a.filter((_, k) => k !== i))}><Trash2 size={16} /></IconBtn>
              </span>
            </div>
            {q.typed ? (
              <div className="space-y-2">
                <textarea aria-label={`Nội dung câu ${i + 1}`} className={`${field} min-h-20`} placeholder="Nội dung câu hỏi (công thức viết trong $…$)" value={q.typed.question} onChange={(e) => editTyped(i, { question: e.target.value })} />
                {q.typed.options.map((o, k) => (
                  <label key={k} className="flex items-center gap-2">
                    <input type="radio" name={`ans-${i}`} aria-label={`Đáp án ${OPTION_STYLE[k].letter} là đúng`} className="size-5 shrink-0" checked={q.typed?.correct === k} onChange={() => editTyped(i, {}, k)} />
                    <span className="w-5 text-sm font-bold text-ink">{OPTION_STYLE[k].letter}</span>
                    <input className={field} placeholder={`Đáp án ${OPTION_STYLE[k].letter}${k >= 2 ? " (bỏ trống nếu không dùng)" : ""}`} value={o} onChange={(e) => editTyped(i, { options: (q.typed?.options ?? []).map((x, j) => (j === k ? e.target.value : x)) })} />
                  </label>
                ))}
                <input className={field} placeholder="Giải thích ngắn sau khi lộ đáp án (không bắt buộc)" value={q.typed.explanation} onChange={(e) => editTyped(i, { explanation: e.target.value })} />
                <p className="text-xs text-muted">Chọn nút tròn bên trái đáp án đúng.</p>
              </div>
            ) : (
              <div className="space-y-2 text-sm text-ink">
                <ContentHtml html={q.question} />
                <ul className="grid gap-1 sm:grid-cols-2">
                  {q.options.map((o, k) => (
                    <li key={k} className={`rounded-lg px-3 py-1.5 ${q.answer === k ? "bg-primary-soft font-semibold text-ok" : "bg-surface-2"}`}>
                      <b className="mr-1">{OPTION_STYLE[k].letter}.</b><ContentHtml html={o} />
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </li>
        ))}
      </ol>
      {qs.length === 0 && <p className="text-sm text-muted">Chưa có câu nào — chọn một trong ba cách thêm ở trên.</p>}

      {/* Bỏ hết câu trống trước khi lưu? Không — giữ nguyên để trợ giảng sửa tiếp; chỉ chặn khi bấm "Lưu & chơi". */}
      <div className="flex flex-wrap gap-2">
        <button disabled={saving} onClick={() => void save(false)} className={btn}>Lưu</button>
        <button disabled={saving} onClick={() => void save(true)} className="min-h-11 rounded-xl bg-primary px-5 font-bold text-white disabled:opacity-50">Lưu & chơi</button>
      </div>

      {id !== null && typedCount > 0 && <BankExport setId={id} grade={grade} typedCount={typedCount} />}
    </div>
  );
}

function IconBtn({ label, onClick, children }: { label: string; onClick: () => void; children: React.ReactNode }) {
  return (
    <button aria-label={label} title={label} onClick={onClick} className="grid size-9 place-items-center rounded-lg text-ink hover:bg-surface-2">
      {children}
    </button>
  );
}

/** Đưa các câu tự gõ (đã LƯU) vào ngân hàng, gắn khối/chủ đề/dạng để sau này lọc được. */
function BankExport({ setId, grade, typedCount }: { setId: number; grade: string; typedCount: number }) {
  const toast = useToast();
  const [open, setOpen] = useState(false);
  const [g, setG] = useState(grade || "10");
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [topic, setTopic] = useState("");
  const [form, setForm] = useState("");
  const [busy, setBusy] = useState(false);

  async function openIt() {
    setOpen(true);
    try {
      setTopics(await fetchQuestionTopics(g));
    } catch {
      setTopics([]);
    }
  }
  async function changeGrade(v: string) {
    setG(v);
    setTopic("");
    try {
      setTopics(await fetchQuestionTopics(v));
    } catch {
      setTopics([]);
    }
  }
  async function run() {
    setBusy(true);
    try {
      const r = await setToBank(setId, g, topic, form);
      toast("success", `Đã đưa ${r.added} câu vào ngân hàng${r.skipped ? ` (bỏ ${r.skipped} câu đã có/không áp dụng)` : ""}`);
      setOpen(false);
    } catch (e) {
      toast("error", quizErrorText(e));
    } finally {
      setBusy(false);
    }
  }

  if (!open)
    return (
      <div className="rounded-2xl border border-dashed border-line p-4 text-sm text-ink">
        <p>Bộ này có {typedCount} câu tự gõ. Muốn dùng lại sau này, đưa vào ngân hàng câu hỏi:</p>
        <button onClick={() => void openIt()} className={`${btn} mt-2`}>Đưa câu tự gõ vào ngân hàng</button>
      </div>
    );
  return (
    <div className="space-y-3 rounded-2xl border border-line bg-surface-2 p-4">
      <p className="text-sm text-ink">Chỉ đưa {typedCount} câu tự gõ (đã lưu); câu lấy từ ngân hàng và câu trùng nội dung sẽ được bỏ qua. Nên gắn chủ đề để câu tìm được sau này.</p>
      <div className="grid gap-2 sm:grid-cols-3">
        <select aria-label="Khối" className={`${field} bg-panel`} value={g} onChange={(e) => void changeGrade(e.target.value)}>
          {["9", "10", "11", "12"].map((x) => <option key={x} value={x}>Lớp {x}</option>)}
        </select>
        <select aria-label="Chủ đề" className={`${field} bg-panel`} value={topic} onChange={(e) => setTopic(e.target.value)}>
          <option value="">Chưa gắn chủ đề</option>
          {topics.filter((t) => t.parentId === null).map((t) => <option key={t.id} value={t.name}>{t.name}</option>)}
        </select>
        <select aria-label="Dạng" className={`${field} bg-panel`} value={form} onChange={(e) => setForm(e.target.value)}>
          <option value="">Dạng: không rõ</option>
          <option value="ly_thuyet">Lý thuyết</option>
          <option value="bai_tap">Bài tập</option>
        </select>
      </div>
      <div className="flex gap-2">
        <button disabled={busy} onClick={() => void run()} className="min-h-11 rounded-xl bg-primary px-5 font-bold text-white disabled:opacity-50">Đưa vào ngân hàng</button>
        <button onClick={() => setOpen(false)} className={btn}>Huỷ</button>
      </div>
    </div>
  );
}
