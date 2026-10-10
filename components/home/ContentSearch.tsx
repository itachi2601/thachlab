"use client";

import { useState } from "react";
import Link from "next/link";
import { Search } from "lucide-react";

/**
 * Tìm bài theo tên, và sâu hơn: tìm cả chữ trong nội dung lý thuyết của từng bài. Danh sách lấy từ
 * /data/catalog.json, chữ trong bài từ /data/search-index.json (file tĩnh lúc build) — chỉ tải khi em
 * chạm ô tìm, không gọi Supabase (quy tắc không thêm round-trip cho /).
 * N1 một việc, C1 chữ ≥16px, D2 đích chạm ≥44px, N3 không hiện danh sách trống trước khi gõ.
 */

interface CatalogClass {
  id: number;
  name: string;
  slug: string;
}

interface CatalogChapter {
  id: number;
  title: string;
  classIds: number[];
  subjectCode: string;
}

interface CatalogLesson {
  id: number;
  chapter_id: number;
  title: string;
  published: boolean;
  sort_order: number;
}

interface CatalogFile {
  classes: CatalogClass[];
  chapters: CatalogChapter[];
  lessons: CatalogLesson[];
}

interface IndexFile {
  lessons: { id: number; x: string }[];
}

interface Hit {
  id: number;
  title: string;
  meta: string;
  href: string;
  titleHay: string;
  chapterHay: string;
  /** Chữ bài đã bỏ dấu (cùng độ dài với `text`) và chữ gốc để hiện đoạn trích. */
  textHay: string;
  text: string;
  rank: number;
}

interface Row {
  hit: Hit;
  score: number;
  /** Vị trí khớp đầu tiên trong `text` — chỉ có khi khớp trong nội dung, không khớp ở tên bài. */
  at: number;
  span: number;
}

const MAX_HITS = 8;
const SNIPPET_BEFORE = 40;
const SNIPPET_AFTER = 90;

// Bỏ dấu từng ký tự, giữ nguyên số ký tự để vị trí khớp trong chữ đã bỏ dấu map thẳng sang chữ gốc.
const charCache = new Map<string, string>();
function foldChar(c: string): string {
  let out = charCache.get(c);
  if (out === undefined) {
    const base = c.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/gi, "d").toLowerCase();
    out = base.length === 1 ? base : c.toLowerCase().length === 1 ? c.toLowerCase() : c;
    charCache.set(c, out);
  }
  return out;
}

function foldKeepLength(value: string): string {
  let out = "";
  for (const c of value) out += foldChar(c);
  return out;
}

function fold(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/đ/gi, "d")
    .toLowerCase()
    .replace(/\s+/g, " ")
    .trim();
}

function classLabel(name: string): string {
  return /^\d+$/.test(name) ? `Lớp ${name}` : name;
}

function toHits(catalog: CatalogFile, index: IndexFile | null): Hit[] {
  const classes = new Map(catalog.classes.map((item) => [item.id, item]));
  const chapters = new Map(catalog.chapters.map((item) => [item.id, item]));
  const texts = new Map((index?.lessons ?? []).map((row) => [row.id, row.x]));
  const hits: Hit[] = [];
  for (const lesson of catalog.lessons) {
    if (!lesson.published) continue;
    const chapter = chapters.get(lesson.chapter_id);
    if (!chapter) continue;
    const schoolClass = classes.get(chapter.classIds[0] ?? -1);
    const grade = schoolClass ? classLabel(schoolClass.name) : "";
    const params = new URLSearchParams({
      id: String(lesson.id),
      subject: chapter.subjectCode || "vat-ly",
      chapter: String(chapter.id),
    });
    if (schoolClass?.slug) params.set("class", schoolClass.slug);
    const meta = [grade, chapter.title].filter(Boolean).join(" · ");
    const text = texts.get(lesson.id) ?? "";
    hits.push({
      id: lesson.id,
      title: lesson.title,
      meta,
      href: `/lop-hoc/bai/?${params.toString()}`,
      titleHay: fold(lesson.title),
      chapterHay: fold(chapter.title),
      textHay: foldKeepLength(text),
      text,
      rank: lesson.sort_order,
    });
  }
  return hits;
}

let catalogPromise: Promise<Hit[] | null> | null = null;

function fetchJson<T>(url: string): Promise<T | null> {
  return fetch(url)
    .then((res) => (res.ok ? (res.json() as Promise<T>) : null))
    .catch(() => null);
}

function loadHits(): Promise<Hit[] | null> {
  if (!catalogPromise) {
    catalogPromise = Promise.all([
      fetchJson<CatalogFile>("/data/catalog.json"),
      fetchJson<IndexFile>("/data/search-index.json"),
    ]).then(([catalog, index]) => {
      if (!catalog || !Array.isArray(catalog.lessons) || !Array.isArray(catalog.chapters)) return null;
      return toHits(catalog, index && Array.isArray(index.lessons) ? index : null);
    });
  }
  return catalogPromise;
}

