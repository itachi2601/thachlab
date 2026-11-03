"use client";

/**
 * Họ hình `dien_truong_deu` (đợt Đ3 3/11/2026, mẫu đầu: bài 18 Điện trường đều L11, dạng 3): hai bản phẳng nằm ngang
 * (dấu + cam, − xanh), electron vào chính giữa với v₀, đường sức nét đứt mũi chevron 30° từ bản + sang bản −, lực điện,
 * quỹ đạo parabol y = y_cuoi·(x/L)² (cắt ở bản nếu chạm, chấm điểm chạm), thước ngang/dọc. Hình kéo dọc cho dễ nhìn
 * (khoảng cách hai bản luôn vẽ 6 đơn vị) nhưng parabol vẫn đúng hình dạng theo đề. Không hoạt hình.
 * Hình không đổi cao giữa các bước (D2); nhãn trên hình (N8, H3); quỹ đạo giả định nét đứt (H4).
 *
 * JSON: { loai: "dien_truong_deu", L, d, duong: "tren"|"duoi" (bản dương), v0?: nhãn, hinh?: [mục…], lop: [[mục…], …] }.
 * x tính từ mép vào (đơn vị như L), y tính từ đường giữa (đơn vị như d), lên là dương. Mục: duong_suc {nhan?}
 *  · luc {huong, nhan?} · quy_dao {y_cuoi, cat?, dut?, mau?} · thuoc_ngang {tu, den, nhan, vi} · thuoc_doc {x, tu, den,
 *  nhan, ben?, mau?} · chu {x, y, text, a?} · ghi {text}. `het: k` = ẩn từ khi xong bước k.
 */

