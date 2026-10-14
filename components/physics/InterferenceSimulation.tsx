"use client";

/**
 * components/physics/InterferenceSimulation.tsx
 *
 * Tab "Giao thoa" của hero: khay sóng nước hai mũi nhọn (Bài 12, Vật lí 11) —
 * canvas 2D thuần (không thư viện), học sinh chạm/kéo chấm M để tự đọc ra
 * d₂ − d₁ = kλ (cực đại) và (k + ½)λ (cực tiểu), tắt nguồn B để thấy vân biến mất,
 * và bấm "Chạy sóng" để xem nước chạy qua lại.
 *
 * HAI CHẾ ĐỘ HÌNH:
 *  - Đứng yên (mặc định): vẽ BAO HÌNH biên độ |2a·cos(πΔd/λ)| — đúng cái khay
 *    sóng thật cho thấy: các đường sáng/tối ĐỨNG YÊN.
 *  - Chạy sóng (HS bấm nút): vẽ LI ĐỘ TỨC THỜI u = Σaᵢ·cos(ωt − k·dᵢ) — nước
 *    chạy qua lại, còn vân thì vẫn đứng yên.
 *
 * Bảng màu đọc từ StagePalette (stage-theme.ts) tự thích ứng theo theme sáng/tối.
 */

import {
  useEffect,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent as ReactKeyboardEvent,
  type PointerEvent as ReactPointerEvent,
} from "react";
import { Pause, Play, RotateCcw } from "lucide-react";
import { formatNumber } from "@/lib/physics";
import {
  AB_RANGE,
  F_RANGE,
  TANK,
  V_RANGE,
  singleSourceFieldIntensity,
  singleSourcePhasor,
  twoSourceFieldIntensity,
  twoSourcePhasors,
  visualPeriod,
  type FringeKind,
} from "@/lib/interference";
import {
  useInterferenceTank,
  type TankPoint,
} from "@/hooks/useInterferenceTank";
import {
  getStagePalette,
  subscribeStageTheme,
  colorToRgb,
  withAlpha,
  type StagePalette,
} from "./stage-theme";

const MONO = "ui-monospace, SFMono-Regular, Menlo, monospace";

/** Bước nhảy khi chỉnh M bằng phím (cm) — D2: bàn phím là đường dự phòng cho ngón tay. */
const KEY_STEP_CM = 0.4;

/**
 * Trần số điểm ảnh của lớp trường. Điện thoại/desktop thường ở dưới trần này nên
 * vẫn vẽ đúng độ phân giải thiết bị; màn hình rất nét (4K/DPR 3) thì hạ nhẹ để
 * ảnh động giữ được 60 khung hình/giây.
 */
const MAX_RASTER_PIXELS = 480_000;

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

const LUT_SIZE = 1024;

/**
 * Tạo bảng LUT đóng gói màu RGB:
 * - Nền tối: cực đại phát sáng cyan (#22D3EE), cực tiểu màu nền đen.
 * - Nền sáng: cực đại đậm hơn nền (waveMax: xanh primary #1d4ed8),
 *   cực tiểu nhạt hơn nền (trắng #ffffff).
 */
function createGlowLut(pal: StagePalette): Int32Array {
  const table = new Int32Array(LUT_SIZE + 1);
  const isDark = pal.bgRgb[0] < 50;

  if (isDark) {
    for (let i = 0; i <= LUT_SIZE; i++) {
      const glow = (i / LUT_SIZE) ** 2.25;
      const r = Math.round(5 + 30 * glow);
      const g = Math.round(8 + 190 * glow);
      const b = Math.round(14 + 214 * glow);
      table[i] = (r << 16) | (g << 8) | b;
    }
  } else {
    const bg = pal.bgRgb;
    const maxRgb = colorToRgb(pal.waveMax, [29, 78, 216]);
    const minRgb: [number, number, number] = [255, 255, 255]; // nhạt hơn nền

    for (let i = 0; i <= LUT_SIZE; i++) {
      const u = i / LUT_SIZE;
      let r: number, g: number, b: number;
      if (u <= 0.5) {
        // u từ 0 đến 0.5: từ trắng (cực tiểu) đến màu nền khay
        const t = (0.5 - u) / 0.5;
        r = Math.round(bg[0] + (minRgb[0] - bg[0]) * t);
        g = Math.round(bg[1] + (minRgb[1] - bg[1]) * t);
        b = Math.round(bg[2] + (minRgb[2] - bg[2]) * t);
      } else {
        // u từ 0.5 đến 1.0: từ màu nền đến xanh đậm (cực đại)
        const t = (u - 0.5) / 0.5;
        const factor = Math.pow(t, 1.25);
        r = Math.round(bg[0] + (maxRgb[0] - bg[0]) * factor);
        g = Math.round(bg[1] + (maxRgb[1] - bg[1]) * factor);
        b = Math.round(bg[2] + (maxRgb[2] - bg[2]) * factor);
      }
      table[i] = (r << 16) | (g << 8) | b;
    }
  }

  return table;
}

