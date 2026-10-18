-- Nhắc luyện hằng ngày: LÙI DẦN theo số ngày HS không học (học kiểu Duolingo, nhưng giọng nhẹ — SDT, không dọa mất chuỗi).
-- Nhắc mỗi ngày khi lần học/nộp đề cuối cách hôm nay 0–3 ngày; sau đó chỉ ở ngày thứ 5, 7, 14; quá 14 ngày thôi hẳn.
-- Trả thêm cột inactive_days để Edge Function chọn mẫu tin (luân phiên mẫu, đổi giọng khi lâu chưa học).
-- Thay hàm claim_push_reminders_due (drop + create vì đổi cột trả về). Chạy lúc nào cũng được. Rollback ở cuối file.
begin;

drop function if exists public.claim_push_reminders_due(timestamptz);

create function public.claim_push_reminders_due(p_now timestamptz default now())
returns table (
  subscription_id bigint,
  student_id uuid,
  endpoint text,
  p256dh text,
  auth_key text,
  topic_name text,
  lesson_id bigint,
  level text,
  inactive_days integer
)
language sql
volatile
security definer
set search_path = public
as $$
  with t as (
    select extract(hour from (p_now at time zone 'Asia/Ho_Chi_Minh'))::int as hr,
           (p_now at time zone 'Asia/Ho_Chi_Minh')::date as today,
           (date_trunc('day', p_now at time zone 'Asia/Ho_Chi_Minh')) at time zone 'Asia/Ho_Chi_Minh' as day_start
  ),
  due as (
    update public.push_subscriptions s
       set last_sent_at = p_now
      from t
     where s.enabled
       and s.remind_hour = t.hr
       and (s.last_sent_at is null or s.last_sent_at < t.day_start)
       and exists (select 1 from public.profiles p where p.id = s.student_id and p.role = 'student')
       and not exists (select 1 from public.practice_sessions ps where ps.student_id = s.student_id and ps.created_at >= t.day_start)
       and not exists (select 1 from public.exam_results er where er.student_id = s.student_id and er.created_at >= t.day_start)
       and (  -- lùi dần: ngày 0–3 sau lần học cuối nhắc mỗi ngày; sau đó chỉ ngày 5, 7, 14; quá 14 ngày thôi hẳn
         (t.today - coalesce((select (max(x.at) at time zone 'Asia/Ho_Chi_Minh')::date from (
             select ps.created_at as at from public.practice_sessions ps where ps.student_id = s.student_id
             union all select er.created_at from public.exam_results er where er.student_id = s.student_id) x),
             (s.created_at at time zone 'Asia/Ho_Chi_Minh')::date)) in (0,1,2,3,5,7,14)
       )
    returning s.id, s.student_id, s.endpoint, s.p256dh, s.auth_key
  ),
  attempts as (
    select u.student_id, u.topic_id, u.earned, u.max,
           row_number() over (partition by u.student_id, u.topic_id order by u.created_at desc) as rn
    from (
      select r.student_id, r.topic_id, r.earned, r.max, r.created_at
        from public.exam_question_results r
       where r.topic_id is not null and r.student_id in (select d.student_id from due d)
      union all
      select r.student_id, r.topic_id, r.earned, r.max, r.created_at
        from public.practice_question_results r
       where r.topic_id is not null and r.student_id in (select d.student_id from due d)
    ) u
  ),
  agg as (
    select student_id, topic_id, count(*)::int as n, sum(earned) as se, sum(max) as sm
      from attempts where rn <= 10 group by student_id, topic_id
  ),
  worst as (
    select distinct on (a.student_id)
           a.student_id, qt.name as topic_name, qt.lesson_id,
           case when a.se / a.sm >= 0.5 then 'practicing' else 'weak' end as level
      from agg a
      join public.question_topics qt on qt.id = a.topic_id and qt.parent_id is not null
     where a.n >= 4 and a.sm > 0 and a.se / a.sm < 0.8
     order by a.student_id, a.se / a.sm asc, a.n desc, qt.id
  )
  select d.id, d.student_id, d.endpoint, d.p256dh, d.auth_key, w.topic_name, w.lesson_id, w.level,
         (select (p_now at time zone 'Asia/Ho_Chi_Minh')::date - coalesce((select (max(x.at) at time zone 'Asia/Ho_Chi_Minh')::date from (
             select ps.created_at as at from public.practice_sessions ps where ps.student_id = d.student_id
             union all select er.created_at from public.exam_results er where er.student_id = d.student_id) x),
             (p_now at time zone 'Asia/Ho_Chi_Minh')::date))::int as inactive_days
    from due d left join worst w on w.student_id = d.student_id;
$$;
revoke all on function public.claim_push_reminders_due(timestamptz) from public, anon, authenticated;
grant execute on function public.claim_push_reminders_due(timestamptz) to service_role;


commit;

-- ROLLBACK: chạy lại phần tạo hàm trong supabase/migrations/20261005160000_push_subscriptions.sql
-- (drop function public.claim_push_reminders_due(timestamptz); rồi create lại bản gốc ở file đó).