/** Đoạn trích quanh chỗ khớp, cắt theo ranh giới từ để không lửng giữa chữ. */
function snippetOf(text: string, at: number, span: number): { before: string; hit: string; after: string } {
  let start = Math.max(0, at - SNIPPET_BEFORE);
  if (start > 0) {
    const space = text.indexOf(" ", start);
    if (space !== -1 && space < at) start = space + 1;
  }
  let end = Math.min(text.length, at + span + SNIPPET_AFTER);
  if (end < text.length) {
    const space = text.lastIndexOf(" ", end);
    if (space > at + span) end = space;
  }
  return {
    before: (start > 0 ? "…" : "") + text.slice(start, at),
    hit: text.slice(at, at + span),
    after: text.slice(at + span, end) + (end < text.length ? "…" : ""),
  };
}

export default function ContentSearch({ variant = "public" }: { variant?: "public" | "account" }) {
  const [query, setQuery] = useState("");
  const [hits, setHits] = useState<Hit[] | null>(null);
  const [failed, setFailed] = useState(false);

  function ensureLoaded() {
    if (hits || failed) return;
    void loadHits().then((rows) => {
      if (!rows) setFailed(true);
      else setHits(rows);
    });
  }

  const folded = fold(query);
  const tokens = folded.split(" ").filter((token) => token.length >= 2);
  const rows: Row[] =
    !hits || tokens.length === 0 || folded.length < 2
      ? []
      : hits
          .map((hit) => {
            let score = 0;
            let missing = false;
            let at = -1;
            let span = 0;
            tokens.forEach((token, i) => {
              const weight = tokens.length - i;
              if (hit.titleHay.includes(token)) score += weight * 2;
              else if (hit.chapterHay.includes(token)) score += weight;
              else if (hit.textHay.includes(token)) {
                score += weight;
                const pos = hit.textHay.indexOf(token);
                if (at === -1 || pos < at) {
                  at = pos;
                  span = token.length;
                }
              } else missing = true;
            });
            // Mỗi từ phải khớp ở đâu đó (tên, chương hoặc nội dung bài) thì bài mới hiện.
            if (missing || score === 0) return null;
            return { hit, score, at, span } satisfies Row;
          })
          .filter((row): row is Row => row !== null)
          // Khớp tên/chương lên trước, rồi tới khớp trong nội dung; trong mỗi nhóm xếp theo điểm, rồi theo thứ tự bài.
          .sort((a, b) => {
            const aTitle = a.at === -1 ? 0 : 1;
            const bTitle = b.at === -1 ? 0 : 1;
            return aTitle - bTitle || b.score - a.score || a.hit.rank - b.hit.rank;
          });

  const shown = rows.slice(0, MAX_HITS);
  const ready = folded.length >= 2;

  const shell =
    variant === "account"
      ? "rounded-2xl border border-line bg-panel p-4"
      : "bg-bg px-6 pb-8 pt-1 lg:px-12";

  return (
    <section className={shell} aria-label="Tìm bài học">
      <div className={variant === "account" ? "" : "mx-auto max-w-6xl"}>
        <h2 className="font-display text-lg font-bold text-ink sm:text-xl">Tìm bài học</h2>
        <form
          className="relative mt-2"
          role="search"
          onSubmit={(event) => {
            event.preventDefault();
            const first = shown[0];
            if (first) window.location.assign(first.hit.href);
          }}
        >
          <label htmlFor="content-search" className="sr-only">
            Tên bài hoặc nội dung trong bài
          </label>
          <Search size={18} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
          <input
            id="content-search"
            type="search"
            enterKeyHint="search"
            value={query}
            placeholder="Tìm tên bài hoặc nội dung"
            onFocus={ensureLoaded}
            onChange={(event) => {
              ensureLoaded();
              setQuery(event.target.value);
            }}
            className="min-h-11 w-full rounded-xl border border-line-strong bg-surface-2 py-2 pl-10 pr-3 text-base text-ink outline-none placeholder:text-muted focus:border-primary"
          />
        </form>

        {ready && !failed && !hits && <p className="mt-2 text-base text-ink">Đang tìm…</p>}
        {ready && failed && (
          <p className="mt-2 text-base text-ink">
            {variant === "account"
              ? "Chưa tải được danh sách bài. Em mở Lớp học để xem."
              : "Chưa tải được danh sách bài. Em chọn lớp ở phía trên để xem."}
          </p>
        )}
        {ready && !failed && hits && shown.length === 0 && (
          <p className="mt-2 text-base text-ink">Không thấy bài khớp. Thử từ khoá khác.</p>
        )}
        {shown.length > 0 && (
          <ul className="mt-2 divide-y divide-line overflow-hidden rounded-xl border border-line">
            {shown.map(({ hit, at, span }) => {
              const snip = at === -1 ? null : snippetOf(hit.text, at, span);
              return (
                <li key={hit.id}>
                  <Link
                    href={hit.href}
                    className="flex min-h-11 flex-col justify-center px-3 py-2 text-ink hover:bg-surface-2"
                  >
                    <span className="text-base font-semibold leading-snug">{hit.title}</span>
                    <span className="text-sm leading-snug text-ink">{hit.meta}</span>
                    {snip && (
                      <span className="mt-0.5 text-sm leading-snug text-ink">
                        {snip.before}
                        <mark className="rounded-sm bg-amber-300/25 px-0.5 text-amber-100">{snip.hit}</mark>
                        {snip.after}
                      </span>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        )}
        {rows.length > MAX_HITS && (
          <p className="mt-2 text-sm text-ink">
            Còn {rows.length - MAX_HITS} bài nữa. Gõ thêm chữ để hẹp lại.
          </p>
        )}
      </div>
    </section>
  );
}