interface FieldParams {
  lambda: number;
  sourceBOn: boolean;
  sources: { a: TankPoint; b: TankPoint };
}

interface FieldTextures {
  width: number;
  height: number;
  tankX0: number;
  tankY0: number;
  tankX1: number;
  tankY1: number;
  cos: Float32Array;
  sin: Float32Array;
  envelope: ImageData;
  wave: ImageData;
  lut: Int32Array;
}

/**
 * Dựng sẵn hai ảnh và bảng pha cho cả hai chế độ. Ảnh phủ kín canvas (kể cả lề
 * ngoài khay — lề tô đúng màu nền gradient) nên mỗi khung hình chỉ cần một
 * `putImageData`, không phải vẽ lại nền.
 */
function buildFieldTextures(
  geo: Geometry,
  rasterDpr: number,
  params: FieldParams,
  pal: StagePalette
): FieldTextures | null {
  if (typeof document === "undefined" || geo.w <= 0 || geo.h <= 0) return null;
  const width = Math.max(1, Math.round(geo.w * rasterDpr));
  const height = Math.max(1, Math.round(geo.h * rasterDpr));
  const scratch = document.createElement("canvas").getContext("2d");
  if (!scratch) return null;

  const envelope = scratch.createImageData(width, height);
  const wave = scratch.createImageData(width, height);
  const envData = envelope.data;
  const waveData = wave.data;
  const lut = createGlowLut(pal);

  const topRgb = colorToRgb(pal.bgTop, [7, 12, 21]);
  const bottomRgb = pal.bgRgb;

  // Nền gradient cho cả hai ảnh
  for (let py = 0; py < height; py++) {
    const f = height > 1 ? py / (height - 1) : 0;
    const r = Math.round(topRgb[0] + (bottomRgb[0] - topRgb[0]) * f);
    const g = Math.round(topRgb[1] + (bottomRgb[1] - topRgb[1]) * f);
    const b = Math.round(topRgb[2] + (bottomRgb[2] - topRgb[2]) * f);
    let index = py * width * 4;
    for (let px = 0; px < width; px++, index += 4) {
      envData[index] = r;
      envData[index + 1] = g;
      envData[index + 2] = b;
      envData[index + 3] = 255;
      waveData[index] = r;
      waveData[index + 1] = g;
      waveData[index + 2] = b;
      waveData[index + 3] = 255;
    }
  }

  // Vùng khay (hình chữ nhật) trong hệ điểm ảnh của lớp trường.
  const tankX0 = Math.max(0, Math.floor(geo.offsetX * rasterDpr));
  const tankY0 = Math.max(0, Math.floor(geo.offsetY * rasterDpr));
  const tankX1 = Math.min(width, Math.ceil((geo.offsetX + TANK.widthCm * geo.scale) * rasterDpr));
  const tankY1 = Math.min(height, Math.ceil((geo.offsetY + TANK.heightCm * geo.scale) * rasterDpr));
  const tankPixels = Math.max(0, (tankX1 - tankX0) * (tankY1 - tankY0));
  const cos = new Float32Array(tankPixels);
  const sin = new Float32Array(tankPixels);

  const { scale, offsetX, offsetY } = geo;
  const { a, b } = params.sources;
  const lambda = params.lambda;
  const twoSources = params.sourceBOn;
  let k = 0;

  for (let py = tankY0; py < tankY1; py++) {
    const yTank = ((py + 0.5) / rasterDpr - offsetY) / scale;
    const dyA = yTank - a.y;
    const dyB = yTank - b.y;
    const dyA2 = dyA * dyA;
    const dyB2 = dyB * dyB;
    let index = (py * width + tankX0) * 4;

    for (let px = tankX0; px < tankX1; px++, k++, index += 4) {
      const xTank = ((px + 0.5) / rasterDpr - offsetX) / scale;
      const dxA = xTank - a.x;
      const d1 = Math.sqrt(dxA * dxA + dyA2);

      let intensity: number;
      if (twoSources) {
        const dxB = xTank - b.x;
        const d2 = Math.sqrt(dxB * dxB + dyB2);
        intensity = twoSourceFieldIntensity(d1, d2, lambda);
        const phasor = twoSourcePhasors(d1, d2, lambda);
        cos[k] = phasor.c;
        sin[k] = phasor.s;
      } else {
        intensity = singleSourceFieldIntensity(d1, lambda);
        const phasor = singleSourcePhasor(d1, lambda);
        cos[k] = phasor.c;
        sin[k] = phasor.s;
      }

      const lutIdx = intensity <= 0 ? 0 : intensity >= 1 ? LUT_SIZE : (intensity * LUT_SIZE) | 0;
      const packed = lut[lutIdx];
      envData[index] = (packed >> 16) & 255;
      envData[index + 1] = (packed >> 8) & 255;
      envData[index + 2] = packed & 255;
    }
  }

  return { width, height, tankX0, tankY0, tankX1, tankY1, cos, sin, envelope, wave, lut };
}

