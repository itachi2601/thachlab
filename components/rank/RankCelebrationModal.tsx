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

/** Pháo hoa + pháo giấy bằng canvas thuần (không thêm thư viện), phủ TRÊN thẻ, bắt đầu khi huy chương lộ diện (~1,3 s), tự dừng ~5 s. */
function useFireworks(cv: React.RefObject<HTMLCanvasElement | null>, badge: React.RefObject<HTMLElement | null>, colors: string[]) {
  useEffect(() => {
    const c = cv.current;
    if (!c || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const ctx = c.getContext("2d");
    if (!ctx) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const W = (c.width = innerWidth * dpr);
    const H = (c.height = innerHeight * dpr);
    const r = badge.current?.getBoundingClientRect();
    const cx = (r ? r.left + r.width / 2 : innerWidth / 2) * dpr;
    const cy = (r ? r.top + r.height / 2 : innerHeight / 3) * dpr;
    const pick = () => colors[Math.floor(Math.random() * colors.length)];
    type P = { x: number; y: number; vx: number; vy: number; life: number; max: number; c: string; kind: "spark" | "paper"; w: number; r: number; vr: number; at: number };
    const ps: P[] = [];
    const burst = (x: number, y: number, at: number) => {
      const col = pick();
      for (let i = 0; i < 46; i++) {
        const a = (i / 46) * Math.PI * 2 + Math.random() * 0.2;
        const v = (3 + Math.random() * 5) * dpr;
        ps.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 0, max: 70 + Math.random() * 30, c: Math.random() < 0.3 ? "#ffffff" : col, kind: "spark", w: 2 * dpr, r: 0, vr: 0, at });
      }
    };
    const paper = (fx: number, ang: number, at: number) => {
      for (let i = 0; i < 45; i++) {
        const a = ang + (Math.random() - 0.5) * 0.9;
        const v = (10 + Math.random() * 11) * dpr;
        ps.push({ x: fx * W, y: H * 0.98, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 0, max: 150, c: pick(), kind: "paper", w: (5 + Math.random() * 6) * dpr, r: Math.random() * 6, vr: (Math.random() - 0.5) * 0.4, at });
      }
    };
    const t0 = 1300;
    burst(cx, cy, t0);
    burst(cx - 110 * dpr, cy - 60 * dpr, t0 + 450);
    burst(cx + 120 * dpr, cy - 40 * dpr, t0 + 800);
    burst(cx - 60 * dpr, cy + 90 * dpr, t0 + 1300);
    burst(cx + 70 * dpr, cy + 80 * dpr, t0 + 1700);
    burst(cx, cy - 120 * dpr, t0 + 2100);
    paper(0.06, -Math.PI / 3, t0 + 300);
    paper(0.94, (-2 * Math.PI) / 3, t0 + 300);
    const start = performance.now();
    let raf = 0;
    const frame = (now: number) => {
      const t = now - start;
      ctx.clearRect(0, 0, W, H);
      let alive = false;
      for (const p of ps) {
        if (t < p.at) { alive = true; continue; }
        if (p.life > p.max) continue;
        alive = true;
        p.life++;
        const k = 1 - p.life / p.max;
        ctx.globalAlpha = Math.max(0, p.kind === "spark" ? k : Math.min(1, k * 2));
        ctx.fillStyle = ctx.strokeStyle = p.c;
        if (p.kind === "spark") {
          p.vx *= 0.97; p.vy = p.vy * 0.97 + 0.07 * dpr;
          ctx.lineWidth = p.w;
          ctx.lineCap = "round";
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x - p.vx * 2.2, p.y - p.vy * 2.2); ctx.stroke();
          p.x += p.vx; p.y += p.vy;
        } else {
          p.vy += 0.32 * dpr; p.vx *= 0.992; p.vy *= 0.992; p.x += p.vx; p.y += p.vy; p.r += p.vr;
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r); ctx.fillRect(-p.w / 2, -p.w / 4, p.w, p.w / 2); ctx.restore();
        }
      }
      if (alive) raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    return () => cancelAnimationFrame(raf);
  }, [cv, badge, colors]);
}

