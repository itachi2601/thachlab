-- ============================================================
-- Migration: Gắn đề vào thông báo "Việc cần làm hôm nay"
--
-- Bối cảnh: cột "Đăng nội dung" (class_announcements, kind='today_task')
-- chỉ nhận văn bản — giáo viên/trợ giảng muốn giao một đề cụ thể cho học
-- sinh làm trong buổi/ngày hôm đó thì không có cách nào để trang chủ học
-- sinh hiện nút "Làm bài" kèm theo dòng thông báo.
--
-- Thêm cột exam_id (nullable — thông báo thuần văn bản vẫn dùng được như
-- cũ). RLS/policy hiện có của class_announcements áp dụng nguyên vẹn, không
-- cần đổi vì đây chỉ là thêm cột.
--
-- Idempotent — chạy lại được.
-- Rollback: perf/rollback/20260927100000_class_announcement_exam.down.sql
-- ============================================================

alter table public.class_announcements
  add column if not exists exam_id bigint references public.exams (id) on delete set null;