/**
 * Vẽ lớp trường. `phase = null` → ảnh đứng yên (bao hình); có pha → li độ tức thời.
 */
function paintField(
  canvas: HTMLCanvasElement | null,
  textures: FieldTextures | null,
  phase: { cos: number; sin: number } | null
) {
  if (!canvas || !textures) return;
  if (canvas.width !== textures.width || canvas.height !== textures.height) {
    canvas.width = textures.width;
    canvas.height = textures.height;
  }
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  if (!phase) {
    ctx.putImageData(textures.envelope, 0, 0);
    return;
  }

  const { cos, sin, wave, width, tankX0, tankY0, tankX1, tankY1, lut } = textures;
  const out = wave.data;
  const cosPhase = phase.cos;
  const sinPhase = phase.sin;
  let k = 0;
  for (let py = tankY0; py < tankY1; py++) {
    let index = (py * width + tankX0) * 4;
    for (let px = tankX0; px < tankX1; px++, k++, index += 4) {
      const u = cos[k] * cosPhase + sin[k] * sinPhase;
      const mag = u < 0 ? -u : u;
      const lutIdx = mag <= 0 ? 0 : mag >= 1 ? LUT_SIZE : (mag * LUT_SIZE) | 0;
      const packed = lut[lutIdx];
      out[index] = (packed >> 16) & 255;
      out[index + 1] = (packed >> 8) & 255;
      out[index + 2] = packed & 255;
    }
  }
  ctx.putImageData(wave, 0, 0);
}

/** Chữ có viền để đọc được cả khi nằm trên vệt vân sáng hay nền tối. */
function label(
  ctx: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  color: string,
  haloColor: string,
  align: CanvasTextAlign = "left",
  size = 12
) {
  ctx.save();
  ctx.font = `${size}px ${MONO}`;
  ctx.textAlign = align;
  ctx.lineWidth = 3;
  ctx.lineJoin = "round";
  ctx.strokeStyle = haloColor;
  ctx.strokeText(text, x, y);
  ctx.fillStyle = color;
  ctx.fillText(text, x, y);
  ctx.restore();
}

function kindLabel(kind: FringeKind, order: number): string {
  if (kind === "max") return `cực đại bậc ${Math.abs(order)}`;
  if (kind === "min") return `cực tiểu (k = ${Math.round(order)})`;
  return "ở giữa hai vân";
}

interface SceneParams {
  geo: Geometry;
  AB: number;
  sourceBOn: boolean;
  sources: { a: TankPoint; b: TankPoint };
  marker: TankPoint;
  d1: number;
  d2: number;
  lambda: number;
  kind: FringeKind;
  order: number;
}

