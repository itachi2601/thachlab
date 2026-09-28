# Huy hiệu rank & danh hiệu chuyên môn

WebP 512 × 512, nền trong suốt, xuất từ design system **"ThachLab Huy Hiệu"** (artifact Claude, PNG gốc 1024 × 1024).
Tra đường dẫn qua `features/rank/badge-assets.ts` (`tierBadgeSrc`, `titleBadgeSrc`), không ghép chuỗi tay.

- `tiers/rank-<ten>.webp` — 7 huy hiệu bậc rank, khoá theo `TierCode` (`tan_binh` … `thach_dau`; tên hiển thị hiện là Starlight/Tinh Quang … Sovereign/Chí Tôn nhưng mã bậc và tên file giữ nguyên).
- `titles/cm-<slug>-<thuc-tinh|lam-chu|huyen-thoai>.webp` — 32 danh hiệu chuyên môn × 3 cấp = 96 file. Slug ↔ `rank_titles.code` xem `SPECIALIST_SLUG`.

Kích thước dùng trong UI: 48 / 96 / 240 px — không phóng quá 240 px. Danh hiệu bộ sưu tập (collection) và thành tích (achievement) chưa có ảnh riêng.
