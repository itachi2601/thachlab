"use client";

/**
 * components/physics/InterferenceSimulation.tsx
 *
 * Tab "Giao thoa" của hero: khay sóng nước hai mũi nhọn (Bài 12, Vật lí 11) —
 * bản đồ vân giao thoa vẽ bằng canvas 2D thuần (không thư viện, không animation
 * CSS), học sinh chạm/kéo chấm M để tự đọc ra d₂ − d₁ = kλ (cực đại) và
 * (k + ½)λ (cực tiểu), và tắt nguồn B để thấy vân biến mất.
 *
 * Vẽ BAO HÌNH biên độ (|2a·cos(πΔd/λ)|) chứ không phải li độ tức thời: vân trên
 * mặt nước là các đường sáng/tối ĐỨNG YÊN, nên không cần vòng lặp hình ảnh nào —
 * mọi thứ chỉ tính lại khi đổi f, v, AB (quy tắc B4: không có gì tự chuyển động,
 * và cũng là cách rẻ nhất về CPU/pin).
 *
 * Quy tắc thiết kế áp dụng: B4 (mô phỏng đứng yên, do HS ra lệnh), D2 (đích chạm
 * ≥ 44px, nhãn nút ≤ 1 dòng), M2 (chữ trên nền tối dùng màu cố định), M4 (cực
 * đại/cực tiểu nói bằng chữ, không chỉ bằng màu), N7 (mỗi đoạn một kiểu nhấn),
 * C1 (chữ đọc được ≥ 13px).
 */

import {
  useEffect,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent as ReactKeyboardEvent,
  type PointerEvent as ReactPointerEvent,
} from "react";
import { RotateCcw } from "lucide-react";
import { formatNumber } from "@/lib/physics";
import {
  AB_RANGE,
  F_RANGE,
  TANK,
  V_RANGE,
  singleSourceFieldIntensity,
  twoSourceFieldIntensity,
  type FringeKind,
} from "@/lib/interference";
import {
  useInterferenceTank,
  type TankPoint,
} from "@/hooks/useInterferenceTank";

// --- Màu cố định cho phần vẽ trên nền tối (M2) ---
const STAGE_BG_TOP = "#070C15";
const STAGE_BG_BOTTOM = "#04070C";
const ACCENT = "#22D3EE";
const ACCENT_SOFT = "rgba(34,211,238,0.55)";
const WARM = "#FBBF24";
const M_MAX = "#E6FEFF";
const M_MIN = "#93C5FD";
const TEXT = "#E2E8F0";
const SLATE_400 = "#94A3B8";
const SLATE_500 = "#64748B";
const SLATE_600 = "#475569";
const SLATE_700 = "#334155";
const MONO = "ui-monospace, SFMono-Regular, Menlo, monospace";

/** Bước nhảy khi chỉnh M bằng phím (cm) — D2: bàn phím là đường dự phòng cho ngón tay. */
const KEY_STEP_CM = 0.4;

interface Box {
  w: number;
  h: number;
  dpr: number;
}

interface Geometry extends Box {
  scale: number; // px màn hình trên cm
  offsetX: number; // lề trái của khay trong canvas (px)
  offsetY: number;
}

/** Khay 20 × 10 cm được đặt giữa canvas theo một tỉ lệ duy nhất (không bóp méo sóng). */
function geometryFor(box: Box): Geometry {
  const scale = Math.min(box.w / TANK.widthCm, box.h / TANK.heightCm);
  return {
    ...box,
    scale,
    offsetX: (box.w - TANK.widthCm * scale) / 2,
    offsetY: (box.h - TANK.heightCm * scale) / 2,
  };
}

interface FieldParams {
  lambda: number;
  sourceBOn: boolean;
  sources: { a: TankPoint; b: TankPoint };
}