/** Lớp trên: khung khay, đường trung trực, nguồn, thước AB, điểm M và ô số liệu. */
function drawOverlay(canvas: HTMLCanvasElement, p: SceneParams, pal: StagePalette) {
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

  const isDark = pal.bgRgb[0] < 50;
  const halo = isDark ? "rgba(4,7,12,0.85)" : "rgba(255,255,255,0.9)";
  const kindColor: Record<FringeKind, string> = {
    max: pal.waveMax,
    min: isDark ? pal.waveMin : pal.accent,
    mid: pal.warm,
  };

  const X = (cm: number) => geo.offsetX + cm * geo.scale;
  const Y = (cm: number) => geo.offsetY + cm * geo.scale;
  const tankW = TANK.widthCm * geo.scale;
  const tankH = TANK.heightCm * geo.scale;

  ctx.strokeStyle = pal.gridStrong;
  ctx.lineWidth = 1.5;
  ctx.strokeRect(geo.offsetX + 0.5, geo.offsetY + 0.5, tankW - 1, tankH - 1);

  // --- đường trung trực: cực đại k = 0 ---
  if (p.sourceBOn) {
    const bisectorX = X(TANK.widthCm / 2);
    ctx.save();
    ctx.setLineDash([5, 5]);
    ctx.strokeStyle = withAlpha(pal.muted, 0.45);
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(bisectorX, geo.offsetY + 2);
    ctx.lineTo(bisectorX, geo.offsetY + tankH - 2);
    ctx.stroke();
    ctx.restore();
    const onRight = bisectorX < geo.offsetX + tankW * 0.55;
    label(
      ctx,
      "k = 0 (trung trực)",
      onRight ? bisectorX + 5 : bisectorX - 5,
      geo.offsetY + 13,
      pal.muted,
      halo,
      onRight ? "left" : "right"
    );
  }

  // --- thước AB ---
  const yRuler = Y(p.sources.a.y) - 14;
  ctx.strokeStyle = pal.line;
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
    pal.muted,
    halo,
    "center"
  );

  // --- hai đường d₁, d₂ từ nguồn tới M ---
  const drawSpoke = (from: TankPoint, to: TankPoint) => {
    ctx.save();
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = withAlpha(pal.ink, 0.45);
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
      ctx.shadowColor = pal.accentSoft;
      ctx.shadowBlur = 10;
      ctx.fillStyle = pal.accent;
    } else {
      ctx.fillStyle = isDark ? "#0B1220" : pal.bgBottom;
    }
    ctx.beginPath();
    ctx.arc(cx, cy, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
    ctx.strokeStyle = on ? pal.accent : pal.line;
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
    label(ctx, name, cx + 8, cy + 17, on ? pal.accent : pal.muted, halo, "left", 13);
  };
  drawSource(p.sources.a, "A", true);
  drawSource(p.sources.b, p.sourceBOn ? "B" : "B tắt", p.sourceBOn);

  // --- điểm M kéo được ---
  const mx = X(p.marker.x);
  const my = Y(p.marker.y);
  const color = p.sourceBOn ? kindColor[p.kind] : pal.muted;
  ctx.save();
  ctx.shadowColor = color;
  ctx.shadowBlur = 12;
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(mx, my, 6, 0, Math.PI * 2);
  ctx.fill();
  if (!isDark) {
    ctx.strokeStyle = pal.gridStrong;
    ctx.lineWidth = 1.4;
    ctx.stroke();
  }
  ctx.restore();

  const delta = p.d2 - p.d1;
  if (tankW < 430) {
    label(ctx, "M", mx + 9, my - 8, color, halo, "left", 13);
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
  ctx.fillStyle = isDark ? "rgba(4,7,12,0.85)" : "rgba(255,255,255,0.92)";
  ctx.strokeStyle = pal.line;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.roundRect(boxX, boxY, boxW, boxH, 8);
  ctx.fill();
  ctx.stroke();
  lines.forEach((text, i) => {
    const last = i === lines.length - 1;
    label(ctx, text, boxX + 8, boxY + 16 + i * 16, last ? color : pal.ink, halo);
  });
}

const MESSAGE_STYLE: Record<"max" | "min" | "mid" | "off", string> = {
  max: "border-primary/40 bg-primary-soft text-primary font-medium",
  min: "border-line bg-surface-2 text-ink",
  mid: "border-amber-300/35 bg-amber-300/[0.08] text-amber-600 dark:text-amber-100",
  off: "border-line bg-surface-2 text-muted",
};

const BUTTON_BASE =
  "inline-flex min-h-10 items-center justify-center gap-1.5 rounded-lg px-3 text-xs sm:text-sm font-medium transition active:scale-[0.98]";

