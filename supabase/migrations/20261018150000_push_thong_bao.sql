-- Đẩy THÔNG BÁO trong web ra màn hình khoá điện thoại (Web Push, rung máy) — kiểu Duolingo.
-- Thêm notifications.pushed_at + hàm claim_notification_pushes (CHỈ service_role; Edge Function send-notification-push
-- gọi mỗi phút). Quy tắc: tối đa 3 push/ngày/em (ngày VN), chỉ trong khung 6–22h VN, thông báo quá 30 phút không
-- đẩy nữa (tin cũ vô nghĩa). Thông báo cũ có sẵn được đánh dấu đã đẩy để không bắn hàng loạt lúc bật.
-- Chạy lúc nào cũng được (chỉ thêm cột + hàm). Rollback ở cuối file.
begin;

alter table public.notifications add column if not exists pushed_at timestamptz;
update public.notifications set pushed_at = now() where pushed_at is null;
create index if not exists notifications_unpushed_idx on public.notifications (created_at) where pushed_at is null;

create or replace function public.claim_notification_pushes(p_now timestamptz default now())
returns table (
  notification_id bigint,
  subscription_id bigint,
  endpoint text,
  p256dh text,
  auth_key text,
  title text,
  body text,
  href text
)
language plpgsql
volatile
security definer
set search_path = public
as $$
declare
  v_hr int := extract(hour from (p_now at time zone 'Asia/Ho_Chi_Minh'))::int;
  v_day_start timestamptz := (date_trunc('day', p_now at time zone 'Asia/Ho_Chi_Minh')) at time zone 'Asia/Ho_Chi_Minh';
begin
  -- Tin quá cũ hoặc ngoài khung giờ: đóng dấu để không đẩy bù về sau.
  update public.notifications n set pushed_at = p_now
   where n.pushed_at is null and (n.created_at < p_now - interval '30 minutes' or v_hr < 6 or v_hr >= 22);

  return query
  with cand as (
    select n.id, n.user_id, n.title, n.body, n.href,
           row_number() over (partition by n.user_id order by n.created_at desc) as rn,
           (select count(*) from public.notifications x
             where x.user_id = n.user_id and x.pushed_at >= v_day_start and x.pushed_at <> p_now) as sent_today
      from public.notifications n
     where n.pushed_at is null and n.read_at is null
  ),
  pick as (
    -- mỗi em tối đa 1 tin mỗi lượt (tin mới nhất), và chưa quá 3 tin/ngày
    select * from cand where rn = 1 and sent_today < 3
  ),
  mark as (
    update public.notifications n set pushed_at = p_now
     where n.pushed_at is null and n.user_id in (select user_id from cand)
    returning n.id
  )
  select p.id, s.id, s.endpoint, s.p256dh, s.auth_key, p.title, p.body, p.href
    from pick p
    join public.push_subscriptions s on s.student_id = p.user_id and s.enabled
   where exists (select 1 from mark);
end;
$$;
revoke all on function public.claim_notification_pushes(timestamptz) from public, anon, authenticated;
grant execute on function public.claim_notification_pushes(timestamptz) to service_role;

commit;

-- ROLLBACK (cũng ở perf/rollback/20261018150000_push_thong_bao.down.sql):
-- drop function if exists public.claim_notification_pushes(timestamptz);
-- drop index if exists public.notifications_unpushed_idx;
-- alter table public.notifications drop column if exists pushed_at;
