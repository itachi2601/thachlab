"use client";

import { useEffect, useMemo, useState } from "react";
import { ChevronDown, ChevronRight, Wand2, X } from "lucide-react";
import { fetchQuestionTopics, lessonTopics, outcomesOf, type QuestionTopic } from "@/services/analytics";
import { fetchBankTopicCounts, QUICK_COMPOSE_DEFAULT, type BankTopicCount } from "@/services/question-bank";

const TYPE_LABELS: [string, string][] = [
  ["multiple_choice", "Trắc nghiệm"],
  ["true_false", "Đúng–Sai"],
  ["short_answer", "Trả lời ngắn"],
];

export interface QuickComposeChoice {
  topicIds: number[];
  counts: Record<string, number>;
}

/** Chọn chủ đề (bài / yêu cầu cần đạt) và số câu mỗi dạng trước khi bốc đề nhanh của một khối. */
export default function QuickComposeDialog({
  grade,
  busy,
  onConfirm,
  onClose,
}: {
  grade: string;
  busy: boolean;
  onConfirm: (c: QuickComposeChoice) => void;
  onClose: () => void;
}) {
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [counts, setCounts] = useState<BankTopicCount[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [picked, setPicked] = useState<Set<number>>(new Set());
  const [open, setOpen] = useState<Set<number>>(new Set());
  const [n, setN] = useState<Record<string, number>>({ ...QUICK_COMPOSE_DEFAULT });

  useEffect(() => {
    let alive = true;
    Promise.all([fetchQuestionTopics(grade), fetchBankTopicCounts(grade)])
      .then(([t, c]) => {
        if (!alive) return;
        setTopics(t);
        setCounts(c);
      })
      .catch(() => undefined)
      .finally(() => alive && setLoaded(true));
    return () => {
      alive = false;
    };
  }, [grade]);

  const have = useMemo(() => new Map(counts.map((c) => [c.topicId, c.active])), [counts]);
  const groups = useMemo(
    () =>
      lessonTopics(topics)
        .sort((a, b) => a.sortOrder - b.sortOrder || a.name.localeCompare(b.name, "vi"))
        .map((p) => {
          const outcomes = outcomesOf(topics, p.id);
          const ids = [p.id, ...outcomes.map((o) => o.id)];
          return { parent: p, outcomes, ids, total: ids.reduce((s, id) => s + (have.get(id) ?? 0), 0) };
        })
        .filter((g) => g.total > 0),
    [topics, have],
  );

  const available = groups.reduce((s, g) => s + g.ids.filter((id) => picked.has(id)).reduce((a, id) => a + (have.get(id) ?? 0), 0), 0);
  const wanted = Object.values(n).reduce((s, v) => s + (v || 0), 0);

  function toggleIds(ids: number[], on: boolean) {
    setPicked((s) => {
      const next = new Set(s);
      for (const id of ids) {
        if (on) next.add(id);
        else next.delete(id);
      }
      return next;
    });
  }

  return (
    <div className="fixed inset-0 z-100 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm" onClick={onClose}>
      <div
        role="dialog"
        aria-label={`Soạn đề nhanh khối ${grade}`}
        className="admin-card flex max-h-[88vh] w-full max-w-2xl flex-col gap-3"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-2">
          <h2 className="mr-auto inline-flex items-center gap-2 text-base font-semibold text-white">
            <Wand2 size={16} /> Soạn đề nhanh · {grade === "9" ? "KHTN 9" : `Lớp ${grade}`}
          </h2>
          <button type="button" onClick={onClose} aria-label="Đóng" className="p-1 text-slate-400 hover:text-white">
            <X size={18} />
          </button>
        </div>

        <div className="flex flex-wrap items-center gap-3 text-sm text-slate-300">
          {TYPE_LABELS.map(([k, label]) => (
            <label key={k} className="inline-flex items-center gap-1.5">
              {label}
              <input
                type="number"
                min={0}
                max={60}
                value={n[k] ?? 0}
                onChange={(e) => setN((m) => ({ ...m, [k]: Math.max(0, Math.min(60, Number(e.target.value) || 0)) }))}
                className="w-16 rounded-lg border border-white/10 bg-white/5 px-2 py-1 text-white"
              />
            </label>
          ))}
          <span className="text-xs text-slate-500">Độ khó bốc 4 Dễ : 4 TB : 2 Khó</span>
        </div>

        <div className="flex items-center gap-3 text-sm">
          <span className="font-semibold text-slate-200">Chủ đề</span>
          <button type="button" className="text-primary hover:underline" onClick={() => toggleIds(groups.flatMap((g) => g.ids), true)}>
            Chọn tất cả
          </button>
          <button type="button" className="text-slate-400 hover:underline" onClick={() => setPicked(new Set())}>
            Bỏ chọn
          </button>
        </div>

        <div className="min-h-0 flex-1 space-y-1 overflow-y-auto rounded-xl border border-white/10 p-2">
          {!loaded ? (
            <p className="p-3 text-sm text-slate-400">Đang tải chủ đề…</p>
          ) : groups.length === 0 ? (
            <p className="p-3 text-sm text-slate-400">Khối này chưa có câu gắn chủ đề trong ngân hàng.</p>
          ) : (
            groups.map((g) => {
              const on = g.ids.filter((id) => picked.has(id)).length;
              const isOpen = open.has(g.parent.id);
              return (
                <div key={g.parent.id}>
                  <div className="flex items-center gap-1">
                    <button
                      type="button"
                      className="p-1 text-slate-500 hover:text-white"
                      aria-label={isOpen ? "Thu gọn" : "Mở yêu cầu cần đạt"}
                      disabled={g.outcomes.length === 0}
                      onClick={() =>
                        setOpen((s) => {
                          const next = new Set(s);
                          if (next.has(g.parent.id)) next.delete(g.parent.id);
                          else next.add(g.parent.id);
                          return next;
                        })
                      }
                    >
                      {g.outcomes.length === 0 ? <span className="inline-block w-3.5" /> : isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                    </button>
                    <label className="flex min-h-9 flex-1 cursor-pointer items-center gap-2 text-sm text-slate-200">
                      <input
                        type="checkbox"
                        checked={on === g.ids.length}
                        ref={(el) => {
                          if (el) el.indeterminate = on > 0 && on < g.ids.length;
                        }}
                        onChange={(e) => toggleIds(g.ids, e.target.checked)}
                      />
                      <span className="flex-1">{g.parent.name}</span>
                      <span className="text-xs text-slate-500">{g.total} câu</span>
                    </label>
                  </div>
                  {isOpen &&
                    g.outcomes
                      .filter((o) => (have.get(o.id) ?? 0) > 0)
                      .map((o) => (
                        <label key={o.id} className="ml-8 flex min-h-8 cursor-pointer items-center gap-2 text-sm text-slate-300">
                          <input type="checkbox" checked={picked.has(o.id)} onChange={(e) => toggleIds([o.id], e.target.checked)} />
                          <span className="flex-1">{o.name}</span>
                          <span className="text-xs text-slate-500">{have.get(o.id)}</span>
                        </label>
                      ))}
                </div>
              );
            })
          )}
        </div>

        <div className="flex items-center gap-3">
          <span className="mr-auto text-xs text-slate-400">
            Cần {wanted} câu · các chủ đề đã chọn có {available} câu
          </span>
          <button type="button" onClick={onClose} className="admin-btn">
            Huỷ
          </button>
          <button
            type="button"
            disabled={busy || picked.size === 0 || wanted === 0}
            onClick={() => onConfirm({ topicIds: [...picked], counts: n })}
            className="admin-btn admin-btn--primary disabled:opacity-40"
          >
            {busy ? "Đang bốc…" : "Bốc đề"}
          </button>
        </div>
      </div>
    </div>
  );
}
