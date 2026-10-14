"use client";

/**
 * components/physics/ShadowSpringSimulation.tsx
 *
 * Tab "Hình chiếu" của hero: BÓNG của một điểm M quay đều và một CON LẮC LÒ XO
 * NẰM NGANG chạy trên CÙNG MỘT TRỤC x — học sinh tự chỉnh tốc độ quay để hai bên
 * giữ đúng nhịp, rồi tự thử câu hỏi chính: kéo con lắc ra xa gấp đôi thì nhịp có
 * đổi không? (Không: T = 2π√(m/k) không chứa A.)
 *
 * Nguồn: `content/thi-nghiem/tn-l11-daodongdieuhoa-03.json` (Bài 1. Dao động điều
 * hoà, Vật lí 11) — thí nghiệm "bóng của van xe đạp", mục 5 "Liên hệ với chuyển
 * động tròn đều".
 *
 * Bảng màu đọc từ StagePalette (stage-theme.ts) tự thích ứng theo theme sáng/tối.
 */

import { useEffect, useMemo, useRef, useState } from "react";
import { Pause, Play, RotateCcw, Waves } from "lucide-react";
import { formatNumber } from "@/lib/physics";
import {
  AXIS_MAX_CM,
  DOT_INTERVAL,
  MASS_RANGE,
  PENDULUM_AMPLITUDE_RANGE,
  SHADOW_AMPLITUDE,
  WHEEL_OMEGA_RANGE,
  equalTimeDots,
  type ProjectionMessageKind,
} from "@/lib/circularProjection";
import { useCircularProjection } from "@/hooks/useCircularProjection";
import {
  getStagePalette,
  subscribeStageTheme,
  withAlpha,
  type StagePalette,
} from "./stage-theme";

const MONO = "ui-monospace, SFMono-Regular, Menlo, monospace";
const TAU = Math.PI * 2;

interface Box {
  w: number;
  h: number;
  dpr: number;
}

interface Stage {
  w: number;
  h: number;
  fs: number; // cỡ chữ trong hình
  pad: number;
  cx: number; // gốc O dùng chung cho hai làn
  scale: number; // px trên cm
  rShadow: number; // bán kính đường tròn trên màn hình (px)
  lane1Y: number; // trục chiếu của bóng
  lane2Y: number; // đường chuyển động của con lắc
  massSize: number;
}

/**
 * Chia chiều cao khả dụng theo nhu cầu thật của từng phần (nhãn M trên cùng, đường
 * tròn, khe chứa mũi tên Δx, vật nặng, hàng vạch chia dưới cùng), rồi CĂN GIỮA cả
 * nhóm theo chiều dọc.
 */
function stageFor(w: number, h: number): Stage {
  const fs = Math.max(10, Math.min(13, w / 26));
  const pad = Math.max(10, w * 0.035);
  const massSize = Math.max(16, Math.min(30, h * 0.13));
  const gap = 0.35 * massSize + 10;
  const labelRow = fs + 8; // hàng số dưới trục con lắc
  const budget = h - 2 * pad - massSize - gap - fs - labelRow;
  const rShadow = Math.max(massSize * 0.9, Math.min(budget / 2, w / 2 - pad - 12));
  const groupH = fs + 2 * rShadow + gap + massSize + labelRow;
  const top = pad + Math.max(0, (h - 2 * pad - groupH) / 2);
  const cx = w / 2;
  const lane1Y = top + fs + rShadow;
  const lane2Y = lane1Y + rShadow + gap + massSize / 2;
  return {
    w,
    h,
    fs,
    pad,
    cx,
    scale: rShadow / SHADOW_AMPLITUDE,
    rShadow,
    lane1Y,
    lane2Y,
    massSize,
  };
}

