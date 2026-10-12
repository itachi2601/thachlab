---
name: project-thachlab-phap-ly-ban-quyen
description: Trang /dieu-khoan (Điều khoản & Bản quyền), quy tắc bản quyền khi soạn bài/tìm tài nguyên; còn treo nhãn nguồn từng câu
metadata:
  type: project
---

Mục tiêu (thầy yêu cầu 2026-10-12): hoàn thiện pháp lý — điều khoản sử dụng/bản quyền, ghi nguồn đề, cơ chế báo vi phạm (DMCA).

**Đã xong, đã lên production 2026-10-12** (commit `b82b3c04e`, deploy nhánh `deploy` 4a69063, `/dieu-khoan/` trả 200):
- `app/(public)/dieu-khoan/page.tsx`: 4 mục (sở hữu, quyền/giới hạn người học, ghi nguồn đề, báo vi phạm). Email nhận khiếu nại = `CONTACT.email` trong `lib/contact.ts` (thầy chốt giữ Gmail hiện có). `TAKEDOWN_DAYS = 5` ngày làm việc do Claude tự đặt, thầy chưa xác nhận.
- Link "Điều khoản & Bản quyền" ở cả 3 kiểu `components/layout/Footer.tsx`; có trong `app/sitemap.ts`.
- Quy tắc bản quyền cho phiên soạn bài/tìm tài nguyên: mục "Bản quyền khi soạn bài và tìm tài nguyên" cuối `AGENTS.md` (viết lại không chép, ghi nguồn đề, tài nguyên chỉ dùng giấy phép rõ, khiếu nại thì gỡ ngay).

**Còn treo:**
- Chưa chụp/kiểm trang ở 375px (preview bị từ chối lúc làm).
- Mục 3 "ghi nguồn đề" mới là quy định trên trang: DB chỉ có `source_exam_id` ở `question_bank`, chưa có trường nguồn cho từng câu. Hiện nhãn nguồn trong giao diện làm bài cần thêm trường/quy ước đặt tên đề (đụng migration) — chờ thầy quyết.
- Chưa có trang Chính sách bảo mật dữ liệu cá nhân (tên, điểm, phụ huynh) — chưa đề xuất với thầy.
- `main` chưa push lên origin ở phiên này.
