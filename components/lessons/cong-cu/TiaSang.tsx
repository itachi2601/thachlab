"use client";

/**
 * Họ hình `tia_sang` (đợt Đ5 4/11/2026, mẫu đầu: KHTN 9 bài 5 Khúc xạ ánh sáng, dạng 4): các môi trường xếp lớp, mặt
 * phân cách nằm ngang, một tia sáng đi qua lần lượt từng lớp. Hình sơ đồ, KHÔNG theo tỉ lệ cm: đơn vị là đơn vị hình
 * (bề ngang 20).
 *  - `moi`: các môi trường theo THỨ TỰ TIA ĐI QUA, mỗi môi trường {ten (vd "nước · n = 4/3"), cao}. `chieu: "len"` thì
 *    lớp đầu nằm dưới cùng (tia đi từ dưới lên, vd từ nước ra không khí).
 *  - `goc[j]`: góc (độ, đo từ pháp tuyến) của tia trong môi trường j — dùng để vẽ, có thể là đáp số (chỉ ghi số lên
 *    hình ở bước đã xong). `x0`: điểm tới trên mặt phân cách đầu (mặc định 10).
 * Mục (mặt k = mặt giữa môi trường k và k + 1):
 *  - tia {moi: j, nhan?, mau?, dut?} — đoạn tia trong môi trường j, có mũi chevron giữa đoạn.
 *  - phan_xa {mat: k, nhan?, mau?} — tia phản xạ ở mặt k, trở lại môi trường k.
 *  - phap_tuyen {mat: k, dai?} — pháp tuyến nét đứt tại điểm tới.
 *  - goc {mat: k, tu, den, nhan, r?, r_nhan?, nhan_goc?, mau?} — cung góc (nhan_goc: hướng đặt nhãn, độ, khi góc hẹp); tu/den là hướng: "phap_vao" | "phap_ra" (pháp tuyến phía môi
 *    trường tới / môi trường khúc xạ), "mat_trai" | "mat_phai", "toi" | "phan_xa" | "khuc_xa", hoặc số độ (toán học).
 *  - chu {x, y, text, a?, mau?} (y đơn vị hình từ đỉnh) · ghi {text}. `het: k` = ẩn từ khi xong bước k.
 * Hình không đổi cao giữa các bước (D2); nhãn trên hình (N8, H3); tia phản xạ/khúc xạ khác màu và có tên (H4).
 */

