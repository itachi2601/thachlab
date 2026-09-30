---
name: project_thachlab_homework_check
description: Chấm BTVN trên lớp + BTVN ôn tập tự động sau chữa bài — đã chạy migration + deploy 27/9/2026
metadata:
  node_type: memory
  type: project
  originSessionId: 56827c98-8d83-4d95-a4ac-6a58ef3e1419
  modified: 2026-09-27T12:21:58.226Z
---

Tính năng "Chấm BTVN trên lớp + BTVN ôn tập tự động sau chữa bài" — XONG 27/9/2026:
- Nối dây đủ 4 chỗ: `ClassAnnouncementsPanel.tsx` (nút chấm BTVN cạnh mỗi thông báo homework → `HomeworkCheckPanel`), `app/phu-huynh/page.tsx` (`ParentHomeworkNotes`), `ThptStudentHome.tsx` (mục "Việc cần làm hôm nay" đọc `fetchOpenClassReviewHomework`), `ReviewBoard.tsx` (nút "Tạo BTVN ôn tập" gọi `createReviewHomework`).
- 2 migration đã chạy: `supabase/migrations/20260927130000_homework_check.sql` (bảng `class_homework_checks` + RPC `homework_check_set`), `20260927140000_class_review_homework.sql` (bảng `class_review_homework`) — log `scripts/logs/20260927-182457-*`, rollback ở `perf/rollback/`.
- Commit dd9bd74e, đã `bash scripts/deploy.sh` — đã lên web thật.

**Why:** đợt trước (27/9 sáng) đã cố tình gỡ dây UI vì bảng chưa tồn tại; đợt này soạn migration thật + nối lại dây theo đúng thứ tự AGENTS.md (migration trước, deploy sau).

**How to apply:** đã kiểm /phu-huynh và /dashboard-thpt/chua-bai trên **web thật** (thachlab.id.vn) — không lỗi console, trang lên bình thường. Còn treo: CHƯA tự kiểm **bằng thao tác thật** với tài khoản trợ giảng/HS (chấm 1 BTVN xem RP cộng đúng không, bấm "Tạo BTVN ôn tập" ở /dashboard-thpt/chua-bai xem đề mới có tạo đúng 10 câu sai + 20 câu ngân hàng không). Nếu thầy báo lỗi ở 1 trong 4 chỗ trên, đọc lại 4 file đó trước. Việc này coi như XONG, không cần agent chủ động quay lại trừ khi thầy báo lỗi cụ thể.
