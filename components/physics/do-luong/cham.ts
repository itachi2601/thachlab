/**
 * components/physics/do-luong/cham.ts — số học phần chấm của bốn dụng cụ đo (Gói A). Không React để thử bằng `npx tsx`.
 * Mọi phép tính làm trên SỐ NGUYÊN đơn vị nhỏ (phần trăm mm…) để tránh lỗi dấu phẩy động (0,1 + 0,2).
 * Quy ước ghi kết quả theo L10 Bài 3 (lesson 48): số chữ số sau dấu phẩy do dụng cụ quyết định (Bẫy 3 "ghi thêm số 0").
 */

import { docSo, soNguyenRaChuoi, type KetQuaCham } from "./chung";

/* ---------------- Thước kẹp ---------------- */

/** Ba loại du xích: p = độ chính xác (phần trăm mm), N vạch dài `len` mm → mỗi khoảng du xích = len/N mm. */
export const DU_XICH = {
  10: { pH: 10, N: 10, len: 9, nhanMoi: 5, decimals: 1, ten: "0,1 mm" },
  5: { pH: 5, N: 20, len: 19, nhanMoi: 4, decimals: 2, ten: "0,05 mm" },
  2: { pH: 2, N: 50, len: 49, nhanMoi: 5, decimals: 2, ten: "0,02 mm" },
} as const;
export type LoaiDuXich = keyof typeof DU_XICH;

/** Tách số đọc (phần trăm mm) thành phần nguyên n (mm) và số thứ tự vạch du xích trùng k. */
export function tachThuocKep(zH: number, pH: LoaiDuXich) {
  const n = Math.floor(zH / 100);
  const k = (zH - n * 100) / pH;
  return { n, k };
}

/** Chuỗi số đọc đúng cách ghi của loại du xích: (1234, 2) → "12,34"; (1230, 10) → "12,3". */
export function ghiThuocKep(zH: number, pH: LoaiDuXich) {
  const d = DU_XICH[pH].decimals;
  return soNguyenRaChuoi(d === 1 ? zH / 10 : zH, d);
}

/**
 * Chấm số học sinh gõ cho số đọc thật zH (phần trăm mm). null = gõ không phải số.
 * Đúng giá trị nhưng sai số chữ số sau dấu phẩy → "chu-so" (không tính vào chuỗi đúng).
 */
export function chamThuocKep(raw: string, zH: number, pH: LoaiDuXich): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const { N, decimals, ten } = DU_XICH[pH];
  const { n, k } = tachThuocKep(zH, pH);
  const dapAn = `${ghiThuocKep(zH, pH)} mm`;
  const xH = k * pH;
  const phanLe = `${k} × ${soNguyenRaChuoi(pH, 2).replace(/0$/, "")} = ${soNguyenRaChuoi(decimals === 1 ? xH / 10 : xH, decimals)} mm`;

  const sH = Math.round(so.value * 100);
  const chinhXacToiPhanTram = Math.abs(so.value * 100 - sH) < 1e-6;

  if (chinhXacToiPhanTram && sH === zH) {
    if (so.decimals === decimals) return { loai: "dung", loi: `Số đọc ${dapAn}.` };
    return {
      loai: "chu-so",
      loi: `Du xích ${ten} cho kết quả tới ${decimals === 1 ? "một" : "hai"} chữ số sau dấu phẩy: ghi ${dapAn}. Chữ số cuối cho biết dụng cụ đo tới đâu.`,
    };
  }

  const nHs = Math.floor(so.value + 1e-9);
  if (nHs !== n) {
    if (k === 0 && nHs === n + 1) {
      return {
        loai: "sai",
        loi: `Vạch 0 du xích trùng đúng vạch ${n} mm (vạch cuối du xích cũng trùng, đừng đếm vạch cuối). Phần lẻ bằng 0: ${dapAn}.`,
      };
    }
    if (nHs === n + 1) {
      return {
        loai: "sai",
        loi: `Phần nguyên lấy vạch thước chính ngay TRƯỚC vạch 0 du xích (${n} mm), không lấy vạch sau nó. Đáp số ${dapAn}.`,
      };
    }
    return {
      loai: "sai",
      loi: `Phần nguyên: vạch 0 du xích nằm sau vạch ${n} mm của thước chính → ${n} mm. Phần lẻ: vạch số ${k} trùng, ${phanLe}. Đáp số ${dapAn}.`,
    };
  }

  const leHs = sH - n * 100;
  if (chinhXacToiPhanTram && leHs % pH === 0 && leHs / pH <= N) {
    const kHs = leHs / pH;
    return {
      loai: "sai",
      loi: `Phần nguyên ${n} mm đúng. Em lấy vạch du xích số ${kHs}; vạch thẳng hàng nhất là vạch số ${k}: ${phanLe}. Đáp số ${dapAn}.`,
    };
  }
  return {
    loai: "sai",
    loi: `Phần nguyên ${n} mm đúng. Phần lẻ = số thứ tự vạch du xích trùng × ${ten}; vạch số ${k} trùng nên ${phanLe}. Đáp số ${dapAn}.`,
  };
}

/** Số đọc ngẫu nhiên (phần trăm mm), n ≤ maxN; ~15% ca vạch 0 trùng, ~10% ca vạch kế cuối trùng (ca biên). */
export function ngauNhienThuocKep(pH: LoaiDuXich, maxN: number, tranh?: number): number {
  const { N } = DU_XICH[pH];
  for (let lan = 0; lan < 20; lan++) {
    const n = Math.floor(Math.random() * (maxN + 1));
    const r = Math.random();
    const k = r < 0.15 ? 0 : r < 0.25 ? N - 1 : 1 + Math.floor(Math.random() * (N - 2));
    const z = n * 100 + k * pH;
    if (z !== tranh) return z;
  }
  return 0;
}
