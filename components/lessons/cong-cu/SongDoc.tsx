"use client";

/**
 * Cảnh `canh: {kieu: "doc"}` của họ `song_day` (5/11/2026, mẫu bài 9 L11 dạng 3): sóng dọc trong ống nằm ngang — ảnh chụp
 * các LỚP KHÍ (vạch đứng) dời khỏi vị trí cân bằng một đoạn u(x) = A·cos(pha·π − 2πx/λ) DỌC trục ống. Vùng nén = vạch dày
 * sít, vùng dãn = vạch thưa. Không vẽ đường u(x) hình sin (dễ hiểu nhầm thành sóng ngang — Đ7 4/11).
 * Dùng chung props của `song_day`: A (cm, chọn kA ≈ 0,45: vùng nén còn rõ mà lớp u = ±A không bị vẽ dời sát vùng nén — A thật rất nhỏ so với λ), lam, x_max, song.pha. Toạ độ x = vị trí
 * cân bằng (cm) tính từ loa.
 * canh: { kieu: "doc", buoc_lop? (cm, mặc định λ/10), nguon? (nhãn cạnh loa, vd "1700 Hz"), vung?: boolean (ghi N/D từ đầu; có N/D thì kèm chú giải "N: nén · D: dãn" ở dòng trên) }
 * Mục lop: vung {dem?} (ghi N/D; dem = đánh số N₁, N₂…) · diem {x, ten} (tô lớp khí có vị trí cân bằng x — nên là bội của buoc_lop — và
 * hai lớp kề, nét đứt vị trí cân bằng + mũi tên độ dời) · thuoc {tu, den, nhan, hang?} (ngoặc dưới ống, hàng 0|1|2) · ghi {text}. `het: k` như chung.
 * Quy tắc: N8 + H3 (nhãn trên hình), H4 (vùng phân biệt bằng mật độ nét, không chỉ màu), N5 (lớp theo bước), B4 (không chạy).
 */

