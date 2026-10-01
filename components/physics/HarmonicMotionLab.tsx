"use client";

/**
 * components/physics/HarmonicMotionLab.tsx
 *
 * Widget tương tác cho Bài 1 — Dao động điều hoà (Vật lí 11). Một nguồn thời gian duy nhất
 * (rAF trong component này) chạy ba hình cùng lúc, nên học sinh thấy ngay mối liên hệ:
 *
 *   1. Điểm M quay tròn đều với tốc độ góc ω trên đường tròn bán kính A.
 *   2. Bóng Q của M trên trục Ox (đường kính thẳng đứng) — Q chính là vật dao động.
 *   3. Con lắc lò xo (SpringSimulation dùng chung với trang chủ) và đồ thị x–t.
 *
 * Phạm vi Bài 1 (theo ghi chú trong bản transcript SGK): KHÔNG đưa chu kì T, tần số f vào —
 * SGK để dành cho Bài 2 "Mô tả dao động điều hoà". Ở đây chỉ có A, ω (tốc độ góc của chuyển
 * động tròn đều, đúng như mục 4 của bài) và φ.
 *
 * Không gọi mạng, không đọc/ghi localStorage. Chỉ mount khi học sinh bấm "Mở mô phỏng"
 * (xem components/lessons/TheoryWidget.tsx) nên vòng lặp rAF không chạy khi chưa cần.
 */

import { useEffect, useMemo, useRef, useState } from "react";
import { Pause, Play, RotateCcw } from "lucide-react";
import { SpringSimulation } from "./SpringSimulation";
import { formatNumber } from "@/lib/physics";

const AMPLITUDE_RANGE = { min: 0.04, max: 0.16, step: 0.005 } as const; // mét (4–16 cm)
const OMEGA_RANGE = { min: 2, max: 10, step: 0.1 } as const; // rad/s — tốc độ góc của điểm M
const PHI_RANGE = { min: 0, max: 2 * Math.PI, step: 0.05 * Math.PI } as const;

const sliderClass =
  "h-1.5 w-full cursor-pointer appearance-none rounded-full bg-white/10 accent-[#2563EB] " +
  "[&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:appearance-none " +
  "[&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary " +
  "[&::-webkit-slider-thumb]:shadow-[0_0_0_3px_rgba(37,99,235,0.25)] " +
  "[&::-moz-range-thumb]:h-4 [&::-moz-range-thumb]:w-4 [&::-moz-range-thumb]:rounded-full " +
  "[&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:bg-primary";

/** φ hiển thị theo bội số của π: 0 · 0,50π · 1,00π … */
function phiLabel(phi: number): string {
  if (Math.abs(phi) < 1e-9) return "0";
  return `${formatNumber(phi / Math.PI, 2)}π`;
}

/** Hình chiếu Q của M lên trục Ox thẳng đứng: góc đo từ trục Ox dương (hướng lên). */
function CircleProjection({ angle, radius }: { angle: number; radius: number }) {
  const cx = 120;
  const cy = 122;
  const mX = cx + radius * Math.sin(angle);
  const mY = cy - radius * Math.cos(angle);
  const qY = cy - radius * Math.cos(angle);
  const topY = cy - radius - 16;
  const bottomY = cy + radius + 16;

  return (
    <svg viewBox="0 0 240 244" className="h-full w-full" role="img" aria-label="Hình chiếu của điểm M chuyển động tròn đều lên trục Ox">
      {/* trục Ox thẳng đứng + vạch chia */}
      <line x1={cx} y1={topY} x2={cx} y2={bottomY} stroke="rgba(148,163,184,.55)" strokeWidth="1.5" />
      <line x1={cx - 6} y1={cy} x2={cx + 6} y2={cy} stroke="rgba(148,163,184,.55)" strokeWidth="1.5" />
      {[1, -1].map((sign) => (
        <g key={sign}>
          <line x1={cx - 5} y1={cy - sign * radius} x2={cx + 5} y2={cy - sign * radius} stroke="rgba(148,163,184,.45)" strokeWidth="1.5" />
          <text x={cx - 12} y={cy - sign * radius + 4} textAnchor="end" fontSize="11" fill="#94a3b8">
            {sign > 0 ? "+A" : "−A"}
          </text>
        </g>
      ))}
      <text x={cx - 10} y={cy + 4} textAnchor="end" fontSize="11" fill="#94a3b8">
        O
      </text>
      <text x={cx + 8} y={topY + 4} fontSize="11" fill="#94a3b8">
        x
      </text>

      {/* quỹ đạo tròn của M */}
      <circle cx={cx} cy={cy} r={radius} fill="none" stroke="rgba(59,130,246,.45)" strokeWidth="1.5" strokeDasharray="4 4" />

      {/* bán kính OM và góc quay */}
      <line x1={cx} y1={cy} x2={mX} y2={mY} stroke="#60a5fa" strokeWidth="1.5" />
      <circle cx={mX} cy={mY} r="6" fill="#60a5fa" />
      <text x={mX + 9} y={mY - 4} fontSize="12" fill="#93c5fd">
        M
      </text>

      {/* đường chiếu M → Q (nằm ngang) và Q trên trục Ox */}
      <line x1={mX} y1={mY} x2={cx} y2={qY} stroke="rgba(250,204,21,.6)" strokeWidth="1.2" strokeDasharray="3 3" />
      <circle cx={cx} cy={qY} r="5.5" fill="#facc15" />
      <text x={cx + 10} y={qY + 4} fontSize="12" fill="#facc15">
        Q
      </text>

      {/* kéo dài sang phải cho thấy Q là "bóng" trên trục Ox */}
      <line x1={cx} y1={qY} x2={222} y2={qY} stroke="rgba(250,204,21,.35)" strokeWidth="1.2" strokeDasharray="3 5" />
    </svg>
  );
}

