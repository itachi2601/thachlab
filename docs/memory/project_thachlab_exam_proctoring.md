---
name: project-thachlab-exam-proctoring
description: "Tính năng chống gian lận khi làm bài trắc nghiệm (theo dõi rời tab, ép fullscreen) — đã chạy migration, test, và deploy 21/9/2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4be5de7e-bc40-4a12-9d2a-303136405700
  modified: 2026-09-21T15:44:05.351Z
---

**Cập nhật 2026-09-21 tối:** thầy xác nhận đã chạy migration + test + deploy (build `deploy`
branch 22:30:32 từ `main` HEAD `376982d3`). Coi như xong, không còn treo.

Đã code xong tính năng chống gian lận trong lúc làm bài kiểm tra trên LMS (commit 563a0f6, 2026-09-21):
- Migration mới `docs/supabase-migration-exam-proctoring.sql` — thêm cột `violation_count`, `violations` (jsonb) vào `exam_results`.
- [components/exams/ExamRunner.tsx](../../../Projects/thachlab/components/exams/ExamRunner.tsx) — bấm "Bắt đầu làm bài" tự ép fullscreen; theo dõi `visibilitychange` (rời tab) và `fullscreenchange` (thoát fullscreen) trong lúc `phase === "running"`; hiện banner cảnh báo ngay, không tự nộp bài; lưu violations kèm khi nộp bài.
- [components/admin/ResultsAdmin.tsx](../../../Projects/thachlab/components/admin/ResultsAdmin.tsx) — thêm cột "Vi phạm" trong bảng kết quả toàn trường + xuất CSV.

**Why:** thầy muốn phát hiện học sinh mở tab khác tra đáp án khi làm bài trắc nghiệm trên web; chọn mức "ghi log + cảnh báo" (không tự động nộp bài khi vi phạm) và ép fullscreen khi bắt đầu.

**Chưa xong / cần thầy làm tiếp:**
1. Chạy SQL migration `docs/supabase-migration-exam-proctoring.sql` trong Supabase SQL editor.
2. Test thật bằng tài khoản học sinh (agent không có sẵn tài khoản để đăng nhập thử luồng làm bài) — alt-tab, thoát fullscreen (Esc), kiểm tra banner + cột "Vi phạm" hiện đúng.
3. Deploy sau khi test OK — theo [[feedback_thachlab_deploy_scope]] chỉ deploy đúng phần này, không kèm các WIP khác đang có trong working tree (ExamSection.tsx, ai-classify.ts, classify-questions function — thuộc việc khác, không đụng tới).

Không làm (theo yêu cầu): không chặn copy/paste, không chặn chuột phải, không phát hiện DevTools, không tự nộp bài khi vi phạm nhiều lần, không làm trang riêng lọc gian lận.