import { C_MAX, C_MIN, Chevron, Label, chiaDong, dangHien, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { DienTruongLop } from "@/features/lessons/types";

type Props = {
  L: number;
  d: number;
  duong: "tren" | "duoi";
  v0?: string;
  hinh?: DienTruongLop[];
  lop?: DienTruongLop[][];
  layer: number;
};

const W = 20,
  H = 12,
  PX0 = 3.2,
  PX1 = 14.5,
  TOP = 3,
  BOT = 9,
  MID = 6;
const mau = (m?: string) => (m === "min" ? C_MIN : C_MAX);

export default function DienTruongDeu({ L, d, duong, v0 = "v_0", hinh = [], lop, layer: Lr }: Props) {
  const X = (x: number) => PX0 + (x / L) * (PX1 - PX0);
  const Yv = (y: number) => MID - (y / (d / 2)) * (BOT - MID);
  const items = dangHien(lop, Lr);
  const ghi = ghiMoiNhat(lop, Lr).flatMap((t) => chiaDong(t, W, 1.05)).slice(0, 2);

  function veMuc(it: DienTruongLop, moi: boolean) {
    const cls = moi ? "cc-in" : undefined;
    if (it.loai === "duong_suc") {
      // E hướng từ bản dương sang bản âm
      const xuong = duong === "tren";
      return (
        <g className={cls}>
          <g opacity={0.6}>
            {[0.1, 0.3, 0.5, 0.7, 0.9].map((f) => {
              const x = PX0 + f * (PX1 - PX0);
              return (
                <g key={f}>
                  <line
                    x1={x}
                    y1={TOP + 0.2}
                    x2={x}
                    y2={BOT - 0.2}
                    stroke={C_MIN}
                    strokeWidth={0.06}
                    strokeDasharray="0.4 0.25"
                  />
                  <Chevron x={x} y={xuong ? MID + 1.6 : MID - 1.6} ang={xuong ? Math.PI / 2 : -Math.PI / 2} color={C_MIN} len={0.4} w={0.08} />
                </g>
              );
            })}
          </g>
          {it.nhan && (
            <Label x={PX0 + 0.52 * (PX1 - PX0)} y={xuong ? TOP + 1.3 : BOT - 0.55} a="start" fill={C_MIN} size={1.05}>
              {it.nhan}
            </Label>
          )}
        </g>
      );
    }
    if (it.loai === "luc") {
      const x = PX0 + 0.9,
        s = it.huong === "len" ? -1 : 1,
        y2 = MID + s * 2.1;
      return (
        <g className={cls}>
          <line x1={x} y1={MID} x2={x} y2={y2} stroke={C_MAX} strokeWidth={0.14} />
          <Chevron x={x} y={y2} ang={(s * Math.PI) / 2} color={C_MAX} len={0.5} w={0.14} />
          {it.nhan && (
            <Label x={x + 0.4} y={MID + s * 1.25 + 0.4} a="start" fill={C_MAX}>
              {it.nhan}
            </Label>
          )}
        </g>
      );
    }
    if (it.loai === "quy_dao") {
      const h = d / 2,
        cham = it.cat && Math.abs(it.y_cuoi) > h,
        xe = cham ? L * Math.sqrt(h / Math.abs(it.y_cuoi)) : L;
      const n = 40,
        pts = Array.from({ length: n + 1 }, (_, i) => {
          const x = (xe * i) / n;
          return `${X(x).toFixed(3)},${Yv(it.y_cuoi * (x / L) ** 2).toFixed(3)}`;
        });
      const c = mau(it.mau);
      return (
        <g className={cls}>
          <polyline
            points={pts.join(" ")}
            fill="none"
            stroke={c}
            strokeWidth={it.dut ? 0.09 : 0.13}
            strokeDasharray={it.dut ? "0.35 0.22" : undefined}
            opacity={it.dut ? 0.85 : 1}
          />
          {cham && <circle cx={X(xe)} cy={Yv(Math.sign(it.y_cuoi) * h)} r={0.26} fill={c} />}
        </g>
      );
    }
    if (it.loai === "thuoc_ngang") {
      const y = it.vi === "tren" ? 1.25 : 10.8,
        x1 = X(it.tu),
        x2 = X(it.den);
      return (
        <g className={cls}>
          <g stroke="currentColor" strokeWidth={0.07}>
            <line x1={x1} y1={y} x2={x2} y2={y} />
            <line x1={x1} y1={y - 0.3} x2={x1} y2={y + 0.3} />
            <line x1={x2} y1={y - 0.3} x2={x2} y2={y + 0.3} />
          </g>
          <Label x={(x1 + x2) / 2} y={it.vi === "tren" ? y - 0.4 : y + 1.35} size={1.05}>
            {it.nhan}
          </Label>
        </g>
      );
    }
    if (it.loai === "thuoc_doc") {
      const x = X(it.x),
        y1 = Yv(it.tu),
        y2 = Yv(it.den),
        c = it.mau ? mau(it.mau) : "currentColor",
        trai = it.ben === "trai";
      return (
        <g className={cls}>
          <g stroke={c} strokeWidth={0.08}>
            <line x1={x} y1={y1} x2={x} y2={y2} />
            <line x1={x - 0.25} y1={y1} x2={x + 0.25} y2={y1} />
            <line x1={x - 0.25} y1={y2} x2={x + 0.25} y2={y2} />
          </g>
          <Label x={trai ? x - 0.35 : x + 0.35} y={(y1 + y2) / 2 + 0.4} a={trai ? "end" : "start"} fill={c} size={1.05}>
            {it.nhan}
          </Label>
        </g>
      );
    }
    if (it.loai === "chu") {
      return (
        <g className={cls}>
          <Label x={X(it.x)} y={Yv(it.y)} a={it.a ?? "middle"} size={1.05}>
            {it.text}
          </Label>
        </g>
      );
    }
    return null;
  }

  const dau = (tren: boolean) => {
    const duongBan = (duong === "tren") === tren;
    return [0.12, 0.37, 0.62].map((f) => (
      <Label
        key={f}
        x={PX0 + f * (PX1 - PX0)}
        y={tren ? TOP - 0.45 : BOT + 1.15}
        fill={duongBan ? C_MAX : C_MIN}
        size={1.25}
      >
        {duongBan ? "+" : "−"}
      </Label>
    ));
  };

  return (
    <svg
      viewBox={`-0.4 -0.2 ${W + 0.8} ${H + 4}`}
      className="cc-fig"
      role="img"
      aria-label="Hai bản phẳng song song, electron bay vào điện trường đều"
    >
      <g stroke="currentColor" strokeWidth={0.28} strokeLinecap="round">
        <line x1={PX0} y1={TOP} x2={PX1} y2={TOP} />
        <line x1={PX0} y1={BOT} x2={PX1} y2={BOT} />
      </g>
      {dau(true)}
      {dau(false)}
      {/* electron vào chính giữa, v₀ song song hai bản */}
      <line x1={0.4} y1={MID} x2={PX0 - 0.55} y2={MID} stroke="currentColor" strokeWidth={0.12} />
      <Chevron x={PX0 - 0.55} y={MID} ang={0} len={0.45} w={0.12} />
      <Label x={(0.4 + PX0) / 2 - 0.2} y={MID - 0.55}>
        {v0}
      </Label>
      <line x1={PX0} y1={MID} x2={PX1} y2={MID} stroke="currentColor" strokeWidth={0.04} strokeDasharray="0.2 0.3" opacity={0.5} />
      {hinh.map((it, k) => (it.het != null && Lr >= it.het ? null : <g key={`h${k}`}>{veMuc(it, false)}</g>))}
      {items.map((it, k) => (
        <g key={`l${k}`}>{veMuc(it, true)}</g>
      ))}
      <circle cx={PX0} cy={MID} r={0.34} fill="var(--cc-halo)" stroke={C_MIN} strokeWidth={0.08} />
      <line x1={PX0 - 0.17} y1={MID} x2={PX0 + 0.17} y2={MID} stroke={C_MIN} strokeWidth={0.08} />
      {ghi.map((t, i) => (
        <Label key={`${Lr}-${i}`} x={W / 2} y={H + 1.7 + i * 1.45} size={1.05}>
          {t}
        </Label>
      ))}
      {/* giữ chỗ dải dưới để hình không đổi cao (D2) */}
      <rect x={0} y={H} width={0.01} height={3.6} fill="none" />
    </svg>
  );
}
