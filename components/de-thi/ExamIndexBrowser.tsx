"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { ExamIndexItem, ExamShelf } from "@/components/de-thi/exam-index.server";
import { examTakePath } from "@/lib/exam-link";

const SHELF_LABEL: Record<ExamShelf, string> = {
  "giua-ki": "Giữa kì",
  "cuoi-ki": "Cuối kì",
  "thi-thu": "Thi thử tốt nghiệp",
};
const PAGE = 24;

/** Bỏ dấu + chữ thường để gõ "ninh binh" vẫn ra "Ninh Bình". */
function fold(s: string) {
  return s
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/đ/gi, "d")
    .toLowerCase();
}

function Chip({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      aria-pressed={active}
      onClick={onClick}
      className={`min-h-11 rounded-full border px-4 text-base font-semibold transition-colors ${
        active ? "border-primary bg-primary text-white" : "border-line bg-surface-2 text-ink hover:bg-primary-soft"
      }`}
    >
      {children}
    </button>
  );
}

export default function ExamIndexBrowser({ exams }: { exams: ExamIndexItem[] }) {
  const [grade, setGrade] = useState("");
  const [shelf, setShelf] = useState("");
  const [year, setYear] = useState("");
  const [q, setQ] = useState("");
  const [shown, setShown] = useState(PAGE);

  const folded = useMemo(() => exams.map((e) => fold(e.name)), [exams]);
  const query = fold(q.trim());

  function matches(e: ExamIndexItem, i: number, skip: "grade" | "shelf" | "year" | null) {
    return (
      (skip === "grade" || !grade || e.grade === grade) &&
      (skip === "shelf" || !shelf || e.shelf === shelf) &&
      (skip === "year" || !year || e.year === year) &&
      (!query || folded[i].includes(query))
    );
  }

  // Số đề cạnh mỗi chip = số đề còn lại khi áp các bộ lọc KHÁC (chip nào bằng 0 thì ẩn).
  function facet(key: "grade" | "shelf" | "year") {
    const counts = new Map<string, number>();
    exams.forEach((e, i) => {
      if (matches(e, i, key)) counts.set(e[key], (counts.get(e[key]) ?? 0) + 1);
    });
    return counts;
  }
  const gradeCounts = facet("grade");
  const shelfCounts = facet("shelf");
  const yearCounts = facet("year");

  const list = exams.filter((e, i) => matches(e, i, null));
  const grades = ["10", "11", "12"].filter((g) => gradeCounts.has(g) || g === grade);
  const years = [...new Set(exams.map((e) => e.year).filter(Boolean))].sort().reverse();

  function pick<T>(setter: (v: T) => void, v: T) {
    setter(v);
    setShown(PAGE);
  }

  return (
    <div>
      <label className="block">
        <span className="text-base font-semibold text-ink">Tìm theo tên trường hoặc tỉnh</span>
        <input
          type="search"
          value={q}
          onChange={(e) => pick(setQ, e.target.value)}
          placeholder="Ví dụ: Nghệ An, Lê Quý Đôn…"
          className="mt-2 block min-h-12 w-full rounded-xl border border-line-strong bg-surface-2 px-4 text-base text-ink placeholder:text-muted"
        />
      </label>

      <div className="mt-5 space-y-4">
        <fieldset>
          <legend className="text-base font-semibold text-ink">Lớp</legend>
          <div className="mt-2 flex flex-wrap gap-2">
            <Chip active={!grade} onClick={() => pick(setGrade, "")}>Tất cả</Chip>
            {grades.map((g) => (
              <Chip key={g} active={grade === g} onClick={() => pick(setGrade, g)}>
                Lớp {g} ({gradeCounts.get(g) ?? 0})
              </Chip>
            ))}
          </div>
        </fieldset>
        <fieldset>
          <legend className="text-base font-semibold text-ink">Loại đề</legend>
          <div className="mt-2 flex flex-wrap gap-2">
            <Chip active={!shelf} onClick={() => pick(setShelf, "")}>Tất cả</Chip>
            {(Object.keys(SHELF_LABEL) as ExamShelf[])
              .filter((s) => shelfCounts.has(s) || s === shelf)
              .map((s) => (
                <Chip key={s} active={shelf === s} onClick={() => pick(setShelf, s)}>
                  {SHELF_LABEL[s]} ({shelfCounts.get(s) ?? 0})
                </Chip>
              ))}
          </div>
        </fieldset>
        <fieldset>
          <legend className="text-base font-semibold text-ink">Năm</legend>
          <div className="mt-2 flex flex-wrap gap-2">
            <Chip active={!year} onClick={() => pick(setYear, "")}>Tất cả</Chip>
            {years
              .filter((y) => yearCounts.has(y) || y === year)
              .map((y) => (
                <Chip key={y} active={year === y} onClick={() => pick(setYear, y)}>
                  {y} ({yearCounts.get(y) ?? 0})
                </Chip>
              ))}
          </div>
        </fieldset>
      </div>

      <p className="mt-6 text-base text-ink" aria-live="polite">
        {list.length > 0 ? `${list.length} đề` : "Không có đề nào khớp. Thử bỏ bớt một bộ lọc."}
      </p>

      <ul className="mt-3 grid gap-3 md:grid-cols-2">
        {list.slice(0, shown).map((e) => (
          <li key={e.id}>
            <Link
              href={examTakePath(e.id)}
              className="flex h-full min-h-14 min-w-0 flex-col rounded-xl border border-line bg-surface-2 px-5 py-4 text-ink transition-colors hover:bg-primary-soft"
            >
              <span className="break-words text-lg font-semibold leading-snug">{e.name}</span>
              <span className="mt-1 text-base">
                {[`Lớp ${e.grade}`, SHELF_LABEL[e.shelf], e.term, e.year].filter(Boolean).join(" · ")}
              </span>
              <span className="mt-1 text-base text-muted">
                {e.questionCount} câu · {e.durationMinutes} phút
              </span>
            </Link>
          </li>
        ))}
      </ul>

      {list.length > shown && (
        <button
          type="button"
          onClick={() => setShown((n) => n + PAGE)}
          className="mt-6 min-h-12 rounded-full border border-line-strong bg-surface-2 px-6 text-base font-semibold text-ink hover:bg-primary-soft"
        >
          Hiện thêm ({list.length - shown} đề)
        </button>
      )}
    </div>
  );
}
