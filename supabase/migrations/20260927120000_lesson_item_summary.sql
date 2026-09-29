-- "Tóm tắt ý chính cần thuộc" cho mục lý thuyết (ly_thuyet) — đoạn ghi nhớ ngắn
-- (công thức/định nghĩa cốt lõi) hiện riêng, tách khỏi bài lý thuyết dài, để học
-- sinh xem nhanh mà không cần đọc hết body_html. Rỗng = chưa có tóm tắt (ẩn khối
-- này, không hiện rỗng) — sẽ được backfill bằng AI qua
-- scripts/backfill-lesson-summary.mts sau khi migration này chạy.
--
-- Chạy: supabase db query --linked -f supabase/migrations/20260927120000_lesson_item_summary.sql
-- Rollback: supabase db query --linked -f perf/rollback/20260927120000_lesson_item_summary.down.sql

alter table public.lesson_items
  add column if not exists summary_html text not null default '';
