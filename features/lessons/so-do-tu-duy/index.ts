import type { SoDoChuong } from "@/features/lessons/so-do-tu-duy/types";

/**
 * Sổ đăng ký sơ đồ tư duy theo chương: khoá = `chapters.id` (đối chiếu `public/data/catalog.json`, không đoán).
 * Mỗi chương một file dữ liệu, nạp động để trang lớp không phải gánh nội dung sơ đồ (không thêm round-trip Supabase).
 * Thêm chương mới: skill `.claude/skills/so-do-tu-duy-chuong/SKILL.md`.
 */
const SO_DO: Record<number, () => Promise<SoDoChuong>> = {
  4: () => import("./l12-chuong-3").then((m) => m.L12_CHUONG_3), // Vật lí 12 · Chương 3. Từ trường
};

export function coSoDoChuong(chapterId: number): boolean {
  return chapterId in SO_DO;
}

export function napSoDoChuong(chapterId: number): Promise<SoDoChuong | null> {
  const nap = SO_DO[chapterId];
  return nap ? nap() : Promise.resolve(null);
}

/** Link trang sơ đồ; `lop` = slug lớp để nút quay lại về đúng trang lớp. */
export function soDoHref(chapterId: number, lop?: string): string {
  const p = new URLSearchParams({ chuong: String(chapterId) });
  if (lop) p.set("lop", lop);
  return `/lop-hoc/so-do/?${p.toString()}`;
}
