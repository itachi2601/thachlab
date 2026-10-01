---
name: project_thachlab_dang_de_azota
description: "Trang /quan-tri/dang-de \"Đăng đề kiểm tra\" kiểu Azota — commit 49cf5562, đã deploy 2026-09-19 (build aa210e6)"
metadata: 
  node_type: memory
  type: project
  originSessionId: aedabca3-fb40-44bb-a80c-57836b8ddee9
  modified: 2026-09-20T04:59:28.257Z
---

Trang **/quan-tri/dang-de** (component `AzotaExamComposer`, helper `services/azota-text.ts`):
dán văn bản đề kiểu Azota hoặc thả .docx → tách câu ngay khi gõ → xem trước + bảng đáp án
(bấm A/B/C/D ghi thẳng dấu `*` vào văn bản) → chọn Lớp/Chương/Bài + mục Kiểm tra/Luyện tập/BTVN
→ Đăng (tạo `exams`, gắn `exam_ids`, rollback nếu lỗi). Commit 49cf5562 (2026-09-19).

**Why:** thầy muốn luồng đăng đề giống Azota thay vì gói JSON/LaTeX ở /quan-tri/nhap-bai.

**How to apply:**
- Đã deploy 2026-09-19 (deploy branch aa210e6) bằng cách build HEAD trong `git worktree` riêng
  (cp -Rl node_modules — Turbopack không chịu symlink ra ngoài root; copy thêm public/lessons
  untracked) thay vì stash tree đang có WIP của session khác — cách này an toàn, nên dùng lại.
  Xem [[feedback_thachlab_deploy_scope]].
- Chỉ test được UI qua route tạm không đăng nhập; luồng bấm "Đăng đề" thật (ghi Supabase) chưa
  chạy end-to-end — nếu lỗi, xem log rollback ngay trên trang.
- Chưa bắt buộc gắn nhãn chủ đề (khác nhap-bai); gắn qua "Sửa chi tiết từng câu" (ExamDraftEditor).
- Liên quan [[project_thachlab_up_de_skill]] (skill cũ vẫn dùng cho PDF/MathType).
- **Tình trạng tree lúc bàn giao 2026-09-19 (cuối phiên):** một session KHÁC đang sửa dở
  `components/admin/AzotaExamComposer.tsx` + `AdminSidebar.tsx` (nhận "giỏ câu" từ trang
  Ngân hàng câu hỏi qua `takeHandoff()` → mở sẵn chế độ sửa chi tiết) và thêm feature mới
  chưa commit: `app/quan-tri/(thpt)/ngan-hang-cau-hoi/`, `components/admin/QuestionBankAdmin.tsx`,
  `services/question-bank.ts`, `docs/supabase-migration-question-bank.sql` (migration chưa chạy).
  Không phải việc của phiên này — đừng stash/revert; hỏi thầy trước khi đụng.
- `main` local đang **ahead 2 / behind 2** so với origin/main (origin có merge nhánh
  "xem lại bài thi" a56874d6). Chưa pull/rebase — cần thầy quyết; deploy hiện tại lấy HEAD local.
- Chưa test end-to-end nút "Đăng đề" (ghi Supabase) vì cần đăng nhập — thầy tự thử với "Đề mẫu".

**Cập nhật 2026-09-20:** WIP "Ngân hàng câu hỏi" nhắc ở trên đã commit — `5ee6a43c refactor(nhap-bai):
đăng bài học dùng chung UI đề với trang Đăng đề kiểu Azota` (cùng ngày, phiên khác). `/quan-tri/nhap-bai`
giờ dùng chung UI phần "3. Kiểm tra & xem trước" + "4. Gắn đề" với `AzotaExamComposer`. Đã tự tay
test end-to-end nút Đăng (qua nhap-bai, không phải dang-de trực tiếp) lần đầu: ghi Supabase đúng
(tạo `exams` row, cập nhật `lesson_items.exam_ids`) — luồng ghi hoạt động tốt. Nhưng phát hiện bug:
mục "Gắn đề" tự gắn đề vào **cả Luyện tập lẫn Kiểm tra** dù chỉ tick Kiểm tra (tạo mới hẳn một
`lesson_items` dòng `luyen_tap` không xin) — rủi ro lộ đáp án trước giờ kiểm tra thật. Vì UI dùng
chung, bug này nhiều khả năng cũng có ở `/quan-tri/dang-de` trực tiếp, chưa xác nhận. Chi tiết cách
phát hiện + cách gỡ ở [[project_thachlab_up_de_skill]] (mục "Lần chạy 2026-09-20").
