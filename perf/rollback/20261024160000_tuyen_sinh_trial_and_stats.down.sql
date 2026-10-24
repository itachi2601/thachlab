-- Rollback tuyển sinh GĐ 0 (T1b, 24/10/2026). Xoá cả dữ liệu đơn học thử: chỉ chạy khi chưa có đơn thật cần giữ.
begin;
do $$
begin
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule('public-stats-refresh');
  end if;
exception when others then null;
end $$;
drop table if exists public.referrals;
alter table public.thpt_courses drop column if exists referral_discount_pct;
drop function if exists public.get_public_stats();
drop function if exists public.refresh_public_stats();
drop table if exists public.public_stats_cache;
drop function if exists public.submit_trial_request(jsonb);
drop trigger if exists trg_trial_request_notify on public.trial_requests;
drop function if exists public.trial_request_notify();
drop table if exists public.trial_requests;
commit;
