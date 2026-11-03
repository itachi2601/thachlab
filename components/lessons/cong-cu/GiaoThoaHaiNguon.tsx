"use client";

/**
 * 🧪 Hình giải dạng giao thoa hai nguồn cùng pha (thử 2/11/2026, bài 14 Sóng dạng 3) — chỉ có nét, không chạy sóng
 * (thầy góp ý 2/11: hình nhỏ, đơn giản, dính nửa trên điện thoại khi em làm từng bước ở nửa dưới).
 *
 * `layer` = số bước đã xong: hình của bước i chỉ vẽ khi em đã làm xong bước đó (không lộ đáp số bước đang hỏi).
 * Thứ tự bước chuẩn của dạng: 1 λ → 2 hiệu đường đi → 3 loại M → 4 đếm cực đại → 5 đếm cực tiểu.
 * Quy tắc: N8 + H3 (nhãn trên hình), H4 (nét 2 màu, chữ ≥ 13px ở 360px), N1 (bỏ sóng chạy: một hình một việc).
 */

import type { ReactNode } from "react";

type Props = { f: number; v: number; AB: number; d1: number; d2: number; kieu?: "dem_day"; layer: number };

const C_MAX = "#c2410c", C_MIN = "#0e7490";

const fmt = (x: number, dp = 1) => {
  const s = x.toFixed(dp).replace(/\.?0+$/, "");
  return (s === "-0" ? "0" : s).replace(".", ",");
};

/** Nhánh hypebol |MA| − |MB| = s (A ở −c, B ở +c), toạ độ SVG (y lật), từ trục AB lên trên. */
function hyperbola(s: number, c: number, yMax: number): string {
  const a = Math.abs(s) / 2;
  if (a < 1e-6) return `M0 0 L0 ${-yMax}`;
  if (a >= c) return "";
  const b = Math.sqrt(c * c - a * a), T = Math.asinh(yMax / b), sg = Math.sign(s);
  const pts: string[] = [];
  for (let i = 0; i <= 32; i++) {
    const t = (T * i) / 32;
    pts.push(`${(sg * a * Math.cosh(t)).toFixed(3)} ${(-b * Math.sinh(t)).toFixed(3)}`);
  }
  return "M" + pts.join(" L");
}

function Label({ x, y, children, fill = "currentColor", a = "middle", size = 1.3 }: { x: number; y: number; children: ReactNode; fill?: string; a?: "start" | "middle" | "end"; size?: number }) {
  return (
    <text x={x} y={y} fontSize={size} textAnchor={a} fill={fill} fontWeight={600} stroke="var(--cc-halo)" strokeWidth={0.3} paintOrder="stroke">
      {children}
    </text>
  );
}

export default function GiaoThoaHaiNguon(p: Props) {
  return p.kieu === "dem_day" ? <DemDay {...p} /> : <TimLoai {...p} />;
}

/**
 * Biến thể "đếm dãy" (đợt Đ1 3/11, bài 12 dạng 3): biết M là cực đại và số dãy giữa M với trung trực → bậc k → λ → v.
 * Bước: 1 bậc k (vẽ các dãy cực đại từ trung trực tới M, đánh số) → 2 hiệu đường đi → 3 λ (chia thành k khúc) → 4 v.
 */
