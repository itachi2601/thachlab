"use client";

/**
 * Họ hình `truc_chuyen_dong` (đợt Đ4 3/11/2026, mẫu đầu: bài 5 Tốc độ và vận tốc L10, dạng 3): trục toạ độ 1D nằm ngang,
 * mũi tên chiều dương ở đầu phải, các điểm mốc dưới trục. Mỗi bước vẽ thêm đoạn dịch chuyển (mũi tên trên một "hàng"
 * phía trên trục, hàng âm ở dưới tên mốc), ngoặc quãng đường, chấm vị trí, vật (khối nhỏ + vectơ v). Không hoạt hình.
 * Hình không đổi cao giữa các bước (D2: số hàng tính từ MỌI lớp); nhãn trên hình (N8, H3); đoạn loại hai nét đứt (H4).
 *
 * JSON: { loai: "truc_chuyen_dong", x_min, x_max, don_vi?: "m", diem?: [{x, ten}], hinh?: [mục…], lop: [[mục…], …] }.
 * Mục: doan {tu, den, hang, nhan?, mau?, dut?} · ngoac {tu, den, hang, nhan} · cham {x, hang?, ten?}
 *  · vat {x, hang?, ten?, v?, nhan_v?} (v: độ dài vectơ vận tốc theo đơn vị trục, có dấu) · chu {x, hang, text, a?} · ghi {text}.
 * `hang` ≥ 1 ở trên trục, ≤ −1 ở dưới; 0 là chính trục. `het: k` = ẩn từ khi xong bước k.
 */

