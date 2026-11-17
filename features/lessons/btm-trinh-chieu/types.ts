/**
 * features/lessons/btm-trinh-chieu/types.ts
 *
 * TRÌNH CHIẾU BÀI TẬP MẪU (mẫu thử 17/11/2026) — dữ liệu cho chế độ chiếu lên tivi khi thầy chữa bài trên lớp.
 * Bố cục theo cách thầy trình bày bảng: TRÁI là "tóm đề" (Cho/Tìm + hình vẽ + bảng trạng thái, điền dần),
 * PHẢI là lời giải từng bước — mỗi bước mở bằng một câu hỏi cho cả lớp, bấm tiếp mới hiện từng dòng như viết bảng.
 *
 * Định dạng chữ: chuỗi HTML ngắn, công thức trong `$…$` (KaTeX). Dự kiến gắn thành trường `trinh_chieu`
 * của LessonWorkedQuestion khi thầy duyệt mẫu — hiện chưa ghi DB.
 */

/** Một dòng "viết bảng" của bước. Hiện ra lần lượt; khi dòng hiện, hình và bảng cập nhật theo. */
export interface ChieuDong {
  html: string;
  /** Kiểu dòng: `ket_qua` đóng khung (kết quả của bước), `ghi_chu` chữ nhỏ (nhận xét/bẫy). */
  kieu?: "ket_qua" | "ghi_chu";
  /** Lớp hình bật thêm khi dòng này hiện (id lớp do hình của bài tự định nghĩa). */
  hinh?: string[];
  /** Ô bảng trạng thái điền khi dòng này hiện: khoá `<hang>.<cot>` (vd `p.1`). */
  bang?: Record<string, string>;
}

export interface ChieuBuoc {
  /** Tên bước = ý chính, giống dòng thầy gạch chân trên bảng. */
  tieu_de: string;
  /** Câu hỏi đặt cho cả lớp trước khi giải (bấm tiếp mới hiện lời giải). */
  hoi?: string;
  dong: ChieuDong[];
  /** Một dòng tóm lại bước khi đã qua bước sau (giữ "lịch sử bảng" mà không chiếm chỗ). */
  tom_tat: string;
}

export interface ChieuBangTrangThai {
  /** Hàng: id + nhãn (kèm đơn vị như thầy ghi ở lề bảng). */
  hang: { id: string; nhan: string; don_vi?: string }[];
  /** Cột trạng thái: id + nhãn (①, ②). */
  cot: { id: string; nhan: string }[];
  /** Ô chưa biết cần tìm — hiện "?" đóng khung từ đầu. */
  can_tim?: string[];
}

export interface ChieuBai {
  nhan: string;
  dang: string;
  de_html: string;
  tom_de: { cho: string[]; tim: string[] };
  /** Lớp hình bật sẵn từ đầu. */
  hinh_dau: string[];
  bang?: ChieuBangTrangThai;
  buoc: ChieuBuoc[];
  dap_so: string;
  nhan_dang?: string;
  bay?: string[];
}
