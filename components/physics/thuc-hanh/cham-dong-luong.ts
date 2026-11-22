/**
 * components/physics/thuc-hanh/cham-dong-luong.ts — số học của thí nghiệm ảo "Xác định động lượng trước và sau va chạm"
 * (L10 Bài 30, lesson 75; Gói C, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5). Không React để thử bằng `npx tsx`.
 *
 * Thông số lấy từ content/thi-nghiem/tn-l10-thuchanhdl-01.json (một nguồn). Quy ước sai số theo đúng bài 30:
 *   p = m1·s/t1 (xe 2 đứng yên), p' = (m1+m2)·s/t1';  δ = |p' − p| / p;
 *   ε = Δm/m1 + Δt/t1 + 2Δm/(m1+m2) + Δt/t1'  (Δm = 0,001 kg, Δt = 0,001 s: MỘT độ chia nhỏ nhất; cân hai xe nên
 *   khối lượng sau có 2Δm; s là cùng một tấm cản quang nên không cộng).
 * Thời gian giữ bằng SỐ NGUYÊN mili giây (đồng hồ chia 0,001 s).
 */

import tn from "@/content/thi-nghiem/tn-l10-thuchanhdl-01.json";
import { docSo, type KetQuaCham } from "@/components/physics/do-luong/chung";
import { phanLoai, vnSo } from "./cham-chung";

type ThamSo = { ky_hieu: string; gia_tri?: number; mac_dinh?: number; min?: number; max?: number; sai_so_do?: number };
const TS = Object.fromEntries((tn.tham_so as ThamSo[]).map((p) => [p.ky_hieu, p])) as Record<string, ThamSo>;

export const S_CAN = TS.s.gia_tri ?? 0.05; // m, bề rộng tấm cản quang
export const DC_T = TS.dcnn_t.gia_tri ?? 0.001; // s — 1 độ chia đồng hồ
export const DC_M = TS.dcnn_m.gia_tri ?? 0.001; // kg — 1 độ chia cân
/** Hai mức khối lượng mỗi xe (xe trống, thêm 1 gia trọng 0,200 kg) — đúng các mức của bảng số liệu mẫu bài 30. */
export const M1_CHON = [0.205, 0.405];
export const M2_CHON = [0.198, 0.398];
/** Tốc độ đẩy xe 1: quanh v1 mặc định, mỗi lần đẩy tay khác nhau ±0,05 m/s (không ảnh hưởng δ, chỉ để bảng thật hơn). */
export const V1_TB = TS.v1.mac_dinh ?? 0.505;
export const V1_LECH = 0.05;
/** Nhiễu đọc đồng hồ, ms (tham_so t1.sai_so_do = 0,001 s). */
export const NHIEU_MS = Math.round((TS.t1.sai_so_do ?? 0.001) * 1000);
/** Tỉ lệ động lượng mất do ma sát khí, sức cản khi bật (goi_y_mo_phong.bat_tat.mat[1], mặc định tham_so mat). */
export const MAT = (tn.goi_y_mo_phong as { bat_tat?: { mat: number[] } }).bat_tat?.mat[1] ?? TS.mat.mac_dinh ?? 0.022;

export type LanDay = { v1: number; n1: number; n2: number };
/** Lần đẩy kế tiếp: tốc độ tay và nhiễu đọc hai đồng hồ (T8: các lần đo khác nhau thật). */
export const lanDayNgauNhien = (): LanDay => ({
  v1: V1_TB + (Math.random() * 2 - 1) * V1_LECH,
  n1: Math.floor(Math.random() * (2 * NHIEU_MS + 1)) - NHIEU_MS,
  n2: Math.floor(Math.random() * (2 * NHIEU_MS + 1)) - NHIEU_MS,
});

/** Tốc độ thật hai xe sau va chạm (m/s). */
export const vSau = (m1: number, m2: number, v1: number, coMaSat: boolean) =>
  ((m1 * v1) / (m1 + m2)) * (1 - (coMaSat ? MAT : 0));

/** Số chỉ hai đồng hồ (ms nguyên). */
export function soChi(m1: number, m2: number, d: LanDay, coMaSat: boolean) {
  return {
    t1Ms: Math.round((1000 * S_CAN) / d.v1 + d.n1),
    t1pMs: Math.round((1000 * S_CAN) / vSau(m1, m2, d.v1, coMaSat) + d.n2),
  };
}

export type Hang = { m1: number; m2: number; t1Ms: number; t1pMs: number };
export type KetQuaHang = { v1: number; p: number; vp: number; pp: number; delta: number; eps: number };

/** Xử lí một lần đo đúng như bài 30 (δ, ε là tỉ số, chưa nhân 100). */
export function tinhHang(h: Hang): KetQuaHang {
  const t1 = h.t1Ms / 1000;
  const t1p = h.t1pMs / 1000;
  const v1 = S_CAN / t1;
  const vp = S_CAN / t1p;
  const p = h.m1 * v1;
  const pp = (h.m1 + h.m2) * vp;
  const eps = DC_M / h.m1 + DC_T / t1 + (2 * DC_M) / (h.m1 + h.m2) + DC_T / t1p;
  return { v1, p, vp, pp, delta: Math.abs(pp - p) / p, eps };
}

const g = (x: number) => vnSo(x, 3);

