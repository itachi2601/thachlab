import type { TierCode, TitleLevel } from "@/features/rank/types";

/**
 * Ảnh huy hiệu rank & danh hiệu chuyên môn — file WebP 512×512 nền trong suốt trong
 * `public/images/rank/`. Nguồn gốc 1024×1024 nằm ở design system "ThachLab Huy Hiệu"
 * (artifact Claude), tên file giữ nguyên: `rank-<ten>.webp`, `cm-<slug>-<cap>.webp`.
 * Không phóng quá 240 px (size lớn nhất trong UI); 48/96 px dùng thẳng.
 */

const BASE = "/images/rank";

/** Mã bậc (TierCode) → tên file huy hiệu rank. Tên file theo bộ tên cũ, mã bậc không đổi. */
const TIER_FILE: Record<TierCode, string> = {
  tan_binh: "rank-tan-binh",
  chien_binh: "rank-chien-binh",
  tinh_anh: "rank-tinh-anh",
  tinh_nhue: "rank-tinh-nhue",
  dai_su: "rank-dai-su",
  cao_thu: "rank-cao-thu",
  thach_dau: "rank-thach-dau",
};

/** Mã danh hiệu chuyên môn (rank_titles.code, kind = specialist) → slug file ảnh. */
export const SPECIALIST_SLUG: Record<string, string> = {
  // Cơ học
  ke_san_quy_dao: "quy-dao",
  bac_thay_gia_toc: "gia-toc",
  chien_than_newton: "newton",
  ke_pha_the_can_bang: "can-bang",
  chua_te_dong_luong: "dong-luong",
  nguoi_giu_nang_luong: "nang-luong",
  vu_cong_quy_dao: "tron",
  // Dao động và sóng
  bac_thay_nhip_dao_dong: "dao-dong",
  ke_dieu_khien_cong_huong: "cong-huong",
  chua_te_song: "truyen-song",
  phap_su_giao_thoa: "giao-thoa",
  nguoi_giu_nut_song: "song-dung",
  tho_san_tan_so: "tan-so",
  // Điện và từ
  phap_su_dien_truong: "dien-truong",
  ke_tich_tru_loi_dinh: "tu-dien",
  bac_thay_mach_dien: "mach-dien",
  chua_te_tu_truong: "tu-truong",
  ke_danh_thuc_dong_dien: "cam-ung",
  vu_cong_lech_pha: "xoay-chieu",
  nguoi_truyen_nang_luong: "bien-ap",
  // Nhiệt học
  hoa_phap_su: "nhiet-luong",
  bac_thay_chuyen_the: "chuyen-the",
  ke_thuan_hoa_phan_tu: "dong-hoc-phan-tu",
  chua_te_ap_suat: "ap-suat",
  nguoi_giu_can_bang_nhiet: "can-bang-nhiet",
  bac_thay_noi_nang: "noi-nang",
  // Ánh sáng và vật lý hiện đại
  ke_be_cong_anh_sang: "khuc-xa",
  phap_su_thau_kinh: "thau-kinh",
  tho_san_photon: "photon",
  nguoi_giai_ma_nguyen_tu: "nguyen-tu",
  ke_giai_ma_phong_xa: "phong-xa",
  nguoi_giu_loi_hat_nhan: "hat-nhan",
};

const LEVEL_FILE: Record<Exclude<TitleLevel, "don">, string> = {
  thuc_tinh: "thuc-tinh",
  lam_chu: "lam-chu",
  huyen_thoai: "huyen-thoai",
};

/** Đường dẫn ảnh huy hiệu rank theo mã bậc. */
export function tierBadgeSrc(code: TierCode): string {
  return `${BASE}/tiers/${TIER_FILE[code]}.webp`;
}

/**
 * Đường dẫn ảnh danh hiệu chuyên môn theo mã danh hiệu + cấp.
 * Trả về null nếu không phải danh hiệu chuyên môn (collection/achievement chưa có ảnh)
 * hoặc cấp là "don".
 */
export function titleBadgeSrc(code: string, level: TitleLevel | null | undefined): string | null {
  const slug = SPECIALIST_SLUG[code];
  if (!slug || !level || level === "don") return null;
  return `${BASE}/titles/cm-${slug}-${LEVEL_FILE[level]}.webp`;
}

/** Ảnh dùng cho ô "chưa mở": cấp Thức Tỉnh, hiển thị mờ/xám ở nơi gọi. */
export function titleBadgeLockedSrc(code: string): string | null {
  return titleBadgeSrc(code, "thuc_tinh");
}
