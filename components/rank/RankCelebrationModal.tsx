"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef } from "react";
import RankBadge from "@/components/rank/RankBadge";
import TitleBadge from "@/components/rank/TitleBadge";
import { levelTextColor } from "@/features/rank/badge-assets";
import { LEVEL_LABELS, divisionLabel, tierMeta, type TierCode, type TitleLevel } from "@/features/rank/types";

export type CelebrationEvent =
  | { kind: "rank"; code: TierCode; division: number | null; paragon: boolean; name: string; en: string }
  | { kind: "title"; code: string; level: TitleLevel; name: string; description: string; first: boolean };

/** Pháo giấy bằng canvas thuần (không thêm thư viện), tự dừng sau ~4,5 s. */
function useConfetti(ref: React.RefObject<HTMLCanvasElement | null>, colors: string[]) {
  useEffect(() => {
    const cv = ref.current;
    if (!cv || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const ctx = cv.getContext("2d");
    if (!ctx) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const W = (cv.width = innerWidth * dpr);
    const H = (cv.height = innerHeight * dpr);
    const mk = (fromX: number, angle: number) => {
      const a = angle + (Math.random() - 0.5) * 0.9;
      const v = (9 + Math.random() * 11) * dpr;
      return {
        x: fromX * W, y: H * 0.95, vx: Math.cos(a) * v, vy: Math.sin(a) * v,
        w: (6 + Math.random() * 6) * dpr, h: (3 + Math.random() * 5) * dpr,
        r: Math.random() * 6, vr: (Math.random() - 0.5) * 0.4,
        c: colors[Math.floor(Math.random() * colors.length)], round: Math.random() < 0.25,
      };
    };
    const ps = [
      ...Array.from({ length: 70 }, () => mk(0.08, -Math.PI / 3)),
      ...Array.from({ length: 70 }, () => mk(0.92, (-2 * Math.PI) / 3)),
    ];
    const start = performance.now();
    let raf = 0;
    const frame = (now: number) => {
      const t = now - start;
      ctx.clearRect(0, 0, W, H);
      for (const p of ps) {
        p.vy += 0.32 * dpr; p.vx *= 0.992; p.vy *= 0.992;
        p.x += p.vx; p.y += p.vy; p.r += p.vr;
        ctx.globalAlpha = Math.max(0, Math.min(1, (4500 - t) / 900));
        ctx.fillStyle = p.c;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r);
        if (p.round) { ctx.beginPath(); ctx.arc(0, 0, p.w / 2, 0, 7); ctx.fill(); }
        else ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
        ctx.restore();
      }
      if (t < 4500) raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    return () => cancelAnimationFrame(raf);
  }, [ref, colors]);
}

export default function RankCelebrationModal({ event, remaining, onNext }: { event: CelebrationEvent; remaining: number; onNext: () => void }) {
  const isRank = event.kind === "rank";
  const meta = isRank ? tierMeta(event.code, event.paragon) : null;
  const accent = meta ? meta.light : levelTextColor(event.kind === "title" ? event.level : "don");
  const base = meta ? meta.color : "#e2b93b";
  const cv = useRef<HTMLCanvasElement>(null);
  const btn = useRef<HTMLButtonElement>(null);
  const palette = useMemo(() => [accent, base, "#fff3cf", "#e2b93b", "#ffffff"], [accent, base]);
  useConfetti(cv, palette);

  useEffect(() => {
    btn.current?.focus();
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onNext();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onNext, event]);

  const headline = isRank
    ? "Lên hạng!"
    : event.first ? "Danh hiệu mới!" : `Lên mức ${LEVEL_LABELS[event.level] || "cao hơn"}!`;
  const rankName = isRank ? `${event.paragon ? "" : `${event.en} ${divisionLabel(event.division)} · `}${event.name}`.trim() : "";

  return (
    <div role="dialog" aria-modal="true" aria-label={headline} className="fixed inset-0 z-[90] grid place-items-center p-4 animate-modal-backdrop-in" style={{ background: "rgba(5,8,20,.82)" }}>
      <canvas ref={cv} aria-hidden className="pointer-events-none absolute inset-0 h-full w-full" />
      <div
        className="rcl-card relative w-full max-w-sm overflow-hidden rounded-3xl border px-6 pb-6 pt-8 text-center shadow-2xl"
        style={{ background: "linear-gradient(170deg,#141a33,#0b0f20)", borderColor: `${base}99`, boxShadow: `0 0 80px ${base}66` }}
      >
        <div aria-hidden className="rcl-rays pointer-events-none absolute left-1/2 top-[150px] h-[520px] w-[520px] -translate-x-1/2 -translate-y-1/2 opacity-40"
          style={{ background: `repeating-conic-gradient(from 0deg, ${accent}55 0 8deg, transparent 8deg 24deg)`, WebkitMaskImage: "radial-gradient(circle, #000 8%, transparent 62%)", maskImage: "radial-gradient(circle, #000 8%, transparent 62%)" }} />
        <div aria-hidden className="rcl-glow pointer-events-none absolute left-1/2 top-[150px] h-52 w-52 -translate-x-1/2 -translate-y-1/2 rounded-full" style={{ background: `radial-gradient(circle, ${accent}88, transparent 70%)` }} />

        <p className="rcl-rise relative text-sm font-semibold uppercase tracking-[.22em]" style={{ color: accent, animationDelay: ".1s" }}>Chúc mừng</p>
        <div className={`rcl-badge relative mx-auto mt-3 grid place-items-center ${isRank ? "h-[250px]" : "h-40"}`}>
          {isRank ? (
            <RankBadge code={event.code} division={event.division} paragon={event.paragon} size={150} />
          ) : (
            <TitleBadge code={event.code} level={event.level} size={140} priority />
          )}
          <span aria-hidden className="rcl-shine absolute inset-0" />
        </div>
        <h2 className="rcl-rise relative mt-4 text-3xl font-extrabold text-white" style={{ animationDelay: ".55s" }}>{headline}</h2>
        <p className="rcl-rise relative mt-1 text-xl font-bold" style={{ color: accent, animationDelay: ".7s" }}>{isRank ? rankName : event.name}</p>
        <p className="rcl-rise relative mx-auto mt-2 max-w-[28ch] text-base leading-relaxed text-slate-300" style={{ animationDelay: ".85s" }}>
          {isRank ? "Nỗ lực bền bỉ của em đã được ghi nhận. Giữ nhịp này và chạm tới bậc kế tiếp nhé!" : event.description || "Em vừa chinh phục thêm một danh hiệu chuyên môn."}
        </p>

        <div className="rcl-rise relative mt-6 flex flex-col gap-2" style={{ animationDelay: "1s" }}>
          <button ref={btn} onClick={onNext} className="min-h-12 rounded-xl px-5 text-base font-bold text-[#1a1305] transition active:scale-[.98]" style={{ background: `linear-gradient(135deg,#fff3cf,${accent})` }}>
            {remaining > 0 ? `Tiếp theo (còn ${remaining})` : "Tuyệt vời!"}
          </button>
          <Link href="/lop-hoc/xep-hang" onClick={onNext} className="inline-flex min-h-11 items-center justify-center text-sm font-semibold text-slate-300 underline-offset-4 hover:underline">
            Xem hành trình rank của em
          </Link>
        </div>
      </div>
    </div>
  );
}
