/**
 * components/physics/thuc-hanh/cham-tong-hop-luc.ts — số học của thí nghiệm ảo "Tổng hợp lực" (L10 Bài 22, lesson 67;
 * Gói C, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5). Không React để thử bằng `npx tsx`.
 *
 * Thông số lấy từ content/thi-nghiem/tn-l10-thuchanhthl-01.json. Quy ước theo đúng bài 67:
 *   tỉ lệ xích 1 cm ↔ 0,5 N; chéo đo trên hình làm tròn 0,1 cm; F vẽ = chéo · 0,5;
 *   δ = |F vẽ − F3 đọc|; Δ = ΔF1 + ΔF2 + ΔF3 = 3 · 0,1 = 0,3 N (mỗi lực kế 1 độ chia).
 * Lực giữ bằng SỐ NGUYÊN phần mười niutơn (độ chia lực kế) để cộng trừ không lệch.
 */

import tn from "@/content/thi-nghiem/tn-l10-thuchanhthl-01.json";
import { docSo, type KetQuaCham } from "@/components/physics/do-luong/chung";
import { gan, phanLoai, vnSo } from "./cham-chung";

export { vnSo };

type ThamSo = {
  ky_hieu: string;
  min?: number;
  max?: number;
  mac_dinh?: number;
  buoc?: number;
  gia_tri?: number;
};
const TS = Object.fromEntries((tn.tham_so as ThamSo[]).map((p) => [p.ky_hieu, p])) as Record<string, ThamSo>;

export const XICH = TS.xich.gia_tri ?? 0.5; // N/cm
export const DF = TS.dF.gia_tri ?? 0.1; // N, sai số một lực kế
export const DELTA_GOP = 3 * DF; // N
/** Số 0 lệch khi bật (phần mười N): JSON cho tới 0,4 N; lấy 0,4 để lần nào cũng thấy rõ chiều lệch. */
export const SO0_LECH_T = Math.round((TS.so_0.max ?? 0.4) * 10);
/** F1, F2 tính bằng phần mười N. */
export const F_T = {
  min: Math.round((TS.F1.min ?? 0.5) * 10),
  max: Math.round((TS.F1.max ?? 2.5) * 10),
  macDinh: Math.round((TS.F1.mac_dinh ?? 2) * 10),
};
/** α từ 50° để F3 (kể cả số 0 lệch) không vượt thang lực kế 5 N: 2 · 2,5 · cos 25° + 0,4 ≈ 4,93 N. */
export const ALPHA = { min: 50, max: 150, buoc: 10, macDinh: TS.alpha.mac_dinh ?? 60 };

const rad = (d: number) => (d * Math.PI) / 180;

/** Độ lớn hợp lực (N) của F1, F2 (N) hợp góc α (độ). */
export const hopLuc = (f1: number, f2: number, a: number) =>
  Math.sqrt(f1 * f1 + f2 * f2 + 2 * f1 * f2 * Math.cos(rad(a)));
/** Nhầm góc bù 180° − α. */
export const hopLucGocBu = (f1: number, f2: number, a: number) =>
  Math.sqrt(Math.max(0, f1 * f1 + f2 * f2 - 2 * f1 * f2 * Math.cos(rad(a))));
/** Góc (độ) của F1, F2 lệch hai bên phương thẳng đứng khi hợp lực thẳng đứng (lực kế 3 treo vật). */
export function gocHaiBen(f1: number, f2: number, a: number) {
  const t1 = (Math.atan2(f2 * Math.sin(rad(a)), f1 + f2 * Math.cos(rad(a))) * 180) / Math.PI;
  return { t1, t2: a - t1 };
}

/** Nhiễu đọc mỗi lần bố trí (phần mười N, [−0,5; 0,5]): nút O, ma sát dây, đọc vạch. */
export const nhieuNgauNhien = () => Math.random() - 0.5;

export type Hang = { f1T: number; f2T: number; a: number; f3T: number; so0: boolean };

