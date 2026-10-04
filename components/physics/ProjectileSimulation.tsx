"use client";

/**
 * components/physics/ProjectileSimulation.tsx
 *
 * Mô phỏng chuyển động ném xiên bằng canvas 2D thuần (không thư viện, không
 * animation CSS): học sinh KÉO bệ phóng như kéo ná cao su rồi thả tay — nét đứt
 * là quỹ đạo sắp ném, vết mờ là các lần ném trước, chấm trên quỹ đạo cách nhau
 * đúng 0,1 s (vì vₓ không đổi nên các chấm cách đều theo phương ngang).
 *
 * Mọi trạng thái nằm ở useProjectileMotion; ở đây chỉ vẽ và bắt thao tác.
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
  GRAVITIES,
  V0_MAX,
  apexOf,
  positionAt,
  rangeOf,
  trajectoryPoints,
  type GravityKey,
} from "@/lib/projectile";
import {
  useProjectileMotion,
  type CompletedShot,
  type GhostTrail,
  type Point,
  type ProjectilePhase,
} from "@/hooks/useProjectileMotion";

// --- Hằng số hình học (đơn vị viewBox canvas, không phải px màn hình) ---
const PAD_L = 46; // chừa chỗ vẽ bệ phóng
const PAD_R = 10;
const PAD_T = 16;
const PAD_B = 26; // chừa chỗ ghi thước đo dưới mặt đất
const STAGE_BG_TOP = "#070C15";
const STAGE_BG_BOTTOM = "#04070C";
const ACCENT = "#22D3EE";
const ACCENT_DIM = "rgba(34,211,238,0.55)";
const WARM = "#FBBF24";
const SLATE_400 = "#94A3B8";
const SLATE_600 = "#475569";
const SLATE_700 = "#334155";

interface Box {
  w: number;
  h: number;
}

interface Geometry {
  w: number;
  h: number;
  s: number; // px trên mét (một tỉ lệ cho cả hai trục — parabol không bị bóp méo)
  xMax: number; // bề ngang khung nhìn (m)
  yMax: number; // chiều cao khung nhìn (m)
  groundY: number;
  anchor: Point; // đầu nòng bệ phóng (px)
}

function geometryFor(box: Box, gKey: GravityKey): Geometry {
  const g = GRAVITIES[gKey].g;
  // Mặt Trăng: cùng v₀ bay xa ~6 lần nên khung nhìn phải rộng hơn mới thấy hết quỹ đạo.
  const xMax = gKey === "moon" ? 285 : 52;
  const yMax = ((V0_MAX * V0_MAX) / 2 / g) * 1.18; // đỉnh cao nhất có thể (α = 45°) + lề
  const s = Math.min((box.w - PAD_L - PAD_R) / xMax, (box.h - PAD_T - PAD_B) / yMax);
  const groundY = box.h - PAD_B;
  return { w: box.w, h: box.h, s, xMax, yMax, groundY, anchor: { x: PAD_L, y: groundY } };
}

interface SceneParams {
  geo: Geometry;
  gKey: GravityKey;
  phase: ProjectilePhase;
  angle: number;
  v0: number;
  t: number;
  trail: Point[];
  dots: Point[];
  ghosts: GhostTrail[];
  lastShot: CompletedShot | null;
  showDots: boolean;
  isAiming: boolean;
  pointer: Point | null;
  earthMarker: number | null;
}

const MONO = "ui-monospace, SFMono-Regular, Menlo, monospace";

/**
 * Hệ số phóng to nét/chữ/theo bề ngang khung: khung desktop rộng gấp đôi điện thoại
 * thì nét vẽ, viên đạn và chữ cũng phải to lên, nếu không sẽ thành "UI điện thoại
 * phóng to" — nhìn nhỏ và rỗng.
 */