/**
 * Bản đồ vân: mỗi điểm ảnh = biên độ tổng hợp tại đó. Ngoài khay để trong suốt
 * (nền gradient của canvas lộ ra). Tính ở độ phân giải thiết bị (≤ 2×) nên vân
 * nhỏ nhất vẫn tách được; đổi tham số mới tính lại một lần.
 */
function buildFieldCanvas(geo: Geometry, params: FieldParams): HTMLCanvasElement | null {
  if (typeof document === "undefined" || geo.w <= 0 || geo.h <= 0) return null;
  const pw = Math.max(1, Math.round(geo.w * geo.dpr));
  const ph = Math.max(1, Math.round(geo.h * geo.dpr));
  const canvas = document.createElement("canvas");
  canvas.width = pw;
  canvas.height = ph;
  const ctx = canvas.getContext("2d");
  if (!ctx) return null;

  const image = ctx.createImageData(pw, ph);
  const data = image.data;
  const { scale, offsetX, offsetY, dpr } = geo;
  const { a, b } = params.sources;
  const lambda = params.lambda;
  const twoSources = params.sourceBOn;

  for (let py = 0; py < ph; py++) {
    const ycm = (py + 0.5) / dpr;
    const yTank = (ycm - offsetY) / scale;
    const dyA = yTank - a.y;
    const dyB = yTank - b.y;
    const dyA2 = dyA * dyA;
    const dyB2 = dyB * dyB;
    const inRow = yTank >= 0 && yTank <= TANK.heightCm;
    let index = py * pw * 4;

    for (let px = 0; px < pw; px++, index += 4) {
      const xTank = ((px + 0.5) / dpr - offsetX) / scale;
      if (!inRow || xTank < 0 || xTank > TANK.widthCm) continue; // alpha = 0

      const dxA = xTank - a.x;
      const d1 = Math.sqrt(dxA * dxA + dyA2);
      let intensity: number;
      if (twoSources) {
        const dxB = xTank - b.x;
        const d2 = Math.sqrt(dxB * dxB + dyB2);
        intensity = twoSourceFieldIntensity(d1, d2, lambda);
      } else {
        intensity = singleSourceFieldIntensity(d1, lambda);
      }

      // glow = I^2,25: thu hẹp vệt sáng thành đúng đường vân, không nhoè cả khay,
      // nhưng vẫn đủ sáng ở xa để mắt thấy vân (độ tắt dần ở lib đã lo phần mờ).
      const glow = intensity ** 2.25;
      data[index] = 5 + 30 * glow;
      data[index + 1] = 8 + 190 * glow;
      data[index + 2] = 14 + 214 * glow;
      data[index + 3] = 255;
    }
  }

  ctx.putImageData(image, 0, 0);
  return canvas;
}

/** Chữ có viền tối để đọc được cả khi nằm trên vệt vân sáng. */
function label(
  ctx: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  color: string = TEXT,
  align: CanvasTextAlign = "left",
  size = 12
) {
  ctx.save();
  ctx.font = `${size}px ${MONO}`;
  ctx.textAlign = align;
  ctx.lineWidth = 3;
  ctx.lineJoin = "round";
  ctx.strokeStyle = "rgba(4,7,12,0.85)";
  ctx.strokeText(text, x, y);
  ctx.fillStyle = color;
  ctx.fillText(text, x, y);
  ctx.restore();
}

const KIND_COLOR: Record<FringeKind, string> = {
  max: M_MAX,
  min: M_MIN,
  mid: WARM,
};

function kindLabel(kind: FringeKind, order: number): string {
  if (kind === "max") return `cực đại bậc ${Math.abs(order)}`;
  if (kind === "min") return `cực tiểu (k = ${Math.round(order)})`;
  return "ở giữa hai vân";
}

interface SceneParams {
  geo: Geometry;
  field: HTMLCanvasElement | null;
  lambda: number;
  AB: number;
  sourceBOn: boolean;
  sources: { a: TankPoint; b: TankPoint };
  marker: TankPoint;
  d1: number;
  d2: number;
  kind: FringeKind;
  order: number;
}

