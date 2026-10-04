/**
 * hooks/useInterferenceTank.ts
 *
 * Nguồn sự thật duy nhất cho mô phỏng khay sóng giao thoa ở hero: f, v, AB,
 * nguồn B đang bật hay tắt, vị trí điểm M và câu nhận xét.
 *
 * KHÔNG có vòng lặp requestAnimationFrame: vân giao thoa là hình đứng yên
 * (biên độ tổng hợp không phụ thuộc thời gian), nên mọi thứ chỉ tính lại khi
 * học sinh đổi tham số hoặc kéo M — đúng tinh thần B4 (không có gì tự chuyển
 * động) và cũng là cách rẻ nhất về pin/CPU.
 */

import { useCallback, useMemo, useState } from "react";
import { formatNumber } from "@/lib/physics";
import {
  DEFAULT_MARKER,
  SOURCE_B_OFF_MESSAGE,
  TANK,
  TANK_DEFAULTS,
  classifyPoint,
  countExtrema,
  distance,
  messageFor,
  sourcePositions,
  wavelength,
  type ExtremaCount,
  type FringeKind,
  type InterferenceMessage,
} from "@/lib/interference";

export interface TankPoint {
  x: number;
  y: number;
}

/** Lề an toàn để kéo M không chạm hẳn mép khay. */
const MARGIN_CM = 0.3;

function clampToTank(point: TankPoint): TankPoint {
  return {
    x: Math.min(
      TANK.widthCm - MARGIN_CM,
      Math.max(MARGIN_CM, point.x)
    ),
    y: Math.min(
      TANK.heightCm - MARGIN_CM,
      Math.max(MARGIN_CM, point.y)
    ),
  };
}

export interface UseInterferenceTankReturn {
  f: number;
  v: number;
  AB: number;
  lambda: number;
  sourceBOn: boolean;
  marker: TankPoint;
  /** Vị trí A, B trong hệ toạ độ khay (cm), gốc ở góc trên trái. */
  sources: { a: TankPoint; b: TankPoint };
  d1: number;
  d2: number;
  counts: ExtremaCount;
  /** Phân loại M: cực đại / cực tiểu / ở giữa. */
  kind: FringeKind;
  /** Bậc k của vân gần nhất (0 khi đã tắt nguồn B). */
  order: number;
  message: InterferenceMessage;
  setF: (value: number) => void;
  setV: (value: number) => void;
  setAB: (value: number) => void;
  toggleSourceB: () => void;
  moveMarker: (point: TankPoint) => void;
  nudgeMarker: (dx: number, dy: number) => void;
  reset: () => void;
}

export function useInterferenceTank(): UseInterferenceTankReturn {
  const [f, setFState] = useState<number>(TANK_DEFAULTS.f);
  const [v, setVState] = useState<number>(TANK_DEFAULTS.v);
  const [AB, setABState] = useState<number>(TANK_DEFAULTS.AB);
  const [sourceBOn, setSourceBOn] = useState(true);
  const [marker, setMarker] = useState<TankPoint>(DEFAULT_MARKER);

  const lambda = wavelength(f, v);
  const sources = useMemo(() => sourcePositions(AB), [AB]);
  const counts = useMemo(() => countExtrema(AB, lambda), [AB, lambda]);
  const d1 = distance(marker.x, marker.y, sources.a.x, sources.a.y);
  const d2 = distance(marker.x, marker.y, sources.b.x, sources.b.y);

  // Bật nguồn B: phân loại theo hiệu đường đi. Tắt B: không còn giao thoa để
  // phân loại nữa, nên dùng thẳng câu của thí nghiệm "bịt một loa".
  const { kind, order, message } = useMemo(() => {
    if (!sourceBOn) {
      return { kind: "mid" as FringeKind, order: 0, message: SOURCE_B_OFF_MESSAGE };
    }
    const classification = classifyPoint(d1, d2, lambda);
    return {
      kind: classification.kind,
      order: classification.order,
      message: messageFor(d1, d2, lambda, formatNumber),
    };
  }, [sourceBOn, d1, d2, lambda]);

  const setF = useCallback((value: number) => setFState(value), []);
  const setV = useCallback((value: number) => setVState(value), []);
  const setAB = useCallback((value: number) => setABState(value), []);
  const toggleSourceB = useCallback(() => setSourceBOn((on) => !on), []);

  const moveMarker = useCallback((point: TankPoint) => {
    setMarker(clampToTank(point));
  }, []);

  const nudgeMarker = useCallback((dx: number, dy: number) => {
    setMarker((current) => clampToTank({ x: current.x + dx, y: current.y + dy }));
  }, []);

  const reset = useCallback(() => {
    setFState(TANK_DEFAULTS.f);
    setVState(TANK_DEFAULTS.v);
    setABState(TANK_DEFAULTS.AB);
    setSourceBOn(true);
    setMarker(DEFAULT_MARKER);
  }, []);

  return {
    f,
    v,
    AB,
    lambda,
    sourceBOn,
    marker,
    sources,
    d1,
    d2,
    counts,
    kind,
    order,
    message,
    setF,
    setV,
    setAB,
    toggleSourceB,
    moveMarker,
    nudgeMarker,
    reset,
  };
}
