"use client";

/**
 * Họ hình `vong_tron` (đợt Đ1 3/11/2026, mẫu đầu: bài 4 Dao động điều hoà, dạng 4): vòng tròn pha + trục x, điểm M
 * quay ngược chiều kim đồng hồ, chiếu xuống trục; cung quét (xoắn ra ngoài khi quá một vòng); giao với đường x = x₀.
 * Góc tính theo đơn vị π rad. Hình không đổi cao giữa các bước (D2); nhãn trên hình (N8, H3); nét đứt cho đường đích (H4).
 *
 * JSON: { loai: "vong_tron", A, don_vi?, x_dich?: number[], lop: [[mục…] cho bước 1, …] }. Mục:
 *  diem {goc, ten, chieu?}  ·  cung {tu, den}  ·  giao {x, so: [nhãn điểm trên, nhãn điểm dưới]}  ·  ghi {text}
 *  Mục nào có `het: k` thì ẩn từ khi xong bước k.
 */

import { C_HL, C_MAX, C_MIN, Chevron, Label, dangHien, fmt, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { VongTronLop } from "@/features/lessons/types";

type Props = { A: number; don_vi?: string; x_dich?: number[]; lop?: VongTronLop[][]; layer: number };

const R = 4.2;
const P = (g: number, r = R) => [r * Math.cos(g * Math.PI), -r * Math.sin(g * Math.PI)] as const;

/** Cung từ góc tu → den (đơn vị π), ngược chiều kim đồng hồ; mỗi vòng bán kính tăng 0,3 để thấy số vòng. */
function cungPath(tu: number, den: number) {
  const n = Math.max(8, Math.ceil(Math.abs(den - tu) * 24));
  const pts: string[] = [];
  let end = { x: 0, y: 0, ang: 0 };
  for (let i = 0; i <= n; i++) {
    const g = tu + ((den - tu) * i) / n, r = R + 0.3 + (0.3 * (g - tu)) / 2;
    const [x, y] = P(g, r);
    pts.push(`${x.toFixed(3)} ${y.toFixed(3)}`);
    if (i === n) end = { x, y, ang: Math.atan2(-Math.cos(g * Math.PI), -Math.sin(g * Math.PI)) * (den >= tu ? 1 : -1) };
  }
  return { d: "M" + pts.join(" L"), end };
}

export default function VongTronPha({ A, don_vi = "cm", x_dich = [], lop, layer: L }: Props) {
  const items = dangHien(lop, L);
  const ghi = ghiMoiNhat(lop, L);
  const X = (x: number) => (x / A) * R;
  const top = -R - 1.6, bot = R + 4.2;
  return (
    <svg viewBox={`-10 ${top} 20 ${bot - top}`} className="cc-fig" role="img" aria-label={`Vòng tròn pha, biên độ ${fmt(A)} ${don_vi}`}>
      {/* trục x và vòng tròn */}
      <circle cx={0} cy={0} r={R} fill="none" stroke="currentColor" strokeWidth={0.08} opacity={0.7} />
      <line x1={-R - 1.4} y1={0} x2={R + 1.8} y2={0} stroke="currentColor" strokeWidth={0.07} />
      <Chevron x={R + 1.8} y={0} ang={0} len={0.45} w={0.07} />
      <Label x={R + 1.8} y={-0.45} size={1}>x</Label>
      {[-1, 1].map((s) => (
        <g key={s}>
          <line x1={s * R} y1={-0.2} x2={s * R} y2={0.2} stroke="currentColor" strokeWidth={0.07} />
          <Label x={s * R + s * 0.35} y={1.05} a={s < 0 ? "end" : "start"} size={0.95}>{fmt(s * A)}</Label>
        </g>
      ))}
      <circle cx={0} cy={0} r={0.12} fill="currentColor" />
      <Label x={-0.3} y={1.05} a="end" size={0.95}>O</Label>
      {/* đường đích theo đề */}
      {x_dich.map((x) => (
        <g key={x}>
          <line x1={X(x)} y1={-R - 0.6} x2={X(x)} y2={R + 0.6} stroke={C_MIN} strokeWidth={0.08} strokeDasharray="0.35 0.25" />
          <Label x={X(x) - 0.2} y={-0.35} a={x < 0 ? "end" : "start"} size={0.95} fill={C_MIN}>{`x = ${fmt(x)}`}</Label>
        </g>
      ))}
      {items.map((it, k) => {
        if (it.loai === "cung") {
          const { d, end } = cungPath(it.tu, it.den);
          return (
            <g key={k} className="cc-in">
              <path d={d} stroke={C_MAX} strokeWidth={0.13} fill="none" strokeLinecap="round" />
              <Chevron x={end.x} y={end.y} ang={end.ang} color={C_MAX} w={0.13} len={0.5} />
            </g>
          );
        }
        if (it.loai === "giao") {
          const g = Math.acos(Math.max(-1, Math.min(1, it.x / A))) / Math.PI;
          return (
            <g key={k} className="cc-in">
              {[g, -g].map((gg, j) => {
                const [x, y] = P(gg), [lx, ly] = P(gg, R + 1.25);
                return (
                  <g key={j}>
                    <circle cx={x} cy={y} r={0.26} fill={C_MIN} className="cc-pop" style={{ animationDelay: `${j * 120}ms` }} />
                    {it.so?.[j] && (
                      <Label x={lx} y={ly + 0.4} a={x < -0.3 ? "end" : x > 0.3 ? "start" : "middle"} size={1} fill={C_MIN}>
                        {it.so[j]}
                      </Label>
                    )}
                  </g>
                );
              })}
            </g>
          );
        }
        return null;
      })}
      {items.map((it, k) => {
        if (it.loai !== "diem") return null;
        const [x, y] = P(it.goc), [lx, ly] = P(it.goc, R + 1.25), vx = -Math.sin(it.goc * Math.PI);
        const arc = it.chieu ? cungArrow(it.goc) : null;
        return (
          <g key={`d${k}`} className="cc-in">
            <line x1={x} y1={y} x2={x} y2={0} stroke="currentColor" strokeWidth={0.06} strokeDasharray="0.25 0.2" opacity={0.8} />
            <circle cx={x} cy={0} r={0.18} fill={C_HL} stroke="currentColor" strokeWidth={0.05} />
            {it.chieu && Math.abs(vx) > 0.05 && (
              <g>
                <line x1={x} y1={0} x2={x + Math.sign(vx) * 1.5} y2={0} stroke={C_MAX} strokeWidth={0.16} />
                <Chevron x={x + Math.sign(vx) * 1.5} y={0} ang={vx < 0 ? Math.PI : 0} color={C_MAX} w={0.14} len={0.45} />
              </g>
            )}
            {arc && (
              <g>
                <path d={arc.d} stroke="currentColor" strokeWidth={0.08} fill="none" />
                <Chevron x={arc.end.x} y={arc.end.y} ang={arc.end.ang} w={0.08} len={0.4} />
              </g>
            )}
            <circle cx={x} cy={y} r={0.3} fill={C_HL} stroke="currentColor" strokeWidth={0.07} />
            {it.ten && (
              <Label x={lx} y={ly + 0.4} a={x < -0.3 ? "end" : x > 0.3 ? "start" : "middle"}>
                {it.ten}
              </Label>
            )}
          </g>
        );
      })}
      {/* dải ghi dưới hình: luôn giữ chỗ */}
      {ghi.map((t, i) => (
        <Label key={`${L}-${i}`} x={0} y={R + 2.4 + i * 1.35} size={1.02}>
          {t}
        </Label>
      ))}
    </svg>
  );
}

/** Mũi tên cong nhỏ chỉ chiều quay (ngược kim đồng hồ) ngay sau điểm. */
function cungArrow(g: number) {
  const pts: string[] = [];
  let end = { x: 0, y: 0, ang: 0 };
  for (let i = 0; i <= 8; i++) {
    const gg = g + 0.04 + (0.16 * i) / 8;
    const [x, y] = P(gg, R + 0.55);
    pts.push(`${x.toFixed(3)} ${y.toFixed(3)}`);
    if (i === 8) end = { x, y, ang: Math.atan2(-Math.cos(gg * Math.PI), -Math.sin(gg * Math.PI)) };
  }
  return { d: "M" + pts.join(" L"), end };
}