function DemDay({ f, v, AB, d1, d2, layer: L }: Props) {
  const lam = v / f, c = AB / 2;
  const mx = (d1 * d1 - d2 * d2) / (4 * c);
  const my = Math.sqrt(Math.max(d2 * d2 - (mx - c) ** 2, 0));
  const X = Math.max(c + 3.6, Math.abs(mx) + 2.2), Y1 = my + 2.4, z = X / 9.6;
  const s = d1 - d2, kM = Math.round(Math.abs(s) / lam), sg = Math.sign(s) || 1;
  const H = 8.8 * z, bandY = 3.2 * z;
  const ks = Array.from({ length: kM }, (_, j) => j + 1);
  // đỉnh mỗi dãy ở mép trên hình — chỗ đặt số k
  const topX = (k: number) => {
    const a = (k * lam) / 2, b = Math.sqrt(c * c - a * a);
    return sg * a * Math.sqrt(1 + (Y1 / b) ** 2);
  };
  const tw = Math.min(2.2 * z, (2 * X - 1.2 * z) / Math.max(kM, 1) - 0.15 * z);
  return (
    <svg viewBox={`${-X} ${-Y1} ${2 * X} ${Y1 + H}`} className="cc-fig" role="img" aria-label={`Hai nguồn A, B cách nhau ${fmt(AB)} cm; M cách A ${fmt(d1)} cm, cách B ${fmt(d2)} cm`}>
      {/* đường trung trực (k = 0) — dữ kiện đề */}
      <line x1={0} y1={0} x2={0} y2={-Y1} stroke={C_MAX} strokeWidth={0.08 * z} strokeDasharray={`${0.4 * z} ${0.3 * z}`} opacity={0.8} />
      <Label x={0.4 * z} y={-Y1 + 1.6 * z} a="start" size={1.1 * z} fill={C_MAX}>trung trực</Label>
      {L >= 1 &&
        ks.map((k, j) => (
          <g key={k} className="cc-in" style={{ animationDelay: `${j * 120}ms` }}>
            <path d={hyperbola(sg * k * lam, c, Y1)} stroke={C_MAX} strokeWidth={(k === kM ? 0.2 : 0.1) * z} fill="none" opacity={k === kM ? 1 : 0.7} />
            {k < kM && <Label x={topX(k)} y={-Y1 + 1.6 * z} size={1.15 * z} fill={C_MAX}>{`${k}`}</Label>}
          </g>
        ))}
      <line x1={-c} y1={0} x2={c} y2={0} stroke="currentColor" strokeWidth={0.1 * z} />
      <line x1={-c} y1={0} x2={mx} y2={-my} stroke="currentColor" strokeWidth={0.1 * z} opacity={0.75} />
      <line x1={c} y1={0} x2={mx} y2={-my} stroke="currentColor" strokeWidth={0.1 * z} opacity={0.75} />
      {/* nhãn d₁ sát A, bên trong góc (M gần mép hình nên không đặt được phía ngoài) */}
      <Label x={sg * (c - 1.0 * z)} y={-2.2 * z} a={sg < 0 ? "start" : "end"} size={1.25 * z}>{sg < 0 ? `d₁ = ${fmt(d1)}` : `d₂ = ${fmt(d2)}`}</Label>
      <Label x={(mx - sg * c) / 2 - sg * 0.8 * z} y={-my / 2} a={sg < 0 ? "start" : "end"} size={1.25 * z}>{sg < 0 ? `d₂ = ${fmt(d2)}` : `d₁ = ${fmt(d1)}`}</Label>
      {[-c, c].map((x, i) => (
        <g key={i}>
          <circle cx={x} cy={0} r={0.3 * z} fill="currentColor" />
          <Label x={x} y={1.35 * z} size={1.3 * z}>{i ? "B" : "A"}</Label>
        </g>
      ))}
      <circle cx={mx} cy={-my} r={0.3 * z} fill="#facc15" stroke="currentColor" strokeWidth={0.08 * z} />
      <Label x={mx - 0.5 * z} y={-my - 0.4 * z} a="end" size={1.3 * z}>M</Label>
      {/* dải dưới: bước 2 thanh |d₁ − d₂|, bước 3 chia thành k khúc λ, bước 4 tốc độ */}
      {L === 1 && (
        <Label x={-X + 0.6 * z} y={bandY + 1.1 * z} a="start" size={1.15 * z} fill={C_MAX}>
          {`M trên dãy thứ ${kM} → k = ${kM}`}
        </Label>
      )}
      {L >= 2 && (
        <g className="cc-in">
          {L < 3 ? (
            <rect x={-X + 0.6 * z} y={bandY} width={kM * (tw + 0.15 * z) - 0.15 * z} height={1.3 * z} rx={0.15 * z} fill={C_MAX} opacity={0.85} />
          ) : (
            ks.map((k, j) => (
              <g key={k} className="cc-pop" style={{ animationDelay: `${j * 110}ms` }}>
                <rect x={-X + 0.6 * z + j * (tw + 0.15 * z)} y={bandY} width={tw} height={1.3 * z} rx={0.15 * z} fill={C_MAX} />
                <text x={-X + 0.6 * z + j * (tw + 0.15 * z) + tw / 2} y={bandY + 0.95 * z} fontSize={0.8 * z} textAnchor="middle" fill="#fff" fontWeight={700}>
                  λ
                </text>
              </g>
            ))
          )}
          <Label x={-X + 0.6 * z} y={bandY + 2.9 * z} a="start" size={1.15 * z}>
            {L < 3 ? `${sg < 0 ? "d₂ − d₁" : "d₁ − d₂"} = ${fmt(Math.abs(s))} cm` : `${fmt(Math.abs(s))} = ${kM}λ → λ = ${fmt(lam, 2)} cm`}
          </Label>
        </g>
      )}
      {L >= 4 && (
        <Label x={-X + 0.6 * z} y={bandY + 4.5 * z} a="start" size={1.15 * z} fill={C_MIN}>
          {`v = λf = ${fmt(lam, 2)}·${fmt(f)} = ${fmt(v)} cm/s`}
        </Label>
      )}
    </svg>
  );
}

