/**
 * Lộ trình kiểu Duolingo — GĐ1 (docs/LO-TRINH-KIEU-DUOLINGO.md): bản đồ CHỈ ĐỌC từ dữ liệu sẵn có, không bảng mới.
 * Mỗi bài = tối đa 5 nút theo thứ tự Hiểu → Nhớ → Mẫu → Luyện → Chốt; bài thiếu loại mục nào thì bỏ nút đó (N3).
 * Hàm thuần (không React, không mạng) để trang và script thử dùng chung.
 */
import type { LessonItemKind } from "@/features/lessons/types";
import type { MasteryLevel } from "@/services/mastery";

export type NutLoai = "hieu" | "nho" | "mau" | "luyen" | "chot";

export const NUT_NHAN: Record<NutLoai, string> = {
  hieu: "Hiểu",
  nho: "Nhớ",
  mau: "Mẫu",
  luyen: "Luyện",
  chot: "Chốt",
};

export const NUT_MO_TA: Record<NutLoai, string> = {
  hieu: "Đọc lý thuyết và trả lời câu kiểm tra nhanh",
  nho: "Ôn 5 phút: lật thẻ ý chính",
  mau: "Tự giải từng bước một bài mẫu",
  luyen: "Luyện câu cơ bản",
  chot: "Làm bài kiểm tra của bài",
};

export interface MucGon {
  id: number;
  lesson_id: number;
  kind: LessonItemKind;
  exam_ids: number[];
}

export interface Nut {
  loai: NutLoai;
  href: string;
  /** null = chưa biết (khách chưa đăng nhập). */
  xong: boolean | null;
}

export interface BaiTrenDuong {
  id: number;
  ten: string;
  so: string | null;
  nut: Nut[];
  mastery: MasteryLevel | null;
  /** Số thẻ Ôn 5 phút đã tới hạn của bài. */
  denHan: number;
}

export interface DauDaHoc {
  completedItems: Set<number>;
  completedExams: Set<number>;
}

export interface TheBai {
  /** Bài có bộ thẻ Ôn 5 phút. */
  coThe: boolean;
  /** Đã ôn lượt đầu (có ít nhất một thẻ trong lịch). null = chưa biết. */
  daOn: boolean | null;
  denHan: number;
}

function mucXong(m: MucGon, dau: DauDaHoc): boolean {
  const examsDone = m.exam_ids.length > 0 && m.exam_ids.every((id) => dau.completedExams.has(id));
  return dau.completedItems.has(m.id) || examsDone;
}

const TAB: Partial<Record<LessonItemKind, string>> = {
  ly_thuyet: "ly-thuyet",
  bai_tap_mau: "bai-tap-mau",
  luyen_tap: "luyen-tap",
  kiem_tra: "kiem-tra",
};

const KIND_CUA_NUT: Partial<Record<NutLoai, LessonItemKind>> = {
  hieu: "ly_thuyet",
  mau: "bai_tap_mau",
  luyen: "luyen_tap",
  chot: "kiem_tra",
};

/** "Bài 22. Từ thông…" → { so: "22", ten: "Từ thông…" }. */
export function tachTenBai(title: string): { so: string | null; ten: string } {
  const m = title.match(/^\s*Bài\s+(\d+)\s*[.:]\s*(.*)$/i);
  return m ? { so: m[1], ten: m[2] } : { so: null, ten: title };
}

export function dungBanDo(input: {
  lessons: { id: number; title: string }[];
  items: MucGon[];
  dau: DauDaHoc | null;
  the: Map<number, TheBai>;
  mastery: Map<number, MasteryLevel>;
}): BaiTrenDuong[] {
  const { lessons, items, dau, the, mastery } = input;
  const theoBai = new Map<number, MucGon[]>();
  for (const it of items) theoBai.set(it.lesson_id, [...(theoBai.get(it.lesson_id) ?? []), it]);

  return lessons.map((l) => {
    const muc = theoBai.get(l.id) ?? [];
    const base = `/lop-hoc/bai?id=${l.id}`;
    const nut: Nut[] = [];
    // Không đọc được mục nào (khách: RLS chỉ mở mục của bài xem thử) → không vẽ nút, trang chỉ hiện "Mở bài".
    if (muc.length > 0)
      for (const loai of ["hieu", "nho", "mau", "luyen", "chot"] as NutLoai[]) {
        if (loai === "nho") {
          const t = the.get(l.id);
          if (t?.coThe) nut.push({ loai, href: `${base}#muc=ly-thuyet`, xong: dau ? t.daOn : null });
          continue;
        }
        const kind = KIND_CUA_NUT[loai]!;
        const cung = muc.filter((m) => m.kind === kind);
        if (cung.length === 0) continue;
        nut.push({ loai, href: `${base}#muc=${TAB[kind]}`, xong: dau ? cung.every((m) => mucXong(m, dau)) : null });
      }
    const { so, ten } = tachTenBai(l.title);
    return { id: l.id, ten, so, nut, mastery: mastery.get(l.id) ?? null, denHan: the.get(l.id)?.denHan ?? 0 };
  });
}

/** Nút "Học tiếp" (L5): nút chưa xong đầu tiên theo thứ tự con đường. Khách: nút đầu tiên. */
export function nutTiepTheo(bai: BaiTrenDuong[]): { bai: BaiTrenDuong; nut: Nut } | null {
  for (const b of bai) for (const n of b.nut) if (n.xong !== true) return { bai: b, nut: n };
  return null;
}

export function demXong(bai: BaiTrenDuong[]): { xong: number; tong: number } {
  let xong = 0;
  let tong = 0;
  for (const b of bai)
    for (const n of b.nut) {
      tong += 1;
      if (n.xong) xong += 1;
    }
  return { xong, tong };
}
