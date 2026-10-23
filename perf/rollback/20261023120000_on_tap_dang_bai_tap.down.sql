-- Rollback ôn tập theo chặng — phần ôn dạng bài tập (23/10/2026).
-- Sau khi chạy: khôi phục review_board bản cũ bằng cách chạy lại hàm review_board trong
-- supabase/migrations/20261021120000_on_tap_theo_chang.sql (bản cũ không có by_dang).
begin;
drop function if exists public.review_dang_pool(bigint);
drop function if exists public.review_build_dang_exam(bigint, bigint, int);
drop function if exists public.lesson_dang_labels(bigint);
drop table if exists public.question_dang;
commit;