import { C_MAX, C_MIN, Chevron, Label, chiaDong, dangHien, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { TrucChuyenDongLop } from "@/features/lessons/types";

type Props = {
  x_min: number;
  x_max: number;
  don_vi?: string;
  diem?: { x: number; ten: string }[];
  hinh?: TrucChuyenDongLop[];
  lop?: TrucChuyenDongLop[][];
  layer: number;
};

const W = 20,
  PX0 = 2,
  PX1 = 17.2,
  ROW = 1.9,
  FS = 1.05;
const mau = (m?: string) => (m === "min" ? C_MIN : m === "max" ? C_MAX : "currentColor");

export default function TrucChuyenDong({ x_min, x_max, don_vi = "m", diem = [], hinh = [], lop, layer: Lr }: Props) {
  const X = (x: number) => PX0 + ((x - x_min) / (x_max - x_min)) * (PX1 - PX0);
  // số hàng trên/dưới lấy từ mọi lớp → hình không đổi cao
  const all = [...hinh, ...(lop ?? []).flat()];
  const hs = all.map((it) => ("hang" in it && typeof it.hang === "number" ? it.hang : 0));
  const up = Math.max(0, ...hs),
    down = Math.max(0, ...hs.map((h) => -h));
  const TOP = 1 + up * ROW,
    AX = TOP + 0.3,
    BELOW = AX + 1.9; // tên mốc dưới trục
  const Y = (h: number) => (h > 0 ? AX - 0.35 - h * ROW + 0.55 : h < 0 ? BELOW + 0.2 + -h * ROW - 0.55 : AX);
  const H = BELOW + down * ROW + 0.4;
  const items = dangHien(lop, Lr);
  const ghi = ghiMoiNhat(lop, Lr).flatMap((t) => chiaDong(t, W, FS)).slice(0, 2);

  function veMuc(it: TrucChuyenDongLop, moi: boolean) {
    const cls = moi ? "cc-in" : undefined;
    if (it.loai === "doan") {
      const y = Y(it.hang),
        x1 = X(it.tu),
        x2 = X(it.den),
        c = mau(it.mau ?? "max"),
        s = Math.sign(x2 - x1) || 1;
      return (
        <g className={cls}>
          <line x1={x1} y1={y - 0.25} x2={x1} y2={y + 0.25} stroke={c} strokeWidth={0.08} />
          <line x1={x1} y1={y} x2={x2 - s * 0.05} y2={y} stroke={c} strokeWidth={0.13} strokeDasharray={it.dut ? "0.45 0.25" : undefined} />
          <Chevron x={x2} y={y} ang={s > 0 ? 0 : Math.PI} color={c} len={0.5} w={0.13} />
          {it.nhan && (
            <Label x={(x1 + x2) / 2} y={y - 0.45} fill={c} size={FS}>
              {it.nhan}
            </Label>
          )}
        </g>
      );
    }
    if (it.loai === "ngoac") {
      const y = Y(it.hang),
        x1 = X(it.tu),
        x2 = X(it.den);
      return (
        <g className={cls}>
          <path d={`M${x1} ${y + 0.3} V${y} H${x2} V${y + 0.3}`} fill="none" stroke="currentColor" strokeWidth={0.07} />
          <Label x={(x1 + x2) / 2} y={y - 0.45} size={FS}>
            {it.nhan}
          </Label>
        </g>
      );
    }
    if (it.loai === "cham") {
      const y = Y(it.hang ?? 0);
      return (
        <g className={cls}>
          <circle cx={X(it.x)} cy={y} r={0.28} fill={C_MAX} stroke="var(--cc-halo)" strokeWidth={0.08} />
          {it.ten && (
            <Label x={X(it.x)} y={y - 0.55} fill={C_MAX} size={FS}>
              {it.ten}
            </Label>
          )}
        </g>
      );
    }
    if (it.loai === "vat") {
      const y = Y(it.hang ?? 0),
        x = X(it.x),
        v = it.v ?? 0,
        xe = x + (v / (x_max - x_min)) * (PX1 - PX0);
      return (
        <g className={cls}>
          <rect x={x - 0.55} y={y - 0.75} width={1.1} height={0.75} rx={0.15} fill="var(--cc-halo)" stroke="currentColor" strokeWidth={0.09} />
          {it.ten && (
            <Label x={x} y={y - 1.05} size={FS}>
              {it.ten}
            </Label>
          )}
          {v !== 0 && (
            <g>
              <line x1={x} y1={y - 0.38} x2={xe} y2={y - 0.38} stroke={C_MIN} strokeWidth={0.13} />
              <Chevron x={xe} y={y - 0.38} ang={v > 0 ? 0 : Math.PI} color={C_MIN} len={0.45} w={0.13} />
              {it.nhan_v && (
                <Label x={xe + Math.sign(v) * 0.4} y={y - 0.05} a={v > 0 ? "start" : "end"} fill={C_MIN} size={FS}>
                  {it.nhan_v}
                </Label>
              )}
            </g>
          )}
        </g>
      );
    }
    if (it.loai === "chu") {
      return (
        <g className={cls}>
          <Label x={X(it.x)} y={Y(it.hang) - 0.45} a={it.a ?? "middle"} size={FS}>
            {it.text}
          </Label>
        </g>
      );
    }
    return null;
  }

  return (
    <svg viewBox={`-0.4 -0.2 ${W + 0.8} ${H + 3.7}`} className="cc-fig" role="img" aria-label="Trục toạ độ, độ dịch chuyển theo từng bước">
      {/* trục + chiều dương */}
      <line x1={PX0 - 0.8} y1={AX} x2={PX1 + 1.5} y2={AX} stroke="currentColor" strokeWidth={0.1} />
      <Chevron x={PX1 + 1.6} y={AX} ang={0} len={0.5} w={0.1} />
      <Label x={PX1 + 1.6} y={AX - 0.45} a="end" size={FS}>
        {`x (${don_vi})`}
      </Label>
      {diem.map((d) => (
        <g key={d.ten}>
          <line x1={X(d.x)} y1={AX - 0.25} x2={X(d.x)} y2={AX + 0.25} stroke="currentColor" strokeWidth={0.1} />
          <Label x={X(d.x)} y={AX + 1.25} size={FS}>
            {d.ten}
          </Label>
        </g>
      ))}
      {hinh.map((it, k) => (it.het != null && Lr >= it.het ? null : <g key={`h${k}`}>{veMuc(it, false)}</g>))}
      {items.map((it, k) => (
        <g key={`l${k}`}>{veMuc(it, true)}</g>
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
