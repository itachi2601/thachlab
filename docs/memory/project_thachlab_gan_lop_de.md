---
name: project_thachlab_gan_lop_de
description: "2026-10-17: gán exam_classes cho 687 đề published chưa gán (664 tự động + 23 thầy duyệt), AVCN cố ý để trống; hệ quả RLS với lượt làm cũ"
metadata:
  type: project
---

**Vấn đề:** 687/899 đề published không có `exam_classes` → `visibleTo` coi là toàn trường, kệ lớp 12 bày cả đề lớp 11.

**Đã làm 2026-10-17 (DB production):**
- `scripts/gan-lop-de-chua-gan.mts` (phiên con, commit `ffcb01e80`): suy lớp theo bài học chứa đề → tiêu đề → subject; 664 đề gán. Sao lưu `scripts/logs/gan-lop-de-*.json`.
- 23 đề không suy được: thầy duyệt qua `scripts/data/duyet/gan-lop-de-2026-10-17/duyet.html` (dựng bằng `scripts/lap-duyet-lop-de.mts`), áp dụng bằng `scripts/ap-dung-duyet-lop-de.mts` (22 → lớp 12, đề 99 → lớp 11). `phan-hoi.json` thầy lưu ở ~/Documents, đã chép vào thư mục đợt.
- **AVCN (subject `avcn`, 10 đề) phải để trống exam_classes** — lớp vào tự do (migration 20261013180000). Phiên con gán nhầm → 51 lượt làm của 27 sinh viên mất quyền xem lại; đã gỡ bằng `scripts/go-gan-lop-de-avcn.mts` và script gán lớp giờ bỏ qua `avcn`.
- Sau cùng: còn đúng 10 đề `avcn` không gán; lớp 10: 312, lớp 11: 173, lớp 12: 395.

**Hệ quả cần nhớ:** RLS `exams` ("students only see own-class exams") giấu đề gán lớp khác → lượt làm cũ của em ngoài lớp hiện "(Đề đã xóa)" ở Bài đã làm. Kiểm 2026-10-17: chỉ 1 em thật dính 2 lượt (đề 893, 897 lớp 11). HS Test 1 (lớp 12) dính đề 908.

**Có thể gỡ sau:** bộ lọc tiêu đề ở `features/exams/exam-grade.ts` + `app/lop-hoc/page.tsx` là vá tạm; giữ cũng vô hại.
