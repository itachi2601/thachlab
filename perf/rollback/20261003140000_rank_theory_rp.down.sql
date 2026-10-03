-- Hoàn tác 20261003140000_rank_theory_rp.sql. RP 'theory' đã cộng: xoá dòng awards/ledger trước (rồi gọi rank_recompute_season để tính lại tổng).
drop function if exists public.rank_theory_submit(bigint, jsonb);
drop function if exists public.rank_theory_open(bigint);
delete from public.rank_rp_ledger where source_kind = 'theory';
delete from public.rank_rp_awards where source_kind = 'theory';
drop table if exists public.theory_sessions;
drop table if exists public.theory_quiz_keys;
alter table public.rank_rp_awards drop constraint if exists rank_rp_awards_source_kind_check;
alter table public.rank_rp_awards add constraint rank_rp_awards_source_kind_check
  check (source_kind in ('practice', 'fix', 'weekly_goal', 'daily_streak', 'manual', 'homework_check', 'progress_week', 'class_goal'));
