/**
 * components/physics/thuc-hanh/cham-roi-tu-do.ts — số học của thí nghiệm ảo "Đo gia tốc rơi tự do" (Gói C,
 * docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5). Không React để thử bằng `npx tsx`.
 *
 * Thông số lấy từ content/thi-nghiem/tn-l10-do-g-01.json (một nguồn). Quy ước sai số theo đúng bài L10 Bài 11 (lesson 56):
 *   Δt = trung bình |t_i − t̄| + Δt_dc, Δt_dc = 1 độ chia = 0,001 s;  δ = Δs/s + 2Δt/t̄;  Δg = δ·ḡ.
 * Thời gian giữ bằng SỐ NGUYÊN mili giây (đồng hồ chia 0,001 s) để tránh lỗi dấu phẩy động.
 */

import tn from "@/content/thi-nghiem/tn-l10-do-g-01.json";
import { docSo, type KetQuaCham } from "@/components/physics/do-luong/chung";

type ThamSo = { ky_hieu: string; min?: number; max?: number; mac_dinh?: number; buoc?: number; gia_tri?: number; sai_so_do?: number };
const TS = Object.fromEntries((tn.tham_so as ThamSo[]).map((p) => [p.ky_hieu, p])) as Record<string, ThamSo>;

export const G_THAT = TS.g_that.gia_tri ?? 9.8; // m/s²
export const DC_T = TS.dcnn_t.gia_tri ?? 0.001; // s — độ chia đồng hồ = sai số dụng cụ (bài 56: lấy 1 độ chia)
export const DC_S = TS.dcnn_s.gia_tri ?? 0.001; // m — độ chia thước
/** Độ cao thả, đơn vị cm (bước 5 cm) để cộng trừ không lệch. */
export const S_CM = {
  min: Math.round((TS.s.min ?? 0.2) * 100),
  max: Math.round((TS.s.max ?? 1) * 100),
  macDinh: Math.round((TS.s.mac_dinh ?? 0.5) * 100),
  buoc: Math.round((TS.s.buoc ?? 0.05) * 100),
};
/** Biên độ nhiễu ngẫu nhiên mỗi lần thả, ms (tham_so "nhieu"). */
export const NHIEU_MS = Math.round((TS.nhieu.mac_dinh ?? 0.002) * 1000);
/** Độ trễ do từ dư khi bật, ms (goi_y_mo_phong.bat_tat.tre_ht[1]). */
export const TRE_TU_DU_MS = Math.round(((tn.goi_y_mo_phong as { bat_tat?: { tre_ht: number[] } }).bat_tat?.tre_ht[1] ?? 0.004) * 1000);

/** Một số nguyên ngẫu nhiên trong [−NHIEU_MS, NHIEU_MS] (T8: các lần đo khác nhau thật). */
export const nhieuNgauNhien = () => Math.floor(Math.random() * (2 * NHIEU_MS + 1)) - NHIEU_MS;

/** Thời gian rơi thật (ms, chưa làm tròn) từ độ cao s (m). */
export const tRoiMs = (s: number) => Math.sqrt((2 * s) / G_THAT) * 1000;

/** Số chỉ đồng hồ (ms nguyên): thời gian rơi + trễ từ dư + nhiễu, làm tròn tới độ chia. */
export const soChiMs = (s: number, tuDu: boolean, nhieu: number) =>
  Math.round(tRoiMs(s) + (tuDu ? TRE_TU_DU_MS : 0) + nhieu);

export type KetQuaLoat = {
  tbar: number; // s
  lech: number[]; // |t_i − t̄|, s
  dbar: number; // trung bình độ lệch, s
  dt: number; // Δt = dbar + DC_T, s
  g: number; // ḡ, m/s²
  delta: number; // sai số tương đối
  dg: number; // Δg, m/s²
};

/** Xử lí một loạt đo đúng như bài 56. tMs: các số chỉ (ms); s: độ cao (m). */
export function tinhLoat(tMs: number[], s: number): KetQuaLoat {
  const n = tMs.length;
  const tbar = tMs.reduce((a, b) => a + b, 0) / n / 1000;
  const lech = tMs.map((t) => Math.abs(t / 1000 - tbar));
  const dbar = lech.reduce((a, b) => a + b, 0) / n;
  const dt = dbar + DC_T;
  const g = (2 * s) / (tbar * tbar);
  const delta = DC_S / s + (2 * dt) / tbar;
  return { tbar, lech, dbar, dt, g, delta, dg: delta * g };
}

