/**
 * hooks/useHarmonicMotion.ts
 *
 * Hook điều khiển vòng lặp requestAnimationFrame duy nhất cho toàn bộ Hero.
 * Đây là "nguồn sự thật" (single source of truth) về thời gian `t` — cả
 * SpringSimulation lẫn DisplacementChart đều đọc từ cùng một state này nên
 * luôn đồng bộ tuyệt đối, không có CSS animation nào chạy lệch pha.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import {
  AMPLITUDE_RANGE,
  FREQUENCY_RANGE,
  clamp,
  computeHarmonicState,
  type HarmonicState,
} from "@/lib/physics";

export interface UseHarmonicMotionOptions {
  initialAmplitude?: number; // mét
  initialFrequency?: number; // Hz
  autoPlay?: boolean;
}

export interface UseHarmonicMotionReturn extends HarmonicState {
  amplitude: number;
  frequency: number;
  isPlaying: boolean;
  setAmplitude: (value: number) => void;
  setFrequency: (value: number) => void;
  play: () => void;
  pause: () => void;
  toggle: () => void;
  reset: () => void;
}

export function useHarmonicMotion(
  options: UseHarmonicMotionOptions = {}
): UseHarmonicMotionReturn {
  const { initialAmplitude = 0.1, initialFrequency = 1, autoPlay = true } = options;

  const [amplitude, setAmplitudeState] = useState(initialAmplitude);
  const [frequency, setFrequencyState] = useState(initialFrequency);
  const [isPlaying, setIsPlaying] = useState(autoPlay);
  const [t, setT] = useState(0);

  // refs giữ giá trị mới nhất để vòng lặp rAF luôn đọc đúng mà không cần
  // huỷ/tạo lại listener mỗi khi state đổi (tránh giật khung hình).
  const amplitudeRef = useRef(amplitude);
  const frequencyRef = useRef(frequency);
  const isPlayingRef = useRef(isPlaying);
  const tRef = useRef(t);
  const rafId = useRef<number | null>(null);
  const lastTimestamp = useRef<number | null>(null);

  amplitudeRef.current = amplitude;
  frequencyRef.current = frequency;
  isPlayingRef.current = isPlaying;

  useEffect(() => {
    const loop = (timestamp: number) => {
      if (lastTimestamp.current === null) lastTimestamp.current = timestamp;
      const dt = (timestamp - lastTimestamp.current) / 1000; // giây
      lastTimestamp.current = timestamp;

      if (isPlayingRef.current) {
        tRef.current += dt;
        setT(tRef.current);
      }
      rafId.current = requestAnimationFrame(loop);
    };

    rafId.current = requestAnimationFrame(loop);
    return () => {
      if (rafId.current !== null) cancelAnimationFrame(rafId.current);
      lastTimestamp.current = null;
    };
  }, []);

  const setAmplitude = useCallback((value: number) => {
    setAmplitudeState(clamp(value, AMPLITUDE_RANGE.min, AMPLITUDE_RANGE.max));
  }, []);

  const setFrequency = useCallback((value: number) => {
    setFrequencyState(clamp(value, FREQUENCY_RANGE.min, FREQUENCY_RANGE.max));
  }, []);

  const play = useCallback(() => setIsPlaying(true), []);
  const pause = useCallback(() => setIsPlaying(false), []);
  const toggle = useCallback(() => setIsPlaying((p) => !p), []);
  const reset = useCallback(() => {
    tRef.current = 0;
    setT(0);
    setIsPlaying(true);
  }, []);

  const state = computeHarmonicState(t, { amplitude, frequency });

  return {
    ...state,
    amplitude,
    frequency,
    isPlaying,
    setAmplitude,
    setFrequency,
    play,
    pause,
    toggle,
    reset,
  };
}
