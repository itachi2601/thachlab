-- Rollback cho supabase/migrations/20260926120000_lesson_item_draft_publish.sql
--
-- Xoá 3 cột vừa thêm. Mất luôn mọi bản nháp đang sửa dở (draft_payload) — cột sống
-- (title/body_html/…) không bị ảnh hưởng, mục vẫn hiện y như trước khi có migration này.
--
-- Chạy: supabase db query --linked -f perf/rollback/20260926120000_lesson_item_draft_publish.down.sql

alter table public.lesson_items
  drop column if exists published_at,
  drop column if exists draft_payload,
  drop column if exists draft_saved_at;
