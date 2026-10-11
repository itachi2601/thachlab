---
name: project-thachlab-bao-live-dang-hoc
description: Báo live "bao nhiêu bạn đang học / chủ đề nào" — thẻ HS toàn trường ẩn danh + panel GV theo lớp; giới hạn heartbeat
metadata:
  type: project
---

11/10/2026: RPC `live_study_summary` (ngưỡng ẩn 3, cửa sổ 2 phút) → `LiveStudyStrip` ở `/lop-hoc` (HS, ẩn 23:00–04:30); `TeacherLiveLearningPanel` gộp theo bài. Dữ liệu từ `student_learning_presence`.

**Why:** thầy chốt toàn trường, ẩn danh, ngưỡng 3, hiện luôn.
**How to apply:** heartbeat chỉ ghi ở `InlineLessonAccordion` — em làm đề/luyện tập ở trang khác chưa được đếm; muốn đủ hơn thì thêm heartbeat ở đó. Chưa đặt thẻ ở trang chủ HS. Chưa xem panel GV bằng tài khoản thật ở nền sáng.
