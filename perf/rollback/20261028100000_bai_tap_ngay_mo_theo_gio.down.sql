-- Rollback 20261028100000_bai_tap_ngay_mo_theo_gio
do $$ begin
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'review-open-due-stages';
  end if;
end $$;
drop function if exists public.review_open_due_stages();
drop function if exists public.review_roster(bigint);
-- review_my_state: chạy lại phần create or replace trong 20261025100000_on_tap_tu_hoc_ve_nha.sql
