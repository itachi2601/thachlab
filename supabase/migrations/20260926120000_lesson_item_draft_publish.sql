-- Nháp → Đăng chính thức cho từng mục bài học (lesson_items).
--
-- published_at:  null = mục chưa từng đăng, học sinh chưa thấy (kể cả trong file tĩnh
--                của scripts/build-content.mjs). Mục cũ đã có sẵn coi như đã đăng từ
--                trước — set = now() một lần cho toàn bộ dòng hiện có (default now()
--                của ALTER TABLE cũng backfill luôn các dòng cũ).
-- draft_payload / draft_saved_at: bản đang sửa dở của 1 mục ĐÃ đăng — lưu tạm ở đây,
--                không đụng cột sống (title/body_html/…) cho tới khi admin bấm
--                "Đăng chính thức" ở /quan-tri/bai-hoc.
--
-- Chạy: supabase db query --linked -f supabase/migrations/20260926120000_lesson_item_draft_publish.sql
-- Rollback: supabase db query --linked -f perf/rollback/20260926120000_lesson_item_draft_publish.down.sql

alter table public.lesson_items
  add column if not exists published_at timestamptz not null default now(),
  add column if not exists draft_payload jsonb,
  add column if not exists draft_saved_at timestamptz;
