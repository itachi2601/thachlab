-- Rollback cho 20260927130000_homework_check.sql.
-- Xoá RP đã cộng từ nguồn 'homework_check' TRƯỚC khi khôi phục constraint cũ
-- (constraint cũ không cho phép 'homework_check').

delete from public.rank_rp_awards where source_kind = 'homework_check';

alter table public.rank_rp_awards drop constraint if exists rank_rp_awards_source_kind_check;
alter table public.rank_rp_awards add constraint rank_rp_awards_source_kind_check
  check (source_kind in ('practice', 'fix', 'weekly_goal', 'daily_streak', 'manual'));

drop trigger if exists trg_notify_homework_announcement on public.class_announcements;
drop function if exists public.trg_notify_homework_announcement();

revoke execute on function public.homework_check_set(bigint, uuid, int, bigint) from authenticated;
drop function if exists public.homework_check_set(bigint, uuid, int, bigint);

drop policy if exists "student read own homework check" on public.class_homework_checks;
drop policy if exists "staff read homework checks" on public.class_homework_checks;
drop table if exists public.class_homework_checks;