function drawScene(canvas: HTMLCanvasElement, p: SceneParams) {
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  const { geo } = p;
  const deviceW = Math.max(1, Math.round(geo.w * geo.dpr));
  const deviceH = Math.max(1, Math.round(geo.h * geo.dpr));
  if (canvas.width !== deviceW || canvas.height !== deviceH) {
    canvas.width = deviceW;
    canvas.height = deviceH;
  }
  ctx.setTransform(geo.dpr, 0, 0, geo.dpr, 0, 0);
  ctx.clearRect(0, 0, geo.w, geo.h);

  const X = (cm: number) => geo.offsetX + cm * geo.scale;
  const Y = (cm: number) => geo.offsetY + cm * geo.scale;
  const tankW = TANK.widthCm * geo.scale;
  const tankH = TANK.heightCm * geo.scale;

  // --- nền + bể nước ---
  const bg = ctx.createLinearGradient(0, 0, 0, geo.h);
  bg.addColorStop(0, STAGE_BG_TOP);
  bg.addColorStop(1, STAGE_BG_BOTTOM);
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, geo.w, geo.h);
  if (p.field) ctx.drawImage(p.field, geo.offsetX, geo.offsetY, tankW, tankH);

  ctx.strokeStyle = SLATE_700;
  ctx.lineWidth = 1.5;
  ctx.strokeRect(geo.offsetX + 0.5, geo.offsetY + 0.5, tankW - 1, tankH - 1);

  // --- đường trung trực: cực đại k = 0 (chỉ có nghĩa khi hai nguồn cùng phát) ---
  if (p.sourceBOn) {
    const bisectorX = X(TANK.widthCm / 2);
    ctx.save();
    ctx.setLineDash([5, 5]);
    ctx.strokeStyle = "rgba(148,163,184,0.45)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(bisectorX, geo.offsetY + 2);
    ctx.lineTo(bisectorX, geo.offsetY + tankH - 2);
    ctx.stroke();
    ctx.restore();
    // Nhãn đặt bên trái hay bên phải đường tuỳ chỗ nào còn chỗ, không để tràn khỏi khay.
    const onRight = bisectorX < geo.offsetX + tankW * 0.55;
    label(
      ctx,
      "k = 0 (trung trực)",
      onRight ? bisectorX + 5 : bisectorX - 5,
      geo.offsetY + 13,
      SLATE_400,
      onRight ? "left" : "right"
    );
  }

  // --- thước AB ---
  const yRuler = Y(p.sources.a.y) - 14;
  ctx.strokeStyle = SLATE_500;
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(X(p.sources.a.x), yRuler);
  ctx.lineTo(X(p.sources.b.x), yRuler);
  ctx.moveTo(X(p.sources.a.x), yRuler - 4);
  ctx.lineTo(X(p.sources.a.x), yRuler + 4);
  ctx.moveTo(X(p.sources.b.x), yRuler - 4);
  ctx.lineTo(X(p.sources.b.x), yRuler + 4);
  ctx.stroke();
  label(
    ctx,
    `AB = ${formatNumber(p.AB, 1)} cm`,
    (X(p.sources.a.x) + X(p.sources.b.x)) / 2,
    yRuler - 6,
    SLATE_400,
    "center"
  );

  // --- hai đường d₁, d₂ từ nguồn tới M (không ghi số lên từng đường: ở 375px
  // hai nhãn chồng nhau — số liệu đã nằm trong ô của M và trong dòng nhận xét) ---
  const drawSpoke = (from: TankPoint, to: TankPoint) => {
    ctx.save();
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = "rgba(226,232,240,0.45)";
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.moveTo(X(from.x), Y(from.y));
    ctx.lineTo(X(to.x), Y(to.y));
    ctx.stroke();
    ctx.restore();
  };
  if (p.sourceBOn) drawSpoke(p.sources.b, p.marker);
  drawSpoke(p.sources.a, p.marker);

  // --- nguồn A, B ---
  const drawSource = (point: TankPoint, name: string, on: boolean) => {
    const cx = X(point.x);
    const cy = Y(point.y);
    ctx.save();
    if (on) {
      ctx.shadowColor = ACCENT_SOFT;
      ctx.shadowBlur = 10;
      ctx.fillStyle = ACCENT;
    } else {
      ctx.fillStyle = "#0B1220";
    }
    ctx.beginPath();
    ctx.arc(cx, cy, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
    ctx.strokeStyle = on ? ACCENT : SLATE_600;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(cx, cy, 5, 0, Math.PI * 2);
    ctx.stroke();
    if (!on) {
      ctx.beginPath();
      ctx.moveTo(cx - 4, cy + 4);
      ctx.lineTo(cx + 4, cy - 4);
      ctx.stroke();
    }
    // Tên nguồn đặt DƯỚI nguồn: phía trên là chỗ của nhãn thước AB, để trên sẽ chồng nhau.
    label(ctx, name, cx + 8, cy + 17, on ? ACCENT : SLATE_400, "left", 13);
  };
  drawSource(p.sources.a, "A", true);
  drawSource(p.sources.b, p.sourceBOn ? "B" : "B tắt", p.sourceBOn);

  // --- điểm M kéo được ---
  const mx = X(p.marker.x);
  const my = Y(p.marker.y);
  // Tắt nguồn B thì M không còn là "cực đại/cực tiểu" nữa → dùng màu trung tính,
  // không mượn màu vàng của trạng thái "ở giữa hai vân" (M4: màu phải khớp nghĩa).
  const color = p.sourceBOn ? KIND_COLOR[p.kind] : "#CBD5E1";
  ctx.save();
  ctx.shadowColor = color;
  ctx.shadowBlur = 12;
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(mx, my, 6, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  // Ô số liệu của M. Khay hẹp (điện thoại ~300 px) không đủ chỗ cho ô chữ mà
  // không đè lên chính chấm M và thước AB → chỉ ghi "M", số liệu nằm ngay dưới
  // khay trong dòng nhận xét (đủ gần để mắt không phải nhảy xa).
  const delta = p.d2 - p.d1;
  if (tankW < 430) {
    label(ctx, "M", mx + 9, my - 8, color, "left", 13);
    return;
  }

  const lines = [
    `M · d₁ = ${formatNumber(p.d1, 2)} cm · d₂ = ${formatNumber(p.d2, 2)} cm`,
    `Δd = d₂ − d₁ = ${formatNumber(delta, 2)} cm = ${formatNumber(delta / p.lambda, 2)}λ`,
    p.sourceBOn ? kindLabel(p.kind, p.order) : "chỉ còn sóng từ A",
  ];
  const boxW = Math.min(268, tankW - 16);
  const boxH = 12 + lines.length * 16;
  let boxX = mx + 12;
  if (boxX + boxW > geo.offsetX + tankW - 4) boxX = mx - boxW - 12;
  boxX = Math.min(Math.max(boxX, geo.offsetX + 4), geo.offsetX + tankW - boxW - 4);
  const boxY = Math.min(
    Math.max(my - boxH / 2, geo.offsetY + 4),
    geo.offsetY + tankH - boxH - 4
  );
  ctx.fillStyle = "rgba(4,7,12,0.8)";
  ctx.strokeStyle = "rgba(148,163,184,0.35)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.roundRect(boxX, boxY, boxW, boxH, 8);
  ctx.fill();
  ctx.stroke();
  lines.forEach((text, i) => {
    const last = i === lines.length - 1;
    label(ctx, text, boxX + 8, boxY + 16 + i * 16, last ? color : TEXT);
  });
}

const MESSAGE_STYLE: Record<"max" | "min" | "mid" | "off", string> = {
  max: "border-cyan-300/45 bg-cyan-300/[0.10] text-cyan-50",
  min: "border-white/10 bg-white/[0.04] text-slate-200",
  mid: "border-amber-300/35 bg-amber-300/[0.08] text-amber-100",
  off: "border-white/10 bg-white/[0.04] text-slate-300",
};

const BUTTON_BASE =
  "inline-flex min-h-11 items-center justify-center gap-1.5 rounded-lg px-3 text-sm font-medium transition active:scale-[0.98]";

const sliderClass =
  "h-1.5 w-full cursor-pointer appearance-none rounded-full bg-white/10 accent-[#2563EB] " +
  "[&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:appearance-none " +
  "[&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary " +
  "[&::-webkit-slider-thumb]:shadow-[0_0_0_3px_rgba(37,99,235,0.25)] " +
  "[&::-moz-range-thumb]:h-4 [&::-moz-range-thumb]:w-4 [&::-moz-range-thumb]:rounded-full " +
  "[&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:bg-primary";

export function InterferenceSimulation() {
  const sim = useInterferenceTank();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [box, setBox] = useState<Box>({ w: 0, h: 0, dpr: 1 });

  const geo = useMemo(() => geometryFor(box), [box]);
  const field = useMemo(
    () => buildFieldCanvas(geo, { lambda: sim.lambda, sourceBOn: sim.sourceBOn, sources: sim.sources }),
    [geo, sim.lambda, sim.sourceBOn, sim.sources]
  );

  // Kích thước thật của canvas (xoay máy, đổi bề ngang, đổi màn hình có DPR khác).
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

  // Vẽ lại sau mỗi lần render — không có vòng lặp rAF vì mọi thứ đứng yên (B4).
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || box.w === 0) return;
    drawScene(canvas, {
      geo,
      field,
      lambda: sim.lambda,
      AB: sim.AB,
      sourceBOn: sim.sourceBOn,
      sources: sim.sources,
      marker: sim.marker,
      d1: sim.d1,
      d2: sim.d2,
      kind: sim.kind,
      order: sim.order,
    });
  });

  const tankPointFromEvent = (event: ReactPointerEvent<HTMLCanvasElement>): TankPoint | null => {
    const rect = event.currentTarget.getBoundingClientRect();
    const x = (event.clientX - rect.left - geo.offsetX) / geo.scale;
    const y = (event.clientY - rect.top - geo.offsetY) / geo.scale;
    if (x < 0 || x > TANK.widthCm || y < 0 || y > TANK.heightCm) return null;
    return { x, y };
  };

  const onPointerDown = (event: ReactPointerEvent<HTMLCanvasElement>) => {
    const point = tankPointFromEvent(event);
    if (!point) return;
    event.currentTarget.setPointerCapture?.(event.pointerId);
    sim.moveMarker(point);
  };

  const onPointerMove = (event: ReactPointerEvent<HTMLCanvasElement>) => {
    if (!event.currentTarget.hasPointerCapture?.(event.pointerId)) return;
    const point = tankPointFromEvent(event);
    if (!point) return;
    sim.moveMarker(point);
    event.preventDefault();
  };

  const onKeyDown = (event: ReactKeyboardEvent<HTMLCanvasElement>) => {
    switch (event.key) {
      case "ArrowUp":
        sim.nudgeMarker(0, -KEY_STEP_CM);
        break;
      case "ArrowDown":
        sim.nudgeMarker(0, KEY_STEP_CM);
        break;
      case "ArrowRight":
        sim.nudgeMarker(KEY_STEP_CM, 0);
        break;
      case "ArrowLeft":
        sim.nudgeMarker(-KEY_STEP_CM, 0);
        break;
      default:
        return;
    }
    event.preventDefault();
  };

  return (
    <div>
      <div className="relative overflow-hidden rounded-xl border border-white/10">
        <canvas
          ref={canvasRef}
          tabIndex={0}
          role="img"
          aria-label="Khay sóng hai nguồn A, B. Chạm hoặc kéo để đặt điểm M rồi đọc hiệu đường đi d₂ − d₁; dùng phím mũi tên để chỉnh từng bước nhỏ."
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onKeyDown={onKeyDown}
          className="block aspect-[2] w-full cursor-crosshair touch-none select-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-300/70"
        />
      </div>

      <p className="mt-2 text-[13px] leading-relaxed text-slate-500">
        Chạm vào khay để đặt điểm M (hoặc dùng phím mũi tên). Đường sáng: cực đại
        (d₂ − d₁ = kλ) · đường tối: cực tiểu ((k + ½)λ).
      </p>

      <p
        role="status"
        aria-live="polite"
        className={`mt-3 min-h-[3.5rem] rounded-lg border px-3 py-2 text-sm leading-relaxed ${MESSAGE_STYLE[sim.message.kind]}`}
      >
        {sim.message.text}
      </p>

      <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3">
        <div>
          <div className="mb-1.5 flex items-center justify-between text-xs text-slate-400">
            <label htmlFor="gt-f">Tần số f</label>
            <span className="font-mono text-slate-200">{formatNumber(sim.f, 0)} Hz</span>
          </div>
          <input
            id="gt-f"
            type="range"
            min={F_RANGE.min}
            max={F_RANGE.max}
            step={F_RANGE.step}
            value={sim.f}
            onChange={(event) => sim.setF(parseFloat(event.target.value))}
            className={sliderClass}
            aria-label="Tần số cần rung"
          />
        </div>

        <div>
          <div className="mb-1.5 flex items-center justify-between text-xs text-slate-400">
            <label htmlFor="gt-v">Tốc độ v</label>
            <span className="font-mono text-slate-200">{formatNumber(sim.v, 0)} cm/s</span>
          </div>
          <input
            id="gt-v"
            type="range"
            min={V_RANGE.min}
            max={V_RANGE.max}
            step={V_RANGE.step}
            value={sim.v}
            onChange={(event) => sim.setV(parseFloat(event.target.value))}
            className={sliderClass}
            aria-label="Tốc độ truyền sóng"
          />
        </div>

        <div className="col-span-2 sm:col-span-1">
          <div className="mb-1.5 flex items-center justify-between text-xs text-slate-400">
            <label htmlFor="gt-ab">Khoảng cách AB</label>
            <span className="font-mono text-slate-200">{formatNumber(sim.AB, 1)} cm</span>
          </div>
          <input
            id="gt-ab"
            type="range"
            min={AB_RANGE.min}
            max={AB_RANGE.max}
            step={AB_RANGE.step}
            value={sim.AB}
            onChange={(event) => sim.setAB(parseFloat(event.target.value))}
            className={sliderClass}
            aria-label="Khoảng cách hai nguồn"
          />
        </div>
      </div>

      <dl className="mt-3 grid grid-cols-3 gap-x-3 gap-y-2 font-mono">
        <div>
          <dt className="text-[13px] text-slate-500">λ = v/f</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.lambda, 2)} cm</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Cực đại AB</dt>
          <dd className="text-sm text-ink">{sim.counts.maxima}</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Cực tiểu AB</dt>
          <dd className="text-sm text-ink">{sim.counts.minima}</dd>
        </div>
      </dl>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <button
          type="button"
          aria-pressed={sim.sourceBOn}
          onClick={sim.toggleSourceB}
          className={`${BUTTON_BASE} ${
            sim.sourceBOn
              ? "bg-cyan-300/[0.14] text-cyan-300 hover:bg-cyan-300/[0.2]"
              : "border border-white/10 text-slate-200 hover:bg-white/[0.08]"
          }`}
        >
          {sim.sourceBOn ? "Nguồn B: bật" : "Nguồn B: tắt"}
        </button>
        <button
          type="button"
          onClick={sim.reset}
          className={`${BUTTON_BASE} border border-white/10 text-slate-200 hover:bg-white/[0.08]`}
        >
          <RotateCcw size={15} />
          Đặt lại
        </button>
      </div>
    </div>
  );
}
