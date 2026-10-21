"use client";

import type { StageState } from "@/services/review-session";

/** 125 → "2:05". */
export function clock(sec: number): string {
  const s = Math.max(0, Math.ceil(sec));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** Nhãn có biểu tượng chữ, không chỉ dựa vào màu (M4). */
export const STATE_META: Record<StageState, { label: string; mark: string; cls: string }> = {
  passed: { label: "Đạt", mark: "✓", cls: "bg-surface-2 text-ok" },
  failed: { label: "Chưa đạt", mark: "↻", cls: "bg-surface-2 text-warn" },
  doing: { label: "Đang làm", mark: "●", cls: "bg-primary-soft text-primary" },
  idle: { label: "Chưa mở", mark: "○", cls: "bg-surface-2 text-muted" },
};

export function StatePill({ state }: { state: StageState }) {
  const m = STATE_META[state];
  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-bold ${m.cls}`}>
      <span aria-hidden>{m.mark}</span>
      {m.label}
    </span>
  );
}

/** Thanh tiến độ mảnh; `value`/`max` bằng nhau là đầy. */
export function Bar({ value, max, tone = "primary" }: { value: number; max: number; tone?: "primary" | "ok" }) {
  const pct = max > 0 ? Math.min(100, Math.round((value / max) * 100)) : 0;
  return (
    <div className="h-2.5 w-full overflow-hidden rounded-full bg-surface-2" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
      <div className={`h-full rounded-full ${tone === "ok" ? "bg-ok" : "bg-primary"}`} style={{ width: `${pct}%`, transition: "width 300ms ease" }} />
    </div>
  );
}

/** Lệch giữa đồng hồ máy chủ và máy này, để đếm ngược không phụ thuộc đồng hồ điện thoại. */
export function clockSkewMs(serverNowIso: string): number {
  const t = Date.parse(serverNowIso);
  return Number.isFinite(t) ? t - Date.now() : 0;
}
