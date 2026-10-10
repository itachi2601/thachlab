"use client";

import { useEffect, useRef, useState } from "react";

/** Bốn màu + chữ cái cho 4 đáp án (có chữ nên không phụ thuộc riêng vào màu — M4). */
export const OPTION_STYLE = [
  { letter: "A", bg: "bg-rose-600", ring: "ring-rose-300", bar: "bg-rose-500" },
  { letter: "B", bg: "bg-blue-600", ring: "ring-blue-300", bar: "bg-blue-500" },
  { letter: "C", bg: "bg-amber-700", ring: "ring-amber-300", bar: "bg-amber-500" },
  { letter: "D", bg: "bg-emerald-600", ring: "ring-emerald-300", bar: "bg-emerald-500" },
] as const;

/**
 * Đếm ngược cục bộ từ `seconds_left` của lần đọc gần nhất (máy chủ là đồng hồ thật; đây chỉ để hiển thị mượt).
 * `stamp` = thời điểm (ms) nhận được lần đọc đó.
 */
export function useCountdown(secondsLeft: number, stamp: number, active: boolean): number {
  const [now, setNow] = useState(0);
  useEffect(() => {
    if (!active) return;
    const t = setInterval(() => setNow(Date.now()), 250);
    return () => clearInterval(t);
  }, [active]);
  return Math.max(0, secondsLeft - (Math.max(now, stamp) - stamp) / 1000);
}

/** Vòng lặp đọc trạng thái định kỳ; lỗi mạng tạm thời không làm vỡ màn hình (thử lại ở nhịp sau). */
export function usePoll<T>(
  fetcher: () => Promise<T>,
  intervalMs: (last: T | null) => number,
  onData: (d: T) => void,
  enabled = true,
): { refresh: () => void; error: string | null } {
  const [error, setError] = useState<string | null>(null);
  const fetcherRef = useRef(fetcher);
  const intervalRef = useRef(intervalMs);
  const onDataRef = useRef(onData);
  const kick = useRef<() => void>(() => {});
  useEffect(() => {
    fetcherRef.current = fetcher;
    intervalRef.current = intervalMs;
    onDataRef.current = onData;
  });
  useEffect(() => {
    if (!enabled) return;
    let stop = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let last: T | null = null;
    const run = async () => {
      clearTimeout(timer);
      try {
        const d = await fetcherRef.current();
        if (stop) return;
        last = d;
        setError(null);
        onDataRef.current(d);
      } catch (e) {
        if (!stop) setError(e instanceof Error ? e.message : String(e));
      }
      if (!stop) timer = setTimeout(run, document.hidden ? 4000 : intervalRef.current(last));
    };
    kick.current = () => void run();
    void run();
    return () => {
      stop = true;
      clearTimeout(timer);
    };
  }, [enabled]);
  return { refresh: () => kick.current(), error };
}

export function TimerBar({ left, total }: { left: number; total: number }) {
  const pct = total > 0 ? Math.min(100, (left / total) * 100) : 0;
  return (
    <div className="flex items-center gap-3" role="timer" aria-label={`Còn ${Math.ceil(left)} giây`}>
      <div className="h-3 flex-1 overflow-hidden rounded-full bg-surface-2">
        <div
          className={`h-3 rounded-full ${left <= 5 ? "bg-red-500" : "bg-primary"}`}
          style={{ width: `${pct}%`, transition: "width 250ms linear" }}
        />
      </div>
      <span className="w-10 text-right font-mono text-xl font-bold tabular-nums text-ink">{Math.ceil(left)}</span>
    </div>
  );
}
