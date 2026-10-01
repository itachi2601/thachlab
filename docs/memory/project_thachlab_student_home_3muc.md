---
name: project_thachlab_student_home_3muc
description: "Trang chủ học sinh THPT thiết kế lại thành 3 mục: việc cần làm hôm nay · BTVN · chủ đề cần phụ đạo + đăng ký lịch tuần — đã chạy 2 migration, test và deploy 21/9/2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: 070a3294-7e20-4fd7-a35e-2bd06fb0aea9
  modified: 2026-09-21T15:44:09.717Z
---

**Cập nhật 2026-09-21 tối:** thầy xác nhận đã chạy 2 migration (`class-announcements`,
`tutoring-slots`) + test + deploy. Coi như xong.

2026-09-21: user muốn trang [tai-khoan/ThptStudentHome](components/dashboard/ThptStudentHome.tsx)
có 3 mục rõ ràng: (1) việc cần làm buổi học hiện tại, (2) bài tập về nhà — cả hai GV lẫn
trợ giảng gửi được, (3) chủ đề cần phụ đạo kèm chỗ đăng ký lịch, nối với trợ giảng lên lịch
phụ đạo trong tuần. Hỏi lại 4 câu, user chọn hết phương án khuyến nghị:
- Mục 1: tự suy ra (bài đang học dở + đề cần làm, logic cũ) + GV/trợ giảng ghi đè bằng ghi chú riêng.
- Quyền gửi thông báo: cả giáo viên và trợ giảng.
- Mục 3: trợ giảng đăng lịch tuần trước, học sinh chọn buổi đăng ký (không phải HS đăng ký nhu cầu rồi trợ giảng xếp).
- Làm trọn 1 đợt, không chia phase.

**Khảo sát trước khi code — hai khái niệm khác nhau tưởng giống:**
- `tutoring_needs` (bảng có sẵn, xem [[project_thachlab_phu_dao]]) = mục "hổng phần nào" có
  trạng thái/workflow → dùng cho mục 3 "chủ đề cần phụ đạo" trên trang mới.
- `TopicGap` từ `fetchMyTopicGaps` (services/analytics.ts) = % sai thô, không trạng thái,
  vẫn dùng riêng ở `/lop-hoc/ket-qua` — đã BỎ khỏi trang chủ HS (trước đây là mục "Chủ đề cần ôn"),
  tránh trùng ý với mục 3 mới.
- Bảng `messages` cũ (chỉ admin gửi, khoá theo `class_name` text, trang đọc `/tin-nhan` mồ côi
  không có trong nav) — KHÔNG tái dùng, vì cần cả trợ giảng gửi được và khoá theo `class_id`
  giống phần còn lại của hệ thống. Làm bảng mới `class_announcements` riêng.
- `ta_sessions` (phiếu ghi buổi, ghi SAU khi dạy xong, để tính lương —
  [[project_thachlab_ta_policy]]) khác hẳn nhu cầu "đăng lịch TRƯỚC cho HS đăng ký" → bảng mới
  `tutoring_slots` + `tutoring_registrations`, KHÔNG đụng vào `ta_sessions`.

**Đã làm (code xong, CHƯA chạy migration, CHƯA deploy):**
- `docs/supabase-migration-class-announcements.sql` — bảng `class_announcements`
  (class_id, kind 'today_task'|'homework', body, created_by), RLS: GV/trợ giảng của lớp
  (`manages_class`/`assists_class`/`is_admin`) đăng+xoá, học sinh lớp đó đọc.
- `docs/supabase-migration-tutoring-slots.sql` — bảng `tutoring_slots` (trợ giảng đăng buổi:
  ngày giờ, topic_ids[], capacity, registered_count) + `tutoring_registrations` (HS tự đăng
  ký/huỷ). Trigger `tutoring_slot_register`/`tutoring_slot_unregister` giữ `registered_count`
  đúng và chặn đăng ký khi đầy — atomic qua UPDATE...WHERE rồi kiểm `FOUND`.
- `services/announcements.ts` (mới) + phần cuối `services/tutoring.ts` (thêm slot/registration
  CRUD: `fetchUpcomingSlots`, `fetchSlotsForAssistant`, `createSlot`, `cancelSlot`,
  `registerForSlot`, `cancelRegistration`, `fetchRegistrationsForSlots`, `fetchMyRegistrations`).
- `components/dashboard/ClassAnnouncementsPanel.tsx` (composer dùng chung) → gắn vào tab mới
  "Thông báo" ở `TeacherThptDashboard.tsx` (GV) và trang mới `/tro-giang/thong-bao` (trợ giảng,
  qua `TaClassAnnouncements.tsx`, có ô chọn lớp nếu phụ trách nhiều lớp).
- `components/tro-giang/TutoringSlotsPlanner.tsx` — trợ giảng đăng buổi (chọn lớp, ngày/giờ,
  chủ đề dự kiến lấy từ `tutoring_needs` đang mở của lớp đó, sức chứa), xem danh sách buổi đã
  đăng kèm tên HS đã đăng ký, huỷ buổi. Gắn làm tab thứ 2 "Lịch tuần" ở `/tro-giang/phu-dao`
  (tab 1 vẫn là `PhuDaoList` cũ "Cần phụ đạo").
- `ThptStudentHome.tsx` viết lại theo 3 mục, giữ nguyên phần hero/thanh năng lượng/stat/cảnh báo
  cũ ở trên: mục 1 gộp ghi chú GV + "Học tiếp theo" + "Bài kiểm tra cần làm" (logic auto cũ);
  mục 2 liệt kê 5 thông báo BTVN gần nhất; mục 3 hiện chip `tutoring_needs` đang mở + danh sách
  buổi phụ đạo sắp tới của lớp kèm nút Đăng ký/Huỷ đăng ký (gọi RPC qua RLS, không cần trang
  quản trị duyệt).

**Đã kiểm tra:** `npx tsc --noEmit` sạch, `npx eslint` sạch các file đổi, `next build` qua hết
71 route kể cả 2 route mới. Soi qua browser pane (dev server có sẵn ở :3000 từ phiên khác) —
`/tro-giang/phu-dao` và `/tro-giang/thong-bao` redirect đúng khi chưa đăng nhập, không lỗi
console. **CHƯA kiểm chứng được giao diện sau đăng nhập** (không tự nhập mật khẩu được) —
theo đúng giới hạn đã ghi ở [[project_thachlab_track_student_home]].

**User cần làm:**
1. Chạy 2 file migration trên trong Supabase SQL Editor (đúng thứ tự: class-announcements
   trước hay sau tutoring-slots đều được, cả hai chỉ cần các hàm từ exam-analytics +
   tutoring-needs đã có sẵn).
2. Đăng nhập thật (HS/GV/trợ giảng) trên localhost để mình soi lại giao diện thật.
3. Quyết định commit/deploy — working tree lúc này còn WIP khác không liên quan
   (`app/globals.css`, `app/lop-hoc/bai/page.tsx`, `scripts/restore-posts.*`) nên PHẢI
   `git add` chọn lọc đúng các file của đợt này khi commit (xem danh sách ở trên +
   [[feedback_thachlab_deploy_scope]]), không add tràn.

Liên quan: [[project_thachlab_phu_dao]], [[project_thachlab_exam_analytics]],
[[project_thachlab_track_student_home]], [[project_thachlab_ta_policy]],
[[feedback_thachlab_deploy_scope]]
