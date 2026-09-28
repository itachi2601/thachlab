# Huy hiệu rank & danh hiệu chuyên môn

WebP 512 × 512, nền trong suốt, xuất từ design system **"ThachLab Huy Hiệu"** (artifact Claude, PNG gốc 1024 × 1024).
Tra đường dẫn qua `features/rank/badge-assets.ts` (`tierBadgeSrc`, `titleBadgeSrc`), không ghép chuỗi tay.

- `tiers/rank-<ten>.webp` — 7 huy hiệu bậc rank, khoá theo `TierCode` (`tan_binh` … `thach_dau`; tên hiển thị hiện là Starlight/Tinh Quang … Sovereign/Chí Tôn nhưng mã bậc và tên file giữ nguyên).
- `titles/cm-<slug>-<thuc-tinh|lam-chu|huyen-thoai>.webp` — 32 danh hiệu chuyên môn × 3 cấp = 96 file. Slug ↔ `rank_titles.code` xem `SPECIALIST_SLUG`.

Kích thước dùng trong UI: 14–20 px (logo cạnh tên), 36–48 px (khung sưu tập, bộ sưu tập), tối đa 240 px — không phóng quá 240 px.

- `titles/bst-<slug>.webp` (6 bộ sưu tập) và `titles/tt-<slug>.webp` (7 thành tích) — **chưa vẽ**; spec ở design system, slug ↔ `rank_titles.code` xem `SINGLE_SLUG`. Vẽ xong: ép 512 px vào đây rồi thêm mã vào `SINGLE_AVAILABLE` trong `badge-assets.ts`, UI tự thay ô dự phòng (lục giác vàng có sao) bằng ảnh.

28/9/2026: `cm-dien-truong-thuc-tinh.webp` trong commit đầu bị 0 byte, đã ép lại từ PNG gốc.
