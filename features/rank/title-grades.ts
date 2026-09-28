// Lớp gợi ý cho từng danh hiệu chuyên môn (kind "specialist"), suy ra từ question_topics.grade
// qua rank_title_topics — xem docs/supabase-migration-rank-system.sql + rank_title_topics.
// Chỉ liệt kê lớp 10/11/12 (chương trình THPT); danh hiệu thuần KHTN9 (Kẻ Bẻ Cong Ánh Sáng,
// Pháp Sư Thấu Kính) không có lớp THPT nên không xuất hiện trong lộ trình này.
// Cố định thành config tĩnh thay vì tính lại qua RPC vì ánh xạ chủ đề→lớp theo chương trình,
// hiếm khi đổi — tránh thêm round-trip Supabase cho trang rank.
export const SPECIALIST_TITLE_GRADES: Record<string, ("10" | "11" | "12")[]> = {
  // Cơ học — Lớp 10
  bac_thay_gia_toc: ["10"],
  chien_than_newton: ["10"],
  chua_te_dong_luong: ["10"],
  ke_pha_the_can_bang: ["10"],
  ke_san_quy_dao: ["10"],
  nguoi_giu_nang_luong: ["10"],
  vu_cong_quy_dao: ["10"],

  // Dao động và sóng — Lớp 11 (Chúa Tể Của Những Loại Sóng trải sang cả Lớp 12)
  bac_thay_nhip_dao_dong: ["11"],
  chua_te_song: ["11", "12"],
  ke_dieu_khien_cong_huong: ["11"],
  nguoi_giu_nut_song: ["11"],
  phap_su_giao_thoa: ["11"],
  tho_san_tan_so: ["11"],

  // Điện và từ — chia Lớp 11 (điện trường/mạch điện) và Lớp 12 (từ trường/điện xoay chiều)
  bac_thay_mach_dien: ["11"],
  ke_tich_tru_loi_dinh: ["11"],
  phap_su_dien_truong: ["11"],
  chua_te_tu_truong: ["12"],
  ke_danh_thuc_dong_dien: ["12"],
  nguoi_truyen_nang_luong: ["12"],
  vu_cong_lech_pha: ["12"],

  // Nhiệt học — Lớp 12
  bac_thay_chuyen_the: ["12"],
  bac_thay_noi_nang: ["12"],
  chua_te_ap_suat: ["12"],
  hoa_phap_su: ["12"],
  ke_thuan_hoa_phan_tu: ["12"],
  nguoi_giu_can_bang_nhiet: ["12"],

  // Vật lý hiện đại — Lớp 12 (lượng tử, hạt nhân)
  ke_giai_ma_phong_xa: ["12"],
  nguoi_giu_loi_hat_nhan: ["12"],
};

export const ROADMAP_GRADES: ("10" | "11" | "12")[] = ["10", "11", "12"];

export const GRADE_LABELS: Record<"10" | "11" | "12", string> = {
  "10": "Lớp 10",
  "11": "Lớp 11",
  "12": "Lớp 12",
};
