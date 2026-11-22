/**
 * components/physics/thuc-hanh/cham-chung.ts — phần chấm dùng chung của các thí nghiệm ảo Gói C
 * (docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5). Không React để thử bằng `npx tsx`.
 */

import type { KetQuaCham } from "@/components/physics/do-luong/chung";

/** Số kiểu Việt: 0.3212 → "0,3212". */
export const vnSo = (x: number, d: number) => x.toFixed(d).replace("-", "−").replace(".", ",");

export const gan = (x: number, y: number, tol: number) => Math.abs(x - y) <= tol + 1e-9;

/**
 * Đáp án đúng được ưu tiên: còn trong dung sai của một giá trị đúng là đúng, dù một lỗi nào đó cũng gần (làm tròn hợp lí
 * không bị phạt). Không thì chọn lỗi GẦN NHẤT còn trong dung sai để gọi đúng tên; không khớp lỗi nào thì chỉ hiện cách tính.
 * dung: [giá trị, dung sai][]; loi: [giá trị, dung sai, lời nhắn][].
 */
export function phanLoai(
  x: number,
  cach: string,
  dung: [number, number][],
  loi: [number, number, string][],
): KetQuaCham {
  if (dung.some(([v, tol]) => gan(x, v, tol))) return { loai: "dung", loi: cach };
  let tot: { d: number; msg: string } | null = null;
  for (const [v, tol, msg] of loi) {
    const d = Math.abs(x - v);
    if (gan(x, v, tol) && (!tot || d < tot.d)) tot = { d, msg };
  }
  return { loai: "sai", loi: tot ? `${tot.msg} ${cach}` : cach };
}
