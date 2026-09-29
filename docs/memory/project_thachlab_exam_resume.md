---
name: project-thachlab-exam-resume
description: "ExamRunner tự lưu tiến độ làm bài, khôi phục khi thoát/mất mạng giữa chừng — deploy 24/9/2026"
metadata:
  node_type: memory
  type: project
  originSessionId: fa2997af-3e49-404b-b58c-aa1dcce3b61d
  modified: 2026-09-24T07:24:37.325Z
---

ExamRunner tự lưu `responses` + `seconds_left` vào `exam_attempts` mỗi 15s và khi rời tab (`document.hidden`), qua `saveExamAttemptProgress()`/`findOpenExamAttempt()` ([services/progress.ts](services/progress.ts)). Vào lại đề đang làm dở (attempt còn `submitted_at is null`) sẽ thấy nút "Làm tiếp bài đang dở" thay vì "Bắt đầu làm bài", giữ nguyên `client_token` cũ nên không tạo lượt trùng. Migration `docs/supabase-migration-exam-attempt-resume.sql` (3 cột mới trên `exam_attempts`, dùng lại RLS sẵn có) đã chạy trên Supabase + đã deploy (commit 5e430e55, deploy branch 649cf1d) 24/9/2026.

**Why:** học sinh làm bài trắc nghiệm chống gian lận (fullscreen + theo dõi rời tab, xem [[project_thachlab_exam_proctoring]]) hay bị thoát ngang do mất mạng/sập máy — trước đây mất hết phải làm lại từ đầu.

**How to apply:** chưa ai test luồng thoát giữa chừng → vào lại trên dữ liệu thật; nếu đề bị sửa (đổi số câu) sau khi đã lưu dở thì code tự bỏ qua `responses` cũ cho an toàn (so `resumable.responses.length === exam.questions.length`), chỉ giữ lại thời gian còn lại.
