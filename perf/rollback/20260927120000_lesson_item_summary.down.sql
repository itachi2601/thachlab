-- Rollback cho supabase/migrations/20260927120000_lesson_item_summary.sql
--
-- Xoá cột summary_html. Mất luôn mọi tóm tắt đã backfill bằng AI — mục lý thuyết
-- vẫn hiện y như trước khi có migration này (chỉ ẩn khối "Tóm tắt ý chính").
--
-- Chạy: supabase db query --linked -f perf/rollback/20260927120000_lesson_item_summary.down.sql

alter table public.lesson_items
  drop column if exists summary_html;