export default function RankCelebrationModal({ event, remaining, onNext }: { event: CelebrationEvent; remaining: number; onNext: () => void }) {
  const isRank = event.kind === "rank";
  const meta = isRank ? tierMeta(event.code, event.paragon) : null;
  const accent = meta ? meta.light : levelTextColor(event.kind === "title" ? event.level : "don");
  const base = meta ? meta.color : "#e2b93b";
  const cv = useRef<HTMLCanvasElement>(null);
  const badgeBox = useRef<HTMLDivElement>(null);
  const btn = useRef<HTMLButtonElement>(null);
  const palette = useMemo(() => [accent, base, "#fff3cf", "#e2b93b", "#ffffff"], [accent, base]);
  useFireworks(cv, badgeBox, palette);

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
      <div
        className="rcl-card relative w-full max-w-sm overflow-hidden rounded-3xl border px-6 pb-6 pt-8 text-center shadow-2xl"
        style={{ background: "linear-gradient(170deg,#141a33,#0b0f20)", borderColor: `${base}99`, boxShadow: `0 0 80px ${base}66` }}
      >
        <div aria-hidden className="rcl-rays pointer-events-none absolute left-1/2 top-[150px] h-[520px] w-[520px] -translate-x-1/2 -translate-y-1/2 opacity-40"
          style={{ background: `repeating-conic-gradient(from 0deg, ${accent}55 0 8deg, transparent 8deg 24deg)`, WebkitMaskImage: "radial-gradient(circle, #000 8%, transparent 62%)", maskImage: "radial-gradient(circle, #000 8%, transparent 62%)" }} />
        <div aria-hidden className="rcl-glow pointer-events-none absolute left-1/2 top-[150px] h-52 w-52 -translate-x-1/2 -translate-y-1/2 rounded-full" style={{ background: `radial-gradient(circle, ${accent}88, transparent 70%)` }} />

        <p className="rcl-rise relative text-sm font-semibold uppercase tracking-[.22em]" style={{ color: accent, animationDelay: ".1s" }}>Chúc mừng</p>
        <div ref={badgeBox} className={`rcl-stage relative mx-auto mt-3 grid place-items-center ${isRank ? "h-[250px]" : "h-40"}`}>
          <span aria-hidden className="rcl-flash" style={{ background: `radial-gradient(circle, #fff 0%, ${accent} 30%, transparent 68%)` }} />
          <span aria-hidden className="rcl-ring" style={{ borderColor: accent }} />
          <span aria-hidden className="rcl-ring rcl-ring2" style={{ borderColor: "#fff" }} />
          <div className="rcl-badge relative grid place-items-center overflow-hidden">
            {isRank ? (
              <RankBadge code={event.code} division={event.division} paragon={event.paragon} size={150} />
            ) : (
              <TitleBadge code={event.code} level={event.level} size={140} priority />
            )}
            <span aria-hidden className="rcl-shine absolute inset-0" />
          </div>
        </div>
        <h2 className="rcl-rise relative mt-4 text-3xl font-extrabold text-white" style={{ animationDelay: "1.5s" }}>{headline}</h2>
        <p className="rcl-rise relative mt-1 text-xl font-bold" style={{ color: accent, animationDelay: "1.65s" }}>{isRank ? rankName : event.name}</p>
        <p className="rcl-rise relative mx-auto mt-2 max-w-[28ch] text-base leading-relaxed text-white/90" style={{ animationDelay: "1.8s" }}>
          {isRank ? "Nỗ lực bền bỉ của em đã được ghi nhận. Giữ nhịp này và chạm tới bậc kế tiếp nhé!" : event.description || "Em vừa chinh phục thêm một danh hiệu chuyên môn."}
        </p>

        <div className="rcl-rise relative mt-6 flex flex-col gap-2" style={{ animationDelay: "1.95s" }}>
          <button ref={btn} onClick={onNext} className="min-h-12 rounded-xl px-5 text-base font-bold text-[#1a1305] transition active:scale-[.98]" style={{ background: `linear-gradient(135deg,#fff3cf,${accent})` }}>
            {remaining > 0 ? `Tiếp theo (còn ${remaining})` : "Tuyệt vời!"}
          </button>
          <Link href="/lop-hoc/xep-hang" onClick={onNext} className="inline-flex min-h-11 items-center justify-center text-sm font-semibold text-white/90 underline-offset-4 hover:underline">
            Xem hành trình rank của em
          </Link>
        </div>
      </div>
      <canvas ref={cv} aria-hidden className="pointer-events-none absolute inset-0 z-10 h-full w-full" />
    </div>
  );
}
