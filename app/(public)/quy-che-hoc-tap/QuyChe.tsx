"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ChevronLeft, ChevronRight, Maximize, Presentation, X } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { PAGE_INTRO, PAGE_TITLE, SECTIONS, UPDATED, type Section } from "./content";

// Bản đọc: cuộn như trang Điều khoản. Bản chiếu (?chieu=1): mỗi mục một màn, chữ to, ←/→/Space đổi mục, Esc thoát.
// Mã quy tắc: N1 (một màn một việc), N2 (≤4 thao tác), C1 (chữ to), B4 (không hoạt hình), D2 (đích chạm 44px).

const h2 = "mt-10 font-display text-xl font-bold text-ink scroll-mt-28";
const p = "mt-3 text-base leading-relaxed text-ink";
const ul = "mt-3 list-disc space-y-2 pl-6 text-base leading-relaxed text-ink marker:text-muted";

function ReadingView() {
  const [first, ...rest] = SECTIONS;
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-2xl px-4 pb-20 pt-28">
        <h1 className="font-display text-3xl font-bold text-ink">{PAGE_TITLE}</h1>
        <p className="mt-2 text-sm text-muted">Cập nhật {UPDATED}</p>
        <p className={p}>{PAGE_INTRO}</p>
        <Link
          href="/quy-che-hoc-tap/?chieu=1"
          className="mt-4 inline-flex min-h-11 items-center gap-2 rounded-full border border-line px-4 text-sm font-semibold text-ink transition hover:border-primary hover:text-primary"
        >
          <Presentation size={16} aria-hidden /> Chiếu cho cả lớp
        </Link>

        <section id={first.id} className="mt-10 scroll-mt-28 rounded-2xl border border-primary/30 bg-primary-soft p-5">
          <h2 className="font-display text-xl font-bold text-ink">1. {first.title}</h2>
          <ol className="mt-3 list-decimal space-y-2 pl-6 text-base leading-relaxed text-ink marker:font-semibold">
            {first.items.map((it, i) => (
              <li key={i}>{it}</li>
            ))}
          </ol>
          {first.note && <p className="mt-3 text-sm text-muted">{first.note}</p>}
        </section>

        <nav aria-label="Mục lục" className="mt-8 rounded-2xl border border-line bg-panel p-4">
          <ul className="space-y-1 text-base">
            {SECTIONS.map((s, i) => (
              <li key={s.id}>
                <a href={`#${s.id}`} className="inline-flex min-h-11 items-center text-primary underline-offset-2 hover:underline">
                  {i + 1}. {s.title}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {rest.map((s, i) => (
          <section key={s.id}>
            <h2 id={s.id} className={h2}>
              {i + 2}. {s.title}
            </h2>
            {s.lead && <p className={p}>{s.lead}</p>}
            <ul className={ul}>
              {s.items.map((it, j) => (
                <li key={j}>{it}</li>
              ))}
            </ul>
          </section>
        ))}

        <div className="mt-10 flex flex-wrap gap-3">
          <Link href="/lop-hoc" className="inline-flex min-h-11 items-center rounded-xl bg-primary px-5 py-3 font-semibold text-white hover:bg-primary-dark">
            Vào lớp học
          </Link>
          <Link href="/tai-khoan" className="inline-flex min-h-11 items-center rounded-xl border border-line px-5 py-3 font-semibold text-ink hover:border-line-strong">
            Trang chủ học sinh
          </Link>
        </div>
      </main>
      <Footer />
    </>
  );
}

// Mỗi slide: slide đầu là tên trang; các slide sau là một mục, tối đa 4 ý một màn (G1, N2) — mục dài tách thành "tiếp".
const MAX_ITEMS = 4;
type SlideData = { section: Section; no: number; part: number; parts: number; items: Section["items"]; start: number };
const SLIDES: SlideData[] = SECTIONS.flatMap((section, k) => {
  const parts = Math.ceil(section.items.length / MAX_ITEMS);
  return Array.from({ length: parts }, (_, part) => ({
    section,
    no: k + 1,
    part,
    parts,
    items: section.items.slice(part * MAX_ITEMS, (part + 1) * MAX_ITEMS),
    start: part * MAX_ITEMS,
  }));
});

function Slide({ index }: { index: number }) {
  if (index === 0) {
    return (
      <div className="m-auto max-w-4xl text-center">
        <h1 className="font-display text-[clamp(2rem,5vw,4rem)] font-bold leading-tight text-ink">{PAGE_TITLE}</h1>
        <p className="mx-auto mt-6 max-w-2xl text-[clamp(1.1rem,2.2vw,1.75rem)] leading-relaxed text-muted">{PAGE_INTRO}</p>
      </div>
    );
  }
  const d = SLIDES[index - 1];
  const s = d.section;
  const Tag = s.ordered ? "ol" : "ul";
  return (
    <div className="m-auto w-full max-w-5xl">
      <p className="font-mono text-[clamp(0.9rem,1.5vw,1.25rem)] uppercase tracking-widest text-primary">
        Mục {d.no}/{SECTIONS.length}
        {d.parts > 1 ? ` · phần ${d.part + 1}/${d.parts}` : ""}
      </p>
      <h1 className="mt-2 font-display text-[clamp(1.75rem,4vw,3.25rem)] font-bold leading-tight text-ink">{s.title}</h1>
      {s.lead && d.part === 0 && <p className="mt-4 text-[clamp(1.1rem,2.2vw,1.75rem)] leading-relaxed text-muted">{s.lead}</p>}
      <Tag
        start={d.start + 1}
        className={`mt-6 space-y-4 pl-8 text-[clamp(1.15rem,2.4vw,2rem)] leading-snug text-ink marker:text-primary ${
          s.ordered ? "list-decimal marker:font-bold" : "list-disc"
        }`}
      >
        {d.items.map((it, i) => (
          <li key={i}>{it}</li>
        ))}
      </Tag>
      {s.note && d.part === d.parts - 1 && <p className="mt-6 text-[clamp(1rem,1.8vw,1.4rem)] text-muted">{s.note}</p>}
    </div>
  );
}

function PresentView() {
  const total = SLIDES.length + 1;
  const [i, setI] = useState(0);
  const go = useCallback((d: number) => setI((v) => Math.min(total - 1, Math.max(0, v + d))), [total]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") {
        e.preventDefault();
        go(1);
      } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        e.preventDefault();
        go(-1);
      } else if (e.key === "Escape") {
        window.location.assign("/quy-che-hoc-tap/");
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [go]);

  const btn =
    "inline-flex min-h-11 min-w-11 items-center justify-center gap-1.5 rounded-full border border-line bg-panel px-4 text-sm font-semibold text-ink transition hover:border-primary hover:text-primary disabled:opacity-40";

  return (
    <div className="fixed inset-0 z-[100] flex flex-col bg-bg">
      <div className="flex flex-1 overflow-y-auto px-6 py-8 sm:px-12">
        <Slide index={i} />
      </div>
      <div className="flex items-center justify-between gap-3 border-t border-line bg-panel px-4 py-3">
        <Link href="/quy-che-hoc-tap/" className={btn} aria-label="Thoát chế độ chiếu">
          <X size={16} aria-hidden /> Thoát
        </Link>
        <div className="flex items-center gap-3">
          <button type="button" onClick={() => go(-1)} disabled={i === 0} className={btn} aria-label="Mục trước">
            <ChevronLeft size={18} aria-hidden />
          </button>
          <span className="min-w-14 text-center text-sm font-semibold tabular-nums text-muted">
            {i + 1}/{total}
          </span>
          <button type="button" onClick={() => go(1)} disabled={i === total - 1} className={btn} aria-label="Mục sau">
            <ChevronRight size={18} aria-hidden />
          </button>
        </div>
        <button
          type="button"
          onClick={() => document.documentElement.requestFullscreen?.().catch(() => undefined)}
          className={`${btn} hidden sm:inline-flex`}
          aria-label="Toàn màn hình"
        >
          <Maximize size={16} aria-hidden /> Toàn màn hình
        </button>
      </div>
    </div>
  );
}

export default function QuyChe() {
  const present = useSearchParams().get("chieu") === "1";
  return present ? <PresentView /> : <ReadingView />;
}