const sliderClass =
  "h-1.5 w-full cursor-pointer appearance-none rounded-full bg-surface-2 accent-primary " +
  "[&::-webkit-slider-thumb]:h-3.5 [&::-webkit-slider-thumb]:w-3.5 [&::-webkit-slider-thumb]:appearance-none " +
  "[&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary " +
  "[&::-webkit-slider-thumb]:shadow-[0_0_0_3px_rgba(37,99,235,0.25)] " +
  "[&::-moz-range-thumb]:h-3.5 [&::-moz-range-thumb]:w-3.5 [&::-moz-range-thumb]:rounded-full " +
  "[&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:bg-primary";

export function InterferenceSimulation() {
  const sim = useInterferenceTank();
  const overlayRef = useRef<HTMLCanvasElement | null>(null);
  const fieldRef = useRef<HTMLCanvasElement | null>(null);
  const [palette, setPalette] = useState<StagePalette>(getStagePalette);
  const paletteRef = useRef<StagePalette>(palette);
  const [box, setBox] = useState<Box>({ w: 0, h: 0, dpr: 1 });
  const [playing, setPlaying] = useState(false);
  const [inView, setInView] = useState(true);
  const phaseRef = useRef(0);

  const geo = useMemo(() => geometryFor(box), [box]);
  const rasterDpr = useMemo(() => {
    const area = Math.max(1, box.w * box.h);
    return Math.min(box.dpr, Math.max(1, Math.sqrt(MAX_RASTER_PIXELS / area)));
  }, [box]);

  const textures = useMemo(
    () =>
      buildFieldTextures(
        geo,
        rasterDpr,
        {
          lambda: sim.lambda,
          sourceBOn: sim.sourceBOn,
          sources: sim.sources,
        },
        palette
      ),
    [geo, rasterDpr, sim.lambda, sim.sourceBOn, sim.sources, palette]
  );
  const period = visualPeriod(sim.lambda);

  // Kích thước thật của khay
  useEffect(() => {
    const canvas = overlayRef.current;
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

  // Lắng nghe thay đổi theme: cập nhật bảng màu và vẽ lại ngay
  useEffect(() => {
    paletteRef.current = getStagePalette();
    const unsubscribe = subscribeStageTheme(() => {
      const updated = getStagePalette();
      paletteRef.current = updated;
      setPalette(updated);
    });
    return unsubscribe;
  }, []);

  // Khay ra khỏi tầm mắt thì dừng vòng lặp
  useEffect(() => {
    const canvas = overlayRef.current;
    if (!canvas || typeof IntersectionObserver === "undefined") return;
    const observer = new IntersectionObserver(
      ([entry]) => setInView(entry.isIntersecting),
      { threshold: 0.15 }
    );
    observer.observe(canvas);
    return () => observer.disconnect();
  }, []);

  // Vẽ lớp chữ/nhãn sau mỗi lần render
  useEffect(() => {
    const canvas = overlayRef.current;
    if (!canvas) return;
    drawOverlay(
      canvas,
      {
        geo,
        AB: sim.AB,
        sourceBOn: sim.sourceBOn,
        sources: sim.sources,
        marker: sim.marker,
        d1: sim.d1,
        d2: sim.d2,
        lambda: sim.lambda,
        kind: sim.kind,
        order: sim.order,
      },
      paletteRef.current
    );
    const phase = playing
      ? { cos: Math.cos(phaseRef.current), sin: Math.sin(phaseRef.current) }
      : null;
    paintField(fieldRef.current, textures, phase);
  });

  // Vòng lặp ảnh động khi chạy sóng
  useEffect(() => {
    if (!playing || !inView || !textures) return;
    let rafId = 0;
    let last: number | null = null;
    const step = (timestamp: number) => {
      if (last !== null) {
        const dt = Math.min(0.05, (timestamp - last) / 1000);
        phaseRef.current = (phaseRef.current + (2 * Math.PI * dt) / period) % (2 * Math.PI);
      }
      last = timestamp;
      paintField(fieldRef.current, textures, {
        cos: Math.cos(phaseRef.current),
        sin: Math.sin(phaseRef.current),
      });
      rafId = requestAnimationFrame(step);
    };
    rafId = requestAnimationFrame(step);
    return () => cancelAnimationFrame(rafId);
  }, [playing, inView, textures, period]);

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
      <div className="relative overflow-hidden rounded-xl border border-line">
        {/* Lớp trường: chỉ ảnh, không bắt sự kiện, không chữ */}
        <canvas
          ref={fieldRef}
          aria-hidden
          className="pointer-events-none absolute inset-0 block h-full w-full"
        />
        {/* Lớp trên: nhãn, nguồn, điểm M — vẽ theo React, bắt mọi thao tác */}
        <canvas
          ref={overlayRef}
          tabIndex={0}
          role="img"
          aria-label="Khay sóng hai nguồn A, B. Chạm hoặc kéo để đặt điểm M rồi đọc hiệu đường đi d₂ − d₁; dùng phím mũi tên để chỉnh từng bước nhỏ."
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onKeyDown={onKeyDown}
          className="relative block aspect-[1.5] w-full sm:aspect-[2] lg:aspect-[2.3] cursor-crosshair touch-none select-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
        />
      </div>

      <div className="mt-2.5 flex flex-wrap items-center gap-2">
        <button
          type="button"
          aria-pressed={playing}
          onClick={() => setPlaying((value) => !value)}
          className={`${BUTTON_BASE} ${
            playing
              ? "bg-primary text-white hover:bg-primary-dark"
              : "border border-line text-ink hover:bg-surface-2"
          }`}
        >
          {playing ? <Pause size={14} /> : <Play size={14} />}
          {playing ? "Dừng sóng" : "Chạy sóng"}
        </button>
        <button
          type="button"
          aria-pressed={sim.sourceBOn}
          onClick={sim.toggleSourceB}
          className={`${BUTTON_BASE} ${
            sim.sourceBOn
              ? "bg-primary-soft text-primary font-semibold hover:bg-primary/20"
              : "border border-line text-ink hover:bg-surface-2"
          }`}
        >
          {sim.sourceBOn ? "Nguồn B: bật" : "Nguồn B: tắt"}
        </button>
        <button
          type="button"
          onClick={sim.reset}
          className={`${BUTTON_BASE} border border-line text-ink hover:bg-surface-2`}
        >
          <RotateCcw size={14} />
          Đặt lại
        </button>
      </div>

      <div className="mt-2.5 grid grid-cols-1 gap-2 sm:grid-cols-3">
        <label className="flex items-center gap-2 rounded-lg border border-line bg-surface-2 px-2.5 py-1.5 text-xs text-muted cursor-pointer">
          <span className="whitespace-nowrap shrink-0">f: <b className="font-mono text-ink">{formatNumber(sim.f, 0)} Hz</b></span>
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
        </label>

        <label className="flex items-center gap-2 rounded-lg border border-line bg-surface-2 px-2.5 py-1.5 text-xs text-muted cursor-pointer">
          <span className="whitespace-nowrap shrink-0">v: <b className="font-mono text-ink">{formatNumber(sim.v, 0)} cm/s</b></span>
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
        </label>

        <label className="flex items-center gap-2 rounded-lg border border-line bg-surface-2 px-2.5 py-1.5 text-xs text-muted cursor-pointer">
          <span className="whitespace-nowrap shrink-0">AB: <b className="font-mono text-ink">{formatNumber(sim.AB, 1)} cm</b></span>
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
        </label>
      </div>

      <p className="mt-2 text-xs leading-relaxed text-muted">
        {playing
          ? "Đang chạy sóng: các đường sáng/tối vẫn đứng yên — chỗ tối là nơi hai sóng luôn triệt tiêu nhau."
          : "Chạm vào khay để đặt điểm M (hoặc dùng phím mũi tên). Đường sáng/đậm: cực đại (d₂ − d₁ = kλ) · đường tối/nhạt: cực tiểu ((k + ½)λ)."}
      </p>

      <p
        role="status"
        aria-live="polite"
        className={`mt-2 min-h-[3rem] rounded-lg border px-3 py-1.5 text-xs sm:text-sm leading-relaxed ${MESSAGE_STYLE[sim.message.kind]}`}
      >
        {sim.message.text}
      </p>

      <dl className="mt-2 grid grid-cols-3 gap-x-3 gap-y-1 font-mono">
        <div>
          <dt className="text-xs text-slate-500">λ = v/f</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.lambda, 2)} cm</dd>
        </div>
        <div>
          <dt className="text-xs text-slate-500">Cực đại AB</dt>
          <dd className="text-sm text-ink">{sim.counts.maxima}</dd>
        </div>
        <div>
          <dt className="text-xs text-slate-500">Cực tiểu AB</dt>
          <dd className="text-sm text-ink">{sim.counts.minima}</dd>
        </div>
      </dl>
    </div>
  );
}
