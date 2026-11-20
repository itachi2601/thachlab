-- Rollback 20261120120000_lesson_clip_views (xoá luôn dữ liệu lượt xem + bảng cộng dồn)
do $$ begin
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'lesson-clip-views-rollup';
  end if;
end $$;
drop function if exists public.rollup_lesson_clip_views(timestamptz);
drop function if exists public.log_clip_view(jsonb);
drop table if exists public.lesson_clip_view_rollups;
drop table if exists public.lesson_clip_views;
