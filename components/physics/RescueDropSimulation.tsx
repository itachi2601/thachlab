"use client";

/**
 * components/physics/RescueDropSimulation.tsx
 *
 * Tab "Thả hàng cứu hộ" của hero: máy bay bay ngang ở độ cao h, học sinh bấm
 * "Thả hàng" đúng lúc để gói rơi trúng bãi đáp (chuyển động ném ngang — Vật lí
 * 10, Bài 12. Chuyển động ném).
 *
 * Ba điều cố ý:
 *  1. Không tự bay khi mới mở (B4): máy bay chỉ cất cánh khi học sinh bấm.
 *  2. Không cho sẵn đáp số: trước khi thả chỉ hiện h, v₀ và t = √(2h/g). Chỗ phải
 *     thả L = v₀·t chỉ hiện ở phần "soi lại" sau lượt thả.
 *  3. Bãi đáp rộng 40 m và có vạch "phải thả ở đây" sau mỗi lượt: thua vì tay
 *     chậm vẫn học được, chứ không phải bài đo phản xạ.
 *
 * Mọi trạng thái nằm ở useRescueDrop; ở đây chỉ vẽ và bắt thao tác.
 */

import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent as ReactKeyboardEvent,
  type PointerEvent as ReactPointerEvent,
} from "react";
import { formatNumber } from "@/lib/physics";
import {
  G_EARTH,
  H_RANGE,
  PAD_HALF,
  PAD_X,
  V0_RANGE,
  fallTime,
  requiredReleaseX,
} from "@/lib/horizontalProjectile";
import { useRescueDrop, type Point, type RescuePhase } from "@/hooks/useRescueDrop";

// --- Hằng số hình học (đơn vị viewBox canvas, không phải px màn hình) ---
const PAD_L = 26; // chừa chỗ cho nửa thân máy bay khi nó ở mép trái
const PAD_R = 12;
const PAD_T = 12;
const PAD_B = 28; // chừa chỗ ghi thước đo dưới mặt đất
const VIEW_X = 400; // bề ngang khung nhìn (m)
const VIEW_Y = 132; // chiều cao khung nhìn (m) — cao hơn h lớn nhất
const STAGE_BG_TOP = "#070C15";
const STAGE_BG_BOTTOM = "#04070C";
const ACCENT = "#22D3EE";
const WARM = "#FBBF24";
const SLATE_400 = "#94A3B8";
const SLATE_500 = "#64748B";
const SLATE_600 = "#475569";
const SLATE_700 = "#334155";
const MONO = "12px ui-monospace, SFMono-Regular, Menlo, monospace";

interface Box {
  w: number;
  h: number;
}

interface Geometry {
  w: number;
  h: number;
  s: number; // px trên mét (một tỉ lệ cho cả hai trục — parabol không bị bóp méo)
  groundY: number;
}

function geometryFor(box: Box): Geometry {
  const s = Math.min((box.w - PAD_L - PAD_R) / VIEW_X, (box.h - PAD_T - PAD_B) / VIEW_Y);
  return { w: box.w, h: box.h, s, groundY: box.h - PAD_B };
}

interface SceneParams {
  geo: Geometry;
  h: number;
  v0: number;
  phase: RescuePhase;
  planeX: number;
  releaseX: number | null;
  packagePos: Point | null;
  trail: Point[];
  dots: Point[];
  showDots: boolean;
  tFall: number; // giây kể từ lúc thả (0 khi gói còn trên máy bay)
  outcome: { landingX: number | null; delta: number | null; hit: boolean } | null;
}

/** Nhãn canh trong khung: không cho chữ chạy ra ngoài mép canvas. */
function labelX(x: number, geo: Geometry, textWidth: number): number {
  return Math.min(Math.max(x, textWidth / 2 + 4), geo.w - textWidth / 2 - 4);
}

