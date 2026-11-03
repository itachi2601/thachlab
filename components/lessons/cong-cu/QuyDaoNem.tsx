"use client";

/**
 * Họ hình `quy_dao_nem` (đợt Đ4 3/11/2026, mẫu đầu: bài Chuyển động ném L10, dạng 4): mặt phẳng đứng Oxy, mặt đất nằm
 * ngang, quỹ đạo parabol vẽ CÙNG tỉ lệ hai trục (góc ném nhìn đúng). Mỗi bước vẽ thêm: thành phần v₀ₓ, v₀ᵧ (nét đứt),
 * nửa quỹ đạo lên đỉnh + vectơ v ở đỉnh (chỉ còn vₓ), thước H, nửa còn lại, thước L, mốc trên mặt đất. Không hoạt hình.
 * Hình không đổi cao giữa các bước (D2: khung theo x_max, y_max); nhãn trên hình (N8, H3); quỹ đạo thứ hai nét đứt (H4).
 *
 * JSON: { loai: "quy_dao_nem", v0, alpha (độ), g?: 9,8, h0?: 0, x_max, y_max (m), hinh?: [mục…], lop: [[mục…], …] }.
 * `t` của mục là PHẦN thời gian bay (0 = lúc ném, 0,5 = đỉnh khi h0 = 0, 1 = chạm đất). Mục:
 *  quy_dao {alpha?, tu?, den?, dut?, mau?, nhan?} · van_toc {t, alpha?, tach?, chi?: "x"|"y"|"ca", nhan?, nhan_x?, nhan_y?}
 *  · diem {t, alpha?, ten, vi?: "t"|"b"|"l"|"r"} · goc {alpha?, nhan} · moc {x, nhan} (cờ trên mặt đất)
 *  · thuoc_ngang {tu, den, nhan} (dưới mặt đất) · thuoc_doc {x, tu, den, nhan, ben?} · ghi {text}. `het: k` = ẩn từ bước k.
 */

