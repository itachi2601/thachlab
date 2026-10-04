/**
 * hooks/useProjectileMotion.ts
 *
 * Nguồn sự thật duy nhất cho mô phỏng ném xiên ở hero: góc ném, tốc độ, pha
 * (đang ngắm / đang bay), quỹ đạo, vết các lần ném trước và câu nhận xét.
 *
 * Vòng lặp requestAnimationFrame chỉ chạy KHI bóng đang bay (2–3 giây mỗi lần
 * ném) — lúc ngắm thì không có gì chạy nền, đúng tinh thần B4: mô phỏng chỉ
 * chuyển động khi học sinh ra lệnh.
 *
 * Ghi chú kỹ thuật: góc và tốc độ được truyền vào vòng lặp qua closure của
 * effect (không sao chép vào ref lúc render — luật react-hooks/refs cấm). Trong
 * lúc bay hai giá trị này không đổi, nên vòng lặp chỉ khởi động lại khi chúng đổi.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { formatNumber } from "@/lib/physics";
import {
  ANGLE_MAX,
  ANGLE_MIN,
  DOT_INTERVAL,
  GRAVITIES,
  MIN_PULL_PX,
  V0_MAX,
  V0_MIN,
  aimFromPull,
  apexOf,
  clamp,
  equalTimeDots,
  feedbackFor,
  hangOf,
  positionAt,
  rangeOf,
  trajectoryPoints,
  type Feedback,
  type GravityKey,
  type Shot,
} from "@/lib/projectile";

export interface Point {
  x: number;
  y: number;
}

/** Một lần ném đã hoàn tất (kèm dữ liệu để vẽ lại). */
export interface CompletedShot extends Shot {
  apex: number; // độ cao cực đại (m)
  hangTime: number; // thời gian bay (s)
  dots: Point[]; // vị trí các chấm cách nhau 0,1 s
}

export interface GhostTrail {
  dots: Point[];
  range: number;
  angle: number;
  gKey: GravityKey;
}

export type ProjectilePhase = "aim" | "flight";

const GOAL_TEXT = "Mục tiêu: tìm góc ném xa nhất.";

export interface UseProjectileMotionReturn {
  gKey: GravityKey;
  g: number;
  angle: number;
  v0: number;
  phase: ProjectilePhase;
  t: number; // thời điểm trong chuyến bay (s)
  trail: Point[]; // quỹ đạo đang bay / vừa bay xong
  dots: Point[];
  ghosts: GhostTrail[];
  lastShot: CompletedShot | null;
  message: Feedback;
  showDots: boolean;
  isAiming: boolean;
  earthMarker: number | null; // tầm xa trên Trái Đất với cùng α, v₀ (vạch so sánh ở Mặt Trăng)
  timeScale: number; // hình được tua nhanh bao nhiêu lần (chuyến bay dài)
  beginAim: (dxs: number, dys: number) => void;
  moveAim: (dxs: number, dys: number) => void;
  releaseAim: () => void;
  fire: () => void;
  nudge: (deltaAngle: number, deltaV0: number) => void;
  setGravity: (key: GravityKey) => void;
  toggleDots: () => void;
  clearTrails: () => void;
}

