/**
 * Bản chiếu "trên lớp" (tivi 50") đã dựng cho từng bài — file tĩnh public/dev/tren-lop/<slug>.html
 * (+ <slug>-ghi-chu.html), sinh bằng content/lesson-samples/<slug>/build_tren_lop.py
 * (skill .claude/skills/ban-chieu-tren-lop). Thêm bài mới = thêm một dòng ở đây:
 * trang mục lục /dev/tren-lop và nút "Bản chiếu lớp" trên trang bài (chỉ chế độ giáo viên) cùng đọc danh sách này.
 */
export type BanChieuTrenLop = { lessonId: number; slug: string; ten: string; ghiChu: string };

export const BAN_CHIEU_TREN_LOP: BanChieuTrenLop[] = [
  { lessonId: 46, slug: "l10-lam-quen-voi-vat-li", ten: "Vật lí 10 · Bài 1 · Làm quen với Vật lí", ghiChu: "26 màn · cuối tiết đề 1222 (QR)" },
  { lessonId: 48, slug: "l10-thuc-hanh-sai-so", ten: "Vật lí 10 · Bài 3 · Thực hành tính sai số", ghiChu: "27 màn · cuối tiết đề 1224 (QR)" },
  { lessonId: 61, slug: "l10-dinh-luat-3-newton", ten: "Vật lí 10 · Bài 16 · Định luật 3 Newton", ghiChu: "25 màn · cuối tiết đề 1237 (QR)" },
  { lessonId: 62, slug: "l10-trong-luc-luc-cang", ten: "Vật lí 10 · Bài 17 · Trọng lực và lực căng", ghiChu: "27 màn · cuối tiết đề 1238 (QR)" },
  { lessonId: 63, slug: "l10-luc-ma-sat", ten: "Vật lí 10 · Bài 18 · Lực ma sát", ghiChu: "22 màn · cuối tiết đề 1239 (QR)" },
  { lessonId: 64, slug: "l10-luc-can-luc-nang", ten: "Vật lí 10 · Bài 19 · Lực cản và lực nâng", ghiChu: "22 màn · cuối tiết đề 1240 (QR)" },
  { lessonId: 49, slug: "l10-do-dich-chuyen-quang-duong", ten: "Vật lí 10 · Bài 4 · Độ dịch chuyển và quãng đường", ghiChu: "26 màn · cuối tiết đề 1225 (QR)" },
  { lessonId: 47, slug: "l10-an-toan-phong-thuc-hanh", ten: "Vật lí 10 · Bài 2 · An toàn phòng thực hành", ghiChu: "24 màn · cuối tiết đề 1223 (QR)" },
  { lessonId: 39, slug: "l11-dien-the", ten: "Vật lí 11 · Bài 20 · Điện thế", ghiChu: "22 màn · cuối tiết đề 1215 (QR)" },
  { lessonId: 40, slug: "l11-tu-dien", ten: "Vật lí 11 · Bài 21 · Tụ điện", ghiChu: "23 màn · cuối tiết đề 1216 (QR)" },
  { lessonId: 41, slug: "l11-cuong-do-dong-dien", ten: "Vật lí 11 · Bài 22 · Cường độ dòng điện", ghiChu: "22 màn · cuối tiết đề 1217 (QR)" },
  { lessonId: 15, slug: "l12-hat-nhan-mo-hinh-nguyen-tu", ten: "Vật lí 12 · Bài 14 · Hạt nhân và mô hình nguyên tử", ghiChu: "27 màn · cuối tiết đề 1191 (QR)" },
];

export const banChieuCuaBai = (lessonId: number) => BAN_CHIEU_TREN_LOP.find((b) => b.lessonId === lessonId);
export const linkBanChieu = (slug: string) => `/dev/tren-lop/${slug}.html`;
export const linkGhiChuDay = (slug: string) => `/dev/tren-lop/${slug}-ghi-chu.html`;
