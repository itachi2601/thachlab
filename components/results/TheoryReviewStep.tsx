"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Check, Circle } from "lucide-react";
import Button from "@/components/ui/Button";
import ContentHtml from "@/components/exams/ContentHtml";
import { estimateTheoryTime, splitTheorySections } from "@/features/lessons/theory-sections";
import {
  NO_THEORY_REVIEW,
  fetchTheoryItem,
  needLabel,
  pingTheoryReview,
  startTheoryReview,
  type TheoryReviewState,
  type TutoringNeed,
} from "@/services/tutoring";

/** Em im lặng quá chừng này (không cuộn, chạm, gõ) thì đồng hồ xem bài dừng — khớp luật "xem thật" của máy chủ. */
const IDLE_MS = 20_000;
const PING_EVERY_MS = 8_000;

/** Tên các nhóm radio (mỗi nhóm = một câu tự kiểm tra) trong HTML bài lý thuyết. */
function quizGroupNames(html: string): string[] {
  const names = new Set<string>();
  for (const tag of html.match(/<input\b[^>]*>/gi) ?? []) {
    if (!/\btype=["']?radio/i.test(tag)) continue;
    const name = tag.match(/\bname=["']([^"']+)["']/i)?.[1];
    if (name) names.add(name);
  }
  return [...names];
}

function mmss(sec: number): string {
  const s = Math.max(0, Math.round(sec));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

function Row({ done, label, value }: { done: boolean; label: string; value: string }) {
  // M4: trạng thái đạt/chưa không chỉ bằng màu — có biểu tượng và chữ.
  return (
    <li className="flex items-center justify-between gap-3 text-sm">
      <span className="flex items-center gap-2 text-slate-200">
        {done ? (
          <Check size={16} className="shrink-0 text-emerald-300" aria-label="Xong" />
        ) : (
          <Circle size={16} className="shrink-0 text-slate-500" aria-label="Chưa xong" />
        )}
        {label}
      </span>
      <span className={done ? "font-semibold text-emerald-300" : "text-slate-400"}>{value}</span>
    </li>
  );
}

/**
 * Bước 1 của tự kiểm tra thoát phụ đạo: xem lại bài LÝ THUYẾT TƯƠNG TÁC của chủ đề. Ghi nhận quá trình xem
 * (thời gian thật, các mốc đã cuộn tới, câu tự kiểm tra trong bài đã trả lời) và gửi lên máy chủ; chỉ khi máy chủ
 * xác nhận hoàn thành thì mới cho sang bài thoát (và trigger DB cũng chặn nộp nếu chưa hoàn thành).
 *
 * Quy tắc: N1 (một màn hình = một việc: chỉ bài lý thuyết + bảng tiến độ), N5 (giữ nguyên các mốc của bài),
 * M4 (tiến độ có biểu tượng + chữ), B4 (không chuyển động khi đang đọc), D2/D3 (nút chính ≥44px, dưới cùng), L4.
 */
export default function TheoryReviewStep({
  need,
  onReady,
}: {
  need: TutoringNeed;
  /** Máy chủ xác nhận đã xem đủ (hoặc chủ đề không có lý thuyết để xem) → sang bài thoát. */
  onReady: () => void;
}) {
  const [item, setItem] = useState<Awaited<ReturnType<typeof fetchTheoryItem>>>(null);
  const [phase, setPhase] = useState<"loading" | "viewing" | "error">("loading");
  const [server, setServer] = useState<TheoryReviewState>(NO_THEORY_REVIEW);
  const [seenCount, setSeenCount] = useState(0);
  const [answeredCount, setAnsweredCount] = useState(0);
  const [activeSec, setActiveSec] = useState(0);

  const scrollRef = useRef<HTMLDivElement>(null);
  const seen = useRef(new Set<number>());
  const answered = useRef(new Set<string>());
  const pending = useRef(0);
  const lastActivity = useRef(0);
  const sentProgress = useRef({ seen: 0, answered: 0 });
  const pinging = useRef(false);
  const completed = useRef(false);

  const onReadyRef = useRef(onReady);
  useEffect(() => {
    onReadyRef.current = onReady;
  });

  const parts = useMemo(() => (item ? splitTheorySections(item.bodyHtml, item.id) : null), [item]);
  const sectionHtmls = useMemo(() => {
    if (!item || !parts) return [];
    return parts.sections.length > 0 ? parts.sections.map((s) => s.html) : [item.bodyHtml];
  }, [item, parts]);

  // 1) Tải bài lý thuyết + mở lượt xem lại trên máy chủ.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        if (!need.lessonId) {
          onReadyRef.current();
          return;
        }
        const loaded = await fetchTheoryItem(need.lessonId);
        if (cancelled) return;
        if (!loaded) {
          onReadyRef.current();
          return;
        }
        const total = Math.max(1, splitTheorySections(loaded.bodyHtml, loaded.id).sections.length);
        const state = await startTheoryReview(need.id, {
          sections: total,
          quizTotal: quizGroupNames(loaded.bodyHtml).length,
          estSeconds: estimateTheoryTime(loaded.bodyHtml).minutes * 60,
        });
        if (cancelled) return;
        if (!state.required) {
          onReadyRef.current();
          return;
        }
        completed.current = state.completed;
        setItem(loaded);
        setServer(state);
        setActiveSec(state.activeSeconds);
        setSeenCount(state.sectionsSeen);
        setAnsweredCount(state.quizAnswered);
        sentProgress.current = { seen: state.sectionsSeen, answered: state.quizAnswered };
        setPhase("viewing");
      } catch {
        if (!cancelled) setPhase("error");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [need.id, need.lessonId]);

  // 2) Gửi tiến độ lên máy chủ (máy chủ là nguồn quyết định "hoàn thành").
  const flush = useCallback(async () => {
    if (pinging.current || completed.current) return;
    const delta = pending.current;
    const prog = { seen: seen.current.size, answered: answered.current.size };
    if (delta === 0 && prog.seen === sentProgress.current.seen && prog.answered === sentProgress.current.answered) return;
    pinging.current = true;
    pending.current = 0;
    try {
      const next = await pingTheoryReview(need.id, { delta, sectionsSeen: prog.seen, quizAnswered: prog.answered });
      if (next) {
        sentProgress.current = prog;
        completed.current = next.completed;
        setServer((prev) => ({
          ...prev,
          ...next,
          activeSeconds: Math.max(prev.activeSeconds, next.activeSeconds),
          sectionsSeen: Math.max(prev.sectionsSeen, next.sectionsSeen),
          quizAnswered: Math.max(prev.quizAnswered, next.quizAnswered),
          requiredSeconds: next.requiredSeconds || prev.requiredSeconds,
          sectionsTotal: next.sectionsTotal || prev.sectionsTotal,
          quizTotal: next.quizTotal || prev.quizTotal,
        }));
      } else {
        pending.current += delta; // mạng lỗi: giữ lại, lần sau gửi bù
      }
    } finally {
      pinging.current = false;
    }
  }, [need.id]);

  // 3) Đồng hồ xem thật + nhịp gửi.
  useEffect(() => {
    if (phase !== "viewing") return;
    const touch = () => {
      lastActivity.current = Date.now();
    };
    touch();
    const tick = window.setInterval(() => {
      if (completed.current) return;
      if (document.visibilityState === "visible" && Date.now() - lastActivity.current < IDLE_MS) {
        pending.current += 1;
        setActiveSec((s) => s + 1);
      }
    }, 1000);
    const ping = window.setInterval(() => void flush(), PING_EVERY_MS);
    const events = ["pointerdown", "keydown", "touchmove", "wheel"] as const;
    events.forEach((e) => window.addEventListener(e, touch, { passive: true }));
    const box = scrollRef.current;
    box?.addEventListener("scroll", touch, { passive: true });
    return () => {
      window.clearInterval(tick);
      window.clearInterval(ping);
      events.forEach((e) => window.removeEventListener(e, touch));
      box?.removeEventListener("scroll", touch);
      void flush();
    };
  }, [phase, flush]);

  // 4) Cuộn tới cuối mỗi mốc = đã xem mốc đó.
  useEffect(() => {
    const box = scrollRef.current;
    if (phase !== "viewing" || !box) return;
    const targets = Array.from(box.querySelectorAll<HTMLElement>("[data-sec-end]"));
    const observer = new IntersectionObserver(
      (entries) => {
        let changed = false;
        for (const e of entries) {
          if (!e.isIntersecting) continue;
          const idx = Number((e.target as HTMLElement).dataset.secEnd);
          if (Number.isInteger(idx) && !seen.current.has(idx)) {
            seen.current.add(idx);
            changed = true;
          }
        }
        if (changed) {
          setSeenCount(seen.current.size);
          lastActivity.current = Date.now();
        }
      },
      { root: box, threshold: 0 },
    );
    targets.forEach((t) => observer.observe(t));
    return () => observer.disconnect();
  }, [phase, sectionHtmls.length]);

  // 5) Trả lời câu tự kiểm tra trong bài (radio CSS-only) = một tương tác.
  useEffect(() => {
    const box = scrollRef.current;
    if (phase !== "viewing" || !box) return;
    const onChange = (e: Event) => {
      const t = e.target;
      if (!(t instanceof HTMLInputElement) || t.type !== "radio" || !t.name) return;
      if (!answered.current.has(t.name)) {
        answered.current.add(t.name);
        setAnsweredCount(answered.current.size);
      }
      lastActivity.current = Date.now();
    };
    box.addEventListener("change", onChange);
    return () => box.removeEventListener("change", onChange);
  }, [phase]);

  // Có thêm mốc/câu mới thì báo sớm một nhịp (không đợi 8 giây) để nút mở khoá nhanh.
  useEffect(() => {
    if (phase !== "viewing") return;
    const t = window.setTimeout(() => void flush(), 700);
    return () => window.clearTimeout(t);
  }, [phase, seenCount, answeredCount, flush]);

  const done = server.completed;
  const secTotal = server.sectionsTotal || sectionHtmls.length || 1;
  const secNow = Math.min(secTotal, Math.max(seenCount, server.sectionsSeen));
  const quizTotal = server.quizTotal;
  const quizNeed = Math.ceil(quizTotal * 0.8);
  const quizNow = Math.min(quizTotal, Math.max(answeredCount, server.quizAnswered));
  const reqSec = server.requiredSeconds;
  const timeNow = Math.min(reqSec, Math.max(activeSec, server.activeSeconds));

  if (phase === "loading") return <p className="text-sm text-slate-400">Đang mở bài lý thuyết…</p>;
  if (phase === "error") {
    return (
      <div className="space-y-3">
        <p className="text-sm text-amber-200">Chưa mở được bài lý thuyết. Em kiểm tra mạng rồi mở lại bài tự kiểm tra nhé.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-sky-300">Bước 1 · Xem lại lý thuyết</p>
        <p className="mt-1 text-sm text-slate-300">
          Đọc bài <strong className="text-white">{item?.title || needLabel(need)}</strong>, làm các câu tự kiểm tra
          trong bài. Xong cả ba mục dưới đây thì mở bài thoát phụ đạo.
        </p>
      </div>

      <ul className="space-y-2 rounded-xl border border-white/10 bg-white/5 p-3" aria-live="polite">
        <Row done={secNow >= secTotal} label="Đọc hết các mốc" value={`${secNow}/${secTotal}`} />
        {quizTotal > 0 && (
          <Row done={quizNow >= quizNeed} label="Trả lời câu tự kiểm tra" value={`${quizNow}/${quizNeed} câu`} />
        )}
        <Row done={timeNow >= reqSec} label="Thời gian đọc" value={`${mmss(timeNow)}/${mmss(reqSec)}`} />
      </ul>

      <div
        ref={scrollRef}
        className="max-h-[52vh] overflow-y-auto rounded-xl border border-white/10 bg-panel/60 p-3 sm:p-4"
        tabIndex={0}
        aria-label="Bài lý thuyết"
      >
        {parts && parts.introHtml.trim() !== "" && parts.sections.length > 0 && (
          <ContentHtml html={parts.introHtml} className="block leading-relaxed" />
        )}
        {sectionHtmls.map((html, i) => (
          <div key={i}>
            <ContentHtml html={html} className="block leading-relaxed" />
            <div data-sec-end={i} aria-hidden className="h-px" />
          </div>
        ))}
      </div>

      <Button onClick={() => onReadyRef.current()} disabled={!done} className="w-full">
        {done ? "Sang bài thoát phụ đạo" : "Hoàn thành cả ba mục để mở bài thoát"}
      </Button>
    </div>
  );
}
