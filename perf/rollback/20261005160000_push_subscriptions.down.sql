-- Hoàn tác 20261005160000_push_subscriptions.sql (mất toàn bộ đăng ký nhắc; HS bật lại ở /tai-khoan).
begin;
drop function if exists public.claim_push_reminders_due(timestamptz);
drop function if exists public.upsert_my_push_subscription(text, text, text, integer);
drop table if exists public.push_subscriptions;
commit;