function drawPlane(ctx: CanvasRenderingContext2D, x: number, y: number) {
  ctx.save();
  ctx.translate(x, y);
  // cánh (vẽ trước cho nằm dưới thân)
  ctx.fillStyle = SLATE_500;
  ctx.beginPath();
  ctx.moveTo(-3, 1);
  ctx.lineTo(9, 1);
  ctx.lineTo(3, 12);
  ctx.lineTo(-9, 12);
  ctx.closePath();
  ctx.fill();
  // đuôi
  ctx.beginPath();
  ctx.moveTo(-15, -3);
  ctx.lineTo(-9, -3);
  ctx.lineTo(-12, -12);
  ctx.lineTo(-17, -12);
  ctx.closePath();
  ctx.fill();
  // thân
  ctx.fillStyle = "#CBD5E1";
  ctx.beginPath();
  ctx.roundRect(-15, -5, 30, 10, 5);
  ctx.fill();
  // mũi
  ctx.beginPath();
  ctx.moveTo(14, -5);
  ctx.lineTo(22, 0);
  ctx.lineTo(14, 5);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function drawPackage(ctx: CanvasRenderingContext2D, x: number, y: number) {
  ctx.save();
  ctx.translate(x, y);
  ctx.fillStyle = WARM;
  ctx.strokeStyle = "#B45309";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.roundRect(-5, -5, 10, 10, 2);
  ctx.fill();
  ctx.stroke();
  ctx.strokeStyle = "rgba(180,83,9,0.9)";
  ctx.beginPath();
  ctx.moveTo(-5, 0);
  ctx.lineTo(5, 0);
  ctx.moveTo(0, -5);
  ctx.lineTo(0, 5);
  ctx.stroke();
  ctx.restore();
}

function drawArrow(
  ctx: CanvasRenderingContext2D,
  x1: number,
  y1: number,
  x2: number,
  y2: number,
  color: string,
  label: string
) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  if (Math.hypot(dx, dy) < 8) return;
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.6;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const ang = Math.atan2(dy, dx);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - 7 * Math.cos(ang - 0.4), y2 - 7 * Math.sin(ang - 0.4));
  ctx.lineTo(x2 - 7 * Math.cos(ang + 0.4), y2 - 7 * Math.sin(ang + 0.4));
  ctx.fill();
  ctx.font = MONO;
  ctx.fillText(label, x2 + 4, y2 + 4);
}