/** Điểm của lò xo nằm ngang: zig-zag giữa tường và vật nặng. */
function springPoints(
  x0: number,
  x1: number,
  y: number,
  amp: number,
  coils: number
): [number, number][] {
  const length = Math.max(8, x1 - x0);
  const straight = Math.min(8, length * 0.12);
  const zig = Math.max(2, length - straight * 2);
  const segments = coils * 2;
  const points: [number, number][] = [
    [x0, y],
    [x0 + straight, y],
  ];
  for (let i = 1; i <= segments; i++) {
    points.push([
      x0 + straight + (zig * i) / segments,
      y + (i % 2 === 0 ? 1 : -1) * amp,
    ]);
  }
  points.push([x1 - straight, y], [x1, y]);
  return points;
}

interface SceneParams {
  box: Box;
  theta: number;
  xShadow: number;
  xPendulum: number;
  synced: boolean;
  dots: { t: number; x: number }[];
  showDots: boolean;
}

function drawScene(canvas: HTMLCanvasElement, p: SceneParams, pal: StagePalette) {
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  const { w, h, dpr } = p.box;
  if (w <= 0 || h <= 0) return;

  const pixelW = Math.max(1, Math.round(w * dpr));
  const pixelH = Math.max(1, Math.round(h * dpr));
  if (canvas.width !== pixelW || canvas.height !== pixelH) {
    canvas.width = pixelW;
    canvas.height = pixelH;
  }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, h);

  const bg = ctx.createLinearGradient(0, 0, 0, h);
  bg.addColorStop(0, pal.bgTop);
  bg.addColorStop(1, pal.bgBottom);
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, w, h);

  const isDark = pal.bgRgb[0] < 50;
  const s = stageFor(w, h);
  ctx.font = `${s.fs}px ${MONO}`;
  ctx.textBaseline = "alphabetic";

  // ================= LÀN 1: đường tròn + bóng (hình chiếu) =================
  const r = s.rShadow;
  const mX = s.cx + p.xShadow * s.scale;
  const mY = s.lane1Y - Math.sin(p.theta) * r;

  // trục chiếu (đường kính ngang) + mũi tên chiều dương
  ctx.strokeStyle = pal.gridStrong;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(s.cx - r - 8, s.lane1Y);
  ctx.lineTo(s.cx + r + 24, s.lane1Y);
  ctx.stroke();
  ctx.fillStyle = pal.line;
  ctx.beginPath();
  ctx.moveTo(s.cx + r + 30, s.lane1Y);
  ctx.lineTo(s.cx + r + 22, s.lane1Y - 4);
  ctx.lineTo(s.cx + r + 22, s.lane1Y + 4);
  ctx.closePath();
  ctx.fill();

  // đường tròn quỹ đạo của M
  ctx.strokeStyle = pal.line;
  ctx.lineWidth = 1.4;
  ctx.beginPath();
  ctx.arc(s.cx, s.lane1Y, r, 0, TAU);
  ctx.stroke();

  // bán kính OM + cung góc quay ωt
  ctx.strokeStyle = pal.accentSoft;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(s.cx, s.lane1Y);
  ctx.lineTo(mX, mY);
  ctx.stroke();

  const sweep = p.theta % TAU;
  if (sweep > 0.02) {
    const arcR = r * 0.36;
    ctx.strokeStyle = withAlpha(pal.muted, 0.55);
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.arc(s.cx, s.lane1Y, arcR, 0, -sweep, true);
    ctx.stroke();

    const halfSweep = -sweep / 2;
    ctx.fillStyle = pal.muted;
    ctx.textAlign = "center";
    ctx.fillText(
      "ωt",
      s.cx + (arcR + 11) * Math.cos(halfSweep),
      s.lane1Y + (arcR + 11) * Math.sin(halfSweep) + 4
    );
  }

  // chấm mỗi 0,1 s
  if (p.showDots) {
    ctx.fillStyle = withAlpha(pal.accent, 0.5);
    for (const dot of p.dots) {
      ctx.beginPath();
      ctx.arc(s.cx + dot.x * s.scale, s.lane1Y, 1.8, 0, TAU);
      ctx.fill();
    }
  }

  // đường nét đứt M → Q, rồi M và Q
  ctx.save();
  ctx.setLineDash([3, 3]);
  ctx.strokeStyle = withAlpha(pal.muted, 0.5);
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(mX, mY);
  ctx.lineTo(mX, s.lane1Y);
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.shadowColor = pal.accentSoft;
  ctx.shadowBlur = 10;
  ctx.fillStyle = pal.accent;
  ctx.beginPath();
  ctx.arc(mX, mY, 4.6, 0, TAU);
  ctx.fill();
  if (!isDark) {
    ctx.strokeStyle = pal.gridStrong;
    ctx.lineWidth = 1;
    ctx.stroke();
  }
  ctx.restore();

  ctx.fillStyle = pal.ink;
  ctx.textAlign = "left";
  ctx.fillText("M", mX + 8, mY <= s.lane1Y ? mY - 6 : mY + s.fs + 4);

  ctx.fillStyle = pal.accent;
  ctx.beginPath();
  ctx.arc(mX, s.lane1Y, 3.4, 0, TAU);
  ctx.fill();
  ctx.fillStyle = pal.muted;
  ctx.fillText("Q", mX + 7, s.lane1Y + s.fs + 3);

  // ================= LÀN 2: con lắc lò xo nằm ngang =================
  const wallX = s.pad;
  const bobX = s.cx + p.xPendulum * s.scale;
  const halfMass = s.massSize / 2;

  // đường ray + vạch chia mỗi 1 cm
  ctx.strokeStyle = pal.gridStrong;
  ctx.lineWidth = 1.1;
  ctx.beginPath();
  ctx.moveTo(wallX, s.lane2Y);
  ctx.lineTo(w - s.pad, s.lane2Y);
  ctx.stroke();

  const labelStep = s.scale * 5 >= 34 ? 5 : 10;
  ctx.textAlign = "center";
  for (let cm = -AXIS_MAX_CM; cm <= AXIS_MAX_CM; cm += 1) {
    const tickX = s.cx + cm * s.scale;
    const major = cm % 5 === 0;
    ctx.strokeStyle = pal.line;
    ctx.beginPath();
    ctx.moveTo(tickX, s.lane2Y);
    ctx.lineTo(tickX, s.lane2Y + (major ? 6 : 3));
    ctx.stroke();
    if (major && cm % labelStep === 0) {
      ctx.fillStyle = pal.muted;
      ctx.fillText(String(cm), tickX, s.lane2Y + s.fs + 5);
    }
  }
  ctx.fillStyle = pal.muted;
  ctx.textAlign = "right";
  ctx.fillText("x (cm)", w - s.pad, s.lane2Y - s.fs * 0.5);

  // gốc O dùng chung cho hai làn
  ctx.save();
  ctx.setLineDash([3, 4]);
  ctx.strokeStyle = withAlpha(pal.muted, 0.35);
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(s.cx, s.lane1Y - r - 4);
  ctx.lineTo(s.cx, s.lane2Y);
  ctx.stroke();
  ctx.restore();

  // tường gắn lò xo
  ctx.strokeStyle = pal.line;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(wallX, s.lane2Y - s.massSize);
  ctx.lineTo(wallX, s.lane2Y + s.massSize * 0.4);
  ctx.stroke();
  ctx.lineWidth = 1.4;
  for (let i = 0; i < 5; i++) {
    const y = s.lane2Y - s.massSize + i * (s.massSize * 0.28);
    ctx.beginPath();
    ctx.moveTo(wallX, y);
    ctx.lineTo(wallX - 6, y + 6);
    ctx.stroke();
  }

  // lò xo
  const springLength = Math.max(8, bobX - halfMass - wallX);
  const coils = Math.min(14, Math.max(6, Math.round(springLength / 18)));
  const spring = springPoints(wallX, bobX - halfMass, s.lane2Y, s.massSize * 0.26, coils);
  ctx.strokeStyle = pal.muted;
  ctx.lineWidth = 1.5;
  ctx.lineJoin = "round";
  ctx.beginPath();
  spring.forEach(([px, py], i) => (i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py)));
  ctx.stroke();

  // vòng tròn nét đứt = chỗ bóng chiếu xuống làn con lắc
  const ringX = s.cx + p.xShadow * s.scale;
  const ringR = s.massSize * 0.85;

  // vật nặng
  const massGrad = ctx.createLinearGradient(0, s.lane2Y - halfMass, 0, s.lane2Y + halfMass);
  massGrad.addColorStop(0, pal.primary);
  massGrad.addColorStop(1, pal.primaryEdge);
  ctx.fillStyle = massGrad;
  ctx.beginPath();
  ctx.roundRect(bobX - halfMass, s.lane2Y - halfMass, s.massSize, s.massSize, 6);
  ctx.fill();
  ctx.strokeStyle = pal.primaryEdge;
  ctx.lineWidth = 1;
  ctx.stroke();

  ctx.save();
  ctx.setLineDash([4, 3]);
  ctx.strokeStyle = pal.accent;
  ctx.lineWidth = 1.6;
  ctx.beginPath();
  ctx.arc(ringX, s.lane2Y, ringR, 0, TAU);
  ctx.stroke();
  ctx.restore();

  // khoảng lệch giữa bóng và vật nặng
  const deltaCm = Math.abs(p.xShadow - p.xPendulum);
  if (deltaCm > 0.15) {
    const y = s.lane2Y - ringR - 5;
    ctx.strokeStyle = p.synced ? pal.muted : pal.warm;
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(Math.min(ringX, bobX), y);
    ctx.lineTo(Math.max(ringX, bobX), y);
    ctx.stroke();
    for (const [tip, dir] of [
      [ringX, Math.sign(bobX - ringX)],
      [bobX, Math.sign(ringX - bobX)],
    ] as [number, number][]) {
      if (dir === 0) continue;
      ctx.beginPath();
      ctx.moveTo(tip, y);
      ctx.lineTo(tip + dir * 5, y - 3);
      ctx.lineTo(tip + dir * 5, y + 3);
      ctx.closePath();
      ctx.fillStyle = p.synced ? pal.muted : pal.warm;
      ctx.fill();
    }
  }
}

