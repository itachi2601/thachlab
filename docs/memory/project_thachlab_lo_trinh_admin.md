---
name: project-thachlab-lo-trinh-admin
description: Trang /quan-tri/lo-trinh cho thầy xem lộ trình chương–bài mỗi lớp (đã mở/ẩn/chưa có từng mục); mới viết 16/10, chưa mở trình duyệt thử
metadata:
  type: project
---

Thầy yêu cầu 16/10/2026 (khi treo việc) có nơi xem lộ trình cần thiết cho học sinh → chọn trang quản trị chỉ-đọc `components/admin/LearningRoadmapAdmin.tsx`, route `app/quan-tri/(thpt)/lo-trinh`, có trong menu THPT.

**Why:** thấy ngay bài nào chưa soạn/đang ẩn theo từng lớp mà không mở từng bài.
**How to apply:** mới qua `tsc`, CHƯA thử trong trình duyệt/375px, chưa deploy. Chưa gồm khung HSG9 "đang soạn" từ `docs/HSG9-KHUNG.md` nếu bài chưa có trong DB; AVCN hiện qua lớp `avcn`. Liên quan [[project-thachlab-khoa-hsg9-vat-ly]].
