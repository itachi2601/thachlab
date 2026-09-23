"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Archive,
  ArchiveRestore,
  ChevronDown,
  ChevronRight,
  Dices,
  FilePlus2,
  ListChecks,
  RefreshCw,
  Search,
  Trash2,
} from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import { useToast } from "@/components/ui/Toast";
import {
  DIFFICULTY_LABELS,
  QUESTION_FORM_LABELS,
  pickRandom,
  type Difficulty,
  type ExamQuestion,
  type QuestionForm,
} from "@/features/exams/types";
import { TYPE_SHORT } from "@/features/lessons/types";
import { fetchQuestionTopics, lessonTopics, outcomesOf, type QuestionTopic } from "@/services/analytics";
import {
  fetchBankQuestions,
  fetchBankQuestionsByIds,
  fetchBankTopicCounts,
  fetchBankUnknownGradeCount,
  readBasket,
  toExamQuestion,
  updateBankQuestion,
  updateBankQuestions,
  writeBasket,
  writeHandoff,
  type BankQuestion,
  type BankTopicCount,
} from "@/services/question-bank";

const GRADES = ["10", "11", "12", "9"];
const LETTERS = ["A", "B", "C", "D"];
const inputCls =
  "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const selectCls = `${inputCls} bg-panel`;
const btnCls =
  "admin-chip";

type Node =
  | { kind: "all" }
  | { kind: "untagged" }
  | { kind: "unknown-grade" }
  | { kind: "topic"; id: number; parent: boolean };

const QTYPE_OPTIONS: { value: ExamQuestion["type"] | ""; label: string }[] = [
  { value: "", label: "Mọi dạng" },
  { value: "multiple_choice", label: "Trắc nghiệm A–D" },
  { value: "true_false", label: "Đúng / Sai" },
  { value: "short_answer", label: "Trả lời ngắn" },
  { value: "essay", label: "Tự luận" },
];