/** Số kiểu Việt: 0.3212 → "0,3212". */
export const vnSo = (x: number, d: number) => x.toFixed(d).replace("-", "−").replace(".", ",");

const gan = (x: number, y: number, tol: number) => Math.abs(x - y) <= tol + 1e-9;

/* ---------------- Chấm bốn ô học sinh tự tính ---------------- */
/* Dung sai đủ rộng để chấp nhận cách làm tròn trung gian hợp lí (t̄ lấy 3 hay 4 chữ số), đủ hẹp để bắt lỗi thật. */

export function chamTbar(raw: string, tMs: number[], kq: KetQuaLoat): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const tong = tMs.reduce((a, b) => a + b, 0) / 1000;
  const cach = `t̄ = (${tMs.map((t) => vnSo(t / 1000, 3)).join(" + ")}) : ${tMs.length} ≈ ${vnSo(kq.tbar, 4)} s.`;
  if (gan(so.value, kq.tbar, 0.0005)) return { loai: "dung", loi: cach };
  if (gan(so.value, tong, 0.001)) return { loai: "sai", loi: `Đó là tổng 5 lần, còn phải chia cho 5. ${cach}` };
  return { loai: "sai", loi: `Cộng 5 số rồi chia 5: ${cach}` };
}

export function chamDt(raw: string, kq: KetQuaLoat): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const cach = `Độ lệch từng lần (cột thứ ba) trung bình ${vnSo(kq.dbar, 4)} s; cộng sai số dụng cụ ${vnSo(DC_T, 3)} s: Δt ≈ ${vnSo(kq.dt, 4)} s.`;
  if (gan(so.value, kq.dt, 0.00045)) return { loai: "dung", loi: cach };
  if (gan(so.value, kq.dbar, 0.0003))
    return { loai: "sai", loi: `Em mới có phần phân tán, quên cộng sai số dụng cụ: lấy trung bình không xoá được Δt_dc. ${cach}` };
  if (gan(so.value, kq.dbar + DC_T / 2, 0.0002))
    return { loai: "sai", loi: `Bài này lấy sai số dụng cụ của đồng hồ hiện số bằng 1 độ chia (0,001 s), không phải nửa độ chia. ${cach}` };
  return { loai: "sai", loi: cach };
}

export function chamG(raw: string, s: number, kq: KetQuaLoat): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const cach = `ḡ = 2s : t̄² = 2 · ${vnSo(s, 3)} : ${vnSo(kq.tbar, 4)}² ≈ ${vnSo(kq.g, 2)} m/s².`;
  if (gan(so.value, kq.g, 0.04)) return { loai: "dung", loi: cach };
  if (gan(so.value, kq.g / 2, 0.04)) return { loai: "sai", loi: `Em tính s : t², quên nhân 2 (từ s = gt²/2). ${cach}` };
  if (gan(so.value, (2 * s) / kq.tbar, 0.05)) return { loai: "sai", loi: `Em chia cho t̄, chưa bình phương. ${cach}` };
  return { loai: "sai", loi: cach };
}

export function chamDg(raw: string, s: number, kq: KetQuaLoat): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const cach = `δ = Δs/s + 2Δt/t̄ = ${vnSo(DC_S, 3)}/${vnSo(s, 3)} + 2 · ${vnSo(kq.dt, 4)}/${vnSo(kq.tbar, 4)} ≈ ${vnSo(kq.delta, 4)}; Δg = δ · ḡ ≈ ${vnSo(kq.dg, 2)} m/s².`;
  if (gan(so.value, kq.dg, 0.025)) return { loai: "dung", loi: cach };
  const quenHai = (DC_S / s + kq.dt / kq.tbar) * kq.g;
  if (gan(so.value, quenHai, 0.012)) return { loai: "sai", loi: `Thiếu hệ số 2 trước Δt/t̄: t² = t · t nên phần của t tính hai lần. ${cach}` };
  if (gan(so.value, kq.delta, 0.002) || gan(so.value, kq.delta * 100, 0.2))
    return { loai: "sai", loi: `Đó là sai số tương đối δ; Δg = δ · ḡ mới là sai số tuyệt đối (m/s²). ${cach}` };
  return { loai: "sai", loi: cach };
}
