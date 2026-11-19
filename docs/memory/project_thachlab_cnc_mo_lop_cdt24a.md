---
name: project-thachlab-cnc-mo-lop-cdt24a
description: Lớp CNC "CĐT 24A" mở 2026-11-09 (mã CNC-753E9D), trang quản trị Mở lớp mới, sửa Thông báo/chương mặc định; đã deploy 09:45
metadata:
  type: project
---

**Lớp:** `course_offerings` id 10 "CĐT 24A - Gia công CNC", năm 2026-2027, mã vào lớp `CNC-753E9D`, ghi danh duyệt tay; đã mở `lesson-1`, `lesson-2` (`open_lesson_ids`). 31 SV track cttc đã active. Lớp cũ id 1 "CĐ CK 24A" mã `CNC-F57D60` mở nhiều bài hơn — không nhầm hai lớp. Tạo lớp/mở bài làm bằng script REST service-role chạy ở tab terminal (không có trang UI mở bài ngoài dashboard giảng viên).

**Code (đã vào main, deploy 2026-11-09 09:45, build `ac3d39b`):**
- `/quan-tri/cnc-mo-lop` (`components/admin/CncOpenClass.tsx`, mục "Mở lớp mới" trong `components/admin/nav.ts`): form tạo lớp + danh sách lớp CNC + mã.
- `services/content.ts` `visibleToCourse(…, subjectCode)`: bài không gán lớp/khoá mà thuộc môn THPT (vat-ly, hsg-vat-ly, hoa-hoc…) không hiện ở khối Thông báo của SV CNC (`CncCourseAnnouncements`). Nguyên nhân: 4 tin Vật lí không gán lớp bị coi là "toàn trường".
- `CncCourseWorkspace`: `pickedChapter` mặc định = chương cuối có bài giảng viên đã mở (bài 2 nằm Chương II nên SV tưởng chỉ có 1 bài).

**Còn treo:**
- Hộp thư `/hop-thu` và `/tin-tuc` vẫn dùng `visibleTo` cũ → SV CNC còn thấy tin Vật lí ở đó (chưa sửa, chờ thầy).
- SV chưa xác nhận trên web thật là thấy bài 2 (cần Ctrl+Shift+R).
- Thầy nhờ "đồng bộ cấu trúc bài CNC với Vật lí + tab Video": đã có sẵn từ 2026-11-08 (Lý thuyết · Video · Bài mẫu · Luyện tập · BTVN, xem `docs/CNC-CAU-TRUC-BAI-THEO-MON-KHAC-2026-11-08.md`); chờ thầy gửi ảnh chỗ còn thiếu.
- Phiên fork đổi "bẫy"→"lỗi" ở 8 bài CNC: chưa đăng lại lên DB.

Liên quan: [[project_thachlab_cnc_flipped]], [[project_thachlab_cnc_kiem_tra_redesign]].