export default function QuestionBankAdmin() {
  const toast = useToast();
  const router = useRouter();

  const [grade, setGrade] = useState("12");
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [counts, setCounts] = useState<BankTopicCount[]>([]);
  const [unknownGrade, setUnknownGrade] = useState(0);
  const [node, setNode] = useState<Node>({ kind: "all" });
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  const [form, setForm] = useState<QuestionForm | "">("");
  const [qtype, setQtype] = useState<ExamQuestion["type"] | "">("");
  const [difficulty, setDifficulty] = useState<Difficulty | "all">("all");
  const [showArchived, setShowArchived] = useState(false);
  const [search, setSearch] = useState("");
  const [debounced, setDebounced] = useState("");

  const [items, setItems] = useState<BankQuestion[]>([]);
  const [basket, setBasket] = useState<number[]>(() => (typeof window === "undefined" ? [] : readBasket()));
  const [basketItems, setBasketItems] = useState<BankQuestion[]>([]);
  const [basketOpen, setBasketOpen] = useState(false);
  const [randomN, setRandomN] = useState(10);
  const [bulkTopic, setBulkTopic] = useState("");

  useEffect(() => {
    const t = setTimeout(() => setDebounced(search), 300);
    return () => clearTimeout(t);
  }, [search]);

  const reloadTree = useCallback(() => {
    fetchQuestionTopics(grade).then(setTopics).catch(() => setTopics([]));
    fetchBankTopicCounts(grade).then(setCounts).catch(() => setCounts([]));
    fetchBankUnknownGradeCount().then(setUnknownGrade).catch(() => setUnknownGrade(0));
  }, [grade]);
  useEffect(reloadTree, [reloadTree]);

  const parents = useMemo(
    () => lessonTopics(topics).sort((a, b) => a.sortOrder - b.sortOrder || a.name.localeCompare(b.name, "vi")),
    [topics],
  );
  const countByTopic = useMemo(() => {
    const m = new Map<number | null, BankTopicCount>();
    for (const c of counts) m.set(c.topicId, c);
    return m;
  }, [counts]);
  const countOf = useCallback(
    (id: number | null) => {
      const c = countByTopic.get(id);
      return showArchived ? (c?.active ?? 0) + (c?.archived ?? 0) : (c?.active ?? 0);
    },
    [countByTopic, showArchived],
  );
  const subtreeCount = useCallback(
    (parent: QuestionTopic) => countOf(parent.id) + outcomesOf(topics, parent.id).reduce((s, o) => s + countOf(o.id), 0),
    [countOf, topics],
  );
  const totalCount = useMemo(() => counts.reduce((s, c) => s + (showArchived ? c.active + c.archived : c.active), 0), [counts, showArchived]);

  // Chủ đề đích để gắn nhãn: mọi YCCĐ + chủ đề tầng bài của khối, nhóm theo bài.
  const topicGroups = useMemo(
    () => parents.map((p) => ({ parent: p, outcomes: outcomesOf(topics, p.id) })),
    [parents, topics],
  );

  const topicIdsFilter = useMemo<(number | null)[] | undefined>(() => {
    if (node.kind === "all" || node.kind === "unknown-grade") return undefined;
    if (node.kind === "untagged") return [null];
    if (!node.parent) return [node.id];
    return [node.id, ...outcomesOf(topics, node.id).map((o) => o.id)];
  }, [node, topics]);

  const reloadItems = useCallback(() => {
    const req = fetchBankQuestions({
      grade: node.kind === "unknown-grade" ? "" : grade,
      topicIds: topicIdsFilter,
      form,
      qtype,
      difficulty,
      includeArchived: showArchived,
      search: debounced,
    });
    req
      .then((list) => setItems(node.kind === "unknown-grade" ? list.filter((q) => q.grade === "") : list))
      .catch((e) => toast("error", e instanceof Error ? e.message : String(e)));
  }, [grade, node, topicIdsFilter, form, qtype, difficulty, showArchived, debounced, toast]);
  useEffect(reloadItems, [reloadItems]);

  // Giỏ: giữ danh sách id trong sessionStorage, nạp nội dung khi mở.
  useEffect(() => {
    writeBasket(basket);
    if (!basketOpen) return;
    fetchBankQuestionsByIds(basket).then(setBasketItems).catch(() => setBasketItems([]));
  }, [basket, basketOpen]);
  const inBasket = useMemo(() => new Set(basket), [basket]);
  function toggleBasket(id: number) {
    setBasket((b) => (b.includes(id) ? b.filter((x) => x !== id) : [...b, id]));
  }
  function addRandom() {
    const pool = items.filter((q) => !inBasket.has(q.id) && !q.archived);
    const picked = pickRandom(pool, randomN).map((q) => q.id);
    if (!picked.length) return toast("warning", "Không còn câu nào để bốc trong danh sách này.");
    setBasket((b) => [...b, ...picked]);
    toast("success", `Đã thêm ${picked.length} câu vào giỏ.`);
  }

  async function patch(id: number, patchIn: Parameters<typeof updateBankQuestion>[1]) {
    // Gắn năng lực thì kèm khối đang xem: tên chủ đề chỉ duy nhất trong một khối.
    const p = patchIn.topicName !== undefined && patchIn.grade === undefined ? { ...patchIn, grade } : patchIn;
    try {
      await updateBankQuestion(id, p);
      setItems((list) =>
        list.map((q) =>
          q.id === id
            ? {
                ...q,
                topicName: p.topicName ?? q.topicName,
                form: p.form ?? q.form,
                difficulty: p.difficulty ?? q.difficulty,
                archived: p.archived ?? q.archived,
                grade: p.grade ?? q.grade,
              }
            : q,
        ),
      );
      if (p.topicName !== undefined || p.archived !== undefined || p.grade !== undefined) reloadTree();
      if (p.topicName !== undefined || p.grade !== undefined) reloadItems();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : String(e));
    }
  }

  async function bulkTag() {
    if (!basket.length) return;
    try {
      await updateBankQuestions(basket, { topicName: bulkTopic, grade });
      toast("success", `Đã gắn "${bulkTopic || "(bỏ nhãn)"}" cho ${basket.length} câu trong giỏ.`);
      reloadTree();
      reloadItems();
      setBasketItems([]);
      setBasketOpen(false);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : String(e));
    }
  }

  async function composeExam() {
    if (!basket.length) return;
    try {
      const list = await fetchBankQuestionsByIds(basket);
      const questions = list.map(toExamQuestion);
      writeHandoff({ title: "", grade, questions, bankIds: list.map((q) => q.id) });
      setBasket([]);
      router.push("/quan-tri/dang-de/");
    } catch (e) {
      toast("error", e instanceof Error ? e.message : String(e));
    }
  }

  const nodeTitle = (() => {
    if (node.kind === "all") return `Tất cả câu khối ${grade}`;
    if (node.kind === "untagged") return "Câu chưa gắn năng lực";
    if (node.kind === "unknown-grade") return "Câu chưa rõ khối";
    return topics.find((t) => t.id === node.id)?.name ?? "";
  })();

  return (
    <div className="space-y-5 pb-24">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="admin-lead max-w-2xl" style={{ marginTop: 0 }}>
            Mọi câu trong đề kiểm tra, đề thi, luyện tập và bài tập về nhà đều tự nạp vào đây, xếp theo năng lực cần
            đạt. Chọn câu vào giỏ rồi bấm <b>Soạn đề</b> — trang Đăng đề sẽ mở sẵn đề để chỉnh và gắn vào bài.
          </p>
        </div>
        <div className="flex gap-1 rounded-xl bg-white/5 p-1">
          {GRADES.map((g) => (
            <button
              key={g}
              type="button"
              onClick={() => {
                setGrade(g);
                setNode({ kind: "all" });
              }}
              className={`rounded-lg px-3 py-1.5 text-sm font-semibold ${grade === g ? "bg-primary text-white" : "text-slate-300 hover:bg-white/10"}`}
            >
              {g === "9" ? "KHTN 9" : `Lớp ${g}`}
            </button>
          ))}
        </div>
      </header>

      <div className="grid gap-5 lg:grid-cols-[300px_1fr]">
        {/* ===== Cây năng lực ===== */}
        <aside className="space-y-2 admin-card lg:sticky lg:top-4 lg:max-h-[calc(100vh-2rem)] lg:overflow-y-auto">
          <TreeRow active={node.kind === "all"} onClick={() => setNode({ kind: "all" })} label="Tất cả" count={totalCount} bold />
          <TreeRow
            active={node.kind === "untagged"}
            onClick={() => setNode({ kind: "untagged" })}
            label="Chưa gắn năng lực"
            count={countOf(null)}
            warn={countOf(null) > 0}
          />
          {unknownGrade > 0 && (
            <TreeRow
              active={node.kind === "unknown-grade"}
              onClick={() => setNode({ kind: "unknown-grade" })}
              label="Chưa rõ khối (mọi lớp)"
              count={unknownGrade}
              warn
            />
          )}
          <div className="my-2 border-t border-white/10" />
          {parents.length === 0 && (
            <p className="px-2 py-3 text-xs text-slate-500">
              Khối này chưa có chủ đề. Thêm ở <Link href="/quan-tri/chu-de" className="text-primary underline">Chủ đề câu hỏi</Link>.
            </p>
          )}
          {parents.map((p) => {
            const outcomes = outcomesOf(topics, p.id);
            const open = expanded.has(p.id);
            return (
              <div key={p.id}>
                <div className="flex items-center">
                  <button
                    type="button"
                    onClick={() =>
                      setExpanded((s) => {
                        const n = new Set(s);
                        if (n.has(p.id)) n.delete(p.id);
                        else n.add(p.id);
                        return n;
                      })
                    }
                    className="shrink-0 p-1 text-slate-500 hover:text-white"
                    aria-label={open ? "Thu gọn" : "Mở"}
                    disabled={outcomes.length === 0}
                  >
                    {outcomes.length === 0 ? <span className="inline-block w-4" /> : open ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                  </button>
                  <TreeRow
                    active={node.kind === "topic" && node.id === p.id}
                    onClick={() => setNode({ kind: "topic", id: p.id, parent: true })}
                    label={p.name}
                    count={subtreeCount(p)}
                    bold
                  />
                </div>
                {open &&
                  outcomes.map((o) => (
                    <div key={o.id} className="pl-6">
                      <TreeRow
                        active={node.kind === "topic" && node.id === o.id}
                        onClick={() => setNode({ kind: "topic", id: o.id, parent: false })}
                        label={o.name}
                        count={countOf(o.id)}
                      />
                    </div>
                  ))}
              </div>
            );
          })}
        </aside>

        {/* ===== Danh sách câu ===== */}
        <section className="min-w-0 space-y-3">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="mr-auto text-base font-semibold text-white">
              {nodeTitle} <span className="text-sm font-normal text-slate-500">· {items.length} câu</span>
            </h2>
            <button type="button" onClick={reloadItems} className={btnCls} title="Tải lại">
              <RefreshCw size={14} />
            </button>
          </div>

          <div className="flex flex-wrap items-center gap-2 admin-card">
            <div className="relative min-w-[200px] flex-1">
              <Search size={14} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Tìm trong nội dung câu hỏi…"
                className={`${inputCls} w-full pl-8`}
              />
            </div>
            <select value={qtype} onChange={(e) => setQtype(e.target.value as ExamQuestion["type"] | "")} className={selectCls}>
              {QTYPE_OPTIONS.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>
            <select value={form} onChange={(e) => setForm(e.target.value as QuestionForm | "")} className={selectCls}>
              <option value="">Lý thuyết + bài tập</option>
              <option value="ly_thuyet">Lý thuyết</option>
              <option value="bai_tap">Bài tập</option>
            </select>
            <select value={difficulty} onChange={(e) => setDifficulty(e.target.value as Difficulty | "all")} className={selectCls}>
              <option value="all">Mọi độ khó</option>
              {(Object.keys(DIFFICULTY_LABELS) as Difficulty[]).map((d) => (
                <option key={d} value={d}>
                  {DIFFICULTY_LABELS[d]}
                </option>
              ))}
            </select>
            <label className="flex items-center gap-1.5 text-xs text-slate-400">
              <input type="checkbox" checked={showArchived} onChange={(e) => setShowArchived(e.target.checked)} />
              Hiện câu đã lưu trữ
            </label>
            <div className="ml-auto flex items-center gap-1">
              <input
                type="number"
                min={1}
                max={100}
                value={randomN}
                onChange={(e) => setRandomN(Math.max(1, Number(e.target.value) || 1))}
                className={`${inputCls} w-16 text-center`}
              />
              <button type="button" onClick={addRandom} disabled={items.length === 0} className={btnCls}>
                <Dices size={14} /> Bốc ngẫu nhiên vào giỏ
              </button>
            </div>
          </div>

          {items.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-white/15 p-10 text-center text-sm text-slate-500">
              Chưa có câu nào ở mục này.
            </div>
          ) : (
            items.map((q, i) => (
              <QuestionRow
                key={q.id}
                index={i + 1}
                q={q}
                picked={inBasket.has(q.id)}
                onPick={() => toggleBasket(q.id)}
                topicGroups={topicGroups}
                onPatch={(p) => patch(q.id, p)}
              />
            ))
          )}
        </section>
      </div>

      {/* ===== Giỏ câu ===== */}
      <div className="fixed inset-x-0 bottom-0 z-30 border-t border-white/10 bg-panel/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-2 px-4 py-3">
          <button type="button" onClick={() => setBasketOpen((o) => !o)} className={`${btnCls} bg-white/5`}>
            <ListChecks size={14} /> Giỏ: <b className="text-white">{basket.length}</b> câu {basketOpen ? "▾" : "▴"}
          </button>
          {basket.length > 0 && (
            <button type="button" onClick={() => setBasket([])} className={btnCls}>
              <Trash2 size={14} /> Bỏ hết
            </button>
          )}
          <div className="ml-auto flex items-center gap-2">
            {basket.length > 0 && (
              <>
                <select value={bulkTopic} onChange={(e) => setBulkTopic(e.target.value)} className={`${selectCls} max-w-[260px]`}>
                  <option value="">— gắn năng lực cho cả giỏ —</option>
                  {topicGroups.map(({ parent, outcomes }) => (
                    <optgroup key={parent.id} label={parent.name}>
                      <option value={parent.name}>{parent.name} (cả bài)</option>
                      {outcomes.map((o) => (
                        <option key={o.id} value={o.name}>
                          {o.name}
                        </option>
                      ))}
                    </optgroup>
                  ))}
                </select>
                <button type="button" onClick={bulkTag} disabled={!bulkTopic} className={btnCls}>
                  Gắn
                </button>
              </>
            )}
            <button
              type="button"
              onClick={composeExam}
              disabled={basket.length === 0}
              className="inline-flex items-center gap-1 admin-btn admin-btn--primary disabled:opacity-40"
            >
              <FilePlus2 size={15} /> Soạn đề từ {basket.length} câu
            </button>
          </div>
        </div>
        {basketOpen && basket.length > 0 && (
          <div className="mx-auto max-h-[40vh] max-w-7xl overflow-y-auto border-t border-white/10 px-4 py-3">
            <ol className="space-y-1 text-sm">
              {basketItems.map((q, i) => (
                <li key={q.id} className="flex items-start gap-2 rounded-lg px-2 py-1 hover:bg-white/5">
                  <span className="w-6 shrink-0 text-right text-xs text-slate-500">{i + 1}.</span>
                  <span className="rounded bg-white/10 px-1.5 text-[11px] text-slate-300">{TYPE_SHORT[q.qtype] ?? q.qtype}</span>
                  <span className="min-w-0 flex-1 truncate text-slate-200">{stripHtml(q.question.question)}</span>
                  <span className="hidden max-w-[200px] truncate text-xs text-slate-500 sm:inline">{q.topicName || "chưa gắn"}</span>
                  <button type="button" onClick={() => toggleBasket(q.id)} className="text-slate-500 hover:text-rose-300" aria-label="Bỏ khỏi giỏ">
                    ×
                  </button>
                </li>
              ))}
            </ol>
          </div>
        )}
      </div>
    </div>
  );
}

