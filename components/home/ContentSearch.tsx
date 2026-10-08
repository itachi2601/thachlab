"use client";

import { useState } from "react";
import Link from "next/link";
import { Search } from "lucide-react";

/**
 * Tìm bài theo tên, trên trang chủ. Danh sách lấy từ /data/catalog.json (file tĩnh lúc build),
 * chỉ tải khi em chạm ô tìm — không gọi Supabase (quy tắc không thêm round-trip cho /).
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

interface Hit {
  id: number;
  title: string;
  meta: string;
  href: string;
  titleHay: string;
  chapterHay: string;
  rank: number;
}

const MAX_HITS = 8;

function fold(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/gi, "d")
    .toLowerCase()
    .replace(/\s+/g, " ")
    .trim();
}

function classLabel(name: string): string {
  return /^\d+$/.test(name) ? `Lớp ${name}` : name;
}

function toHits(catalog: CatalogFile): Hit[] {
  const classes = new Map(catalog.classes.map((item) => [item.id, item]));
  const chapters = new Map(catalog.chapters.map((item) => [item.id, item]));
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
    hits.push({
      id: lesson.id,
      title: lesson.title,
      meta,
      href: `/lop-hoc/bai/?${params.toString()}`,
      titleHay: fold(lesson.title),
      chapterHay: fold(chapter.title),
      rank: lesson.sort_order,
    });
  }
  return hits;
}

let catalogPromise: Promise<Hit[] | null> | null = null;

function loadHits(): Promise<Hit[] | null> {
  if (!catalogPromise) {
    catalogPromise = fetch("/data/catalog.json")
      .then((res) => (res.ok ? (res.json() as Promise<CatalogFile>) : null))
      .then((catalog) => {
        if (!catalog || !Array.isArray(catalog.lessons) || !Array.isArray(catalog.chapters)) return null;
        return toHits(catalog);
      })
      .catch(() => null);
  }
  return catalogPromise;
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
  const matches =
    !hits || tokens.length === 0 || folded.length < 2
      ? []
      : hits
          .map((hit) => {
            let score = 0;
            tokens.forEach((token, index) => {
              const weight = tokens.length - index;
              if (hit.titleHay.includes(token)) score += weight * 2;
              else if (hit.chapterHay.includes(token)) score += weight;
            });
            return score > 0 ? { hit, score } : null;
          })
          .filter((row): row is { hit: Hit; score: number } => row !== null)
          .sort((a, b) => b.score - a.score || a.hit.rank - b.hit.rank)
          .map((row) => row.hit);

  const shown = matches.slice(0, MAX_HITS);
  const ready = folded.length >= 2;

  const shell =
    variant === "account"
      ? "rounded-2xl border border-white/10 bg-panel p-4 sm:p-5"
      : "bg-[#05070B] px-6 pb-10 pt-2 lg:px-12";

  return (
    <section className={shell} aria-label="Tìm bài học">
      <div className={variant === "account" ? "" : "mx-auto max-w-6xl"}>
        <h2 className="font-display text-xl font-bold text-white sm:text-2xl">Tìm bài học</h2>
        <form
          className="relative mt-3"
          role="search"
          onSubmit={(event) => {
            event.preventDefault();
            const first = shown[0];
            if (first) window.location.assign(first.href);
          }}
        >
          <label htmlFor="content-search" className="sr-only">
            Tên bài học
          </label>
          <Search size={18} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            id="content-search"
            type="search"
            enterKeyHint="search"
            value={query}
            placeholder="Gõ tên bài, ví dụ ném ngang"
            onFocus={ensureLoaded}
            onChange={(event) => {
              ensureLoaded();
              setQuery(event.target.value);
            }}
            className="min-h-11 w-full rounded-xl border border-white/15 bg-white/[0.07] py-2 pl-10 pr-3 text-base text-white outline-none placeholder:text-slate-400 focus:border-cyan-300/70"
          />
        </form>

        {!ready && (
          <p className="mt-3 text-base leading-relaxed text-slate-300">
            Gõ tên bài. Ví dụ: ném ngang, dao động, điện trường.
          </p>
        )}
        {ready && !failed && !hits && (
          <p className="mt-3 text-base leading-relaxed text-slate-300">Đang tìm…</p>
        )}
        {ready && failed && (
          <p className="mt-3 text-base leading-relaxed text-slate-300">
            {variant === "account"
              ? "Chưa tải được danh sách bài. Em mở Lớp học để xem."
              : "Chưa tải được danh sách bài. Em chọn lớp ở phía trên để xem."}
          </p>
        )}
        {ready && !failed && hits && shown.length === 0 && (
          <p className="mt-3 text-base leading-relaxed text-slate-300">
            Không thấy bài khớp. Thử tên ngắn hơn, ví dụ «dao động».
          </p>
        )}
        {shown.length > 0 && (
          <ul className="mt-3 divide-y divide-white/10 overflow-hidden rounded-xl border border-white/10">
            {shown.map((hit) => (
              <li key={hit.id}>
                <Link
                  href={hit.href}
                  className="flex min-h-11 flex-col justify-center px-3 py-2 text-white hover:bg-white/[0.08]"
                >
                  <span className="text-base font-semibold leading-snug">{hit.title}</span>
                  <span className="text-base leading-snug text-slate-300">{hit.meta}</span>
                </Link>
              </li>
            ))}
          </ul>
        )}
        {matches.length > MAX_HITS && (
          <p className="mt-2 text-base text-slate-300">
            Còn {matches.length - MAX_HITS} bài nữa. Gõ thêm chữ để hẹp lại.
          </p>
        )}
      </div>
    </section>
  );
}
