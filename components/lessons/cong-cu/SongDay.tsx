"use client";

/**
 * Họ hình `song_day` (đợt Đ1 3/11/2026, mẫu đầu: bài 8 Mô tả sóng, dạng 4): sợi dây dọc trục Ox, ảnh chụp sóng
 * u(x) = A·cos(pha·π − 2πx/λ) tại một thời điểm (chỉ tới đầu sóng `dau`, sau đó dây còn thẳng), các điểm O, M, N,
 * thước đo khoảng cách, mũi tên chiều chuyển động của phần tử. Chỉ có nét, không chạy sóng (thầy 2/11).
 *
 * JSON: { loai: "song_day", A, lam, x_max, diem: [{x, ten}], song?: {pha, dau?}, lop: [[mục…], …] }. Mục:
 *  song {pha, dau?} (thay ảnh sóng)  ·  thuoc {tu, den, nhan, hang?: 0|1}  ·  mui {x, huong: "len"|"xuong"}
 *  ·  dau_song {x}  ·  ghi {text}. `het: k` = ẩn từ khi xong bước k. Đơn vị cm.
 */

import { C_HL, C_MAX, C_MIN, Chevron, Label, dangHien, fmt, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { SongDayLop } from "@/features/lessons/types";

type Song = { pha: number; dau?: number };
type Props = { A: number; lam: number; x_max: number; diem?: { x: number; ten: string }[]; song?: Song; lop?: SongDayLop[][]; layer: number };

const W = 18, UA = 2; // bề ngang trục x và độ cao biên độ (đơn vị hình)

export default function SongDay({ A, lam, x_max, diem = [], song, lop, layer: L }: Props) {
  const items = dangHien(lop, L);
  const ghi = ghiMoiNhat(lop, L);
  let cur: Song | undefined = song;
  for (const it of items) if (it.loai === "song") cur = { pha: it.pha, dau: it.dau };
  const X = (x: number) => (x / x_max) * W;
  const u = (x: number) => (!cur || (cur.dau != null && x > cur.dau + 1e-9) ? 0 : A * Math.cos(cur.pha * Math.PI - (2 * Math.PI * x) / lam));
  const Y = (v: number) => -(v / A) * UA;
  const n = 160;
  const pts = Array.from({ length: n + 1 }, (_, i) => {
    const x = (x_max * i) / n;
    return `${X(x).toFixed(3)} ${Y(u(x)).toFixed(3)}`;
  });
  const top = -UA - 1.7, bot = 9.6;
  const rowY = (h = 0) => UA + 1.1 + h * 1.9;

  return (
    <svg viewBox={`-1.2 ${top} ${W + 2.6} ${bot - top}`} className="cc-fig" role="img" aria-label={`Sợi dây có sóng, biên độ ${fmt(A)} cm`}>
      {/* trục Ox (vị trí cân bằng) và chiều truyền */}
      <line x1={0} y1={0} x2={W + 1} y2={0} stroke="currentColor" strokeWidth={0.05} opacity={0.6} strokeDasharray="0.3 0.2" />
      <Chevron x={W + 1} y={0} ang={0} len={0.4} w={0.06} />
      <Label x={W + 1.2} y={-0.4} size={0.95} a="end">x</Label>
      <g>
        <line x1={W - 4.2} y1={top + 0.75} x2={W - 1.6} y2={top + 0.75} stroke={C_MIN} strokeWidth={0.1} />
        <Chevron x={W - 1.6} y={top + 0.75} ang={0} color={C_MIN} w={0.1} len={0.45} />
        <Label x={W - 4.5} y={top + 1.1} a="end" size={0.95} fill={C_MIN}>truyền</Label>
      </g>
      {/* dây */}
      <path d={"M" + pts.join(" L")} stroke="currentColor" strokeWidth={0.12} fill="none" strokeLinejoin="round" />
      {cur?.dau != null && cur.dau < x_max && (
        <g>
          <line x1={X(cur.dau)} y1={-UA - 0.4} x2={X(cur.dau)} y2={UA + 0.4} stroke={C_MIN} strokeWidth={0.06} strokeDasharray="0.25 0.2" />
        </g>
      )}
      {items.map((it, k) => {
        if (it.loai === "thuoc") {
          const y = rowY(it.hang ?? 0), x1 = X(it.tu), x2 = X(it.den);
          return (
            <g key={k} className="cc-in">
              {[x1, x2].map((x, j) => (
                <line key={j} x1={x} y1={0} x2={x} y2={y} stroke={C_MAX} strokeWidth={0.05} strokeDasharray="0.2 0.2" opacity={0.7} />
              ))}
              <path d={`M${x1} ${y - 0.3} v0.3 H${x2} v-0.3`} stroke={C_MAX} strokeWidth={0.1} fill="none" />
              <Label x={(x1 + x2) / 2} y={y + 1.15} size={1} fill={C_MAX}>
                {it.nhan}
              </Label>
            </g>
          );
        }
        if (it.loai === "dau_song") {
          return (
            <g key={k} className="cc-in">
              <Chevron x={X(it.x)} y={-UA - 0.4} ang={0} color={C_MIN} w={0.1} len={0.45} />
            </g>
          );
        }
        return null;
      })}
      {/* các điểm theo đề */}
      {diem.map((d) => {
        const x = X(d.x), y = Y(u(d.x));
        return (
          <g key={d.ten}>
            <circle cx={x} cy={y} r={0.28} fill={C_HL} stroke="currentColor" strokeWidth={0.07} />
            <Label x={x + 0.45} y={y < -0.5 ? y - 0.35 : y - 0.45} a="start">
              {d.ten}
            </Label>
          </g>
        );
      })}
      {items.map((it, k) => {
        if (it.loai !== "mui") return null;
        const x = X(it.x), y = Y(u(it.x)), s = it.huong === "len" ? -1 : 1;
        return (
          <g key={`m${k}`} className="cc-in">
            <line x1={x - 0.45} y1={y + s * 0.4} x2={x - 0.45} y2={y + s * 1.6} stroke={C_MAX} strokeWidth={0.14} />
            <Chevron x={x - 0.45} y={y + s * 1.6} ang={s < 0 ? -Math.PI / 2 : Math.PI / 2} color={C_MAX} w={0.14} len={0.45} />
          </g>
        );
      })}
      {ghi.map((t, i) => (
        <Label key={`${L}-${i}`} x={W / 2} y={rowY(1) + 2.5 + i * 1.3} size={1}>
          {t}
        </Label>
      ))}
    </svg>
  );
}
