-- Thẻ "3 kỹ năng yếu nhất" ở trang chủ học sinh: một RPC gộp, KHÔNG gọi get_lesson_mastery từng bài.
-- Cùng quy tắc docs/mastery-rules.md: gộp exam_question_results + practice_question_results,
-- 10 lượt gần nhất mỗi YCCĐ, <4 lượt = chưa đủ dữ liệu (không lên danh sách),
-- >=80% Nắm vững, 50–79% Cần luyện thêm, <50% Chưa đạt. Chỉ trả YCCĐ con (parent_id not null).
-- security invoker: học sinh chỉ thấy dữ liệu của chính mình (auth.uid()).
-- Chạy: supabase db query --linked -f <file này>. Cột lesson_id trên question_topics đã có.
begin;

create or replace function public.get_my_weakest_topics(p_limit integer default 3)
returns table (
  topic_id bigint,
  topic_name text,
  lesson_id bigint,
  lesson_title text,
  answered_count integer,
  pct integer,
  level text
)
language sql
stable
security invoker
set search_path = public
as $$
  with attempts as (
    select topic_id, earned, max, created_at,
           row_number() over (partition by topic_id order by created_at desc) as rn
    from (
      select topic_id, earned, max, created_at
      from public.exam_question_results
      where student_id = (select auth.uid()) and topic_id is not null
      union all
      select topic_id, earned, max, created_at
      from public.practice_question_results
      where student_id = (select auth.uid()) and topic_id is not null
    ) u
  ),
  agg as (
    select topic_id,
           count(*)::int as answered_count,
           sum(earned) as sum_earned,
           sum(max) as sum_max
    from attempts
    where rn <= 10
    group by topic_id
  )
  select t.id, t.name, t.lesson_id, l.title, a.answered_count,
         round(a.sum_earned / a.sum_max * 100)::int,
         case when a.sum_earned / a.sum_max >= 0.5 then 'practicing' else 'weak' end
  from agg a
  join public.question_topics t on t.id = a.topic_id and t.parent_id is not null
  join public.lessons l on l.id = t.lesson_id
  where a.answered_count >= 4 and a.sum_max > 0 and a.sum_earned / a.sum_max < 0.8
  order by a.sum_earned / a.sum_max asc, a.answered_count desc, t.id
  limit greatest(coalesce(p_limit, 3), 1);
$$;

revoke all on function public.get_my_weakest_topics(integer) from public;
grant execute on function public.get_my_weakest_topics(integer) to authenticated;

commit;

-- ROLLBACK:
-- drop function if exists public.get_my_weakest_topics(integer);