function scaleFor(width: number): number {
  return Math.max(0.85, Math.min(1.55, width / 520));
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

  const k = scaleFor(geo.w);
  const X = (xm: number) => PAD_L + xm * geo.s;
  const Y = (ym: number) => geo.groundY - ym * geo.s;
  const rad = (deg: number) => (deg * Math.PI) / 180;
  const setFont = (size: number) => {
    ctx.font = `${size}px ${MONO}`;
  };
  const fsRuler = Math.max(11, 12 * k);
  const fsValue = Math.max(12, 13 * k);

  // --- nền + lưới ---
  const bg = ctx.createLinearGradient(0, 0, 0, geo.groundY);
  bg.addColorStop(0, STAGE_BG_TOP);
  bg.addColorStop(1, STAGE_BG_BOTTOM);
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, geo.w, geo.groundY);

  // Lưới mỗi 5 m (Mặt Trăng: 25 m) — cùng tỉ lệ ở cả hai trục nên ô lưới là hình vuông thật.
  const gridStep = geo.xMax > 120 ? 25 : 5;
  ctx.strokeStyle = "rgba(148,163,184,0.10)";
  ctx.lineWidth = 1;
  for (let x = 0; x <= geo.xMax; x += gridStep) {
    ctx.beginPath();
    ctx.moveTo(X(x), PAD_T - 6);
    ctx.lineTo(X(x), geo.groundY);
    ctx.stroke();
  }
  for (let y = gridStep; Y(y) > PAD_T; y += gridStep) {
    ctx.beginPath();
    ctx.moveTo(PAD_L, Y(y));
    ctx.lineTo(geo.w - PAD_R, Y(y));
    ctx.stroke();
  }

  // --- thang đo ĐỘ CAO ở lề trái ---
  // Không chỉ để đẹp: nhờ nó vùng trời phía trên quỹ đạo thành không gian đo được
  // ("đỉnh cao 10 m" có mốc để đối chiếu) thay vì một khoảng trống.
  ctx.textAlign = "left";
  setFont(fsRuler);
  for (let y = gridStep; Y(y) > PAD_T + 3; y += gridStep) {
    const py = Y(y);
    // Bỏ qua dải trên cùng: dòng gợi ý "Kéo từ bệ phóng…" nằm đè ở đó (nhãn sẽ bị che).
    if (py < 42) continue;
    ctx.strokeStyle = "rgba(148,163,184,0.20)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(PAD_L - 5 * k, py);
    ctx.lineTo(PAD_L, py);
    ctx.stroke();
    ctx.fillStyle = "rgba(100,116,139,0.95)";
    ctx.fillText(`${y} m`, 6, py + fsRuler * 0.35);
  }

  // --- mặt đất + thước đo ngang ---
  ctx.strokeStyle = SLATE_700;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, geo.groundY);
  ctx.lineTo(geo.w, geo.groundY);
  ctx.stroke();

  ctx.strokeStyle = "rgba(51,65,85,0.75)";
  ctx.lineWidth = 1;
  const hatches = Math.max(12, Math.round(geo.w / 22));
  for (let i = 0; i < hatches; i++) {
    const x = (geo.w * i) / (hatches - 1);
    ctx.beginPath();
    ctx.moveTo(x, geo.groundY);
    ctx.lineTo(x - 8 * k, geo.groundY + 12 * k);
    ctx.stroke();
  }

  const rulerStep = geo.xMax <= 60 ? 10 : 50;
  setFont(fsRuler);
  ctx.textAlign = "center";
  for (let x = rulerStep; x <= geo.xMax; x += rulerStep) {
    ctx.strokeStyle = SLATE_600;
    ctx.beginPath();
    ctx.moveTo(X(x), geo.groundY);
    ctx.lineTo(X(x), geo.groundY + 7 * k);
    ctx.stroke();
    ctx.fillStyle = SLATE_400;
    ctx.fillText(`${x} m`, X(x), geo.groundY + 8 * k + fsRuler);
  }
  ctx.textAlign = "left";

  const drawPath = (
    points: Point[],
    color: string | CanvasGradient,
    width: number,
    dash: number[] = []
  ) => {
    if (points.length < 2) return;
    ctx.save();
    ctx.setLineDash(dash);
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.beginPath();
    points.forEach((point, i) =>
      i ? ctx.lineTo(X(point.x), Y(point.y)) : ctx.moveTo(X(point.x), Y(point.y))
    );
    ctx.stroke();
    ctx.restore();
  };

  // Vệt quỹ đạo mờ dần về phía đã đi qua: mắt đọc được chiều chuyển động ngay cả
  // khi chỉ nhìn một khung hình tĩnh.
  const drawMotionTrail = (points: Point[], maxAlpha: number) => {
    if (points.length < 2) return;
    const first = points[0];
    const last = points[points.length - 1];
    const gradient = ctx.createLinearGradient(X(first.x), Y(first.y), X(last.x), Y(last.y));
    gradient.addColorStop(0, `rgba(34,211,238,${maxAlpha * 0.06})`);
    gradient.addColorStop(1, `rgba(34,211,238,${maxAlpha})`);
    drawPath(points, gradient, 2.4 * k);
  };

  // --- vết các lần ném trước (mờ dần theo thứ tự) ---
  p.ghosts.forEach((ghost, i) => {
    const alpha = 0.13 + 0.08 * i;
    drawPath(ghost.dots, `rgba(148,163,184,${alpha})`, 1.5 * k, [5, 5]);
    const landing = ghost.dots[ghost.dots.length - 1];
    if (!landing) return;
    ctx.fillStyle = `rgba(148,163,184,${alpha + 0.15})`;
    ctx.beginPath();
    ctx.arc(X(landing.x), Y(landing.y), 2.5 * k, 0, Math.PI * 2);
    ctx.fill();
  });

  // --- nét đứt: quỹ đạo sắp ném (chỉ khi đang ngắm) ---
  if (p.phase === "aim") {
    const preview = trajectoryPoints(p.v0, p.angle, GRAVITIES[p.gKey].g, 70);
    drawPath(preview, ACCENT_DIM, 1.7 * k, [6, 6]);
    const range = rangeOf(p.v0, p.angle, GRAVITIES[p.gKey].g);
    ctx.fillStyle = "rgba(34,211,238,0.75)";
    ctx.beginPath();
    ctx.arc(X(range), Y(0), 3.5 * k, 0, Math.PI * 2);
    ctx.fill();
    // Nhãn chỉ hiện trong lúc đang kéo: để thường trực thì nó đè lên nhãn độ cao h ở đỉnh.
    if (p.isAiming) {
      ctx.fillStyle = "#67E8F9";
      setFont(fsValue);
      ctx.textAlign = "center";
      ctx.fillText(
        "quỹ đạo sắp ném",
        Math.min(Math.max(X(range / 2), 70), geo.w - 70),
        Y(apexOf(p.v0, p.angle, GRAVITIES[p.gKey].g) / 2) - 6
      );
      ctx.textAlign = "left";
    }
  }

  // --- vạch so sánh: cùng cú ném trên Trái Đất (chỉ hiện ở Mặt Trăng) ---
  if (p.earthMarker !== null) {
    const x = X(p.earthMarker);
    if (x < geo.w - 6) {
      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = "rgba(251,191,36,0.55)";
      ctx.lineWidth = 1.4 * k;
      ctx.beginPath();
      ctx.moveTo(x, geo.groundY);
      ctx.lineTo(x, geo.groundY - 46 * k);
      ctx.stroke();
      ctx.restore();
      ctx.fillStyle = WARM;
      setFont(fsRuler);
      const text = `Trái Đất: ${formatNumber(p.earthMarker, 0)} m`;
      ctx.fillText(text, Math.min(x + 5, geo.w - ctx.measureText(text).width - 6), geo.groundY - 50 * k);
    }
  }

  // --- lần ném vừa rồi: nét liền + mốc tầm xa ---
  if (p.phase === "aim" && p.lastShot) {
    drawMotionTrail(p.trail, 0.6);
    const x = X(Math.min(p.lastShot.range, geo.xMax));
    ctx.save();
    ctx.setLineDash([3, 4]);
    ctx.strokeStyle = "rgba(34,211,238,0.35)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x, geo.groundY);
    ctx.lineTo(x, geo.groundY - 30 * k);
    ctx.stroke();
    ctx.restore();
    setFont(fsValue);
    const rangeText = `R = ${formatNumber(p.lastShot.range, 1)} m`;
    ctx.fillStyle = ACCENT;
    ctx.fillText(rangeText, Math.min(x + 4, geo.w - ctx.measureText(rangeText).width - 4), geo.groundY - 34 * k);

    // độ cao cực đại của lần ném đó
    const xApex = X(p.lastShot.range / 2);
    const yApex = Y(p.lastShot.apex);
    ctx.save();
    ctx.setLineDash([3, 4]);
    ctx.strokeStyle = "rgba(148,163,184,0.4)";
    ctx.beginPath();
    ctx.moveTo(xApex, geo.groundY);
    ctx.lineTo(xApex, yApex);
    ctx.stroke();
    ctx.restore();
    ctx.fillStyle = SLATE_400;
    setFont(fsRuler);
    ctx.fillText(`h = ${formatNumber(p.lastShot.apex, 1)} m`, xApex + 5, yApex + 4);
  }

  // --- đang bay ---
  if (p.phase === "flight") {
    const g = GRAVITIES[p.gKey].g;
    const pos = positionAt(p.t, p.v0, p.angle, g);
    const bx = X(pos.x);
    const by = Y(pos.y);

    drawMotionTrail(p.trail, 0.9);

    ctx.fillStyle = ACCENT;
    p.dots.forEach((dot) => {
      ctx.beginPath();
      ctx.arc(X(dot.x), Y(dot.y), 2.4 * k, 0, Math.PI * 2);
      ctx.fill();
    });

    // Hai thành phần vận tốc: vₓ không đổi, v_y giảm dần rồi đổi dấu ở đỉnh.
    // Lưu ý hệ toạ độ màn hình (y hướng xuống): vy > 0 thì mũi tên phải chỉ LÊN,
    // nên độ dời trên màn hình là −vy · (px trên mỗi m/s).
    const a = rad(p.angle);
    const vx = p.v0 * Math.cos(a);
    const vy = p.v0 * Math.sin(a) - g * p.t;
    const pxPerVel = 0.26 * geo.s;
    drawArrow(ctx, bx, by, bx + vx * pxPerVel, by, "rgba(94,234,212,0.95)", "v", "x", k);
    drawArrow(ctx, bx, by, bx, by - vy * pxPerVel, "rgba(251,191,36,0.95)", "v", "y", k);

    ctx.save();
    ctx.shadowColor = "rgba(34,211,238,0.75)";
    ctx.shadowBlur = 12 * k;
    ctx.fillStyle = "#E6FEFF";
    ctx.beginPath();
    ctx.arc(bx, by, 6 * k, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  } else if (p.lastShot) {
    const end = p.trail[p.trail.length - 1];
    if (end) {
      ctx.save();
      ctx.shadowColor = "rgba(34,211,238,0.7)";
      ctx.shadowBlur = 12 * k;
      ctx.fillStyle = "#E6FEFF";
      ctx.beginPath();
      ctx.arc(X(Math.min(end.x, geo.xMax)), Y(end.y), 6 * k, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  // --- bệ phóng ---
  const { x: ax, y: ay } = geo.anchor;
  ctx.save();
  ctx.translate(ax, ay);
  ctx.rotate(-rad(p.angle));
  ctx.fillStyle = "#1E293B";
  ctx.strokeStyle = SLATE_600;
  ctx.lineWidth = 1.5 * k;
  ctx.beginPath();
  ctx.roundRect(-6 * k, -6 * k, 40 * k, 12 * k, 4 * k);
  ctx.fill();
  ctx.stroke();
  ctx.restore();
  ctx.fillStyle = SLATE_700;
  ctx.beginPath();
  ctx.roundRect(ax - 12 * k, ay - 2 * k, 24 * k, 16 * k, 3 * k);
  ctx.fill();
  // Không ghi nhãn "bệ phóng" lên khung: hàng dưới mặt đất đã dành cho thước đo
  // (nhãn sẽ đè lên "10 m"), còn trên mặt đất thì vướng quỹ đạo. Chú thích đã có
  // ở dòng gợi ý "Kéo từ bệ phóng…" ngay trên khung.

  // --- dây kéo + cung góc khi đang kéo ---
  if (p.pointer) {
    ctx.save();
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = "rgba(251,191,36,0.8)";
    ctx.lineWidth = 1.6 * k;
    ctx.beginPath();
    ctx.moveTo(ax, ay);
    ctx.lineTo(p.pointer.x, p.pointer.y);
    ctx.stroke();
    ctx.restore();
    ctx.fillStyle = "rgba(251,191,36,0.9)";
    ctx.beginPath();
    ctx.arc(p.pointer.x, p.pointer.y, 5 * k, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "rgba(251,191,36,0.5)";
    ctx.lineWidth = 1.4 * k;
    ctx.beginPath();
    ctx.arc(ax, ay, 30 * k, -rad(p.angle), 0);
    ctx.stroke();
    ctx.fillStyle = WARM;
    setFont(fsValue);
    ctx.fillText(`${Math.round(p.angle)}°  ·  ${formatNumber(p.v0, 1)} m/s`, p.pointer.x + 10, p.pointer.y - 8);
  }
}

/** Mũi tên vector có nhãn kiểu vₓ / v_y (chỉ số dưới vẽ nhỏ hơn và hạ xuống). */
function drawArrow(
  ctx: CanvasRenderingContext2D,
  x1: number,
  y1: number,
  x2: number,
  y2: number,
  color: string,
  label: string,
  sub: string | null,
  k: number
) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  if (Math.hypot(dx, dy) < 9 * k) return;
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.7 * k;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const ang = Math.atan2(dy, dx);
  const head = 7 * k;
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - head * Math.cos(ang - 0.4), y2 - head * Math.sin(ang - 0.4));
  ctx.lineTo(x2 - head * Math.cos(ang + 0.4), y2 - head * Math.sin(ang + 0.4));
  ctx.fill();

  const fs = Math.max(11, 12 * k);
  ctx.font = `${fs}px ${MONO}`;
  const labelWidth = ctx.measureText(label).width;
  ctx.fillText(label, x2 + 5, y2 + 4);
  if (sub) {
    ctx.font = `${Math.max(9, fs - 3)}px ${MONO}`;
    ctx.fillText(sub, x2 + 5 + labelWidth + 0.5, y2 + 4 + fs * 0.3);
  }
}

const MESSAGE_STYLE: Record<"goal" | "best" | "win", string> = {
  goal: "border-white/10 bg-white/[0.04] text-slate-300",
  best: "border-amber-300/35 bg-amber-300/[0.08] text-amber-100",
  win: "border-cyan-300/45 bg-cyan-300/[0.10] text-cyan-50",
};

const BUTTON_BASE =
  "inline-flex min-h-11 items-center justify-center rounded-lg px-3 text-sm font-medium transition active:scale-[0.98]";

export function ProjectileSimulation() {
  const sim = useProjectileMotion();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [box, setBox] = useState<Box>({ w: 0, h: 0 });
  const [pointer, setPointer] = useState<Point | null>(null);
  const [hint, setHint] = useState("Kéo từ bệ phóng xuống dưới rồi thả tay");
  const hintTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const geo = useMemo(() => geometryFor(box, sim.gKey), [box, sim.gKey]);

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

  // Vẽ lại sau mỗi lần render (mỗi khung hình khi bóng đang bay, còn lại theo thao tác).
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || box.w === 0) return;
    drawScene(canvas, {
      geo,
      gKey: sim.gKey,
      phase: sim.phase,
      angle: sim.angle,
      v0: sim.v0,
      t: sim.t,
      trail: sim.trail,
      dots: sim.dots,
      ghosts: sim.ghosts,
      lastShot: sim.lastShot,
      showDots: sim.showDots,
      isAiming: sim.isAiming,
      pointer,
      earthMarker: sim.earthMarker,
    });
  });

  const flashHint = useCallback((text: string) => {
    setHint(text);
    if (hintTimer.current) clearTimeout(hintTimer.current);
    hintTimer.current = setTimeout(() => setHint("Kéo từ bệ phóng xuống dưới rồi thả tay"), 2400);
  }, []);

  useEffect(() => () => {
    if (hintTimer.current) clearTimeout(hintTimer.current);
  }, []);

  const localPoint = (event: ReactPointerEvent<HTMLCanvasElement>): Point => {
    const rect = event.currentTarget.getBoundingClientRect();
    return { x: event.clientX - rect.left, y: event.clientY - rect.top };
  };

  const onPointerDown = (event: ReactPointerEvent<HTMLCanvasElement>) => {
    if (sim.phase === "flight") return;
    const point = localPoint(event);
    const nearLauncher = Math.hypot(point.x - geo.anchor.x, point.y - geo.anchor.y) < 96;
    // Vùng "sân" quanh bệ phóng cũng nhận được — ngón tay to vẫn kéo dễ.
    const inField = point.x < geo.w * 0.45 && point.y > geo.groundY - 130;
    if (!nearLauncher && !inField) {
      flashHint("Bắt đầu kéo từ bệ phóng ở góc dưới bên trái");
      return;
    }
    event.currentTarget.setPointerCapture?.(event.pointerId);
    setPointer(point);
    sim.beginAim(geo.anchor.x - point.x, geo.anchor.y - point.y);
  };

  const onPointerMove = (event: ReactPointerEvent<HTMLCanvasElement>) => {
    if (!sim.isAiming) return;
    const point = localPoint(event);
    setPointer(point);
    sim.moveAim(geo.anchor.x - point.x, geo.anchor.y - point.y);
    event.preventDefault();
  };

  const finishPointer = () => {
    setPointer(null);
    sim.releaseAim();
  };

  const onKeyDown = (event: ReactKeyboardEvent<HTMLCanvasElement>) => {
    // Đang bay thì bỏ qua phím chỉnh góc/tốc độ (sẽ cắt ngang chuyến bay giữa chừng).
    if (sim.phase === "flight" && event.key !== " " && event.key !== "Enter") return;
    switch (event.key) {
      case "ArrowUp":
        sim.nudge(0, 0.5);
        break;
      case "ArrowDown":
        sim.nudge(0, -0.5);
        break;
      case "ArrowRight":
        sim.nudge(1, 0);
        break;
      case "ArrowLeft":
        sim.nudge(-1, 0);
        break;
      case " ":
      case "Enter":
        sim.fire();
        break;
      default:
        return;
    }
    event.preventDefault();
  };

  const showHint = sim.lastShot === null && sim.ghosts.length === 0;

  return (
    <div>
      <div className="relative overflow-hidden rounded-xl border border-white/10">
        <canvas
          ref={canvasRef}
          tabIndex={0}
          role="img"
          aria-label="Sân ném: kéo bệ phóng xuống dưới rồi thả tay để ném; dùng phím trái/phải để chỉnh góc, lên/xuống để chỉnh tốc độ, phím cách để ném"
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={finishPointer}
          onPointerCancel={finishPointer}
          onKeyDown={onKeyDown}
          className="block aspect-[2.2] w-full cursor-grab touch-none select-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-300/70 active:cursor-grabbing sm:aspect-[2.1] lg:aspect-[2.3]"
        />
        {/* Dòng gợi ý nằm trên nền canvas luôn tối nên phải dùng màu cố định: lớp phủ theme sáng
            trong globals.css đổi .text-slate-200 thành chữ sẫm → chữ sẫm trên nền tối (M2). */}
        {showHint && (
          <p className="pointer-events-none absolute left-2.5 top-2.5 rounded-full border border-[#334155] bg-black/70 px-3 py-1 text-[13px] text-[#E2E8F0]">
            {hint}
          </p>
        )}
      </div>

      <dl className="mt-3 grid grid-cols-3 gap-x-3 gap-y-2 font-mono lg:grid-cols-6">
        <div>
          <dt className="text-[13px] text-slate-500">Góc ném</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.angle, 0)}°</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Tốc độ v₀</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.v0, 1)} m/s</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">g</dt>
          <dd className="text-sm text-ink">{formatNumber(sim.g, 1)} m/s²</dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Tầm xa R</dt>
          <dd className="text-sm text-ink">
            {sim.lastShot || sim.phase === "flight"
              ? `${formatNumber(sim.phase === "flight" ? positionAt(sim.t, sim.v0, sim.angle, sim.g).x : (sim.lastShot?.range ?? 0), 1)} m`
              : "—"}
          </dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Cao nhất</dt>
          <dd className="text-sm text-ink">
            {sim.phase === "flight"
              ? `${formatNumber(positionAt(sim.t, sim.v0, sim.angle, sim.g).y, 1)} m`
              : sim.lastShot
                ? `${formatNumber(sim.lastShot.apex, 1)} m`
                : "—"}
          </dd>
        </div>
        <div>
          <dt className="text-[13px] text-slate-500">Thời gian bay</dt>
          <dd className="text-sm text-ink">
            {sim.phase === "flight"
              ? `${formatNumber(sim.t, 2)} s`
              : sim.lastShot
                ? `${formatNumber(sim.lastShot.hangTime, 2)} s`
                : "—"}
          </dd>
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
        <div className="flex overflow-hidden rounded-lg border border-white/10" role="group" aria-label="Chọn gia tốc trọng trường">
          {(Object.keys(GRAVITIES) as GravityKey[]).map((key) => (
            <button
              key={key}
              type="button"
              aria-pressed={sim.gKey === key}
              onClick={() => sim.setGravity(key)}
              className={`${BUTTON_BASE} px-3 ${
                sim.gKey === key
                  ? "bg-cyan-300/[0.14] text-cyan-300"
                  : "text-slate-400 hover:bg-white/[0.06]"
              }`}
            >
              {GRAVITIES[key].label}
            </button>
          ))}
        </div>

        <label className="inline-flex min-h-11 cursor-pointer items-center gap-2 text-[13px] text-slate-400">
          <input
            type="checkbox"
            checked={sim.showDots}
            onChange={sim.toggleDots}
            className="h-4 w-4 accent-[#22D3EE]"
          />
          Chấm mỗi 0,1 s
        </label>

        <button
          type="button"
          onClick={sim.clearTrails}
          className={`${BUTTON_BASE} border border-white/10 text-slate-200 hover:bg-white/[0.08]`}
        >
          Xoá vết ném
        </button>
      </div>

      {sim.gKey === "moon" && (
        <p className="mt-2 text-[13px] text-slate-500">
          Trên Mặt Trăng chuyến bay dài hơn nên hình được tua nhanh ×{formatNumber(sim.timeScale, 0)}.
        </p>
      )}
    </div>
  );
}
