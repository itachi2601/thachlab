/**
 * components/physics/DisplacementChart.tsx
 *
 * Đồ thị x theo t, vẽ bằng SVG thuần (không Chart.js). Cuộn theo thời gian
 * thực kiểu oscilloscope: luôn hiển thị vài chu kỳ gần nhất, chấm vàng đứng
 * yên ở mép phải đại diện cho "hiện tại" — đồng bộ tuyệt đối với vật nặng vì
 * cùng đọc từ state `t` do useHarmonicMotion cấp.
 */

import { useMemo, useState } from "react";
import {
  AMPLITUDE_RANGE,
  positionAt,
  velocityAt,
  sampleWindow,
  formatNumber,
} from "@/lib/physics";
import { Tooltip } from "./Tooltip";

export interface DisplacementChartProps {
  t: number;
  amplitude: number;
  frequency: number;
}

const VIEW_W = 400;
const VIEW_H = 190;
const MARGIN = { top: 12, right: 14, bottom: 20, left: 34 };
const PLOT_W = VIEW_W - MARGIN.left - MARGIN.right;
const PLOT_H = VIEW_H - MARGIN.top - MARGIN.bottom;
const Y_MAX = AMPLITUDE_RANGE.max; // trục y cố định theo biên độ tối đa cho phép

export function DisplacementChart({ t, amplitude, frequency }: DisplacementChartProps) {
  const [hover, setHover] = useState<{ vx: number; vy: number; s: number } | null>(null);

  // Cửa sổ thời gian hiển thị: luôn thấy khoảng 4 chu kỳ, giới hạn 1.5s - 6s
  // để không quá dày (f lớn) hay quá thưa (f nhỏ).
  const windowDuration = Math.min(6, Math.max(1.5, 4 / frequency));

  const points = useMemo(
    () => sampleWindow(t, amplitude, frequency, windowDuration, 200),
    [t, amplitude, frequency, windowDuration]
  );

  const toPx = (s: number) => MARGIN.left + ((s - (t - windowDuration)) / windowDuration) * PLOT_W;
  const toPy = (x: number) => MARGIN.top + PLOT_H / 2 - (x / Y_MAX) * (PLOT_H / 2);

  const linePath = points
    .map((p, i) => `${i === 0 ? "M" : "L"}${toPx(p.t).toFixed(2)},${toPy(p.x).toFixed(2)}`)
    .join(" ");

  const currentX = positionAt(t, amplitude, frequency);
  const dotPx = toPx(t);
  const dotPy = toPy(currentX);

  const yTicks = [-Y_MAX, -Y_MAX / 2, 0, Y_MAX / 2, Y_MAX];

  return (
    <div className="relative h-full w-full">
      <svg
        viewBox={`0 0 ${VIEW_W} ${VIEW_H}`}
        className="h-full w-full"
        role="img"
        aria-label="Đồ thị li độ x theo thời gian t"
      >
        {/* Lưới ngang theo các mốc biên độ */}
        {yTicks.map((yt) => (
          <g key={yt}>
            <line
              x1={MARGIN.left}
              x2={VIEW_W - MARGIN.right}
              y1={toPy(yt)}
              y2={toPy(yt)}
              stroke="#1E293B"
              strokeWidth={1}
            />
            <text x={4} y={toPy(yt) + 3} fontSize={8} fill="#64748B">
              {yt === 0 ? "0" : formatNumber(yt, 2)}
            </text>
          </g>
        ))}

        {/* Trục t */}
        <line
          x1={MARGIN.left}
          x2={VIEW_W - MARGIN.right}
          y1={VIEW_H - MARGIN.bottom}
          y2={VIEW_H - MARGIN.bottom}
          stroke="#334155"
          strokeWidth={1.2}
        />
        <text x={VIEW_W - MARGIN.right - 10} y={VIEW_H - 4} fontSize={9} fill="#64748B">
          t (s)
        </text>
        <text x={4} y={12} fontSize={9} fill="#64748B">
          x (m)
        </text>

        {/* Đường hình sin */}
        <path d={linePath} fill="none" stroke="#2563EB" strokeWidth={2} strokeLinejoin="round" />

        {/* Vùng bắt hover rộng hơn, trong suốt, phủ lên đường sin */}
        <path
          d={linePath}
          fill="none"
          stroke="transparent"
          strokeWidth={16}
          onMouseMove={(e) => {
            const svg = e.currentTarget.ownerSVGElement as SVGSVGElement;
            const rect = svg.getBoundingClientRect();
            const localX = ((e.clientX - rect.left) / rect.width) * VIEW_W;
            const s = t - windowDuration + ((localX - MARGIN.left) / PLOT_W) * windowDuration;
            setHover({
              vx: rect.width * (localX / VIEW_W),
              vy: rect.height * (toPy(positionAt(s, amplitude, frequency)) / VIEW_H),
              s,
            });
          }}
          onMouseLeave={() => setHover(null)}
          className="cursor-crosshair"
        />

        {/* Chấm vàng — hiện tại, luôn đồng bộ với vật nặng */}
        <circle cx={dotPx} cy={dotPy} r={5} fill="#FACC15" stroke="#0F172A" strokeWidth={1.5} />
        <circle cx={dotPx} cy={dotPy} r={9} fill="#FACC15" opacity={0.18} />
      </svg>

      <Tooltip
        visible={hover !== null}
        x={hover?.vx ?? 0}
        y={hover?.vy ?? 0}
        rows={
          hover
            ? [
                { label: "t", value: formatNumber(hover.s, 2), unit: "s" },
                { label: "x", value: formatNumber(positionAt(hover.s, amplitude, frequency), 3), unit: "m" },
                { label: "v", value: formatNumber(velocityAt(hover.s, amplitude, frequency), 3), unit: "m/s" },
              ]
            : []
        }
      />
    </div>
  );
}
