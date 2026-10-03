-- Hoàn tác 20261003150000_phu_dao_kiem_tra_cuoi_buoi.sql
-- THỨ TỰ: chạy TRƯỚC docs/supabase-migration-ta-policy-phudao-exit-quiz.sql (công thức "một em đạt 80% cùng ngày")
-- và supabase/migrations/20260930100000_tutoring_exit_cooldown.sql (guard cũ) để hai hàm không còn gọi
-- ta_tutoring_pass_ratio / window_id; rồi mới chạy file này.
begin;
drop policy if exists "ta reads own window attempts" on public.tutoring_exit_attempts;
drop index if exists public.tutoring_exit_attempts_window_need_uniq;
alter table public.tutoring_exit_attempts drop column if exists window_id;
drop function if exists public.ta_tutoring_pass_ratio(uuid);
drop table if exists public.tutoring_exit_windows;
commit;