function drawScene(canvas: HTMLCanvasElement, p: SceneParams) {
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  const { geo } = p;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);

  if (canvas.width !== Math.round(geo.w * dpr) || canvas.height !== Math.round(geo.h * dpr)) {
    canvas.width = Math.round(geo.w * dpr);
    canvas.height = Math.round(geo.h * dpr);
  }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, geo.w, geo.h);

  const X = (xm: number) => PAD_L + xm * geo.s;
  const Y = (ym: number) => geo.groundY - ym * geo.s;

  // --- nền + lưới ---
  const bg = ctx.createLinearGradient(0, 0, 0, geo.groundY);
  bg.addColorStop(0, STAGE_BG_TOP);
  bg.addColorStop(1, STAGE_BG_BOTTOM);
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, geo.w, geo.groundY);

  ctx.strokeStyle = "rgba(148,163,184,0.10)";
  ctx.lineWidth = 1;
  for (let x = 100; x < VIEW_X; x += 50) {
    ctx.beginPath();
    ctx.moveTo(X(x), PAD_T - 6);
    ctx.lineTo(X(x), geo.groundY);
    ctx.stroke();
  }
  for (let y = 25; y < VIEW_Y; y += 25) {
    ctx.beginPath();
    ctx.moveTo(PAD_L, Y(y));
    ctx.lineTo(geo.w - 8, Y(y));
    ctx.stroke();
  }

  // --- vạch độ cao của máy bay + thước độ cao bên trái ---
  ctx.save();
  ctx.setLineDash([5, 5]);
  ctx.strokeStyle = "rgba(148,163,184,0.35)";
  ctx.beginPath();
  ctx.moveTo(PAD_L - 12, Y(p.h));
  ctx.lineTo(geo.w - 4, Y(p.h));
  ctx.stroke();
  ctx.restore();

  // Thước độ cao đặt sát mép trái, nhãn nằm ngay trên mặt đất: vùng đó luôn trống
  // (gói hàng chỉ chạm đất quanh bãi đáp, còn máy bay thì ở trên cao) nên nhãn
  // không bao giờ bị máy bay che — khác nhãn đặt ở góc phải (máy bay đáp xuống đó).
  const dimX = 9;
  ctx.strokeStyle = SLATE_500;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(dimX, geo.groundY);
  ctx.lineTo(dimX, Y(p.h));
  ctx.stroke();
  [geo.groundY, Y(p.h)].forEach((y, i) => {
    const dir = i === 0 ? -1 : 1;
    ctx.beginPath();
    ctx.moveTo(dimX, y);
    ctx.lineTo(dimX + 4, y + dir * 5);
    ctx.lineTo(dimX - 4, y + dir * 5);
    ctx.closePath();
    ctx.fillStyle = SLATE_500;
    ctx.fill();
  });
  ctx.font = MONO;
  ctx.fillStyle = SLATE_400;
  ctx.textAlign = "left";
  ctx.fillText(`h = ${formatNumber(p.h, 0)} m`, dimX + 4, geo.groundY - 5);

  // --- mặt đất + thước đo ---
  ctx.strokeStyle = SLATE_700;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, geo.groundY);
  ctx.lineTo(geo.w, geo.groundY);
  ctx.stroke();

  ctx.font = MONO;
  ctx.textAlign = "center";
  for (let x = 0; x <= VIEW_X; x += 50) {
    const major = x % 100 === 0;
    ctx.strokeStyle = major ? SLATE_600 : "rgba(51,65,85,0.75)";
    ctx.beginPath();
    ctx.moveTo(X(x), geo.groundY);
    ctx.lineTo(X(x), geo.groundY + (major ? 8 : 5));
    ctx.stroke();
    if (major && x > 0) {
      ctx.fillStyle = SLATE_500;
      ctx.fillText(`${x} m`, X(x), geo.groundY + 21);
    }
  }

  // --- bãi đáp ---
  const padLeft = X(PAD_X - PAD_HALF);
  const padRight = X(PAD_X + PAD_HALF);
  ctx.fillStyle = p.outcome?.hit ? "rgba(34,211,238,0.22)" : "rgba(34,211,238,0.10)";
  ctx.fillRect(padLeft, geo.groundY - 9, padRight - padLeft, 9);
  ctx.strokeStyle = p.outcome?.hit ? ACCENT : "rgba(34,211,238,0.65)";
  ctx.lineWidth = 1.4;
  ctx.strokeRect(padLeft, geo.groundY - 9, padRight - padLeft, 9);
  ctx.fillStyle = ACCENT;
  ctx.font = MONO;
  ctx.textAlign = "center";
  // Lúc soi lại, chỗ này đã dành cho nhãn "trúng!" / "lệch x m" nên bỏ nhãn bãi đáp
  // (dải bãi đáp vẫn được tô viền nên vẫn thấy đích).
  if (p.phase !== "done") {
    ctx.fillText("bãi đáp", labelX(X(PAD_X), geo, 52), geo.groundY - 14);
  }

  // --- quỹ đạo gói hàng ---
  if (p.trail.length > 1) {
    ctx.strokeStyle = "rgba(34,211,238,0.8)";
    ctx.lineWidth = 2;
    ctx.lineJoin = "round";
    ctx.beginPath();
    p.trail.forEach((point, i) =>
      i ? ctx.lineTo(X(point.x), Y(point.y)) : ctx.moveTo(X(point.x), Y(point.y))
    );
    ctx.stroke();
  }

  if (p.showDots) {
    ctx.fillStyle = ACCENT;
    p.dots.forEach((dot) => {
      ctx.beginPath();
      ctx.arc(X(dot.x), Y(dot.y), 2.4, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  // --- gói hàng: luôn nằm thẳng dưới máy bay cho tới lúc chạm đất ---
  if (p.packagePos) {
    ctx.save();
    ctx.setLineDash([3, 4]);
    ctx.strokeStyle = "rgba(251,191,36,0.4)";
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.moveTo(X(p.planeX), Y(p.h) + 12);
    ctx.lineTo(X(p.packagePos.x), Y(p.packagePos.y) - 7);
    ctx.stroke();
    ctx.restore();

    if (p.showDots && p.phase === "falling") {
      const vx = p.v0 * 0.5;
      const vy = G_EARTH * p.tFall * 0.5;
      drawArrow(ctx, X(p.packagePos.x), Y(p.packagePos.y), X(p.packagePos.x) + vx * geo.s, Y(p.packagePos.y), "rgba(94,234,212,0.9)", "vₓ");
      drawArrow(ctx, X(p.packagePos.x), Y(p.packagePos.y), X(p.packagePos.x), Y(p.packagePos.y) + vy * geo.s, "rgba(251,191,36,0.9)", "v_y");
    }

    drawPackage(ctx, X(Math.min(p.packagePos.x, VIEW_X)), Y(p.packagePos.y));
  }

  // --- máy bay ---
  drawPlane(ctx, X(Math.min(p.planeX, VIEW_X)), Y(p.h));

  // --- soi lại lượt vừa thả: chỗ phải thả, chỗ em thả, chỗ gói chạm đất ---
  if (p.phase === "done") {
    const required = requiredReleaseX(p.v0, p.h, G_EARTH);

    const markLine = (xm: number, color: string, dash: number[], from: number, to: number) => {
      ctx.save();
      ctx.setLineDash(dash);
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(X(xm), Y(from));
      ctx.lineTo(X(xm), Y(to));
      ctx.stroke();
      ctx.restore();
    };

    const drawTag = (xm: number, text: string, color: string, topY: number) => {
      ctx.font = MONO;
      ctx.fillStyle = color;
      ctx.textAlign = "center";
      ctx.fillText(text, labelX(X(xm), geo, ctx.measureText(text).width), topY);
    };

    // chỗ phải thả (đáp số của bài) — vẽ trước để vạch của học sinh nổi lên trên
    markLine(required, "rgba(251,191,36,0.7)", [5, 4], p.h, 0);
    // chỗ học sinh đã thả
    if (p.releaseX !== null) {
      markLine(p.releaseX, "rgba(34,211,238,0.75)", [3, 3], p.h, 0);
    }
    // chỗ gói chạm đất
    if (p.outcome?.landingX != null) {
      const lx = p.outcome.landingX;
      ctx.fillStyle = p.outcome.hit ? ACCENT : "#F87171";
      ctx.beginPath();
      ctx.arc(X(Math.min(lx, VIEW_X)), geo.groundY - 2, 4, 0, Math.PI * 2);
      ctx.fill();

      const delta = p.outcome.delta ?? 0;
      if (Math.abs(delta) > 0.05) {
        const text = `lệch ${formatNumber(Math.abs(delta), 1)} m`;
        ctx.font = MONO;
        const w = ctx.measureText(text).width;
        const fromX = X(Math.min(PAD_X, lx));
        const toX = X(Math.min(Math.max(PAD_X, lx), VIEW_X));
        ctx.strokeStyle = "rgba(248,113,113,0.75)";
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(fromX, geo.groundY - 22);
        ctx.lineTo(toX, geo.groundY - 22);
        ctx.stroke();
        // mũi hai đầu
        [fromX, toX].forEach((x, i) => {
          ctx.beginPath();
          ctx.moveTo(x, geo.groundY - 22);
          ctx.lineTo(x + (i === 0 ? 6 : -6), geo.groundY - 25);
          ctx.lineTo(x + (i === 0 ? 6 : -6), geo.groundY - 19);
          ctx.closePath();
          ctx.fillStyle = "rgba(248,113,113,0.85)";
          ctx.fill();
        });
        ctx.fillStyle = "#FCA5A5";
        ctx.textAlign = "center";
        ctx.fillText(text, labelX((fromX + toX) / 2, geo, w), geo.groundY - 27);
      } else {
        ctx.font = MONO;
        ctx.fillStyle = ACCENT;
        ctx.textAlign = "center";
        ctx.fillText("trúng!", labelX(X(PAD_X), geo, 44), geo.groundY - 27);
      }
    }

    drawTag(required, "phải thả ở đây", WARM, Y(p.h) + 16);
    if (p.releaseX !== null) {
      drawTag(p.releaseX, "em thả ở đây", ACCENT, Y(p.h) + 32);
    }
  }
}

const MESSAGE_STYLE: Record<"goal" | "best" | "win", string> = {
  goal: "border-white/10 bg-white/[0.04] text-slate-300",
  best: "border-amber-300/35 bg-amber-300/[0.08] text-amber-100",
  win: "border-cyan-300/45 bg-cyan-300/[0.10] text-cyan-50",
};

const BUTTON_BASE =
  "inline-flex min-h-11 items-center justify-center rounded-lg px-3 text-sm font-medium transition active:scale-[0.98]";

export function RescueDropSimulation() {
  const sim = useRescueDrop();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [box, setBox] = useState<Box>({ w: 0, h: 0 });

  const geo = useMemo(() => geometryFor(box), [box]);
  const tFall = sim.packagePos ? fallTime(sim.h, G_EARTH) - Math.sqrt((2 * Math.max(sim.packagePos.y, 0)) / G_EARTH) : 0;

  // Theo dõi kích thước thật của canvas (điện thoại xoay máy, đổi bề ngang...).
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const measure = () => {
      const rect = canvas.getBoundingClientRect();
      setBox((prev) =>
        Math.abs(prev.w - rect.width) < 0.5 && Math.abs(prev.h - rect.height) < 0.5
          ? prev
          : { w: rect.width, h: rect.height }
      );
    };
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(canvas);
    return () => observer.disconnect();
  }, []);

  // Vẽ lại sau mỗi lần render (mỗi khung hình khi máy bay bay / gói rơi, còn lại theo thao tác).
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || box.w === 0) return;
    drawScene(canvas, {
      geo,
      h: sim.h,
      v0: sim.v0,
      phase: sim.phase,
      planeX: sim.planeX,
      releaseX: sim.releaseX,
      packagePos: sim.packagePos,
      trail: sim.trail,
      dots: sim.dots,
      showDots: sim.showDots,
      tFall,
      outcome: sim.outcome,
    });
  });

  // Chạm vào khung khi máy bay đang bay = thả hàng: cả khung thành một nút to.
  // Dùng pointerup (không phải pointerdown) và KHÔNG nhận chạm lúc chờ: khi học
  // sinh cuộn trang, trình duyệt phát pointercancel nên không có cú thả oan.
  const onCanvasPointerUp = useCallback(
    (event: ReactPointerEvent<HTMLCanvasElement>) => {
      if (sim.phase !== "flying") return;
      event.currentTarget.focus();
      sim.drop();
    },
    [sim]
  );

  const onKeyDown = (event: ReactKeyboardEvent<HTMLCanvasElement>) => {
    if (event.key === " " || event.key === "Enter") {
      sim.primaryAction();
      event.preventDefault();
      return;
    }
    if (sim.phase !== "ready") return;
    switch (event.key) {
      case "ArrowUp":
        sim.setHeight(sim.h + H_RANGE.step);
        break;
      case "ArrowDown":
        sim.setHeight(sim.h - H_RANGE.step);
        break;
      case "ArrowRight":
        sim.setSpeed(sim.v0 + V0_RANGE.step);
        break;
      case "ArrowLeft":
        sim.setSpeed(sim.v0 - V0_RANGE.step);
        break;
      default:
        return;
    }
    event.preventDefault();
  };

  const primaryLabel =
    sim.phase === "ready" ? "Cho máy bay bay" : sim.phase === "flying" ? "Thả hàng" : "Thử lại";

  const landingText =
    sim.phase === "done" && sim.outcome
      ? sim.outcome.delta === null
        ? "chưa thả"
        : Math.abs(sim.outcome.delta) < 0.05
          ? "trúng"
          : `${sim.outcome.delta > 0 ? "+" : "−"}${formatNumber(Math.abs(sim.outcome.delta), 1)} m`
      : "—";

  return (
    <div>
      <div className="relative overflow-hidden rounded-xl border border-white/10">
        <canvas
          ref={canvasRef}
          tabIndex={0}
          role="img"
          aria-label={
            `Mô phỏng thả hàng cứu hộ: máy bay ở độ cao ${formatNumber(sim.h, 1)} m, bay ngang ` +
            `${formatNumber(sim.v0, 1)} m/s, bãi đáp rộng 40 m nằm ở vạch ${PAD_X} m. ` +
            `Chạm vào khung hoặc bấm phím cách để ${sim.phase === "flying" ? "thả hàng" : "điều khiển mô phỏng"}.`
          }
          onPointerUp={onCanvasPointerUp}
          onKeyDown={onKeyDown}
          className="block aspect-[2.2] w-full select-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-300/70 sm:aspect-[2.1] lg:aspect-[2.7]"
        />
      </div>

      <dl className="mt-3 grid grid-cols-3 gap-x-3 gap-y-2 font-mono">
        <div>
          <dt className="text-[13px] text-slate-500">Độ cao h</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.h, 1)} m</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Tốc độ v₀</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.v0, 1)} m/s</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Thời gian rơi t</dt>
          <dd className="text-sm text-ink">{formatNumber(fallTime(sim.h, G_EARTH), 2)} s</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Gói đã rơi</dt>
          <dd className="text-sm text-ink">
            {sim.packagePos ? `${formatNumber(tFall, 2)} s` : "—"}
          </dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Còn cao</dt>
          <dd className="text-sm text-ink">
            {sim.packagePos ? `${formatNumber(sim.packagePos.y, 1)} m` : "—"}
          </dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Lệch bãi đáp</dt>
          <dd className="text-sm text-ink">{landingText}</dd>
        </div>
      </dl>

      <p
        role="status"
        aria-live="polite"
        className={`mt-3 min-h-[3.5rem] rounded-lg border px-3 py-2 text-sm leading-relaxed ${MESSAGE_STYLE[sim.message.kind]}`}
      >
        {sim.message.text}
      </p>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <button
          type="button"
          onClick={sim.primaryAction}
          className={`${BUTTON_BASE} px-4 font-semibold ${
            sim.phase === "flying"
              ? "bg-amber-300 text-slate-950 hover:bg-amber-200"
              : "bg-cyan-300 text-slate-950 hover:bg-cyan-200"
          }`}
        >
          {primaryLabel}
        </button>

        <label className="inline-flex min-h-11 flex-1 cursor-pointer items-center gap-2 text-[13px] text-slate-400">
          <span className="whitespace-nowrap">Độ cao h</span>
          <input
            type="range"
            min={H_RANGE.min}
            max={H_RANGE.max}
            step={H_RANGE.step}
            value={sim.h}
            disabled={sim.phase === "flying" || sim.phase === "falling"}
            onChange={(event) => sim.setHeight(Number(event.target.value))}
            className="h-11 flex-1 accent-[#22D3EE] disabled:opacity-50"
          />
        </label>

        <label className="inline-flex min-h-11 flex-1 cursor-pointer items-center gap-2 text-[13px] text-slate-400">
          <span className="whitespace-nowrap">Tốc độ v₀</span>
          <input
            type="range"
            min={V0_RANGE.min}
            max={V0_RANGE.max}
            step={V0_RANGE.step}
            value={sim.v0}
            disabled={sim.phase === "flying" || sim.phase === "falling"}
            onChange={(event) => sim.setSpeed(Number(event.target.value))}
            className="h-11 flex-1 accent-[#22D3EE] disabled:opacity-50"
          />
        </label>

        <label className="inline-flex min-h-11 cursor-pointer items-center gap-2 text-[13px] text-slate-400">
          <input
            type="checkbox"
            checked={sim.showDots}
            onChange={sim.toggleDots}
            className="h-4 w-4 accent-[#22D3EE]"
          />
          Chấm mỗi 0,1 s
        </label>
      </div>
    </div>
  );
}