/** Đồ thị x–t của đúng một chu kì, kèm chấm ở thời điểm hiện tại. */
function OnePeriodChart({ amplitude, omega, phi, t }: { amplitude: number; omega: number; phi: number; t: number }) {
  const W = 340;
  const H = 172;
  const margin = { top: 14, right: 14, bottom: 24, left: 34 };
  const plotW = W - margin.left - margin.right;
  const plotH = H - margin.top - margin.bottom;
  const period = (2 * Math.PI) / omega;
  const midY = margin.top + plotH / 2;
  const toPx = (time: number) => margin.left + (time / period) * plotW;
  const toPy = (x: number) => midY - (x / amplitude) * (plotH / 2);

  const path = useMemo(() => {
    const steps = 120;
    let d = "";
    for (let i = 0; i <= steps; i++) {
      const time = (period * i) / steps;
      const x = amplitude * Math.cos(omega * time + phi);
      d += `${i === 0 ? "M" : "L"}${toPx(time).toFixed(2)},${toPy(x).toFixed(2)} `;
    }
    return d.trim();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [amplitude, omega, phi, period, plotW, plotH]);

  const phase = omega * t + phi;
  const dotX = toPx(((phase % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI) / omega);
  const dotY = toPy(amplitude * Math.cos(phase));

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="h-full w-full" role="img" aria-label="Đồ thị li độ theo thời gian trong một chu kì">
      {/* trục */}
      <line x1={margin.left} y1={midY} x2={W - margin.right} y2={midY} stroke="rgba(148,163,184,.4)" strokeWidth="1" />
      <line x1={margin.left} y1={margin.top} x2={margin.left} y2={H - margin.bottom} stroke="rgba(148,163,184,.4)" strokeWidth="1" />
      <text x={margin.left - 6} y={midY + 4} textAnchor="end" fontSize="10" fill="#94a3b8">
        0
      </text>
      <text x={margin.left - 6} y={toPy(amplitude) + 4} textAnchor="end" fontSize="10" fill="#94a3b8">
        +A
      </text>
      <text x={margin.left - 6} y={toPy(-amplitude) + 4} textAnchor="end" fontSize="10" fill="#94a3b8">
        −A
      </text>
      <text x={W - margin.right} y={H - 8} textAnchor="end" fontSize="10" fill="#94a3b8">
        t
      </text>
      <text x={margin.left + 4} y={H - 8} fontSize="10" fill="#94a3b8">
        1 chu kì
      </text>

      <path d={path} fill="none" stroke="#60a5fa" strokeWidth="2" strokeLinecap="round" />
      <circle cx={dotX} cy={dotY} r="4.5" fill="#facc15" />
    </svg>
  );
}

export default function HarmonicMotionLab() {
  const [amplitude, setAmplitude] = useState(0.1); // mét
  const [omega, setOmega] = useState(2 * Math.PI); // rad/s
  const [phi, setPhi] = useState(0); // rad
  const [t, setT] = useState(0); // s
  const [playing, setPlaying] = useState(() => {
    if (typeof window === "undefined" || !window.matchMedia) return true;
    return !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  });
  const lastRef = useRef<number | null>(null);

  useEffect(() => {
    if (!playing) {
      lastRef.current = null;
      return;
    }
    let raf = 0;
    const step = (now: number) => {
      const last = lastRef.current ?? now;
      const dt = Math.min((now - last) / 1000, 0.05); // chuyển tab về bị nhảy thời gian
      lastRef.current = now;
      setT((prev) => prev + dt);
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [playing]);

  const phase = omega * t + phi;
  const x = amplitude * Math.cos(phase);
  const v = -amplitude * omega * Math.sin(phase);
  const a = -amplitude * omega * omega * Math.cos(phase);
  const radius = Math.max(8, amplitude * 500);

  return (
    <div className="space-y-4">
      <p className="rounded-xl border border-line bg-black/20 px-4 py-3 text-center font-mono text-[15px] text-ink">
        x = {formatNumber(amplitude * 100, 1)}cos({formatNumber(omega, 2)}t + {phiLabel(phi)}) cm
      </p>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <div className="h-56 rounded-xl border border-line bg-black/20 p-2">
          <CircleProjection angle={phase} radius={radius} />
        </div>
        <div className="h-56 rounded-xl border border-line bg-black/20 p-2">
          <SpringSimulation x={x} v={v} a={a} amplitude={amplitude} />
        </div>
        <div className="h-56 rounded-xl border border-line bg-black/20 p-2 sm:col-span-1">
          <OnePeriodChart amplitude={amplitude} omega={omega} phi={phi} t={t} />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2 text-center sm:grid-cols-4">
        {[
          { label: "t", value: `${formatNumber(t, 2)} s` },
          { label: "pha (ωt + φ)", value: `${formatNumber(phase, 2)} rad` },
          { label: "li độ x", value: `${formatNumber(x * 100, 2)} cm` },
          { label: "vận tốc v", value: `${formatNumber(v * 100, 1)} cm/s` },
        ].map((item) => (
          <div key={item.label} className="rounded-lg border border-line bg-white/[0.03] px-2 py-1.5">
            <p className="text-[11px] uppercase tracking-wide text-muted">{item.label}</p>
            <p className="font-mono text-sm text-ink">{item.value}</p>
          </div>
        ))}
      </div>

      <div className="space-y-3">
        <div>
          <div className="mb-1.5 flex items-center justify-between text-xs text-muted">
            <label htmlFor="tl-amplitude">Biên độ A</label>
            <span className="font-mono text-ink">{formatNumber(amplitude * 100, 1)} cm</span>
          </div>
          <input
            id="tl-amplitude"
            type="range"
            min={AMPLITUDE_RANGE.min}
            max={AMPLITUDE_RANGE.max}
            step={AMPLITUDE_RANGE.step}
            value={amplitude}
            onChange={(e) => setAmplitude(parseFloat(e.target.value))}
            className={sliderClass}
            aria-label="Biên độ dao động"
          />
        </div>
        <div>
          <div className="mb-1.5 flex items-center justify-between text-xs text-muted">
            <label htmlFor="tl-omega">Tốc độ góc ω của điểm M</label>
            <span className="font-mono text-ink">{formatNumber(omega, 2)} rad/s</span>
          </div>
          <input
            id="tl-omega"
            type="range"
            min={OMEGA_RANGE.min}
            max={OMEGA_RANGE.max}
            step={OMEGA_RANGE.step}
            value={omega}
            onChange={(e) => setOmega(parseFloat(e.target.value))}
            className={sliderClass}
            aria-label="Tốc độ góc của chuyển động tròn đều"
          />
        </div>
        <div>
          <div className="mb-1.5 flex items-center justify-between text-xs text-muted">
            <label htmlFor="tl-phi">Pha ban đầu φ</label>
            <span className="font-mono text-ink">{phiLabel(phi)} rad</span>
          </div>
          <input
            id="tl-phi"
            type="range"
            min={PHI_RANGE.min}
            max={PHI_RANGE.max}
            step={PHI_RANGE.step}
            value={phi}
            onChange={(e) => setPhi(parseFloat(e.target.value))}
            className={sliderClass}
            aria-label="Pha ban đầu"
          />
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={() => setPlaying((p) => !p)}
          className="flex flex-1 items-center justify-center gap-1.5 rounded-lg bg-primary px-3 py-2 text-sm font-medium text-white transition hover:bg-primary-dark active:scale-[0.98]"
        >
          {playing ? <Pause size={15} /> : <Play size={15} />}
          {playing ? "Tạm dừng" : "Chạy"}
        </button>
        <button
          type="button"
          onClick={() => {
            setT(0);
            lastRef.current = null;
          }}
          className="flex items-center justify-center gap-1.5 rounded-lg border border-line bg-white/[0.04] px-3 py-2 text-sm text-ink transition hover:bg-white/[0.08] active:scale-[0.98]"
          aria-label="Đặt lại thời gian về 0"
        >
          <RotateCcw size={15} /> Đặt lại
        </button>
      </div>

      <p className="text-xs leading-relaxed text-muted">
        Chấm vàng Q trên trục Ox luôn trùng với vị trí quả cầu của con lắc lò xo — đó là nội dung
        mục 4 của bài: <em>dao động điều hoà là hình chiếu của một chuyển động tròn đều</em>.
      </p>
    </div>
  );
}
