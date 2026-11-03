/**
 * Phần dùng chung cho các hình "giải cùng hình" (đợt Đ1 3/11/2026): nhãn có viền halo, chữ có chỉ số dưới, mũi tên
 * chevron 30°, dải ghi chú dưới hình. Dữ liệu từng bước (`lop`) do JSON khai: lop[i] vẽ khi em đã xong bước i + 1.
 */

import type { ReactNode } from "react";

export const C_MAX = "#c2410c", C_MIN = "#0e7490", C_HL = "#facc15";

export const fmt = (x: number, dp = 1) => {
  const s = x.toFixed(dp).replace(/\.?0+$/, "");
  return (s === "-0" ? "0" : s).replace(".", ",");
};

/** "u_M", "d_{12}" → chỉ số dưới bằng tspan (SVG không có KaTeX). */
export function Txt({ s }: { s: string }) {
  const parts = s.split(/(_\{[^}]+\}|_[^\s{])/);
  return (
    <>
      {parts.map((p, i) =>
        p.startsWith("_") ? (
          <tspan key={i} baselineShift="sub" fontSize="72%">
            {p.length > 2 && p[1] === "{" ? p.slice(2, -1) : p.slice(1)}
          </tspan>
        ) : (
          p
        ),
      )}
    </>
  );
}

export function Label({
  x,
  y,
  children,
  fill = "currentColor",
  a = "middle",
  size = 1.2,
}: {
  x: number;
  y: number;
  children: ReactNode;
  fill?: string;
  a?: "start" | "middle" | "end";
  size?: number;
}) {
  return (
    <text x={x} y={y} fontSize={size} textAnchor={a} fill={fill} fontWeight={600} stroke="var(--cc-halo)" strokeWidth={size * 0.23} paintOrder="stroke">
      {typeof children === "string" ? <Txt s={children} /> : children}
    </text>
  );
}

/** Đầu mũi tên chevron 30° tại (x, y), hướng theo góc `ang` (rad, toạ độ SVG). */
export function Chevron({ x, y, ang, len = 0.5, color = "currentColor", w = 0.1 }: { x: number; y: number; ang: number; len?: number; color?: string; w?: number }) {
  const a1 = ang + Math.PI - Math.PI / 6, a2 = ang + Math.PI + Math.PI / 6;
  return (
    <path
      d={`M${x + len * Math.cos(a1)} ${y + len * Math.sin(a1)} L${x} ${y} L${x + len * Math.cos(a2)} ${y + len * Math.sin(a2)}`}
      stroke={color}
      strokeWidth={w}
      fill="none"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  );
}

/** Mục của bước: `het` = ẩn từ khi xong bước thứ `het` (nhường chỗ). */
export type LopChung = { het?: number };

/** Các mục đang hiện: lop[i] hiện khi L ≥ i + 1 và (không có het hoặc L < het). */
export function dangHien<T extends LopChung>(lop: T[][] | undefined, L: number): T[] {
  const out: T[] = [];
  (lop ?? []).forEach((items, i) => {
    if (L >= i + 1) for (const it of items) if (it.het == null || L < it.het) out.push(it);
  });
  return out;
}

/** Ghi chú của bước gần nhất có ghi (tối đa 2 dòng) — dải dưới hình luôn giữ chỗ để hình không đổi cao (D2). */
export function ghiMoiNhat(lop: ({ loai: string; text?: string } & LopChung)[][] | undefined, L: number): string[] {
  for (let i = Math.min(L, lop?.length ?? 0) - 1; i >= 0; i--) {
    const g = (lop![i] ?? []).filter((x) => x.loai === "ghi" && x.text).map((x) => x.text!);
    if (g.length) return g.slice(0, 2);
  }
  return [];
}
