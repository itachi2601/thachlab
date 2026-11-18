"use client";
import { useState } from "react";

export const parseNum = (s: string): number | null => {
  const t = s.trim().replace(",", ".");
  if (!t) return null;
  const n = Number(t);
  return Number.isFinite(n) && n >= 0 ? n : null;
};
export const vn = (n: number, d = 1) => (Math.round(n * 10 ** d) / 10 ** d).toLocaleString("vi-VN");
export const pad = (n: number) => String(n).padStart(2, "0");
export const fmtClock = (sec: number) => {
  const s = Math.max(0, Math.round(sec));
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
  return h ? `${h}:${pad(m)}:${pad(s % 60)}` : `${m}:${pad(s % 60)}`;
};
export const fmtDur = (min: number) => (min >= 60 ? `${Math.floor(min / 60)} giờ ${Math.round(min % 60)} phút` : `${Math.round(min)} phút`);
const WD = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"];
export const fmtDay = (iso: string) => {
  const d = new Date(iso.length <= 10 ? `${iso}T00:00:00` : iso);
  return `${WD[d.getDay()]} ${pad(d.getDate())}/${pad(d.getMonth() + 1)}`;
};
export const todayIso = () => {
  const d = new Date();
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
};
export const mondayOf = (d = new Date()) => {
  const x = new Date(d);
  x.setHours(0, 0, 0, 0);
  x.setDate(x.getDate() - ((x.getDay() + 6) % 7));
  return x;
};

/** Ô số: giữ chuỗi người gõ (cho phép "2," đang gõ dở), báo số khi hợp lệ. */
export function NumInput({
  value,
  onChange,
  placeholder,
  label,
  className = "",
}: {
  value: number | null;
  onChange: (n: number | null) => void;
  placeholder?: string;
  label: string;
  className?: string;
}) {
  const show = (v: number | null) => (v == null ? "" : String(v).replace(".", ","));
  const [text, setText] = useState(show(value));
  const [seen, setSeen] = useState(value);
  // giá trị đổi từ ngoài (tick tự điền, thay bài) → cập nhật chữ trong ô
  if (value !== seen) {
    setSeen(value);
    if (parseNum(text) !== value) setText(show(value));
  }
  return (
    <input
      inputMode="decimal"
      aria-label={label}
      value={text}
      placeholder={placeholder}
      onFocus={(e) => e.currentTarget.select()}
      onChange={(e) => {
        const t = e.target.value.replace(/[^0-9.,]/g, "");
        setText(t);
        onChange(parseNum(t));
      }}
      className={`h-11 w-full min-w-0 rounded-lg border border-line bg-surface-2 px-1 text-center text-base font-semibold tabular-nums text-ink placeholder:font-normal placeholder:text-slate-500 focus:border-primary focus:outline-none ${className}`}
    />
  );
}

/** Biểu đồ đường tối giản (SVG), tự co theo khung. */
export function LineChart({
  points,
  unit,
  target,
  height = 160,
}: {
  points: { x: string; y: number }[];
  unit: string;
  target?: { y: number; label: string };
  height?: number;
}) {
  if (points.length === 0) return null;
  const W = 340, H = height, L = 36, R = 10, T = 12, B = 22;
  const ys = points.map((p) => p.y).concat(target ? [target.y] : []);
  let lo = Math.min(...ys), hi = Math.max(...ys);
  if (hi - lo < 1) { lo -= 1; hi += 1; }
  const padY = (hi - lo) * 0.12;
  lo -= padY; hi += padY;
  const x = (i: number) => (points.length === 1 ? (L + W - R) / 2 : L + (i * (W - L - R)) / (points.length - 1));
  const y = (v: number) => T + ((hi - v) * (H - T - B)) / (hi - lo);
  const d = points.map((p, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${y(p.y).toFixed(1)}`).join(" ");
  const ticks = [lo + padY, (lo + hi) / 2, hi - padY];
  const labelIdx = points.length <= 4 ? points.map((_, i) => i) : [0, Math.floor((points.length - 1) / 2), points.length - 1];
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full" role="img" aria-label={`Biểu đồ ${unit}`}>
      {ticks.map((t, i) => (
        <g key={i}>
          <line x1={L} x2={W - R} y1={y(t)} y2={y(t)} stroke="currentColor" className="text-line" />
          <text x={L - 4} y={y(t) + 4} textAnchor="end" fontSize="10" className="fill-muted">{vn(t, 1)}</text>
        </g>
      ))}
      {target && (
        <g>
          <line x1={L} x2={W - R} y1={y(target.y)} y2={y(target.y)} strokeDasharray="4 4" stroke="currentColor" className="text-ok" />
          <text x={W - R} y={y(target.y) - 4} textAnchor="end" fontSize="10" className="fill-ok">{target.label}</text>
        </g>
      )}
      <path d={d} fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinejoin="round" className="text-primary" />
      {points.map((p, i) => (
        <circle key={i} cx={x(i)} cy={y(p.y)} r="3.5" fill="currentColor" className="text-primary">
          <title>{`${p.x}: ${vn(p.y)} ${unit}`}</title>
        </circle>
      ))}
      {labelIdx.map((i) => (
        <text key={i} x={x(i)} y={H - 6} textAnchor={i === 0 && points.length > 1 ? "start" : i === points.length - 1 && points.length > 1 ? "end" : "middle"} fontSize="10" className="fill-muted">
          {fmtDay(points[i].x).slice(3)}
        </text>
      ))}
    </svg>
  );
}

export function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={`rounded-2xl border border-line bg-panel p-4 ${className}`}>{children}</section>;
}
