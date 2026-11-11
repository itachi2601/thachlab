/**
 * Sơ đồ tư duy tổng hợp một chương (mẫu đầu: Vật lí 12, Chương 3 — 11/11/2026).
 * Một chương = 1 nút trung tâm + ≤ 5 nhánh (G1: trí nhớ làm việc giữ ~4 khối); mỗi nhánh ≤ 4 ý con.
 * Chữ trong `chot`, `y`, `bay`, `nhiemVu` có thể chứa công thức `$…$` (KaTeX qua ContentHtml).
 */

export type SoDoYCon = {
  /** từ khoá ≤ 4 chữ — thứ mắt dừng lại khi quét (G3) */
  tu: string;
  /** một dòng giải nghĩa, không chứa công thức cần nhớ (để chế độ Tự kiểm che được công thức) */
  y: string;
  /** công thức cần nhớ (LaTeX, không kèm $) — bị che ở chế độ Tự kiểm */
  ct?: string;
};

export type SoDoMoPhong =
  | { kieu: "phet"; ten: string; src: string; nhiemVu: string }
  /** mô phỏng/clip nằm sẵn trong bài học: mở bài ở tab mới */
  | { kieu: "bai"; ten: string; href: string; nhiemVu: string };

export type SoDoNhanh = {
  id: string;
  ten: string;
  /** hình khoá của nhánh (vẽ trong components/lessons/so-do/HinhNhanh.tsx) */
  hinh:
    | "tu_truong"
    | "luc_tu"
    | "cam_ung"
    | "xoay_chieu"
    | "song_dien_tu"
    | "hop_luc"
    | "newton"
    | "cac_luc"
    | "dong_luc_hoc"
    | "moment";
  /** bài học thuộc nhánh: số bài trong SGK + lesson id trên web */
  bai: { so: number; id: number; ten: string }[];
  /** câu chốt ≤ 12 chữ */
  chot: string;
  /** công thức lõi của nhánh (LaTeX, không kèm $) */
  ct: string;
  /** vì sao nhánh này nối tiếp nhánh trước (mạch truyện của chương) */
  noiTiep?: string;
  yCon: SoDoYCon[];
  /** bẫy hay sập nhất — đúng một dòng */
  bay: string;
  moPhong?: SoDoMoPhong;
};

export type SoDoChuong = {
  lop: string;
  chuong: string;
  /** chữ ở nút trung tâm */
  tam: string;
  /** một câu tóm cả chương */
  mach: string;
  nhanh: SoDoNhanh[];
};