export function useProjectileMotion(): UseProjectileMotionReturn {
  // Bắt đầu ở 35° chứ không phải 45°: để học sinh tự tìm ra góc tối ưu.
  const [angle, setAngle] = useState(35);
  const [v0, setV0] = useState(14);
  const [gKey, setGKey] = useState<GravityKey>("earth");
  const [phase, setPhase] = useState<ProjectilePhase>("aim");
  const [t, setT] = useState(0);
  const [trail, setTrail] = useState<Point[]>([]);
  const [dots, setDots] = useState<Point[]>([]);
  const [ghosts, setGhosts] = useState<GhostTrail[]>([]);
  const [lastShot, setLastShot] = useState<CompletedShot | null>(null);
  const [message, setMessage] = useState<Feedback>({ kind: "goal", text: GOAL_TEXT });
  const [showDots, setShowDots] = useState(true);
  const [isAiming, setIsAiming] = useState(false);
  const [earthMarker, setEarthMarker] = useState<number | null>(null);
  const [timeScale, setTimeScale] = useState(1);

  const g = GRAVITIES[gKey].g;

  // Các ref dưới đây chỉ được đọc/ghi trong callback và effect, không đụng lúc render.
  const tRef = useRef(0);
  const flightTimeRef = useRef(0);
  const timeScaleRef = useRef(1);
  const dotsRef = useRef<Point[]>([]);
  const pullLengthRef = useRef(0);
  const shotsRef = useRef<Shot[]>([]);
  const lastShotRef = useRef<CompletedShot | null>(null);

  const finishFlight = useCallback(() => {
    const gravity = GRAVITIES[gKey].g;
    const range = rangeOf(v0, angle, gravity);
    const apex = apexOf(v0, angle, gravity);
    const hangTime = flightTimeRef.current;
    const shotDots = equalTimeDots(v0, angle, gravity);

    const completed: CompletedShot = { angle, v0, gKey, range, apex, hangTime, dots: shotDots };

    // Lần ném trước đó trở thành vết mờ để so sánh (giữ tối đa 4 vết).
    const previous = lastShotRef.current;
    if (previous) {
      setGhosts((list) =>
        [
          ...list,
          { dots: previous.dots, range: previous.range, angle: previous.angle, gKey: previous.gKey },
        ].slice(-4)
      );
    }

    const history = shotsRef.current;
    const feedback = feedbackFor(completed, history, formatNumber);
    shotsRef.current = [...history, completed];
    lastShotRef.current = completed;

    setPhase("aim");
    setT(hangTime);
    setTrail(trajectoryPoints(v0, angle, gravity, 120));
    setDots(shotDots);
    setLastShot(completed);
    setMessage(feedback);
  }, [angle, v0, gKey]);

  // Vòng lặp chỉ sống trong lúc bay.
  useEffect(() => {
    if (phase !== "flight") return;
    const gravity = GRAVITIES[gKey].g;
    let rafId = 0;
    let lastTimestamp: number | null = null;

    const step = (timestamp: number) => {
      if (lastTimestamp === null) lastTimestamp = timestamp;
      const dt = Math.min(0.05, (timestamp - lastTimestamp) / 1000);
      lastTimestamp = timestamp;
      tRef.current += dt * timeScaleRef.current;

      if (tRef.current >= flightTimeRef.current) {
        tRef.current = flightTimeRef.current;
        setT(flightTimeRef.current);
        setTrail((points) => [...points, positionAt(flightTimeRef.current, v0, angle, gravity)]);
        finishFlight();
        return;
      }

      setT(tRef.current);
      setTrail((points) => [...points, positionAt(tRef.current, v0, angle, gravity)]);

      const wanted = Math.min(
        Math.floor(tRef.current / DOT_INTERVAL),
        Math.floor(flightTimeRef.current / DOT_INTERVAL)
      );
      if (wanted > dotsRef.current.length) {
        dotsRef.current = equalTimeDots(v0, angle, gravity).slice(0, wanted);
        setDots(dotsRef.current);
      }
      rafId = requestAnimationFrame(step);
    };

    rafId = requestAnimationFrame(step);
    return () => cancelAnimationFrame(rafId);
  }, [phase, angle, v0, gKey, finishFlight]);

  const startFlight = useCallback(() => {
    const gravity = GRAVITIES[gKey].g;
    const hangTime = hangOf(v0, angle, gravity);

    flightTimeRef.current = hangTime;
    // Chuyến bay trên Mặt Trăng dài gấp ~6 lần → tua nhanh để không phải chờ, có ghi chú dưới khung.
    const scale = clamp(hangTime / 3.6, 1, 8);
    timeScaleRef.current = scale;
    tRef.current = 0;
    dotsRef.current = [];

    setTimeScale(scale);
    setEarthMarker(gKey === "moon" ? rangeOf(v0, angle, GRAVITIES.earth.g) : null);
    setTrail([positionAt(0, v0, angle, gravity)]);
    setDots([]);
    setLastShot(null);
    setT(0);
    setPhase("flight");
  }, [angle, v0, gKey]);

  const applyPull = useCallback((dxs: number, dys: number) => {
    const aim = aimFromPull(dxs, dys);
    pullLengthRef.current = aim.pullLength;
    setAngle(aim.angle);
    setV0(aim.v0);
  }, []);

  const beginAim = useCallback(
    (dxs: number, dys: number) => {
      setIsAiming(true);
      applyPull(dxs, dys);
    },
    [applyPull]
  );

  const moveAim = useCallback(
    (dxs: number, dys: number) => {
      applyPull(dxs, dys);
    },
    [applyPull]
  );

  const releaseAim = useCallback(() => {
    setIsAiming(false);
    // Kéo quá ngắn (chạm nhầm vào sân) thì không ném — tránh một cú ném vô ý.
    const pulled = pullLengthRef.current;
    pullLengthRef.current = 0;
    if (pulled < MIN_PULL_PX) return;
    startFlight();
  }, [startFlight]);

  const fire = useCallback(() => {
    setIsAiming(false);
    startFlight();
  }, [startFlight]);

  const nudge = useCallback((deltaAngle: number, deltaV0: number) => {
    setPhase("aim");
    setAngle((current) => clamp(current + deltaAngle, ANGLE_MIN, ANGLE_MAX));
    setV0((current) => clamp(current + deltaV0, V0_MIN, V0_MAX));
  }, []);

  const setGravity = useCallback((key: GravityKey) => {
    // Đổi môi trường trọng trường là bắt đầu thí nghiệm mới: xoá vết và kỷ lục cũ.
    shotsRef.current = [];
    lastShotRef.current = null;
    setGKey(key);
    setGhosts([]);
    setLastShot(null);
    setTrail([]);
    setDots([]);
    setEarthMarker(null);
    setPhase("aim");
    setT(0);
    setMessage({
      kind: "goal",
      text:
        key === "moon"
          ? `Mặt Trăng: g = ${formatNumber(GRAVITIES.moon.g, 1)} m/s². Ném y hệt lần trước xem bóng bay tới đâu.`
          : GOAL_TEXT,
    });
  }, []);

  const toggleDots = useCallback(() => setShowDots((value) => !value), []);

  const clearTrails = useCallback(() => {
    shotsRef.current = [];
    lastShotRef.current = null;
    setGhosts([]);
    setLastShot(null);
    setTrail([]);
    setDots([]);
    setEarthMarker(null);
    setMessage({ kind: "goal", text: GOAL_TEXT });
  }, []);

  return {
    gKey,
    g,
    angle,
    v0,
    phase,
    t,
    trail,
    dots,
    ghosts,
    lastShot,
    message,
    showDots,
    isAiming,
    earthMarker,
    timeScale,
    beginAim,
    moveAim,
    releaseAim,
    fire,
    nudge,
    setGravity,
    toggleDots,
    clearTrails,
  };
}
