"use client";

/**
 * Họ hình `van_giao_thoa` (đợt Đ1 3/11/2026, mẫu đầu: bài 12 Giao thoa sóng, dạng 4 — khe Young): màn quan sát nhìn
 * thẳng, vân trung tâm O, các điểm M, N theo đề (mm); thước khoảng vân i; hệ vân sáng hiện sau khi em đã xét xong
 * (không lộ đáp số); sơ đồ "n vân sáng liên tiếp dài L" ở dải dưới, khác tỉ lệ với màn để không đếm được i từ hình.
 *
 * JSON: { loai: "van_giao_thoa", i, x_min, x_max, diem: [{x, ten}], nhom?: {n, L}, lop: [[mục…], …] }. Mục:
 *  dem (đánh số khoảng giữa các vân của sơ đồ) · thuoc_i (vạch k·i trên trục) · van (vẽ hệ vân sáng trên màn)
 *  · thuoc {tu, den, nhan} (ngoặc dưới trục) · ghi {text}. `het: k` = ẩn từ khi xong bước k.
 */

import { C_HL, C_MAX, Label, dangHien, fmt, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { VanGiaoThoaLop } from "@/features/lessons/types";

type Props = {
  i: number;
  x_min: number;
  x_max: number;
  diem?: { x: number; ten: string }[];
  nhom?: { n: number; L: number };
  lop?: VanGiaoThoaLop[][];
  layer: number;
};

const BRIGHT = "#fbbf24", SCREEN = "#1e293b";

export default function VanGiaoThoa({ i, x_min, x_max, diem = [], nhom, lop, layer: L }: Props) {
  const items = dangHien(lop, L);
  const ghi = ghiMoiNhat(lop, L);
  const has = (k: string) => items.some((x) => x.loai === k);
  const X = (x: number) => 0.5 + ((x - x_min) / (x_max - x_min)) * 18;
  const sy0 = -5.2, sy1 = -3.2, ay = -2.5; // dải màn, trục
  const ks: number[] = [];
  for (let k = Math.ceil(x_min / i - 1e-9); k <= Math.floor(x_max / i + 1e-9); k++) ks.push(k);
  const top = -8.2, bot = 7.4;
  const gap = 1.45; // khoảng giữa hai vân của sơ đồ (đơn vị hình, cố ý khác tỉ lệ màn)

  return (
    <svg viewBox={`-0.6 ${top} 19.8 ${bot - top}`} className="cc-fig" role="img" aria-label="Màn quan sát vân giao thoa">
      {/* màn */}
      <rect x={0.2} y={sy0} width={18.6} height={sy1 - sy0} rx={0.2} fill={SCREEN} stroke="currentColor" strokeWidth={0.05} />
      {has("van") &&
        ks.map((k) => (
          <rect
            key={k}
            x={X(k * i) - 0.2 * i * (18 / (x_max - x_min))}
            y={sy0 + 0.1}
            width={0.4 * i * (18 / (x_max - x_min))}
            height={sy1 - sy0 - 0.2}
            rx={0.15}
            fill={BRIGHT}
            opacity={k === 0 ? 1 : 0.85}
            className="cc-pop"
            style={{ animationDelay: `${Math.abs(k) * 50}ms` }}
          />
        ))}
      {!has("van") && <rect x={X(0) - 0.25} y={sy0 + 0.1} width={0.5} height={sy1 - sy0 - 0.2} rx={0.15} fill={BRIGHT} />}
      {/* trục x trên màn */}
      <line x1={0.2} y1={ay} x2={18.8} y2={ay} stroke="currentColor" strokeWidth={0.06} />
      <line x1={X(0)} y1={sy1} x2={X(0)} y2={ay + 0.25} stroke="currentColor" strokeWidth={0.06} />
      <Label x={X(0)} y={-6.0} size={1}>O</Label>
      {has("thuoc_i") &&
        ks.map((k) => (
          <g key={k} className="cc-in">
            <line x1={X(k * i)} y1={ay - 0.2} x2={X(k * i)} y2={ay + 0.2} stroke={C_MAX} strokeWidth={0.07} />
            <text x={X(k * i)} y={ay + 1.15} fontSize={0.85} textAnchor="middle" fill={C_MAX} fontWeight={600}>
              {k === 0 ? "0" : k === 1 ? "i" : k === -1 ? "−i" : `${k < 0 ? "−" : ""}${Math.abs(k)}i`}
            </text>
          </g>
        ))}
      {diem.map((d) => (
        <g key={d.ten}>
          <line x1={X(d.x)} y1={sy0 - 0.3} x2={X(d.x)} y2={ay + 0.3} stroke={C_HL} strokeWidth={0.12} />
          <circle cx={X(d.x)} cy={ay} r={0.22} fill={C_HL} stroke="currentColor" strokeWidth={0.05} />
          <Label x={X(d.x)} y={-6.9}>{d.ten}</Label>
          <Label x={X(d.x)} y={-5.65} size={0.9}>{`${fmt(d.x, 2)} mm`}</Label>
        </g>
      ))}
      {items.map((it, k) =>
        it.loai === "thuoc" ? (
          <g key={k} className="cc-in">
            <path d={`M${X(it.tu)} ${ay + 1.5} v0.3 H${X(it.den)} v-0.3`} stroke={C_MAX} strokeWidth={0.08} fill="none" />
            <Label x={(X(it.tu) + X(it.den)) / 2} y={ay + 2.85} size={0.95} fill={C_MAX}>
              {it.nhan}
            </Label>
          </g>
        ) : null,
      )}
      {/* sơ đồ n vân sáng liên tiếp (dữ kiện đề) */}
      {nhom && (
        <g>
          <rect x={0.2} y={0.7} width={(nhom.n - 1) * gap + 1} height={1.3} rx={0.15} fill={SCREEN} />
          {Array.from({ length: nhom.n }, (_, j) => (
            <rect key={j} x={0.7 + j * gap - 0.18} y={0.8} width={0.36} height={1.1} rx={0.1} fill={BRIGHT} />
          ))}
          {has("dem") &&
            Array.from({ length: nhom.n - 1 }, (_, j) => (
              <text key={j} x={0.7 + (j + 0.5) * gap} y={0.45} fontSize={0.8} textAnchor="middle" fill={C_MAX} fontWeight={700} className="cc-pop" style={{ animationDelay: `${j * 90}ms` }}>
                {j + 1}
              </text>
            ))}
          <path d={`M0.7 2.3 v0.3 H${0.7 + (nhom.n - 1) * gap} v-0.3`} stroke="currentColor" strokeWidth={0.07} fill="none" />
          <Label x={0.7 + (nhom.n - 1) * gap + 0.6} y={1.2} a="start" size={0.95}>{`${nhom.n} vân sáng`}</Label>
          <Label x={0.7 + (nhom.n - 1) * gap + 0.6} y={2.4} a="start" size={0.95}>liên tiếp</Label>
          <Label x={0.7 + ((nhom.n - 1) * gap) / 2} y={3.6} size={0.95}>{`${fmt(nhom.L, 2)} mm`}</Label>
        </g>
      )}
      {ghi.map((t, j) => (
        <Label key={`${L}-${j}`} x={9.3} y={5.1 + j * 1.3} size={1}>
          {t}
        </Label>
      ))}
    </svg>
  );
}
