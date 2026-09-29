-- Rollback cho supabase/migrations/20260927100000_class_announcement_exam.sql
--
-- Chạy: supabase db query --linked -f perf/rollback/20260927100000_class_announcement_exam.down.sql

alter table public.class_announcements drop column if exists exam_id;