import { C_MAX, C_MIN, Chevron, Label, chiaDong, dangHien, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { TiaSangLop, TiaSangMoi } from "@/features/lessons/types";

type Props = { moi: TiaSangMoi[]; goc: number[]; x0?: number; chieu?: "xuong" | "len"; hinh?: TiaSangLop[]; lop?: TiaSangLop[][]; layer: number };

const W = 20,
  FS = 1.05,
  TOP = 0.3,
  rad = (d: number) => (d * Math.PI) / 180;

const mauCua = (m?: string, md = "currentColor") => (m === "max" ? C_MAX : m === "min" ? C_MIN : m === "chu" ? "currentColor" : md);

export default function TiaSang({ moi, goc, x0 = 10, chieu = "xuong", hinh = [], lop, layer: Lr }: Props) {
  const items = dangHien(lop, Lr);
  const hinhHien = hinh.filter((it) => it.het == null || Lr < it.het);
  const ghi = ghiMoiNhat(lop, Lr).flatMap((t) => chiaDong(t, W, FS)).slice(0, 2);

  const tong = moi.reduce((s, m) => s + m.cao, 0);
  const BOT = TOP + tong;
  const len = chieu === "len";
  // toạ độ "theo chiều đi": s = quãng đã đi theo phương pháp tuyến tính từ mép lớp đầu; lật khi tia đi lên
  const Y = (s: number) => (len ? BOT - s : TOP + s);
  const sMat = moi.map((_, k) => moi.slice(0, k + 1).reduce((a, m) => a + m.cao, 0)); // mặt k ở s = sMat[k]
  const xs: number[] = [x0];
  for (let k = 1; k < moi.length - 1; k++) xs.push(xs[k - 1] + moi[k].cao * Math.tan(rad(goc[k])));
  const H = BOT + 0.4;

  // đoạn tia trong môi trường j: [x1, s1, x2, s2]
  function doan(j: number): [number, number, number, number] {
    const g = rad(goc[j]),
      sn = Math.sin(g),
      cs = Math.cos(g);
    if (j === 0) {
      const t = Math.min(moi[0].cao / cs, sn > 1e-6 ? (xs[0] - 0.3) / sn : Infinity);
      return [xs[0] - t * sn, sMat[0] - t * cs, xs[0], sMat[0]];
    }
    if (j === moi.length - 1) {
      const xa = xs[j - 1],
        t = Math.min(moi[j].cao / cs, sn > 1e-6 ? (W - 0.3 - xa) / sn : Infinity);
      return [xa, sMat[j - 1], xa + t * sn, sMat[j - 1] + t * cs];
    }
    return [xs[j - 1], sMat[j - 1], xs[j], sMat[j]];
  }

  // hướng (độ, toán học: ngược chiều kim, y lên) tại mặt k, đã tính chiều lật
  function huong(k: number, h: string | number): number {
    if (typeof h === "number") return h;
    const gv = goc[k],
      gr = goc[k + 1] ?? 0;
    const a =
      h === "phap_vao" ? 90 : h === "phap_ra" ? -90 : h === "mat_trai" ? 180 : h === "mat_phai" ? 0 : h === "toi" ? 90 + gv : h === "phan_xa" ? 90 - gv : -90 + gr;
    return len ? -a : a;
  }

  function veTia(x1: number, s1: number, x2: number, s2: number, c: string, dut: boolean | undefined, nhan: string | undefined, cls?: string) {
    const ya = Y(s1),
      yb = Y(s2),
      ang = Math.atan2(yb - ya, x2 - x1),
      mx = (x1 + x2) / 2,
      my = (ya + yb) / 2;
    // nhãn tia: lệch vuông góc về phía ngoài pháp tuyến
    const nx = -Math.sin(ang),
      ny = Math.cos(ang),
      sg = (mx < x0 ? -1 : 1) * Math.sign(nx || 1);
    return (
      <g className={cls}>
        <line x1={x1} y1={ya} x2={x2} y2={yb} stroke={c} strokeWidth={0.13} strokeDasharray={dut ? "0.4 0.25" : undefined} strokeLinecap="round" />
        <Chevron x={mx + 0.25 * Math.cos(ang)} y={my + 0.25 * Math.sin(ang)} ang={ang} color={c} len={0.5} w={0.13} />
        {nhan && (
          <Label x={mx + sg * nx * 1.0} y={my + sg * ny * 1.0 + 0.35} fill={c} size={FS}>
            {nhan}
          </Label>
        )}
      </g>
    );
  }

  function veMuc(it: TiaSangLop, moi_: boolean) {
    const cls = moi_ ? "cc-in" : undefined;
    if (it.loai === "tia") {
      const [x1, s1, x2, s2] = doan(it.moi);
      return veTia(x1, s1, x2, s2, mauCua(it.mau, it.moi === 0 ? "currentColor" : C_MIN), it.dut, it.nhan, cls);
    }
    if (it.loai === "phan_xa") {
      const k = it.mat,
        g = rad(goc[k]),
        xa = xs[k],
        t = Math.min(moi[k].cao / Math.cos(g), Math.sin(g) > 1e-6 ? (W - 0.3 - xa) / Math.sin(g) : Infinity);
      return veTia(xa, sMat[k], xa + t * Math.sin(g), sMat[k] - t * Math.cos(g), mauCua(it.mau, C_MAX), it.dut, it.nhan, cls);
    }
    if (it.loai === "phap_tuyen") {
      const k = it.mat,
        d = it.dai ?? 2.6,
        s1 = Math.max(0, sMat[k] - d),
        s2 = Math.min(tong, sMat[k] + d);
      return (
        <g className={cls}>
          <line x1={xs[k]} y1={Y(s1)} x2={xs[k]} y2={Y(s2)} stroke="currentColor" strokeWidth={0.06} strokeDasharray="0.3 0.2" opacity={0.75} />
        </g>
      );
    }
    if (it.loai === "goc") {
      const k = it.mat,
        cx = xs[k],
        cy = Y(sMat[k]);
      let a1 = huong(k, it.tu),
        a2 = huong(k, it.den);
      let d = (((a2 - a1) % 360) + 360) % 360;
      if (d > 180) {
        [a1, a2] = [a2, a1];
        d = 360 - d;
      }
      const r = it.r ?? 1.5,
        P = (a: number, rr: number) => [cx + rr * Math.cos(rad(a)), cy - rr * Math.sin(rad(a))],
        [ax, ay] = P(a1, r),
        [bx, by] = P(a2, r),
        [lx, ly] = P(it.nhan_goc != null ? (len ? -it.nhan_goc : it.nhan_goc) : a1 + d / 2, r + (it.r_nhan ?? 1.05)),
        c = mauCua(it.mau, C_MAX);
      return (
        <g className={cls}>
          <path d={`M${ax} ${ay} A${r} ${r} 0 0 0 ${bx} ${by}`} fill="none" stroke={c} strokeWidth={0.08} />
          <Label x={lx} y={ly + 0.38} fill={c} size={FS}>
            {it.nhan}
          </Label>
        </g>
      );
    }
    if (it.loai === "chu") {
      return (
        <g className={cls}>
          <Label x={it.x} y={it.y} a={it.a ?? "middle"} size={FS} fill={mauCua(it.mau)}>
            {it.text}
          </Label>
        </g>
      );
    }
    return null;
  }

  const thu = (arr: TiaSangLop[], m: boolean, key: string) => arr.map((it, j) => <g key={`${key}${j}`}>{veMuc(it, m)}</g>);
  const nen = (it: TiaSangLop) => it.loai === "phap_tuyen";

  return (
    <svg viewBox={`-0.4 -0.2 ${W + 0.8} ${H + 3.7}`} className="cc-fig" role="img" aria-label="Tia sáng qua các môi trường">
      {/* nền môi trường: lớp sau đậm dần; mặt phân cách nét liền */}
      {moi.map((m, j) => {
        const sa = j === 0 ? 0 : sMat[j - 1],
          sb = j === 0 ? sMat[0] : j === moi.length - 1 ? tong : sMat[j];
        const y1 = Math.min(Y(sa), Y(sb)),
          h = Math.abs(Y(sb) - Y(sa));
        const dam = m.dam ?? (j === 0 ? 0 : 0.08 + 0.07 * j);
        return dam > 0 ? <rect key={`n${j}`} x={0} y={y1} width={W} height={h} fill={C_MIN} fillOpacity={dam} /> : null;
      })}
      {sMat.slice(0, -1).map((s, k) => (
        <line key={`m${k}`} x1={0} y1={Y(s)} x2={W} y2={Y(s)} stroke="currentColor" strokeWidth={0.1} />
      ))}
      {thu(hinhHien.filter(nen), false, "hn")}
      {thu(items.filter(nen), true, "ln")}
      {/* tên môi trường: lớp đầu ở giữa mép ngoài, các lớp sau ở góc trái phía mép xa */}
      {moi.map((m, j) => {
        const sb = j === moi.length - 1 ? tong : sMat[j];
        const y = Y(j === 0 ? 0.95 : sb - 0.45) + (len ? 0.38 : 0);
        return (
          <Label key={`t${j}`} x={m.nhan_x ?? (j === 0 ? x0 + 0.4 : 0.4)} y={y} a="start" size={FS * 0.92}>
            {m.ten}
          </Label>
        );
      })}
      {thu(hinhHien.filter((it) => !nen(it)), false, "h")}
      {thu(items.filter((it) => !nen(it)), true, "l")}
      <circle cx={x0} cy={Y(sMat[0])} r={0.14} fill="currentColor" />
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