const MESSAGE_STYLE: Record<ProjectionMessageKind, string> = {
  idle: "border-line bg-surface-2 text-ink",
  drift: "border-amber-300/35 bg-amber-300/[0.08] text-amber-600 dark:text-amber-100",
  samePeriod: "border-cyan-300/25 bg-cyan-300/[0.05] text-ink",
  inphase: "border-primary/40 bg-primary-soft text-primary font-medium",
  inphaseEqual: "border-primary/40 bg-primary-soft text-primary font-medium",
};

const BUTTON_BASE =
  "inline-flex min-h-11 items-center justify-center gap-1.5 rounded-lg px-3 text-sm font-medium transition active:scale-[0.98]";

const sliderClass =
  "h-1.5 w-full cursor-pointer appearance-none rounded-full bg-surface-2 accent-primary " +
  "[&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:appearance-none " +
  "[&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary " +
  "[&::-webkit-slider-thumb]:shadow-[0_0_0_3px_rgba(37,99,235,0.25)] " +
  "[&::-moz-range-thumb]:h-4 [&::-moz-range-thumb]:w-4 [&::-moz-range-thumb]:rounded-full " +
  "[&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:bg-primary";

export function ShadowSpringSimulation() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const paletteRef = useRef<StagePalette>(getStagePalette());
  const [box, setBox] = useState<Box>({ w: 0, h: 0, dpr: 1 });
  const [inView, setInView] = useState(true);
  const sim = useCircularProjection({ active: inView });

  const dots = useMemo(
    () => equalTimeDots(sim.shadowAmplitude, sim.wheelOmega, sim.theta, DOT_INTERVAL),
    [sim.shadowAmplitude, sim.wheelOmega, sim.theta]
  );

  // Kích thước thật của vùng vẽ
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const measure = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      setBox((prev) =>
        Math.abs(prev.w - rect.width) < 0.5 &&
        Math.abs(prev.h - rect.height) < 0.5 &&
        prev.dpr === dpr
          ? prev
          : { w: rect.width, h: rect.height, dpr }
      );
    };
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(canvas);
    window.addEventListener("resize", measure);
    return () => {
      observer.disconnect();
      window.removeEventListener("resize", measure);
    };
  }, []);

  // Lắng nghe thay đổi theme và vẽ lại ngay
  useEffect(() => {
    paletteRef.current = getStagePalette();
    const unsubscribe = subscribeStageTheme(() => {
      paletteRef.current = getStagePalette();
      const canvas = canvasRef.current;
      if (canvas && box.w > 0) {
        drawScene(
          canvas,
          {
            box,
            theta: sim.theta,
            xShadow: sim.xShadow,
            xPendulum: sim.xPendulum,
            synced: sim.synced,
            dots,
            showDots: sim.showDots,
          },
          paletteRef.current
        );
      }
    });
    return unsubscribe;
  }, [box, dots, sim]);

  // Ra khỏi tầm mắt thì dừng vòng lặp
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || typeof IntersectionObserver === "undefined") return;
    const observer = new IntersectionObserver(([entry]) => setInView(entry.isIntersecting), {
      threshold: 0.15,
    });
    observer.observe(canvas);
    return () => observer.disconnect();
  }, []);

  // Vẽ lại mỗi lần render
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    drawScene(
      canvas,
      {
        box,
        theta: sim.theta,
        xShadow: sim.xShadow,
        xPendulum: sim.xPendulum,
        synced: sim.synced,
        dots,
        showDots: sim.showDots,
      },
      paletteRef.current
    );
  });

  return (
    <div>
      <div className="relative overflow-hidden rounded-xl border border-line">
        <canvas
          ref={canvasRef}
          role="img"
          aria-label="Trục x dùng chung cho hai hệ: làn trên là đường tròn bán kính A₁ có điểm M quay đều, bóng Q là hình chiếu của M; làn dưới là con lắc lò xo nằm ngang. Bấm Chạy để cả hai cùng chuyển động."
          className="block aspect-[1.8] w-full select-none"
        />
      </div>

      <p className="mt-2 text-[13px] leading-relaxed text-muted">
        Bóng Q (làn trên) và vật nặng (làn dưới) chạy trên <strong>cùng một trục x</strong>. Vòng
        tròn nét đứt là chỗ bóng chiếu xuống làn con lắc: hai bên trùng nhau khi cùng ω và cùng
        biên độ.
      </p>
      {sim.showDots && (
        <p className="mt-1 text-[13px] leading-relaxed text-muted">
          Chấm là vị trí bóng sau mỗi 0,1 s kể từ bây giờ: bóng gần biên thì chấm dồn lại, bóng ở giữa
          thì chấm giãn ra — bóng không chuyển động đều, nó chậm lại ở biên.
        </p>
      )}

      <p
        role="status"
        aria-live="polite"
        className={`mt-3 min-h-[3.5rem] rounded-lg border px-3 py-2 text-sm leading-relaxed ${
          MESSAGE_STYLE[sim.message.kind]
        }`}
      >
        {sim.message.text}
      </p>

      <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3">
        <div>
          <div className="mb-1.5 flex items-center justify-between text-xs text-muted">
            <label htmlFor="hc-m">Khối lượng m</label>
            <span className="font-mono text-ink">{formatNumber(sim.mass, 2)} kg</span>
          </div>
          <input
            id="hc-m"
            type="range"
            min={MASS_RANGE.min}
            max={MASS_RANGE.max}
            step={MASS_RANGE.step}
            value={sim.mass}
            onChange={(event) => sim.setMass(parseFloat(event.target.value))}
            className={sliderClass}
            aria-label="Khối lượng vật nặng của con lắc lò xo"
          />
        </div>

        <div>
          <div className="mb-1.5 flex items-center justify-between text-xs text-muted">
            <label htmlFor="hc-a2">Biên độ A₂</label>
            <span className="font-mono text-ink">
              {formatNumber(sim.pendulumAmplitude, 1)} cm
            </span>
          </div>
          <input
            id="hc-a2"
            type="range"
            min={PENDULUM_AMPLITUDE_RANGE.min}
            max={PENDULUM_AMPLITUDE_RANGE.max}
            step={PENDULUM_AMPLITUDE_RANGE.step}
            value={sim.pendulumAmplitude}
            disabled={sim.playing}
            onChange={(event) => sim.setPendulumAmplitude(parseFloat(event.target.value))}
            className={`${sliderClass} disabled:cursor-not-allowed disabled:opacity-45`}
            aria-label="Biên độ con lắc — chỗ thả vật nặng, chỉ đổi được khi đang dừng"
          />
        </div>

        <div className="col-span-2 sm:col-span-1">
          <div className="mb-1.5 flex items-center justify-between text-xs text-muted">
            <label htmlFor="hc-w">Tốc độ quay ω</label>
            <span className="font-mono text-ink">
              {formatNumber(sim.wheelOmega, 2)} rad/s
            </span>
          </div>
          <input
            id="hc-w"
            type="range"
            min={WHEEL_OMEGA_RANGE.min}
            max={WHEEL_OMEGA_RANGE.max}
            step={WHEEL_OMEGA_RANGE.step}
            value={sim.wheelOmega}
            onChange={(event) => sim.setWheelOmega(parseFloat(event.target.value))}
            className={sliderClass}
            aria-label="Tốc độ quay của điểm M — cũng là tần số góc của bóng"
          />
        </div>
      </div>

      {sim.playing && (
        <p className="mt-2 text-[13px] leading-relaxed text-muted">
          Đang chạy nên chỗ thả A₂ bị khoá: đổi giữa chừng thì vật nặng nhảy vị trí. Bấm
          &ldquo;Dừng&rdquo; nếu muốn kéo con lắc ra xa hơn.
        </p>
      )}

      <dl className="mt-3 grid grid-cols-3 gap-x-3 gap-y-2 font-mono">
        <div>
          <dt className="text-[13px] text-slate-500">T bóng</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.periodShadow, 2)} s</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">T con lắc</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.periodPendulum, 2)} s</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">ω = √(k/m)</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.omegaSpring, 2)} rad/s</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Lệch pha</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.phaseDiffDeg, 0)}°</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Δx bóng − con lắc</dt>
          <dd className="text-sm text-ink">
            {formatNumber(sim.xShadow - sim.xPendulum, 1)} cm
          </dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Dao động bóng / con lắc</dt>
          <dd className="text-sm text-ink">
            {sim.countShadow} / {sim.countPendulum}
          </dd>
        </div>
      </dl>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <button
          type="button"
          aria-pressed={sim.playing}
          onClick={sim.toggle}
          className={`${BUTTON_BASE} ${
            sim.playing
              ? "bg-primary text-white hover:bg-primary-dark"
              : "border border-line text-ink hover:bg-surface-2"
          }`}
        >
          {sim.playing ? <Pause size={15} /> : <Play size={15} />}
          {sim.playing ? "Dừng" : "Chạy"}
        </button>
        <button
          type="button"
          onClick={sim.snapRhythm}
          className={`${BUTTON_BASE} border border-line text-ink hover:bg-surface-2`}
        >
          <Waves size={15} />
          Khớp nhịp
        </button>
        <button
          type="button"
          onClick={sim.reset}
          className={`${BUTTON_BASE} border border-line text-ink hover:bg-surface-2`}
        >
          <RotateCcw size={15} />
          Đặt lại
        </button>
        <label className="inline-flex min-h-11 cursor-pointer items-center gap-2 px-1 text-[13px] text-muted">
          <input
            type="checkbox"
            checked={sim.showDots}
            onChange={sim.toggleDots}
            className="h-4 w-4 accent-primary"
          />
          Chấm mỗi 0,1 s
        </label>
      </div>
    </div>
  );
}
