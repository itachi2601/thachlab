---
name: project-thachlab-so-do-tu-duy-chuong
description: Sơ đồ tư duy tổng hợp chương — L12 Chương 3 đã gắn cuối chương ở trang lớp (đã deploy 11/11/2026); chương khác làm bằng skill so-do-tu-duy-chuong
metadata:
  type: project
---

Sơ đồ tư duy chương (thầy duyệt mẫu 11/11/2026): component `components/lessons/so-do/SoDoTuDuy.tsx` + `HinhNhanh.tsx`, dữ liệu mỗi chương một file trong `features/lessons/so-do-tu-duy/`, sổ đăng ký `index.ts` theo `chapters.id`. Trang HS `/lop-hoc/so-do/?chuong=<id>&lop=<slug>`; dòng "Sơ đồ tư duy chương" tự hiện cuối chương (trước Kiểm tra chương) ở trang lớp khi chương có trong sổ đăng ký. Đã có: L12 Ch.3 (chapters.id 4; lesson 10, 11, 12, 13, 14, 125, 126, 127 đã đối chiếu `catalog.json`).

**Làm chương khác:** skill `.claude/skills/so-do-tu-duy-chuong/SKILL.md` (thứ tự đề xuất: L12 Ch.1 → Ch.2 → Ch.4, rồi L11, L10).

**Đã deploy 11/11/2026 10:17**, đã kiểm trang thật. **Treo:** bố cục toả tròn 3 và 4 nhánh chưa chụp kiểm; nhánh 2 và 5 của Ch.3 mở mô phỏng trong bài (chưa có mô phỏng mini tại chỗ); đo sau khi lên: tỉ lệ đúng câu công thức ở đề kiểm tra chương, nhóm có mở sơ đồ so với không.

**Why:** cố ý vượt M3 (mỗi nhánh một màu = mã ghi nhớ), lý do ghi ở đầu component. **How to apply:** không sửa component khi thêm chương; chỉ thêm file dữ liệu + hình khoá + một dòng sổ đăng ký.
