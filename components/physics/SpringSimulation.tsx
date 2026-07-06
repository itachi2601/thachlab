/**
 * components/physics/SpringSimulation.tsx
 *
 * Mô phỏng con lắc lò xo treo thẳng đứng bằng SVG thuần (không ảnh, không
 * GIF, không Lottie). Lò xo co giãn thật theo chiều dài tính từ x(t), vẽ
 * lại mỗi khung hình bằng dữ liệu do useHarmonicMotion cung cấp — không hề
 * dùng CSS @keyframes.
 *
 * Quy ước trục: x dương hướng lên (vật đi lên khi x > 0, lò xo ngắn lại).
 */

import { useId, useMemo, useState } from "react";
import { formatNumber } from "@/lib/physics";
import { Tooltip } from "./Tooltip";

export interface SpringSimulationProps {
  x: number; // vị trí hiện tại (m)
  v: number; // vận tốc hiện tại (m/s)
  a: number; // gia tốc hiện tại (m/s²)
  amplitude: number; // biên độ (m), dùng để vẽ giới hạn trên trục Ox
}

// --- Hằng số hình học của SVG (đơn vị viewBox, không phải px màn hình) ---
const VIEW_W = 260;
const VIEW_H = 320;
const ANCHOR = { x: 118, y: 34 }; // điểm treo lò xo vào giá
const REST_LENGTH = 132; // chiều dài lò xo khi ở vị trí cân bằng
const PX_PER_METER = 320; // hệ số quy đổi mét sang đơn vị viewBox
const COILS = 9; // số vòng xoắn hiển thị
const COIL_WIDTH = 13; // biên độ ngang của mỗi vòng xoắn
const MASS_SIZE = 42;

function buildSpringPath(length: number): string {
  // Vẽ lò xo dạng zig-zag từ điểm treo xuống điểm nối với vật nặng.
  // Đoạn đầu/cuối để thẳng một chút cho giống móc treo thật.
  const straight = 10;
  const zigLength = Math.max(length - straight * 2, 10);
  const segments = COILS * 2;
  const points: [number, number][] = [[ANCHOR.x, ANCHOR.y]];
  points.push([ANCHOR.x, ANCHOR.y + straight]);

  for (let i = 1; i <= segments; i++) {
    const yy = ANCHOR.y + straight + (zigLength * i) / segments;
    const dir = i % 2 === 0 ? 1 : -1;
    const xx = ANCHOR.x + dir * COIL_WIDTH;
    points.push([xx, yy]);
  }

  points.push([ANCHOR.x, ANCHOR.y + straight + zigLength]);
  points.push([ANCHOR.x, ANCHOR.y + length]);

  return points.map(([px, py], i) => `${i === 0 ? "M" : "L"}${px.toFixed(2)},${py.toFixed(2)}`).join(" ");
}

export function SpringSimulation({ x, v, a, amplitude }: SpringSimulationProps) {
  const gradientId = useId();
  const [hover, setHover] = useState<{ vx: number; vy: number } | null>(null);

  // x dương = đi lên => chiều dài lò xo giảm.
  const length = REST_LENGTH - x * PX_PER_METER;
  const massCenterY = ANCHOR.y + length;
  const equilibriumY = ANCHOR.y + REST_LENGTH;

  const springPath = useMemo(() => buildSpringPath(length), [length]);

  // Trục Ox đặt bên phải, đánh dấu +A / O / -A theo đúng biên độ hiện tại.
  const axisX = 208;
  const axisTopY = equilibriumY - amplitude * PX_PER_METER - 26;
  const axisBottomY = equilibriumY + amplitude * PX_PER_METER + 18;

  return (
    <div className="relative flex h-full items-center justify-center">
      <svg
        viewBox={`0 0 ${VIEW_W} ${VIEW_H}`}
        className="h-full w-full max-w-[260px]"
        role="img"
        aria-label="Mô phỏng con lắc lò xo dao động điều hòa"
      >
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#3B82F6" />
            <stop offset="100%" stopColor="#1D4ED8" />
          </linearGradient>
        </defs>

        {/* Giá treo */}
        <g>
          <rect x={70} y={16} width={96} height={10} rx={3} fill="#1E293B" stroke="#334155" />
          {/* vạch chéo mô tả bề mặt cố định */}
          {Array.from({ length: 7 }).map((_, i) => (
            <line
              key={i}
              x1={76 + i * 13}
              y1={26}
              x2={68 + i * 13}
              y2={16}
              stroke="#334155"
              strokeWidth={2}
            />
          ))}
        </g>

        {/* Vị trí cân bằng (đường đứt nét) */}
        <line
          x1={40}
          y1={equilibriumY}
          x2={220}
          y2={equilibriumY}
          stroke="#475569"
          strokeWidth={1}
          strokeDasharray="4 4"
        />
        <text x={40} y={equilibriumY - 6} fontSize={9} fill="#64748B">
          vị trí cân bằng
        </text>

        {/* Trục Ox thẳng đứng, chiều dương hướng lên */}
        <g>
          <line x1={axisX} y1={axisBottomY} x2={axisX} y2={axisTopY} stroke="#475569" strokeWidth={1.5} />
          <polygon
            points={`${axisX - 4},${axisTopY + 8} ${axisX + 4},${axisTopY + 8} ${axisX},${axisTopY}`}
            fill="#475569"
          />
          <text x={axisX + 8} y={axisTopY + 6} fontSize={11} fill="#94A3B8" fontStyle="italic">
            x
          </text>
          <text x={axisX + 8} y={equilibriumY + 3} fontSize={10} fill="#94A3B8">
            O
          </text>
          <line x1={axisX - 4} y1={equilibriumY} x2={axisX + 4} y2={equilibriumY} stroke="#94A3B8" strokeWidth={1.5} />
        </g>

        {/* Lò xo */}
        <path d={springPath} fill="none" stroke="#94A3B8" strokeWidth={2} strokeLinejoin="round" />

        {/* Vật nặng */}
        <g
          transform={`translate(${ANCHOR.x - MASS_SIZE / 2}, ${massCenterY - MASS_SIZE / 2})`}
          onMouseEnter={(e) => {
            const rect = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
            setHover({ vx: rect.width * (ANCHOR.x / VIEW_W), vy: rect.height * (massCenterY / VIEW_H) });
          }}
          onMouseMove={(e) => {
            const rect = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
            setHover({ vx: rect.width * (ANCHOR.x / VIEW_W), vy: rect.height * (massCenterY / VIEW_H) });
          }}
          onMouseLeave={() => setHover(null)}
          className="cursor-pointer"
        >
          <rect
            width={MASS_SIZE}
            height={MASS_SIZE}
            rx={8}
            fill={`url(#${gradientId})`}
            stroke="#60A5FA"
            strokeWidth={1}
          />
          <rect width={MASS_SIZE} height={MASS_SIZE} rx={8} fill="black" opacity={0.06} />
        </g>
      </svg>

      <Tooltip
        visible={hover !== null}
        x={hover?.vx ?? 0}
        y={hover?.vy ?? 0}
        title="Vật nặng"
        rows={[
          { label: "Vị trí x", value: formatNumber(x, 3), unit: "m" },
          { label: "Vận tốc v", value: formatNumber(v, 3), unit: "m/s" },
          { label: "Gia tốc a", value: formatNumber(a, 2), unit: "m/s²" },
        ]}
      />
    </div>
  );
}
