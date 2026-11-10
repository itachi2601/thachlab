// Danh mục bài đọc SHCN (bản sinh viên) — dữ liệu sinh bởi scripts/gen-shcn-bai-doc.mjs.
// File này dùng được cả ở client (editor GVCN, thẻ tuần); phần đọc Markdown nằm ở bai-doc-server.ts.
import list from "./bai-doc.json";

export interface BaiDoc {
  /** "hk1/b03" — giá trị lưu ở homeroom_weekly_sessions.lesson_key. */
  key: string;
  hk: number;
  /** 0 = khởi động, 15 = tổng kết. */
  bai: number;
  ten: string;
  chu_de: string;
  trong_tam: string;
}

export const BAI_DOC: BaiDoc[] = list;

export function findBaiDoc(key: string | null | undefined): BaiDoc | null {
  if (!key) return null;
  return BAI_DOC.find((item) => item.key === key) ?? null;
}

export function baiDocHref(key: string): string {
  return `/sinh-hoat/${key}`;
}

export function nhanBai(bai: number): string {
  if (bai === 0) return "Khởi động";
  if (bai === 15) return "Tổng kết";
  return `Bài ${bai}`;
}
