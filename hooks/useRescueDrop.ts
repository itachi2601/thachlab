/**
 * hooks/useRescueDrop.ts
 *
 * Nguồn sự thật duy nhất cho mô phỏng "máy bay cứu hộ thả hàng" ở hero: cài đặt
 * chuyến bay (h, v₀), pha (chờ / đang bay / gói đang rơi / xong), vị trí máy bay,
 * quỹ đạo gói hàng và câu nhận xét.
 *
 * Vòng lặp requestAnimationFrame chỉ chạy KHI máy bay đang bay hoặc gói đang rơi
 * (mỗi lượt 5–9 giây) — lúc chờ thì không có gì chạy nền, đúng tinh thần B4: mô
 * phỏng chỉ chuyển động khi học sinh ra lệnh.
 *
 * Ghi chú kỹ thuật: h và v₀ được truyền vào vòng lặp qua closure của effect
 * (không sao chép vào ref lúc render — luật react-hooks/refs cấm). Trong lúc bay
 * hai giá trị này không đổi (thanh trượt bị khoá), nên vòng lặp chỉ khởi động
 * lại khi chúng đổi.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { formatNumber } from "@/lib/physics";
import {
  DOT_INTERVAL,
  G_EARTH,
  H_RANGE,
  PAD_X,
  V0_RANGE,
  clampHeight,
  clampSpeed,
  describeDrop,
  equalTimeDots,
  fallTime,
  outcomeOf,
  packageAt,
  readyFeedback,
  startXOf,
  type DropAttempt,
  type DropOutcome,
  type Feedback,
} from "@/lib/horizontalProjectile";

export interface Point {
  x: number;
  y: number;
}

export type RescuePhase = "ready" | "flying" | "falling" | "done";

export interface UseRescueDropReturn {
  h: number;
  v0: number;
  phase: RescuePhase;
  tRun: number; // giây kể từ lúc bấm "Cho máy bay bay"
  planeX: number; // vị trí máy bay (m dọc mặt đất)
  releaseX: number | null; // chỗ đã thả; null = chưa thả
  packagePos: Point | null; // vị trí gói trong khung nhìn (x dọc đất, y độ cao); null = còn trên máy bay
  trail: Point[];
  dots: Point[];
  outcome: DropOutcome | null;
  message: Feedback;
  showDots: boolean;
  setHeight: (value: number) => void;
  setSpeed: (value: number) => void;
  toggleDots: () => void;
  start: () => void;
  drop: () => void;
  reset: () => void;
  primaryAction: () => void;
}

export function useRescueDrop(): UseRescueDropReturn {
  const [h, setH] = useState<number>(H_RANGE.initial);
  const [v0, setV0] = useState<number>(V0_RANGE.initial);
  const [phase, setPhase] = useState<RescuePhase>("ready");
  const [tRun, setTRun] = useState(0);
  const [releaseX, setReleaseX] = useState<number | null>(null);
  // Thời điểm trong lượt bay mà học sinh bấm thả (s). Để ở state chứ không phải ref
  // vì phần vẽ phải đọc được nó lúc render (luật react-hooks/refs cấm đọc ref khi render).
  const [dropAt, setDropAt] = useState<number | null>(null);
  const [trail, setTrail] = useState<Point[]>([]);
  const [dots, setDots] = useState<Point[]>([]);
  const [outcome, setOutcome] = useState<DropOutcome | null>(null);
  const [message, setMessage] = useState<Feedback>(() =>
    readyFeedback(H_RANGE.initial, V0_RANGE.initial, formatNumber)
  );
  const [showDots, setShowDots] = useState(true);

  /** Chỗ máy bay xuất phát: sớm hơn điểm thả sớm nhất RUNUP mét (không bao giờ âm). */
  const startX = useMemo(() => startXOf(v0, h), [v0, h]);

  // Các ref dưới đây chỉ được đọc/ghi trong callback và effect, không đụng lúc render.
  const tRunRef = useRef(0);
  const dotsRef = useRef<Point[]>([]);
  const attemptRef = useRef<DropAttempt | null>(null);

  /** Đưa mô phỏng về trạng thái chờ với cài đặt mới — dùng chung cho reset/đổi thanh trượt. */
  const primeRun = useCallback((nextH: number, nextV0: number) => {
    tRunRef.current = 0;
    dotsRef.current = [];
    setTRun(0);
    setReleaseX(null);
    setDropAt(null);
    setTrail([]);
    setDots([]);
    setOutcome(null);
    setPhase("ready");
    setMessage(readyFeedback(nextH, nextV0, formatNumber));
  }, []);

  const start = useCallback(() => {
    tRunRef.current = 0;
    dotsRef.current = [];
    setTRun(0);
    setReleaseX(null);
    setDropAt(null);
    setTrail([]);
    setDots([]);
    setOutcome(null);
    setPhase("flying");
    setMessage({
      kind: "goal",
      text:
        `Máy bay đang bay ngang ở h = ${formatNumber(h, 1)} m với v₀ = ${formatNumber(v0, 1)} m/s. ` +
        `Bấm "Thả hàng" khi em nghĩ gói sẽ rơi trúng bãi đáp.`,
    });
  }, [h, v0]);

  const drop = useCallback(() => {
    if (phase !== "flying") return;
    const at = tRunRef.current;
    setDropAt(at);
    setReleaseX(startX + v0 * at);
    setPhase("falling");
  }, [phase, startX, v0]);

  const reset = useCallback(() => {
    primeRun(h, v0);
  }, [primeRun, h, v0]);

  const setHeight = useCallback(
    (value: number) => {
      const next = clampHeight(value);
      setH(next);
      primeRun(next, v0);
    },
    [primeRun, v0]
  );

  const setSpeed = useCallback(
    (value: number) => {
      const next = clampSpeed(value);
      setV0(next);
      primeRun(h, next);
    },
    [primeRun, h]
  );

  const toggleDots = useCallback(() => setShowDots((value) => !value), []);

  const primaryAction = useCallback(() => {
    if (phase === "ready") start();
    else if (phase === "flying") drop();
    else reset();
  }, [phase, start, drop, reset]);

  /** Chốt lượt thả: phân loại kết quả + câu nhận xét, giữ lượt này làm "lượt trước". */
  const finishRun = useCallback(
    (release: number | null) => {
      const attempt: DropAttempt = { h, v0, releaseX: release };
      const result = outcomeOf(attempt);
      const prev = attemptRef.current;
      attemptRef.current = attempt;
      setOutcome(result);
      setMessage(describeDrop(attempt, result, prev, formatNumber));
      setPhase("done");
    },
    [h, v0]
  );

  // Vòng lặp chỉ sống trong lúc máy bay bay / gói đang rơi.
  useEffect(() => {
    if (phase !== "flying" && phase !== "falling") return;
    if (phase === "falling" && (releaseX === null || dropAt === null)) return;

    const T = fallTime(h, G_EARTH);
    let rafId = 0;
    let lastTimestamp: number | null = null;

    const step = (timestamp: number) => {
      if (lastTimestamp === null) lastTimestamp = timestamp;
      const dt = Math.min(0.05, (timestamp - lastTimestamp) / 1000);
      lastTimestamp = timestamp;
      tRunRef.current += dt;

      if (phase === "flying") {
        // Bay qua bãi đáp mà chưa thả thì lượt này chắc chắn trượt — dừng ngay tại bãi đáp.
        if (startX + v0 * tRunRef.current >= PAD_X) {
          tRunRef.current = (PAD_X - startX) / v0;
          setTRun(tRunRef.current);
          finishRun(null);
          return;
        }
        setTRun(tRunRef.current);
        rafId = requestAnimationFrame(step);
        return;
      }

      // Gói đang rơi: mọi vị trí suy từ tRun − thời điểm thả nên vệt vẽ luôn khớp số đọc.
      const at = releaseX as number;
      const from = dropAt as number;
      const tFall = tRunRef.current - from;
      if (tFall >= T) {
        tRunRef.current = from + T;
        setTRun(tRunRef.current);
        setTrail((points) => [...points, packageAt(T, at, v0, h, G_EARTH)]);
        finishRun(at);
        return;
      }

      setTRun(tRunRef.current);
      setTrail((points) => [...points, packageAt(tFall, at, v0, h, G_EARTH)]);

      const wanted = Math.min(Math.floor(tFall / DOT_INTERVAL), Math.floor(T / DOT_INTERVAL));
      if (wanted > dotsRef.current.length) {
        dotsRef.current = equalTimeDots(at, v0, h, G_EARTH).slice(0, wanted);
        setDots(dotsRef.current);
      }
      rafId = requestAnimationFrame(step);
    };

    rafId = requestAnimationFrame(step);
    return () => cancelAnimationFrame(rafId);
  }, [phase, h, v0, startX, releaseX, dropAt, finishRun]);

  const planeX = phase === "ready" ? startX : startX + v0 * tRun;

  const packagePos: Point | null =
    phase === "falling" || phase === "done"
      ? releaseX === null
        ? null
        : packageAt(Math.max(0, tRun - (dropAt ?? 0)), releaseX, v0, h, G_EARTH)
      : null;

  return {
    h,
    v0,
    phase,
    tRun,
    planeX,
    releaseX,
    packagePos,
    trail,
    dots,
    outcome,
    message,
    showDots,
    setHeight,
    setSpeed,
    toggleDots,
    start,
    drop,
    reset,
    primaryAction,
  };
}
