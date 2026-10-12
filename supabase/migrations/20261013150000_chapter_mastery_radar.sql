-- ============================================================================
-- Sơ đồ mạng nhện năng lực theo BÀI trong CHƯƠNG đang học (13/10/2026)
--
-- RPC get_my_chapter_mastery_pct(p_before timestamptz default null):
--   Trả 1 dòng/bài đã công bố của chương mà học sinh đang đăng nhập làm bài gần nhất
--   (chương suy từ lượt trả lời mới nhất, tính tới thời điểm p_before nếu có).
--   Cột: chapter_id, chapter_title, lesson_id, lesson_title, sort_order,
--        answered_count, pct (0–100, null khi chưa có), level (mastered/practicing/weak/insufficient).
--   p_before = null → hiện tại; p_before = now() - 30 ngày → "chính em tháng trước".
--
-- Công thức giữ ĐÚNG docs/mastery-rules.md: mỗi YCCĐ lấy ≤10 lượt gần nhất (gộp exam_ +
-- practice_question_results), pct của bài = Σearned/Σmax của mọi nhóm; nhãn bài = nhãn THẤP
-- NHẤT trong các nhóm (như get_lesson_mastery), <4 lượt ở mọi nhóm → insufficient.
-- Chỉ đọc theo auth.uid(), security invoker, không nới RLS.
-- Cách chạy: bash scripts/run-migrations.sh (đã thêm vào FILES)
-- ============================================================================

begin;

create or replace function public.get_my_chapter_mastery_pct(p_before timestamptz default null)
returns table (
  chapter_id bigint,
  chapter_title text,
  lesson_id bigint,
  lesson_title text,
  sort_order integer,
  answered_count integer,
  pct integer,
  level text
)
language sql
stable
security invoker
set search_path = public
as $$
  with me as (select auth.uid() as uid),
  all_attempts as (
    select topic_id, earned, max, created_at
    from public.exam_question_results
    where student_id = (select uid from me)
      and topic_id is not null
      and (p_before is null or created_at <= p_before)
    union all
    select topic_id, earned, max, created_at
    from public.practice_question_results
    where student_id = (select uid from me)
      and topic_id is not null
      and (p_before is null or created_at <= p_before)
  ),
  latest_chapter as (
    select l.chapter_id
    from all_attempts a
    join public.question_topics t on t.id = a.topic_id
    join public.lessons l on l.id = t.lesson_id
    order by a.created_at desc
    limit 1
  ),
  chapter_lessons as (
    select l.id, l.title, l.sort_order, l.chapter_id
    from public.lessons l
    where l.chapter_id = (select chapter_id from latest_chapter)
      and l.published
  ),
  groups as (
    select t.id as topic_id, t.lesson_id
    from public.question_topics t
    where t.lesson_id in (select id from chapter_lessons)
  ),
  ranked_attempts as (
    select a.topic_id, a.earned, a.max,
           row_number() over (partition by a.topic_id order by a.created_at desc) as rn
    from all_attempts a
    where a.topic_id in (select topic_id from groups)
  ),
  last10 as (select topic_id, earned, max from ranked_attempts where rn <= 10),
  agg as (
    select g.lesson_id, g.topic_id,
           count(a.topic_id)::int as n,
           coalesce(sum(a.earned), 0)::numeric as se,
           coalesce(sum(a.max), 0)::numeric as sm
    from groups g
    left join last10 a on a.topic_id = g.topic_id
    group by g.lesson_id, g.topic_id
  ),
  leveled as (
    select *,
      case
        when n < 4 or sm = 0 then null
        when se / sm >= 0.8 then 2
        when se / sm >= 0.5 then 1
        else 0
      end as rnk
    from agg
  ),
  per_lesson as (
    select lesson_id,
           sum(n)::int as answered_count,
           sum(se) as se, sum(sm) as sm,
           min(rnk) as min_rnk,
           count(*) filter (where rnk is not null) as have_data
    from leveled
    group by lesson_id
  )
  select
    cl.chapter_id,
    c.title,
    cl.id,
    cl.title,
    cl.sort_order,
    coalesce(p.answered_count, 0),
    case when coalesce(p.sm, 0) = 0 then null else round(p.se / p.sm * 100)::int end,
    case
      when p.lesson_id is null or p.have_data = 0 then 'insufficient'
      when p.min_rnk = 0 then 'weak'
      when p.min_rnk = 1 then 'practicing'
      else 'mastered'
    end
  from chapter_lessons cl
  join public.chapters c on c.id = cl.chapter_id
  left join per_lesson p on p.lesson_id = cl.id
  order by cl.sort_order;
$$;

revoke all on function public.get_my_chapter_mastery_pct(timestamptz) from public;
grant execute on function public.get_my_chapter_mastery_pct(timestamptz) to authenticated;

commit;

-- ============================================================================
-- ROLLBACK
-- drop function if exists public.get_my_chapter_mastery_pct(timestamptz);
-- ============================================================================