import { C_HL, C_MAX, C_MIN, Chevron, Label, dangHien, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { SongDayCanh, SongDayLop } from "@/features/lessons/types";

type Props = { A: number; lam: number; x_max: number; pha: number; canh: Extract<SongDayCanh, { kieu: "doc" }>; lop?: SongDayLop[][]; layer: number };

const W = 18, HT = 1.3; // bề ngang ống, nửa chiều cao ống (đơn vị hình)

export default function SongDoc({ A, lam, x_max, pha, canh, lop, layer: L }: Props) {
  const items = dangHien(lop, L);
  const ghi = ghiMoiNhat(lop, L);
  const X = (x: number) => (x / x_max) * W;
  const u = (x: number) => A * Math.cos(pha * Math.PI - (2 * Math.PI * x) / lam);
  const dx = canh.buoc_lop ?? lam / 10;
  const lopKhi: number[] = [];
  for (let x = 0; x <= x_max + 1e-9; x += dx) {
    const p = x + u(x);
    if (p >= 0.15 && p <= x_max - 0.1) lopKhi.push(X(p));
  }
  // tâm vùng nén: du/dx nhỏ nhất ⇔ x = λ(pha/2 + 1/4 − n); tâm vùng dãn: x = λ(pha/2 − 1/4 − n)
  const tam = (c: number) => {
    const out: number[] = [];
    const x0 = lam * (((c % 1) + 1) % 1);
    for (let x = x0; x <= x_max - lam * 0.06; x += lam) if (x >= lam * 0.06) out.push(x);
    return out;
  };
  const nen = tam(pha / 2 + 0.25), dan = tam(pha / 2 - 0.25);
  const vung = [...items].reverse().find((it) => it.loai === "vung") as Extract<SongDayLop, { loai: "vung" }> | undefined;
  const hienVung = !!vung || !!canh.vung;
  const dem = !!vung?.dem;

  const allThuoc = (lop ?? []).flat().filter((it) => it.loai === "thuoc") as Extract<SongDayLop, { loai: "thuoc" }>[];
  const nRow = Math.max(0, ...allThuoc.map((t) => (t.hang ?? 0) + 1));
  const rowY = (h: number) => HT + 1.2 + h * 2.2;
  const top = -HT - 3.1;
  const ghiY = rowY(nRow) - 0.2;
  const bot = ghiY + 2 * 1.3 + 0.2;

  return (
    <svg viewBox={`-2.6 ${top} ${W + 3.4} ${bot - top}`} className="cc-fig" role="img" aria-label={`Sóng dọc trong ống, bước sóng ${lam} cm`}>
      {/* chiều truyền */}
      <g>
        <line x1={W - 4.2} y1={top + 0.75} x2={W - 1.6} y2={top + 0.75} stroke={C_MIN} strokeWidth={0.1} />
        <Chevron x={W - 1.6} y={top + 0.75} ang={0} color={C_MIN} w={0.1} len={0.45} />
        <Label x={W - 4.5} y={top + 1.1} a="end" size={0.95} fill={C_MIN}>
          truyền
        </Label>
      </g>
      {/* loa */}
      <g>
        <rect x={-2.3} y={-0.5} width={0.6} height={1} fill="none" stroke="currentColor" strokeWidth={0.09} />
        <path d={`M-1.7 -0.5 L-0.5 -1.1 L-0.5 1.1 L-1.7 0.5`} fill="none" stroke="currentColor" strokeWidth={0.09} strokeLinejoin="round" />
        {hienVung && (
          <text x={5.9} y={top + 1.1} fontSize={0.95} textAnchor="middle" fontWeight={600} fill="currentColor">
            <tspan fill={C_MAX}>N</tspan>: nén · <tspan fill={C_MIN}>D</tspan>: dãn
          </text>
        )}
        {canh.nguon && (
          <Label x={-2.4} y={top + 1.1} a="start" size={0.95}>
            {canh.nguon}
          </Label>
        )}
      </g>
      {/* ống + các lớp khí */}
      <path d={`M0 ${-HT} H${W} M0 ${HT} H${W}`} stroke="currentColor" strokeWidth={0.12} />
      {/* vùng nén tô nhạt (rộng λ/5) — phân biệt chính bằng mật độ vạch, tô chỉ để mắt bắt nhanh (H4) */}
      {hienVung && nen.map((x, i) => <rect key={`v${i}`} x={X(x - lam / 10)} y={-HT + 0.06} width={X(lam / 5)} height={2 * HT - 0.12} fill={C_MAX} fillOpacity={0.1} />)}
      {lopKhi.map((x, i) => (
        <line key={i} x1={x} y1={-HT + 0.12} x2={x} y2={HT - 0.12} stroke="currentColor" strokeWidth={0.05} opacity={0.75} />
      ))}
      {hienVung && (
        <g className={vung && !canh.vung ? "cc-in" : undefined}>
          {nen.map((x, i) => (
            <Label key={`n${i}`} x={X(x)} y={-HT - 0.45} size={1} fill={C_MAX}>
              {dem ? `N_${i + 1}` : "N"}
            </Label>
          ))}
          {dan.map((x, i) => (
            <Label key={`d${i}`} x={X(x)} y={-HT - 0.45} size={1} fill={C_MIN}>
              D
            </Label>
          ))}
        </g>
      )}
      {items.map((it, k) => {
        if (it.loai === "diem") {
          const x0 = X(it.x), x1 = X(it.x + u(it.x));
          const ke = [it.x - dx, it.x + dx].map((x) => X(x + u(x))); // hai lớp kề M: cách M gần bằng khoảng lúc chưa có sóng
          return (
            <g key={k} className="cc-in">
              {ke.map((x, j) => (
                <line key={j} x1={x} y1={-HT} x2={x} y2={HT} stroke={C_MAX} strokeWidth={0.09} />
              ))}
              <line x1={x0} y1={-HT} x2={x0} y2={HT} stroke={C_MAX} strokeWidth={0.07} strokeDasharray="0.2 0.15" />
              <line x1={x1} y1={-HT} x2={x1} y2={HT} stroke={C_HL} strokeWidth={0.32} opacity={0.9} />
              <line x1={x1} y1={-HT} x2={x1} y2={HT} stroke={C_MAX} strokeWidth={0.1} />
              {Math.abs(x1 - x0) > 0.2 && <Chevron x={x1} y={HT + 0.45} ang={x1 > x0 ? 0 : Math.PI} color={C_MAX} w={0.09} len={0.25} />}
              {Math.abs(x1 - x0) > 0.2 && <line x1={x0} y1={HT + 0.45} x2={x1} y2={HT + 0.45} stroke={C_MAX} strokeWidth={0.09} />}
              <Label x={x1} y={HT + 1.5} size={1.05} fill={C_MAX}>
                {it.ten}
              </Label>
            </g>
          );
        }
        if (it.loai === "thuoc") {
          const y = rowY(it.hang ?? 0), x1 = X(it.tu), x2 = X(it.den);
          return (
            <g key={k} className="cc-in">
              {[x1, x2].map((x, j) => (
                <line key={j} x1={x} y1={HT + 0.1} x2={x} y2={y} stroke={C_MAX} strokeWidth={0.05} strokeDasharray="0.2 0.2" opacity={0.7} />
              ))}
              <path d={`M${x1} ${y - 0.3} v0.3 H${x2} v-0.3`} stroke={C_MAX} strokeWidth={0.1} fill="none" />
              <Label x={(x1 + x2) / 2} y={y + 1.1} size={1} fill={C_MAX}>
                {it.nhan}
              </Label>
            </g>
          );
        }
        return null;
      })}
      {ghi.map((t, i) => (
        <Label key={`${L}-${i}`} x={W / 2} y={ghiY + 1 + i * 1.3} size={1}>
          {t}
        </Label>
      ))}
    </svg>
  );
}