import { C_MAX, C_MIN, Chevron, Label, chiaDong, dangHien, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { QuyDaoNemLop } from "@/features/lessons/types";

type Props = {
  v0: number;
  alpha: number;
  g?: number;
  h0?: number;
  x_max: number;
  y_max: number;
  hinh?: QuyDaoNemLop[];
  lop?: QuyDaoNemLop[][];
  layer: number;
};

const W = 20,
  PX0 = 2.2,
  PX1 = 18.6,
  FS = 1.05;
const mau = (m?: string) => (m === "min" ? C_MIN : m === "muc" ? "currentColor" : C_MAX);
const rad = (d: number) => (d * Math.PI) / 180;

export default function QuyDaoNem({ v0, alpha, g = 9.8, h0 = 0, x_max, y_max, hinh = [], lop, layer: Lr }: Props) {
  const k = (PX1 - PX0) / x_max; // đơn vị hình / m — cùng tỉ lệ hai trục
  const TOP = 1.6,
    GY = TOP + y_max * k; // mặt đất
  const X = (x: number) => PX0 + x * k,
    Y = (y: number) => GY - y * k;
  const kv = 3.4 / v0; // vectơ vận tốc: v₀ dài 3,4 đơn vị
  const H = GY + 2.6;
  const items = dangHien(lop, Lr);
  const ghi = ghiMoiNhat(lop, Lr).flatMap((t) => chiaDong(t, W, FS)).slice(0, 2);

  const bay = (a: number) => {
    const vx = v0 * Math.cos(rad(a)),
      vy = v0 * Math.sin(rad(a)),
      T = (vy + Math.sqrt(vy * vy + 2 * g * h0)) / g;
    const at = (f: number) => {
      const t = f * T;
      return { x: vx * t, y: h0 + vy * t - (g * t * t) / 2, vx, vy: vy - g * t };
    };
    return { T, at, dinh: vy / g / T };
  };

  function veMuc(it: QuyDaoNemLop, moi: boolean) {
    const cls = moi ? "cc-in" : undefined;
    if (it.loai === "quy_dao") {
      const b = bay(it.alpha ?? alpha),
        f0 = it.tu ?? 0,
        f1 = it.den ?? 1,
        n = 48;
      const pts = Array.from({ length: n + 1 }, (_, i) => {
        const p = b.at(f0 + ((f1 - f0) * i) / n);
        return `${X(p.x).toFixed(3)},${Y(p.y).toFixed(3)}`;
      });
      const c = mau(it.mau),
        e = b.at(f1);
      return (
        <g className={cls}>
          <polyline points={pts.join(" ")} fill="none" stroke={c} strokeWidth={it.dut ? 0.1 : 0.13} strokeDasharray={it.dut ? "0.4 0.25" : undefined} />
          {f1 >= 1 && <circle cx={X(e.x)} cy={Y(e.y)} r={0.22} fill={c} />}
          {it.nhan &&
            (() => {
              const top = b.at(Math.min(f1, b.dinh)); // nhãn ngay trên đỉnh
              return (
                <Label x={X(top.x)} y={Y(top.y) - 0.5} fill={c} size={FS}>
                  {it.nhan}
                </Label>
              );
            })()}
        </g>
      );
    }
    if (it.loai === "van_toc") {
      const p = bay(it.alpha ?? alpha).at(it.t),
        ox = X(p.x),
        oy = Y(p.y),
        ex = ox + p.vx * kv,
        ey = oy - p.vy * kv,
        chi = it.chi ?? "ca";
      const arrow = (x2: number, y2: number, c: string, dut: boolean, w: number) => {
        const ang = Math.atan2(y2 - oy, x2 - ox);
        return (
          <>
            <line x1={ox} y1={oy} x2={x2} y2={y2} stroke={c} strokeWidth={w} strokeDasharray={dut ? "0.35 0.22" : undefined} />
            <Chevron x={x2} y={y2} ang={ang} color={c} len={0.45} w={w} />
          </>
        );
      };
      const hasX = Math.abs(p.vx) > 1e-6,
        hasY = Math.abs(p.vy) > 1e-3;
      return (
        <g className={cls}>
          {chi === "ca" && hasX && hasY && arrow(ex, ey, "currentColor", false, 0.13)}
          {(it.tach || chi === "x" || (chi === "ca" && !hasY)) && hasX && arrow(ex, oy, C_MIN, chi === "ca" && hasY, 0.1)}
          {(it.tach || chi === "y") && hasY && arrow(ox, ey, C_MIN, chi === "ca", 0.1)}
          {it.tach && chi === "ca" && hasX && hasY && (
            <path d={`M${ex} ${oy} L${ex} ${ey} M${ox} ${ey} L${ex} ${ey}`} stroke="currentColor" strokeWidth={0.04} strokeDasharray="0.15 0.15" opacity={0.6} />
          )}
          {it.nhan && chi === "ca" && hasY && (
            <Label x={ex + 0.3} y={ey - 0.25} a="start" size={FS}>
              {it.nhan}
            </Label>
          )}
          {it.nhan_x && (
            <Label x={ox + 0.3} y={oy + 1.15} a="start" fill={C_MIN} size={FS}>
              {it.nhan_x}
            </Label>
          )}
          {it.nhan_y && (
            // bên phải nét dóng (trục y ở mép trái, không còn chỗ bên trái)
            <Label x={Math.max(ex, ox) + 0.3} y={(oy + ey) / 2 + 0.35} a="start" fill={C_MIN} size={FS}>
              {it.nhan_y}
            </Label>
          )}
        </g>
      );
    }
    if (it.loai === "diem") {
      const p = bay(it.alpha ?? alpha).at(it.t),
        x = X(p.x),
        y = Y(p.y),
        vi = it.vi ?? "t";
      const [lx, ly, a] = vi === "t" ? [x, y - 0.5, "middle"] : vi === "b" ? [x, y + 1.3, "middle"] : vi === "l" ? [x - 0.45, y + 0.4, "end"] : [x + 0.45, y + 0.4, "start"];
      return (
        <g className={cls}>
          <circle cx={x} cy={y} r={0.2} fill="currentColor" />
          <Label x={lx} y={ly} a={a as "start" | "middle" | "end"} size={FS}>
            {it.ten}
          </Label>
        </g>
      );
    }
    if (it.loai === "goc") {
      const a = it.alpha ?? alpha,
        r = 1.6,
        ox = X(0),
        oy = Y(h0);
      return (
        <g className={cls}>
          <path d={`M${ox + r} ${oy} A${r} ${r} 0 0 0 ${ox + r * Math.cos(rad(a))} ${oy - r * Math.sin(rad(a))}`} fill="none" stroke="currentColor" strokeWidth={0.07} />
          <Label x={ox + (r + 0.35) * Math.cos(rad(a / 2))} y={oy - (r + 0.35) * Math.sin(rad(a / 2)) + 0.4} a="start" size={FS}>
            {it.nhan}
          </Label>
        </g>
      );
    }
    if (it.loai === "moc") {
      const x = X(it.x);
      return (
        <g className={cls}>
          <line x1={x} y1={GY} x2={x} y2={GY - 1.3} stroke="currentColor" strokeWidth={0.08} />
          <path d={`M${x} ${GY - 1.3} L${x + 0.8} ${GY - 1.05} L${x} ${GY - 0.8} Z`} fill={C_MAX} />
          <Label x={x} y={GY + 1.15} size={FS}>
            {it.nhan}
          </Label>
        </g>
      );
    }
    if (it.loai === "thuoc_ngang") {
      const y = GY + 0.6,
        x1 = X(it.tu),
        x2 = X(it.den);
      return (
        <g className={cls}>
          <g stroke="currentColor" strokeWidth={0.07}>
            <line x1={x1} y1={y} x2={x2} y2={y} />
            <line x1={x1} y1={y - 0.3} x2={x1} y2={y + 0.3} />
            <line x1={x2} y1={y - 0.3} x2={x2} y2={y + 0.3} />
          </g>
          <Label x={(x1 + x2) / 2} y={y + 1.3} size={FS}>
            {it.nhan}
          </Label>
        </g>
      );
    }
    if (it.loai === "thuoc_doc") {
      const x = X(it.x),
        y1 = Y(it.tu),
        y2 = Y(it.den),
        trai = it.ben === "trai";
      return (
        <g className={cls}>
          <g stroke={C_MAX} strokeWidth={0.07}>
            <line x1={x} y1={y1} x2={x} y2={y2} />
            <line x1={x - 0.25} y1={y1} x2={x + 0.25} y2={y1} />
            <line x1={x - 0.25} y1={y2} x2={x + 0.25} y2={y2} />
          </g>
          <Label x={trai ? x - 0.35 : x + 0.35} y={(y1 + y2) / 2 + 0.4} a={trai ? "end" : "start"} fill={C_MAX} size={FS}>
            {it.nhan}
          </Label>
        </g>
      );
    }
    return null;
  }

  return (
    <svg viewBox={`-0.4 -0.2 ${W + 0.8} ${H + 3.7}`} className="cc-fig" role="img" aria-label="Quỹ đạo vật ném trong mặt phẳng đứng">
      {/* mặt đất + trục */}
      <line x1={0.6} y1={GY} x2={W} y2={GY} stroke="currentColor" strokeWidth={0.14} />
      <g stroke="currentColor" strokeWidth={0.05} opacity={0.5}>
        {Array.from({ length: 13 }, (_, i) => (
          <line key={i} x1={1 + i * 1.5} y1={GY + 0.07} x2={0.4 + i * 1.5} y2={GY + 0.6} />
        ))}
      </g>
      <line x1={X(0)} y1={GY} x2={X(0)} y2={TOP - 1.1} stroke="currentColor" strokeWidth={0.06} />
      <Chevron x={X(0)} y={TOP - 1.2} ang={-Math.PI / 2} len={0.4} w={0.06} />
      <Label x={X(0) - 0.35} y={TOP - 0.55} a="end" size={FS}>
        y
      </Label>
      <Label x={X(0) - 0.35} y={GY + 1.15} a="end" size={FS}>
        O
      </Label>
      {hinh.map((it, j) => (it.het != null && Lr >= it.het ? null : <g key={`h${j}`}>{veMuc(it, false)}</g>))}
      {items.map((it, j) => (
        <g key={`l${j}`}>{veMuc(it, true)}</g>
      ))}
      {ghi.map((t, i) => (
        <Label key={`${Lr}-${i}`} x={W / 2} y={H + 1.2 + i * 1.45} size={FS}>
          {t}
        </Label>
      ))}
      {/* giữ chỗ dải dưới để hình không đổi cao (D2) */}
      <rect x={0} y={H} width={0.01} height={3.1} fill="none" />
    </svg>
  );
}