/* ---------------- Chấm các ô học sinh tự tính (lần 1) ---------------- */
/* p, p' nhận làm tròn v tới 0,001 m/s như bài (lệch ≤ 0,4 %); δ, ε ghi theo %, dung sai đủ cho làm tròn 1 chữ số. */

export function chamP(raw: string, h: Hang, kq: KetQuaHang): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const cach = `v1 = s : t1 = ${vnSo(S_CAN, 4)} : ${g(h.t1Ms / 1000)} ≈ ${g(kq.v1)} m/s; p = m1 · v1 = ${g(h.m1)} · ${g(kq.v1)} ≈ ${vnSo(kq.p, 4)} kg·m/s.`;
  return phanLoai(
    so.value,
    cach,
    [[kq.p, 0.005 * kq.p]],
    [
      [kq.p * 100, 0.01 * kq.p * 100, "Tấm cản quang rộng 5,00 cm: đổi ra 0,0500 m trước khi chia."],
      [kq.v1, 0.005 * kq.v1, "Đó mới là tốc độ v1; còn phải nhân với m1."],
    ],
  );
}

export function chamPp(raw: string, h: Hang, kq: KetQuaHang): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const cach = `v' = s : t1' = ${vnSo(S_CAN, 4)} : ${g(h.t1pMs / 1000)} ≈ ${g(kq.vp)} m/s; p' = (m1 + m2) · v' = ${g(h.m1 + h.m2)} · ${g(kq.vp)} ≈ ${vnSo(kq.pp, 4)} kg·m/s.`;
  return phanLoai(
    so.value,
    cach,
    [[kq.pp, 0.005 * kq.pp]],
    [
      [
        h.m1 * kq.vp,
        0.005 * h.m1 * kq.vp,
        "Sau va chạm hai xe dính nhau, cùng đi với v': khối lượng là m1 + m2, không chỉ m1.",
      ],
      [
        h.m2 * kq.vp,
        0.005 * h.m2 * kq.vp,
        "Sau va chạm hai xe dính nhau, cùng đi với v': khối lượng là m1 + m2, không chỉ m2.",
      ],
      [kq.pp * 100, 0.01 * kq.pp * 100, "Tấm cản quang rộng 5,00 cm: đổi ra 0,0500 m trước khi chia."],
      [kq.vp, 0.005 * kq.vp, "Đó mới là tốc độ v'; còn phải nhân với m1 + m2."],
    ],
  );
}

/** δ (%) chấm theo p, p' CỦA HỌC SINH (đã được nhận đúng) để không phạt làm tròn hợp lí ở hai ô trước. */
export function chamDelta(raw: string, kq: KetQuaHang, pHs = kq.p, ppHs = kq.pp): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const d = (Math.abs(ppHs - pHs) / pHs) * 100;
  const cach = `δ = |p' − p| : p = |${vnSo(ppHs, 4)} − ${vnSo(pHs, 4)}| : ${vnSo(pHs, 4)} ≈ ${vnSo(d, 1)} %.`;
  return phanLoai(
    so.value,
    cach,
    [
      [d, 0.15],
      [kq.delta * 100, 0.15],
    ],
    [
      [d / 100, 0.0015, "Đó là δ dạng số thập phân; ô này ghi theo %, nhân thêm 100."],
      [-d, 0.15, "Độ lệch lấy trị tuyệt đối nên không âm."],
      [Math.abs(ppHs - pHs), 0.0003, "Đó là |p' − p| (kg·m/s); còn phải chia cho p rồi đổi ra %."],
    ],
  );
}

export function chamEps(raw: string, h: Hang, kq: KetQuaHang): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const t1 = h.t1Ms / 1000;
  const t1p = h.t1pMs / 1000;
  const M = h.m1 + h.m2;
  const phanM = DC_M / h.m1 + (2 * DC_M) / M;
  const phanT = DC_T / t1 + DC_T / t1p;
  const e = kq.eps * 100;
  const cach = `ε = Δm/m1 + Δt/t1 + 2Δm/(m1 + m2) + Δt/t1' = 0,001/${g(h.m1)} + 0,001/${g(t1)} + 0,002/${g(M)} + 0,001/${g(t1p)} ≈ ${vnSo(e, 1)} %.`;
  return phanLoai(
    so.value,
    cach,
    [[e, 0.1]],
    [
      [e - (DC_M / M) * 100, 0.06, "m1 + m2 là hai lần cân nên sai số của nó là 2Δm = 0,002 kg."],
      [e / 2, 0.08, "Bài này lấy sai số dụng cụ bằng 1 độ chia (0,001 kg; 0,001 s), không phải nửa độ chia."],
      [
        e - (phanT / 2) * 100,
        0.06,
        "Bài này lấy sai số dụng cụ của đồng hồ bằng 1 độ chia (0,001 s), không phải nửa độ chia.",
      ],
      [phanT * 100, 0.08, "Thiếu phần sai số của khối lượng (Δm/m1 và 2Δm/(m1 + m2))."],
      [phanM * 100, 0.08, "Thiếu phần sai số của thời gian (Δt/t1 và Δt/t1')."],
      [kq.eps, 0.001, "Đó là ε dạng số thập phân; ô này ghi theo %, nhân thêm 100."],
    ],
  );
}

export { vnSo };
