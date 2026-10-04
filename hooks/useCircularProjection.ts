/**
 * hooks/useCircularProjection.ts
 *
 * Nguồn sự thật duy nhất cho mô hình "hình chiếu đồng nhịp với con lắc lò xo":
 * cài đặt (m, A₂, ω bánh xe), trạng thái chạy (góc quay θ của M và pha φ của con
 * lắc, cả hai đều TÍCH LUỸ theo thời gian), số đo suy ra và câu nhận xét.
 *
 * Vì sao tích luỹ góc thay vì tính lại θ = ω·t mỗi khung hình: học sinh phải chỉnh
 * được ω của bánh xe NGAY TRONG LÚC CHẠY — đó chính là động tác khoá nhịp. Nếu
 * tính lại từ t thì vừa kéo thanh trượt, bóng đã nhảy sang vị trí khác và không
 * quan sát được gì. Tích luỹ θ += ω·dt giống đúng cái đĩa quay thật: đổi tốc độ
 * thì vị trí liền mạch, chỉ tốc độ đổi. Đổi m giữa chừng cũng vậy: ω_c = √(k/m)
 * đổi, còn φ thì liền mạch.
 *
 * Đổi A₂ thì KHÁC: biên độ là chỗ thả vật, không phải tham số đổi được giữa chừng
 * — đổi lúc đang chạy sẽ làm vật nặng nhảy vị trí. Nên giao diện khoá thanh trượt
 * A₂ trong lúc chạy (xem ShadowSpringSimulation), hook chỉ nhận giá trị đã có hiệu
 * lực từ đầu lượt.
 *
 * Vòng lặp requestAnimationFrame CHỈ chạy khi học sinh đã bấm "Chạy" VÀ mô phỏng
 * còn trong tầm mắt (B4; xem docs/prompt-toc-do-va-may-cu.md — chuyển tab đi thì
 * không được chạy nền). Trình duyệt ẩn tab thì rAF tự dừng, và dt được kẹp trần
 * 0,05 s nên quay lại không bị nhảy một bước khổng lồ.
 */

import { useCallback, useEffect, useMemo, useState } from "react";
import { formatNumber } from "@/lib/physics";
import {
  MASS_RANGE,
  PENDULUM_AMPLITUDE_RANGE,
  SHADOW_AMPLITUDE,
  SPRING_K,
  WHEEL_OMEGA_RANGE,
  alignedPhase,
  messageForProjection,
  omegaOfSpring,
  oscillationCount,
  periodOf,
  phaseDifferenceDeg,
  sameRhythm,
  turnsPerSecond,
  type ProjectionMessage,
} from "@/lib/circularProjection";

/** Trần dt mỗi khung hình (s) — xem ghi chú đầu file. */
const MAX_STEP_SECONDS = 0.05;

interface RunState {
  tRun: number;
  theta: number; // góc quay tích luỹ của M (rad)
  phi: number; // pha tích luỹ của con lắc (rad)
}

const IDLE_RUN: RunState = { tRun: 0, theta: 0, phi: 0 };

/** Làm tròn theo bước của thanh trượt, tránh 0.30000000000000004 trên nhãn số. */
function roundToStep(value: number, step: number): number {
  return Number((Math.round(value / step) * step).toFixed(4));
}