/** Số chỉ lực kế 3 (phần mười N): hợp lực + nhiễu, làm tròn tới độ chia, cộng số 0 lệch. */
export const docF3T = (f1T: number, f2T: number, a: number, so0: boolean, n: number) =>
  Math.round(hopLuc(f1T, f2T, a) + n) + (so0 ? SO0_LECH_T : 0);

export type KetQuaHang = { F: number; cheo: number; fVe: number; f3: number; delta: number; khop: boolean };

export function tinhHang(h: Hang): KetQuaHang {
  const F = hopLuc(h.f1T / 10, h.f2T / 10, h.a);
  const cheo = Math.round((F / XICH) * 10) / 10;
  const fVe = cheo * XICH;
  const f3 = h.f3T / 10;
  const delta = Math.abs(fVe - f3);
  return { F, cheo, fVe, f3, delta, khop: delta <= DELTA_GOP + 1e-9 };
}

/* ---------------- Chấm ô học sinh tự tính (lần 1) ---------------- */

export function chamCanh(raw: string, f1: number): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const canh = f1 / XICH;
  const cach = `Cạnh = F1 : xích = ${vnSo(f1, 1)} : ${vnSo(XICH, 1)} = ${vnSo(canh, 1)} cm.`;
  return phanLoai(
    so.value,
    cach,
    [[canh, 0.02]],
    [[f1 * XICH, 0.02, "Em nhân với 0,5; 1 cm ứng 0,5 N nên phải chia cho 0,5 (mỗi niutơn dài 2 cm)."]],
  );
}

export function chamFve(raw: string, h: Hang, kq: KetQuaHang): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const f1 = h.f1T / 10;
  const f2 = h.f2T / 10;
  const cach = `F vẽ = chéo · xích = ${vnSo(kq.cheo, 1)} · ${vnSo(XICH, 1)} = ${vnSo(kq.fVe, 2)} N.`;
  return phanLoai(
    so.value,
    cach,
    [
      [kq.fVe, 0.051],
      [kq.F, 0.011],
    ],
    [
      [kq.cheo / XICH, 0.06, "Em chia chéo cho 0,5; từ cm ra N phải nhân với 0,5."],
      [
        f1 + f2,
        0.06,
        "Em cộng hai độ lớn như hai lực cùng phương, cùng chiều; hai dây hợp góc α nên phải vẽ hình bình hành.",
      ],
      [
        hopLucGocBu(f1, f2, h.a),
        0.06,
        "Đó là đường chéo kia (hai cạnh hợp góc 180° − α); hợp lực là đường chéo đi qua O, giữa hai cạnh hợp góc α.",
      ],
    ],
  );
}

export function chamDelta(raw: string, fVeHs: number, kq: KetQuaHang): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const d = Math.abs(fVeHs - kq.f3);
  const cach = `δ = |F vẽ − F3| = |${vnSo(fVeHs, 2)} − ${vnSo(kq.f3, 1)}| = ${vnSo(d, 2)} N.`;
  if (gan(so.value, -d, 0.011) && d > 0.011)
    return { loai: "sai", loi: `δ là độ lớn của độ lệch, lấy trị tuyệt đối. ${cach}` };
  return phanLoai(so.value, cach, [[d, 0.011]], [[fVeHs + kq.f3, 0.03, "Em cộng hai số; độ lệch là hiệu."]]);
}

export function chamDeltaGop(raw: string): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const cach = `Δ = ΔF1 + ΔF2 + ΔF3 = 0,1 + 0,1 + 0,1 = ${vnSo(DELTA_GOP, 1)} N (mỗi lực kế 1 độ chia).`;
  return phanLoai(
    so.value,
    cach,
    [[DELTA_GOP, 0.001]],
    [
      [DF, 0.001, "Đó là sai số của một lực kế; F vẽ lấy từ F1, F2 và đem so với F3 nên cộng cả ba."],
      [2 * DF, 0.001, "Còn thiếu một lực kế: F vẽ mang sai số của F1, F2, và F3 cũng có sai số đọc."],
      [1.5 * DF, 0.001, "Bài này lấy sai số mỗi lực kế bằng 1 độ chia (0,1 N), không phải nửa độ chia."],
    ],
  );
}
