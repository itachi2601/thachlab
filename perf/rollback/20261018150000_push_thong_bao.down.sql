drop function if exists public.claim_notification_pushes(timestamptz);
drop index if exists public.notifications_unpushed_idx;
alter table public.notifications drop column if exists pushed_at;
