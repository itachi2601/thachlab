---
name: project-thachlab-ruot-tap-bai14
description: Ruột tập in 4 trang cho Bài 14 VL12 (script dựng PDF trong repo) + mã data-tap nối web với tập; chờ thầy cập nhật DB và deploy
metadata:
  type: project
---

Ruột tập bài 14 dựng bằng `node scripts/ruot-tap/bai14.mjs` (ra `scripts/ruot-tap/out/`); QR kiểm bằng `npx tsx scripts/ruot-tap/giai-ma-qr.mts <png>`. Mã ô "Tập: trang · ô" nằm ở `data-tap` trong `theory.src.html` (h3/h4), Trình chiếu đọc ra nhãn ✍.

**Why:** thầy chiếu bài, HS ghi vào tập; mã ô giúp HS tìm đúng chỗ ghi (24/10/2026).
**How to apply:** sửa web hay tập thì giữ hai bên khớp mã ô. Còn chờ: `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/theory.html 15` (để data-tap vào DB), deploy, và migration `20261024190000_lesson_notes.sql` (ghi chú HS đồng bộ tài khoản; trước đó chỉ lưu máy).
