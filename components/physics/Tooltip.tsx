/**
 * components/physics/Tooltip.tsx
 *
 * Tooltip nổi, dùng lại cho cả vật nặng (vị trí/vận tốc/gia tốc) và
 * đồ thị (t, x, v). Vị trí được truyền vào bằng toạ độ pixel tương đối
 * so với container cha (container cha cần position: relative).
 */

import type { ReactNode } from "react";

export interface TooltipRow {
  label: string;
  value: string;
  unit?: string;
}

export interface TooltipProps {
  x: number; // vị trí pixel, trục ngang, tương đối với container cha
  y: number; // vị trí pixel, trục dọc, tương đối với container cha
  visible: boolean;
  rows: TooltipRow[];
  title?: ReactNode;
}

export function Tooltip({ x, y, visible, rows, title }: TooltipProps) {
  if (!visible) return null;

  return (
    <div
      className="pointer-events-none absolute z-20 -translate-x-1/2 -translate-y-[calc(100%+10px)] rounded-lg border border-white/10 bg-[#0B1220]/95 px-3 py-2 text-xs shadow-lg shadow-black/40 backdrop-blur-sm transition-opacity duration-100"
      style={{ left: x, top: y }}
      role="tooltip"
    >
      {title ? (
        <div className="mb-1 font-medium text-slate-300">{title}</div>
      ) : null}
      <dl className="space-y-0.5">
        {rows.map((row) => (
          <div key={row.label} className="flex items-center gap-3 whitespace-nowrap">
            <dt className="text-slate-400">{row.label}</dt>
            <dd className="ml-auto font-mono tabular-nums text-slate-100">
              {row.value}
              {row.unit ? <span className="ml-0.5 text-slate-400">{row.unit}</span> : null}
            </dd>
          </div>
        ))}
      </dl>
      {/* mũi tên nhỏ trỏ xuống điểm đang hover */}
      <div className="absolute left-1/2 top-full h-2 w-2 -translate-x-1/2 -translate-y-1/2 rotate-45 border-b border-r border-white/10 bg-[#0B1220]" />
    </div>
  );
}