function clampTo(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

export interface UseCircularProjectionOptions {
  /** Mô phỏng còn trong tầm mắt không — false thì vòng lặp dừng (B4). */
  active: boolean;
}

export interface UseCircularProjectionReturn {
  // Cài đặt
  k: number;
  mass: number;
  pendulumAmplitude: number;
  wheelOmega: number;
  shadowAmplitude: number;
  // Trạng thái chạy
  playing: boolean;
  tRun: number;
  theta: number;
  phi: number;
  // Số đo suy ra
  xShadow: number;
  xPendulum: number;
  omegaSpring: number;
  periodShadow: number;
  periodPendulum: number;
  phaseDiffDeg: number;
  countShadow: number;
  countPendulum: number;
  synced: boolean;
  turns: number;
  showDots: boolean;
  message: ProjectionMessage;
  // Hành động
  setMass: (value: number) => void;
  setPendulumAmplitude: (value: number) => void;
  setWheelOmega: (value: number) => void;
  snapRhythm: () => void;
  toggle: () => void;
  reset: () => void;
  toggleDots: () => void;
}

export function useCircularProjection({
  active,
}: UseCircularProjectionOptions): UseCircularProjectionReturn {
  const [mass, setMassState] = useState<number>(MASS_RANGE.initial);
  const [pendulumAmplitude, setPendulumAmplitudeState] = useState<number>(
    PENDULUM_AMPLITUDE_RANGE.initial
  );
  const [wheelOmega, setWheelOmegaState] = useState<number>(WHEEL_OMEGA_RANGE.initial);
  const [playing, setPlaying] = useState(false);
  const [run, setRun] = useState<RunState>(IDLE_RUN);
  const [showDots, setShowDots] = useState(true);

  const omegaSpring = omegaOfSpring(SPRING_K, mass);
  const periodShadow = periodOf(wheelOmega);
  const periodPendulum = periodOf(omegaSpring);

  // Một khung hình = mỗi bên tiến pha theo ω của riêng nó. Đây là toàn bộ phần
  // "Vật lí" chạy theo thời gian của mô hình; mọi số đo khác đều suy ra lúc render.
  const stepPhase = useCallback(
    (dt: number) => {
      setRun((prev) => ({
        tRun: prev.tRun + dt,
        theta: prev.theta + wheelOmega * dt,
        phi: prev.phi + omegaSpring * dt,
      }));
    },
    [wheelOmega, omegaSpring]
  );

  // stepPhase đổi danh tính khi ω đổi → effect tự đăng ký lại vòng lặp, nên vòng
  // lặp luôn dùng đúng ω mới nhất mà không cần đọc ref lúc render (luật
  // react-hooks/refs cấm) — cùng cách useRescueDrop.ts đang làm.
  useEffect(() => {
    if (!playing || !active) return;
    let rafId = 0;
    let last: number | null = null;
    const step = (timestamp: number) => {
      if (last !== null) {
        stepPhase(Math.min(MAX_STEP_SECONDS, (timestamp - last) / 1000));
      }
      last = timestamp;
      rafId = requestAnimationFrame(step);
    };
    rafId = requestAnimationFrame(step);
    return () => cancelAnimationFrame(rafId);
  }, [playing, active, stepPhase]);

  const xShadow = SHADOW_AMPLITUDE * Math.cos(run.theta);
  const xPendulum = pendulumAmplitude * Math.cos(run.phi);
  const synced = sameRhythm(wheelOmega, omegaSpring);
  // Boolean (không phải số đo) để câu nhận xét chỉ đổi khi trạng thái ĐỔI, không đổi
  // theo từng khung hình — xem ghi chú aria-live ở messageForProjection.
  const aligned = alignedPhase(run.theta, run.phi);

  const message = useMemo(
    () =>
      messageForProjection(
        {
          playing,
          omegaWheel: wheelOmega,
          omegaSpring,
          shadowAmplitude: SHADOW_AMPLITUDE,
          pendulumAmplitude,
          aligned,
        },
        formatNumber
      ),
    [playing, wheelOmega, omegaSpring, pendulumAmplitude, aligned]
  );

  const setMass = useCallback((value: number) => {
    setMassState(roundToStep(clampTo(value, MASS_RANGE.min, MASS_RANGE.max), MASS_RANGE.step));
  }, []);

  const setPendulumAmplitude = useCallback((value: number) => {
    setPendulumAmplitudeState(
      roundToStep(
        clampTo(value, PENDULUM_AMPLITUDE_RANGE.min, PENDULUM_AMPLITUDE_RANGE.max),
        PENDULUM_AMPLITUDE_RANGE.step
      )
    );
  }, []);

  const setWheelOmega = useCallback((value: number) => {
    setWheelOmegaState(
      roundToStep(
        clampTo(value, WHEEL_OMEGA_RANGE.min, WHEEL_OMEGA_RANGE.max),
        WHEEL_OMEGA_RANGE.step
      )
    );
  }, []);

  // "Khớp nhịp": đặt ω bánh xe đúng bằng ω con lắc. Không phải cho sẵn đáp án —
  // câu hỏi chính của mô hình là BIÊN ĐỘ có đổi nhịp không; khớp ω chỉ là động tác
  // dựng hiện trường để làm thí nghiệm đó.
  const snapRhythm = useCallback(() => {
    setWheelOmegaState(
      roundToStep(
        clampTo(omegaSpring, WHEEL_OMEGA_RANGE.min, WHEEL_OMEGA_RANGE.max),
        WHEEL_OMEGA_RANGE.step
      )
    );
  }, [omegaSpring]);

  const toggle = useCallback(() => setPlaying((value) => !value), []);

  const reset = useCallback(() => {
    setRun(IDLE_RUN);
    setPlaying(false);
  }, []);

  const toggleDots = useCallback(() => setShowDots((value) => !value), []);

  return {
    k: SPRING_K,
    mass,
    pendulumAmplitude,
    wheelOmega,
    shadowAmplitude: SHADOW_AMPLITUDE,
    playing,
    tRun: run.tRun,
    theta: run.theta,
    phi: run.phi,
    xShadow,
    xPendulum,
    omegaSpring,
    periodShadow,
    periodPendulum,
    phaseDiffDeg: phaseDifferenceDeg(run.theta, run.phi),
    countShadow: oscillationCount(run.theta),
    countPendulum: oscillationCount(run.phi),
    synced,
    turns: turnsPerSecond(wheelOmega),
    showDots,
    message,
    setMass,
    setPendulumAmplitude,
    setWheelOmega,
    snapRhythm,
    toggle,
    reset,
    toggleDots,
  };
}