function TimLoai({ f, v, AB, d1, d2, layer: L }: Props) {
  const lam = v / f, c = AB / 2;
  // M theo đề: (x + c)² + y² = d1², (x − c)² + y² = d2²
  const mx = (d1 * d1 - d2 * d2) / (4 * c);
  const my = Math.sqrt(Math.max(d2 * d2 - (mx - c) ** 2, 0));
  const X = Math.max(c + 3.6, Math.abs(mx) + 2.2), Y1 = my + 2.4;
  const s = d1 - d2, kM = s / lam, onMax = Math.abs(kM - Math.round(kM)) < 1e-6;
  const nAB = AB / lam;
  const maxima: number[] = [], minima: number[] = [];
  for (let k = Math.ceil(-nAB); k <= Math.floor(nAB); k++) if (Math.abs(k) < nAB - 1e-9) maxima.push(k);
  for (let k = Math.ceil(-nAB - 0.5); k <= Math.floor(nAB - 0.5); k++) if (Math.abs(k + 0.5) < nAB - 1e-9) minima.push(k + 0.5);

  // dải dưới hình: bước 2–3 thanh |d1 − d2| chia khúc λ; bước 4+ trục số k
  const ratio = Math.abs(s) / lam, full = Math.floor(ratio + 1e-9), rest = ratio - full;
  const R = Math.ceil(nAB) + 1;
  const kx = (k: number) => (k / R) * (X - 1);
  const bandY = 3.2;
  const H = 7.2; // dải dưới luôn giữ chỗ: hình không đổi cao giữa các bước (nút ◀ ▶ đứng yên)
  const tile = 1.5, gap = 0.12;

  return (
    <svg viewBox={`${-X} ${-Y1} ${2 * X} ${Y1 + H}`} className="cc-fig" role="img" aria-label={`Hai nguồn A, B cách nhau ${fmt(AB)} cm; M cách A ${fmt(d1)} cm, cách B ${fmt(d2)} cm`}>
      {/* bước 4–5: mọi vân trên nửa mặt nước, nét mảnh */}
      {L >= 4 && maxima.map((k) => <path key={`M${k}`} d={hyperbola(k * lam, c, Y1)} stroke={C_MAX} strokeWidth={0.07} fill="none" opacity={0.45} />)}
      {L >= 5 && minima.map((k) => <path key={`m${k}`} d={hyperbola(k * lam, c, Y1)} stroke={C_MIN} strokeWidth={0.07} strokeDasharray="0.3 0.25" fill="none" opacity={0.6} />)}
      {/* bước 3: vân qua M kẹp giữa hai vân cực đại */}
      {L >= 3 && (
        <g className="cc-in">
          {!onMax && [Math.floor(kM), Math.ceil(kM)].map((k) => <path key={k} d={hyperbola(k * lam, c, Y1)} stroke={C_MAX} strokeWidth={0.14} fill="none" />)}
          <path d={hyperbola(s, c, Y1)} stroke={onMax ? C_MAX : C_MIN} strokeWidth={0.2} strokeDasharray={onMax ? undefined : "0.45 0.3"} fill="none" />
        </g>
      )}
      {/* dữ kiện đề: AB, d1, d2 */}
      <line x1={-c} y1={0} x2={c} y2={0} stroke="currentColor" strokeWidth={0.1} />
      <line x1={-c} y1={0} x2={mx} y2={-my} stroke="currentColor" strokeWidth={0.1} opacity={0.75} />
      <line x1={c} y1={0} x2={mx} y2={-my} stroke="currentColor" strokeWidth={0.1} opacity={0.75} />
      <Label x={(mx - c) / 2 - 0.7} y={-my / 2 - 0.2} a="end">{`d₁ = ${fmt(d1)}`}</Label>
      <Label x={(mx + c) / 2 - 1} y={-my / 2 + 1.8} a="end">{`d₂ = ${fmt(d2)}`}</Label>
      {/* bước 1: thước λ đặt ngoài B (từ bước 4 nhường chỗ cho trục số k) */}
      {L >= 1 && L < 4 && (
        <g className="cc-in">
          <path d={`M${c + 0.9} 0.3 v0.4 h${lam} v-0.4`} stroke="currentColor" strokeWidth={0.1} fill="none" />
          <Label x={c + 0.9 + lam / 2} y={2.1}>{`λ=${fmt(lam, 2)}`}</Label>
        </g>
      )}
      {/* bước 4–5: điểm trên AB */}
      {L >= 4 && maxima.map((k, i) => <circle key={`pM${k}`} cx={(k * lam) / 2} cy={0} r={0.22} fill={C_MAX} className="cc-pop" style={{ animationDelay: `${i * 70}ms` }} />)}
      {L >= 5 &&
        minima.map((k, i) => (
          <circle key={`pm${k}`} cx={(k * lam) / 2} cy={0} r={0.17} fill="var(--cc-halo)" stroke={C_MIN} strokeWidth={0.09} className="cc-pop" style={{ animationDelay: `${i * 70}ms` }} />
        ))}
      {[-c, c].map((x, i) => (
        <g key={i}>
          <circle cx={x} cy={0} r={0.3} fill="currentColor" />
          <Label x={x} y={1.35}>{i ? "B" : "A"}</Label>
        </g>
      ))}
      <circle cx={mx} cy={-my} r={0.3} fill="#facc15" stroke="currentColor" strokeWidth={0.08} />
      <Label x={mx + 0.5} y={-my - 0.3} a="start">M</Label>

      {/* dải dưới */}
      {L >= 2 && L < 4 && (
        <g>
          {Array.from({ length: full }, (_, i) => (
            <g key={i} className="cc-pop" style={{ animationDelay: `${i * 110}ms` }}>
              <rect x={-X + 0.5 + i * (tile + gap)} y={bandY} width={tile} height={1.3} rx={0.15} fill={C_MAX} />
              <text x={-X + 0.5 + i * (tile + gap) + tile / 2} y={bandY + 0.95} fontSize={0.8} textAnchor="middle" fill="#fff" fontWeight={700}>
                λ
              </text>
            </g>
          ))}
          {rest > 0.02 && (
            <rect x={-X + 0.5 + full * (tile + gap)} y={bandY} width={tile * rest} height={1.3} rx={0.15} fill={C_MIN} className="cc-pop" style={{ animationDelay: `${full * 110}ms` }} />
          )}
          <Label x={-X + 0.5 + Math.ceil(ratio) * (tile + gap) + 0.3} y={bandY + 1} a="start">
            {`|d₁ − d₂| = ${fmt(Math.abs(s))} = ${fmt(ratio, 2)}λ`}
          </Label>
        </g>
      )}
      {L >= 4 && (
        <g>
          <line x1={kx(-R)} y1={bandY + 0.6} x2={kx(R)} y2={bandY + 0.6} stroke="currentColor" strokeWidth={0.06} />
          {Array.from({ length: 2 * R + 1 }, (_, i) => i - R).map((k) => (
            <g key={k}>
              <line x1={kx(k)} y1={bandY + 0.45} x2={kx(k)} y2={bandY + 0.75} stroke="currentColor" strokeWidth={0.05} />
              {(R <= 8 || k % 2 === 0) && (
                <text x={kx(k)} y={bandY + 2.0} fontSize={0.95} textAnchor="middle" fill="currentColor">
                  {k}
                </text>
              )}
            </g>
          ))}
          {[-nAB, nAB].map((x) => (
            <circle key={x} cx={kx(x)} cy={bandY + 0.6} r={0.24} fill="var(--cc-halo)" stroke="currentColor" strokeWidth={0.08} />
          ))}
          {maxima.map((k, i) => <circle key={`nM${k}`} cx={kx(k)} cy={bandY + 0.6} r={0.18} fill={C_MAX} className="cc-pop" style={{ animationDelay: `${i * 70}ms` }} />)}
          {L >= 5 &&
            minima.map((k, i) => (
              <circle key={`nm${k}`} cx={kx(k)} cy={bandY + 0.6} r={0.15} fill="var(--cc-halo)" stroke={C_MIN} strokeWidth={0.08} className="cc-pop" style={{ animationDelay: `${i * 70}ms` }} />
            ))}
          <Label x={-X + 0.4} y={bandY - 0.5} a="start" size={1.1}>{`−${fmt(nAB, 2)} < k < ${fmt(nAB, 2)}`}</Label>
          <Label x={0} y={bandY + 3.5} size={1.1} fill={L >= 5 ? C_MIN : C_MAX}>
            {L >= 5 ? `${maxima.length} cực đại · ${minima.length} cực tiểu` : `${maxima.length} cực đại`}
          </Label>
        </g>
      )}
    </svg>
  );
}
