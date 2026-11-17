import type { ReactNode } from "react";

/**
 * features/lessons/btm-trinh-chieu/types.ts
 *
 * TRÌNH CHIẾU BÀI TẬP MẪU (thầy duyệt mẫu 17/11/2026) — chế độ chiếu lên tivi khi thầy chữa bài trên lớp.
 * Bố cục theo cách thầy trình bày bảng: TRÁI là "tóm đề" (Cho/Tìm + hình vẽ theo bước + bảng trạng thái điền dần),
 * PHẢI là lời giải từng bước — mỗi bước mở bằng câu hỏi cho cả lớp, bấm tiếp mới hiện từng dòng như viết bảng.
 *
 * Nguồn dữ liệu: mọi dạng đã soạn theo skill soan-bai-tap-mau TỰ chiếu được (tu-dang.ts đọc `buoc`, `tom_de`,
 * `cong_cu`, `solution_html`). Trường tuỳ chọn `trinh_chieu` trên dạng chỉ để thầy/skill viết đè chỗ cần
 * (câu hỏi lớp khác câu hỏi HS tự làm, chia dòng khác, bảng trạng thái ①②).
 */

/** Một dòng "viết bảng" của bước. Hiện ra lần lượt; khi dòng hiện, hình và bảng cập nhật theo. */
export interface ChieuDong {
  html: string;
  /** `ket_qua` đóng khung (kết quả của bước), `ghi_chu` chữ nhỏ (nhận xét), `bay` ⚠ lỗi hay gặp. */
  kieu?: "ket_qua" | "ghi_chu" | "bay";
  /** Lớp hình bật thêm khi dòng này hiện (chỉ dùng cho hình tự vẽ của trang /dev; hình `cong_cu` vẽ theo số bước). */
  hinh?: string[];
  /** Ô bảng trạng thái điền khi dòng này hiện: khoá `<hang>.<cot>` (vd `p.1`), giá trị là TeX. */
  bang?: Record<string, string>;
}

/** Phương án "bước tiếp theo làm gì" để cả lớp chọn (lấy từ `buoc[].chon_buoc_ke`). */
export interface ChieuLuaChon {
  text: string;
  dung: boolean;
  vi_sao?: string;
}

export interface ChieuBuoc {
  /** Tên bước = ý chính, giống dòng thầy gạch chân trên bảng. */
  tieu_de: string;
  /** Câu hỏi đặt cho cả lớp trước khi giải (bấm tiếp mới hiện lời giải). */
  hoi?: string;
  /** Phương án cho lớp chọn; dòng giải đầu tiên hiện thì đánh dấu phương án đúng. */
  lua_chon?: ChieuLuaChon[];
  dong: ChieuDong[];
  /** Một dòng tóm lại bước khi đã qua bước sau (giữ "lịch sử bảng" mà không chiếm chỗ). */
  tom_tat: string;
}

export interface ChieuBangTrangThai {
  /** Hàng: id + nhãn TeX (kèm đơn vị như thầy ghi ở lề bảng). */
  hang: { id: string; nhan: string; don_vi?: string }[];
  /** Cột trạng thái: id + nhãn (①, ②). */
  cot: { id: string; nhan: string }[];
  /** Ô chưa biết cần tìm — hiện "?" đóng khung từ đầu. */
  can_tim?: string[];
}

/** Ngữ cảnh vẽ hình: số bước đã giải xong (lớp hình), bước đang xem, các lớp tự đặt tên đã bật. */
export interface ChieuHinhCtx {
  layer: number;
  step: number;
  lop: Set<string>;
}

/** Một dạng đã sẵn sàng chiếu (sau tu-dang.ts, hoặc soạn tay ở trang /dev). */
export interface ChieuBai {
  nhan: string;
  dang?: string;
  de_html: string;
  tom_de?: { cho: string[]; tim: string[] };
  /** Khung "Kiến thức cần gọi lại" — chiếu thành một nhịp sau đề. */
  kien_thuc_html?: string;
  hinh?: (ctx: ChieuHinhCtx) => ReactNode;
  /** Lớp hình bật sẵn từ đầu (hình tự vẽ). */
  hinh_dau?: string[];
  bang?: ChieuBangTrangThai;
  buoc: ChieuBuoc[];
  dap_so: string;
  nhan_dang?: string;
  bay?: string[];
}

/** Trường tuỳ chọn `trinh_chieu` của LessonWorkedQuestion — viết đè từng phần của bản tự sinh (giữ đúng thứ tự bước). */
export interface ChieuGhiDe {
  bang?: ChieuBangTrangThai;
  /** Phần tử thứ i viết đè bước i; `null`/thiếu = giữ bản tự sinh. */
  buoc?: (Partial<Pick<ChieuBuoc, "hoi" | "dong" | "tom_tat">> | null)[];
  bay?: string[];
}
