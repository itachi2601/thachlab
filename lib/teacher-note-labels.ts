// Nhãn ghi chú của giáo viên lúc dạy — thuần, không đụng supabase (dùng được ở cả chỗ render đồng bộ).
export type TeacherNoteTag = "hs_hieu_sai" | "thieu_hinh" | "vi_du" | "dai_nhanh" | "loi" | "y_tuong";
export type TeacherNoteStatus = "moi" | "da_xem" | "da_xu_ly";

/** Thứ tự = thứ tự nút trong hộp ghi chú; phím 1–6 chọn nhanh nhãn. */
export const TEACHER_NOTE_TAGS: Array<{ value: TeacherNoteTag; label: string }> = [
  { value: "hs_hieu_sai", label: "HS hiểu sai" },
  { value: "thieu_hinh", label: "Thiếu hình / mô phỏng" },
  { value: "vi_du", label: "Ví dụ chưa hay" },
  { value: "dai_nhanh", label: "Dài / quá nhanh" },
  { value: "loi", label: "Lỗi" },
  { value: "y_tuong", label: "Ý tưởng" },
];

export const TEACHER_NOTE_MAX = 1000;
