-- Rollback ôn tập theo chặng — xem lại chặng cũ + em sai (24/10/2026).
-- BƯỚC 1: chạy lại phần `create or replace function public.review_board` trong
--   supabase/migrations/20261023120000_on_tap_dang_bai_tap.sql (đè bản gọi review_board_stage).
-- BƯỚC 2: chạy file này.
begin;
drop function if exists public.review_wrong_students(bigint, int);
drop function if exists public.review_board_stage(bigint, int);
commit;
