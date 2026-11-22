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

type ThamSo = {
  ky_hieu: string;
  min?: number;
  max?: number;
  mac_dinh?: number;
  buoc?: number;
  gia_tri?: number;
  sai_so_do?: number;
};
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
export const TRE_TU_DU_MS = Math.round(
  ((tn.goi_y_mo_phong as { bat_tat?: { tre_ht: number[] } }).bat_tat?.tre_ht[1] ?? 0.005) * 1000,
);

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

/**
 * Chọn ứng viên GẦN NHẤT (đáp án đúng gồm cả bản làm tròn Δt về 0,001 s, vì ô Δt đã nhận cách làm tròn đó) trong số các ứng viên còn trong dung sai (đáp án đúng + các lỗi thật), để dung sai của đáp án
 * đúng có thể rộng (nhận làm tròn trung gian) mà một lỗi nằm gần vẫn bị gọi đúng tên.
 */
function phanLoai(x: number, cach: string, dung: [number, number][], loi: [number, number, string][]): KetQuaCham {
  // Đáp án đúng được ưu tiên: còn trong dung sai là đúng, dù một lỗi nào đó cũng gần (làm tròn hợp lí không bị phạt).
  if (dung.some(([v, tol]) => gan(x, v, tol))) return { loai: "dung", loi: cach };
  let tot: { d: number; msg: string } | null = null;
  for (const [v, tol, msg] of loi) {
    const d = Math.abs(x - v);
    if (gan(x, v, tol) && (!tot || d < tot.d)) tot = { d, msg };
  }
  return { loai: "sai", loi: tot ? `${tot.msg} ${cach}` : cach };
}

export function chamDt(raw: string, kq: KetQuaLoat): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const cach = `Độ lệch từng lần (cột thứ ba) trung bình ${vnSo(kq.dbar, 4)} s; cộng sai số dụng cụ ${vnSo(DC_T, 3)} s: Δt ≈ ${vnSo(kq.dt, 4)} s.`;
  return phanLoai(
    so.value,
    cach,
    [
      [kq.dt, 0.00045],
      [Math.round(kq.dt * 1000) / 1000, 1e-7],
    ],
    [
      [kq.dbar, 0.0003, "Em mới có phần phân tán, quên cộng sai số dụng cụ: lấy trung bình không xoá được Δt_dc."],
      [
        kq.dbar + DC_T / 2,
        0.0002,
        "Bài này lấy sai số dụng cụ của đồng hồ hiện số bằng 1 độ chia (0,001 s), không phải nửa độ chia.",
      ],
    ],
  );
}

export function chamG(raw: string, s: number, kq: KetQuaLoat): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const cach = `ḡ = 2s : t̄² = 2 · ${vnSo(s, 3)} : ${vnSo(kq.tbar, 4)}² ≈ ${vnSo(kq.g, 2)} m/s².`;
  return phanLoai(
    so.value,
    cach,
    [[kq.g, 0.05]],
    [
      [kq.g / 2, 0.05, "Em tính s : t², quên nhân 2 (từ s = gt²/2)."],
      [(2 * s) / kq.tbar, 0.05, "Em chia cho t̄, chưa bình phương."],
    ],
  );
}

/**
 * Δg chấm theo Δt và ḡ CỦA HỌC SINH ở hai ô trước (nếu ô đó đúng; sai thì dùng số đúng): làm tròn Δt về 0,001 s là hợp lí
 * và kéo Δg đi tới 0,01 m/s², nên so với số máy tính từ Δt đầy đủ sẽ chấm oan. Dung sai 0,0055 = làm tròn 2 chữ số thập phân.
 * Giới hạn đã biết: ở s ≥ 0,8 m phần Δs/s chỉ cỡ 0,01 m/s² (dưới 0,15 %), ghi 2 chữ số thập phân không phân biệt được
 * "quên Δs/s" với đáp án đúng nên được nhận đúng; ở s = 0,5 m trở xuống thì bắt được.
 */
export function chamDg(raw: string, s: number, kq: KetQuaLoat, dtHs = kq.dt, gHs = kq.g): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const voi = (dt: number, heSo: number, coDs: boolean) => ((coDs ? DC_S / s : 0) + (heSo * dt) / kq.tbar) * gHs;
  const delta = DC_S / s + (2 * dtHs) / kq.tbar;
  const dg = voi(dtHs, 2, true);
  const cach = `δ = Δs/s + 2Δt/t̄ = ${vnSo(DC_S, 3)}/${vnSo(s, 3)} + 2 · ${vnSo(dtHs, 4)}/${vnSo(kq.tbar, 4)} ≈ ${vnSo(delta, 4)}; Δg = δ · ḡ ≈ ${vnSo(dg, 2)} m/s².`;
  const sai: [number, number, string][] = [
    [voi(dtHs, 1, true), 0.008, "Thiếu hệ số 2 trước Δt/t̄: t² = t · t nên phần của t tính hai lần."],
    [voi(dtHs, 2, false), 0.008, "Thiếu phần Δs/s của thước (0,001 m chia cho s)."],
    [
      voi(kq.dbar + DC_T / 2, 2, true),
      0.008,
      "Bài này lấy sai số dụng cụ 1 độ chia (0,001 s) trong Δt, không phải nửa độ chia.",
    ],
    [delta, 0.002, "Đó là sai số tương đối δ; Δg = δ · ḡ mới là sai số tuyệt đối (m/s²)."],
    [delta * 100, 0.2, "Đó là sai số tương đối δ tính theo %; Δg = δ · ḡ mới là sai số tuyệt đối (m/s²)."],
  ];
  return phanLoai(so.value, cach, [[dg, 0.0055]], sai);
}
