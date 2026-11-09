---
name: project_thachlab_cttc_tab_hop_thu
description: Thanh đáy SV CTTC (Khoá học · Bài học · Hộp thư · Thêm), lọc tin THPT khỏi hộp thư CTTC, trang /quan-tri/cnc-sua-de — commit 10/11/2026, chưa kiểm bằng tài khoản đăng nhập, chưa deploy
metadata:
  type: project
---

10/11/2026 (nhánh claude/redesign-cttc-student-tabs-4ff9da, commit db053cc45):
- Thanh đáy SV CTTC theo khuôn THPT: Hộp thư (`/hop-thu`) thay tab Thông báo, Thêm là trang `/tai-khoan/them` (bộ mục `CTTC_LINKS`).
- Nguồn "mục lớp 10 lẫn vào thông báo CTTC" đo trên DB: SV CTTC thật có 0 dòng `notifications`; thứ lẫn là (1) 7 bài `posts` Vật lí/HSG không gán lớp, `/hop-thu` và `/tin-tuc` dùng `visibleTo` nên coi là toàn trường, (2) khi admin "Xem như SV CTTC" thì chuông/hộp thư đọc thông báo của chính tài khoản admin. Đã sửa: `visibleToCttcStudent` (services/content.ts) và ẩn thông báo + số chưa đọc khi `previewMode` bật.
- Sửa đề CTTC: `ExamLibraryAdmin area="cttc"` lọc `cnc_key not null` hoặc `subject_code in (avcn, worldskills-im)` (26 + 15 đề). Đề ngân hàng CNC có `subject_code = vat-ly`, chỉ nhận ra bằng `cnc_key`. Ghi `exams` vẫn chỉ `is_admin()`; giảng viên CTTC không phải admin mở được trang nhưng Lưu sẽ bị RLS chặn (giống THPT).

**Còn treo:** chưa chụp 375px và chưa thử Lưu vì tab Browser pane ở cổng dev mới không có phiên đăng nhập; chưa deploy.