function TreeRow({
  active,
  onClick,
  label,
  count,
  bold,
  warn,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  count: number;
  bold?: boolean;
  warn?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex w-full items-center gap-2 rounded-lg px-2 py-1.5 text-left text-sm ${
        active ? "bg-primary/20 text-white" : "text-slate-300 hover:bg-white/5"
      }`}
    >
      <span className={`min-w-0 flex-1 truncate ${bold ? "font-semibold" : ""}`}>{label}</span>
      <span
        className={`shrink-0 rounded-full px-1.5 text-[11px] ${
          count === 0 ? "text-slate-600" : warn ? "bg-amber-500/20 text-amber-200" : "bg-white/10 text-slate-300"
        }`}
      >
        {count}
      </span>
    </button>
  );
}

function stripHtml(html: string): string {
  return html
    .replace(/<img[^>]*alt="([^"]*)"[^>]*>/g, " $1 ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function QuestionRow({
  index,
  q,
  picked,
  onPick,
  topicGroups,
  onPatch,
}: {
  index: number;
  q: BankQuestion;
  picked: boolean;
  onPick: () => void;
  topicGroups: { parent: QuestionTopic; outcomes: QuestionTopic[] }[];
  onPatch: (p: Parameters<typeof updateBankQuestion>[1]) => void;
}) {
  const [showAnswer, setShowAnswer] = useState(false);
  const body = q.question;
  const topicKnown = topicGroups.some(({ parent, outcomes }) => parent.name === q.topicName || outcomes.some((o) => o.name === q.topicName));

  return (
    <article
      className={`rounded-2xl border p-4 ${picked ? "border-primary/60 bg-primary/5" : "border-white/10 bg-panel"} ${q.archived ? "opacity-60" : ""}`}
    >
      <div className="flex flex-wrap items-center gap-2">
        <label className="flex cursor-pointer items-center gap-2">
          <input type="checkbox" checked={picked} onChange={onPick} className="h-4 w-4" />
          <span className="text-sm font-semibold text-white">Câu {index}</span>
        </label>
        <span className="rounded bg-white/10 px-1.5 py-0.5 text-[11px] text-slate-300">{TYPE_SHORT[q.qtype] ?? q.qtype}</span>
        {q.archived && <span className="rounded bg-amber-500/20 px-1.5 py-0.5 text-[11px] text-amber-200">đã lưu trữ</span>}
        <span className="ml-auto text-[11px] text-slate-500">
          {q.sourceExamId !== null ? (
            <>
              từ đề <Link href={`/kiem-tra/lam/?id=${q.sourceExamId}`} className="text-primary hover:underline">#{q.sourceExamId}</Link>
              {q.sourceIndex !== null ? ` câu ${q.sourceIndex + 1}` : ""}
            </>
          ) : (
            "nhập tay"
          )}
        </span>
      </div>

      <ContentHtml html={body.question} className="prose prose-invert mt-2 max-w-none text-sm text-slate-200" />

      {body.type === "multiple_choice" && (
        <ol className="mt-2 grid gap-1 sm:grid-cols-2">
          {body.options.map((o, i) => (
            <li
              key={i}
              className={`flex gap-2 rounded-lg px-2 py-1 text-sm ${showAnswer && i === body.answer ? "bg-emerald-500/15 text-emerald-200" : "text-slate-300"}`}
            >
              <b className="shrink-0">{LETTERS[i]}.</b>
              <ContentHtml html={o} className="min-w-0" />
            </li>
          ))}
        </ol>
      )}
      {body.type === "true_false" && (
        <ol className="mt-2 space-y-1">
          {body.statements.map((s, i) => (
            <li key={i} className="flex gap-2 text-sm text-slate-300">
              <b className="shrink-0">{LETTERS[i].toLowerCase()})</b>
              <ContentHtml html={s.text} className="min-w-0 flex-1" />
              {showAnswer && (
                <span className={`shrink-0 text-xs font-semibold ${s.answer ? "text-emerald-300" : "text-rose-300"}`}>{s.answer ? "Đúng" : "Sai"}</span>
              )}
            </li>
          ))}
        </ol>
      )}
      {body.type === "short_answer" && showAnswer && (
        <p className="mt-2 text-sm text-emerald-200">
          Đáp án: <b>{body.answer}</b>
        </p>
      )}
      {showAnswer && body.explanation && (
        <div className="mt-2 rounded-lg border border-white/10 bg-white/[.03] p-2 text-xs text-slate-300">
          <b className="text-slate-400">Lời giải: </b>
          <ContentHtml html={body.explanation} className="inline" />
        </div>
      )}

      <div className="mt-3 flex flex-wrap items-center gap-2 border-t border-white/10 pt-3">
        <select
          value={topicKnown ? q.topicName : q.topicName ? "__unknown" : ""}
          onChange={(e) => onPatch({ topicName: e.target.value === "__unknown" ? q.topicName : e.target.value })}
          className={`${selectCls} max-w-[320px] ${q.topicName ? "" : "border-amber-500/40"}`}
          title="Năng lực cần đạt"
        >
          <option value="">— chưa gắn năng lực —</option>
          {!topicKnown && q.topicName && <option value="__unknown">{q.topicName} (không có trong danh mục)</option>}
          {topicGroups.map(({ parent, outcomes }) => (
            <optgroup key={parent.id} label={parent.name}>
              <option value={parent.name}>{parent.name} (cả bài)</option>
              {outcomes.map((o) => (
                <option key={o.id} value={o.name}>
                  {o.name}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
        <select value={q.form} onChange={(e) => onPatch({ form: e.target.value as QuestionForm | "" })} className={selectCls}>
          <option value="">— loại —</option>
          {(Object.keys(QUESTION_FORM_LABELS) as QuestionForm[]).map((f) => (
            <option key={f} value={f}>
              {QUESTION_FORM_LABELS[f]}
            </option>
          ))}
        </select>
        <select value={q.difficulty} onChange={(e) => onPatch({ difficulty: e.target.value as Difficulty })} className={selectCls}>
          {(Object.keys(DIFFICULTY_LABELS) as Difficulty[]).map((d) => (
            <option key={d} value={d}>
              {DIFFICULTY_LABELS[d]}
            </option>
          ))}
        </select>
        <div className="ml-auto flex items-center gap-2">
          <button type="button" onClick={() => setShowAnswer((s) => !s)} className={btnCls}>
            {showAnswer ? "Ẩn đáp án" : "Đáp án & lời giải"}
          </button>
          <button
            type="button"
            onClick={() => onPatch({ archived: !q.archived })}
            className={btnCls}
            title={q.archived ? "Đưa lại vào ngân hàng" : "Lưu trữ: không bốc câu này khi soạn đề"}
          >
            {q.archived ? <ArchiveRestore size={14} /> : <Archive size={14} />}
          </button>
        </div>
      </div>
    </article>
  );
}
