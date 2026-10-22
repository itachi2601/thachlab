"use client";

import { useMemo, useState } from "react";
import { ChevronDown, Search } from "lucide-react";

export interface PickerExam {
  id: number;
  title: string;
  own: boolean;
  done: number;
  /** ISO time của lượt nộp gần nhất; null = chưa ai nộp. */
  last: string | null;
}

const VISIBLE = 8;
const DAY = 86_400_000;

export function agoLabel(iso: string, now = Date.now()) {
  const diff = now - new Date(iso).getTime();
  if (diff < 60_000) return "vừa xong";
  if (diff < 3_600_000) return `${Math.floor(diff / 60_000)} phút trước`;
  if (diff < DAY) return `${Math.floor(diff / 3_600_000)} giờ trước`;
  if (diff < 30 * DAY) return `${Math.floor(diff / DAY)} ngày trước`;
  return new Date(iso).toLocaleDateString("vi-VN");
}

/** Sắp theo lượt nộp gần nhất; đề chưa ai nộp xuống cuối. */
export function sortByRecent<T extends { last: string | null; id: number }>(list: T[]): T[] {
  return [...list].sort((a, b) => {
    if (!a.last && !b.last) return b.id - a.id;
    if (!a.last) return 1;
    if (!b.last) return -1;
    return b.last.localeCompare(a.last);
  });
}

export default function ExamPicker({
  exams,
  value,
  onChange,
  total,
  periodicIds,
}: {
  exams: PickerExam[];
  value: number | null;
  onChange: (id: number) => void;
  total: number;
  periodicIds: Set<number>;
}) {
  const [search, setSearch] = useState("");
  const [showAll, setShowAll] = useState(false);
  const [showEmpty, setShowEmpty] = useState(false);
  // Mốc thời gian ổn định cho lần render đầu, tránh gọi Date.now() trong render.
  const [now] = useState(() => Date.now());

  const { submitted, empty, matches } = useMemo(() => {
    const sorted = sortByRecent(exams);
    const kw = search.trim().toLowerCase();
    return {
      submitted: sorted.filter((e) => e.done > 0),
      empty: sorted.filter((e) => e.done === 0),
      matches: kw ? sorted.filter((e) => e.title.toLowerCase().includes(kw) || String(e.id) === kw) : null,
    };
  }, [exams, search]);

  const card = (e: PickerExam) => (
    <li key={e.id}>
      <button
        type="button"
        onClick={() => onChange(e.id)}
        aria-pressed={value === e.id}
        className={`flex min-h-12 w-full flex-col gap-0.5 rounded-xl border px-3 py-2 text-left transition ${
          value === e.id ? "border-primary bg-primary/15" : "border-white/10 bg-panel hover:border-white/25"
        }`}
      >
        <span className="text-sm font-semibold text-white">
          {periodicIds.has(e.id) && (
            <span className="mr-1.5 rounded-full bg-emerald-500/15 px-2 py-0.5 text-xs text-emerald-300">Định kỳ</span>
          )}
          {e.title}
        </span>
        <span className="text-xs text-slate-400">
          {e.done > 0 && e.last ? `Nộp ${e.done}/${total} · gần nhất ${agoLabel(e.last, now)}` : "Chưa ai nộp"}
          {!e.own && " · ngoài khối"}
        </span>
      </button>
    </li>
  );

  const groups: { label: string; items: PickerExam[] }[] = [];
  if (!matches) {
    const today: PickerExam[] = [];
    const week: PickerExam[] = [];
    const older: PickerExam[] = [];
    const shown = showAll ? submitted : submitted.slice(0, VISIBLE);
    for (const e of shown) {
      const age = now - new Date(e.last as string).getTime();
      (age < DAY ? today : age < 7 * DAY ? week : older).push(e);
    }
    if (today.length) groups.push({ label: "Hôm nay", items: today });
    if (week.length) groups.push({ label: "Trong 7 ngày", items: week });
    if (older.length) groups.push({ label: "Cũ hơn", items: older });
  }

  return (
    <div className="space-y-3">
      <label className="relative block">
        <Search size={16} className="pointer-events-none absolute top-1/2 left-3 -translate-y-1/2 text-slate-500" />
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Tìm đề theo tên hoặc mã…"
          aria-label="Tìm đề"
          className="w-full rounded-xl border border-white/10 bg-panel py-2 pr-3 pl-9 text-sm text-white focus:border-primary focus:outline-none"
        />
      </label>

      {matches ? (
        matches.length === 0 ? (
          <p className="text-sm text-slate-500">Không thấy đề nào khớp.</p>
        ) : (
          <ul className="grid gap-2 sm:grid-cols-2">{matches.map(card)}</ul>
        )
      ) : (
        <>
          {submitted.length === 0 && <p className="text-sm text-slate-500">Chưa có đề nào được nộp.</p>}
          {groups.map((g) => (
            <section key={g.label} className="space-y-1.5">
              <h3 className="text-xs font-semibold tracking-wide text-slate-400 uppercase">{g.label}</h3>
              <ul className="grid gap-2 sm:grid-cols-2">{g.items.map(card)}</ul>
            </section>
          ))}
          {submitted.length > VISIBLE && (
            <button type="button" onClick={() => setShowAll((v) => !v)} className="text-sm text-blue-300 underline">
              {showAll ? "Thu gọn" : `Xem thêm ${submitted.length - VISIBLE} đề`}
            </button>
          )}
          {empty.length > 0 && (
            <div>
              <button
                type="button"
                onClick={() => setShowEmpty((v) => !v)}
                aria-expanded={showEmpty}
                className="inline-flex items-center gap-1 text-sm text-slate-400"
              >
                <ChevronDown size={14} className={showEmpty ? "rotate-180" : ""} />
                Đề chưa ai làm ({empty.length})
              </button>
              {showEmpty && <ul className="mt-2 grid gap-2 sm:grid-cols-2">{empty.map(card)}</ul>}
            </div>
          )}
        </>
      )}
    </div>
  );
}
