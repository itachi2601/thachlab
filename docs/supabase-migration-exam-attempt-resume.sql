-- ============================================================
-- Migration: Lưu tạm bài đang làm dở để khôi phục khi thoát/vào lại
-- Chạy SAU: supabase-migration-learning-progress.sql (cần bảng exam_attempts)
-- Idempotent — chạy lại được.
-- RLS: dùng lại policy "student updates own open attempt" đã có sẵn trên
-- exam_attempts (student_id = auth.uid() and submitted_at is null) —
-- không cần policy mới.
-- ============================================================

alter table public.exam_attempts add column if not exists responses jsonb;
alter table public.exam_attempts add column if not exists seconds_left int;
alter table public.exam_attempts add column if not exists saved_at timestamptz;
