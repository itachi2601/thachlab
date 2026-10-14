-- ============================================================================
-- Mạng nhện năng lực: thêm phạm vi "cả khoá" (14/10/2026)
--
-- RPC get_my_course_mastery_pct(p_before timestamptz default null):
--   Như get_my_chapter_mastery_pct nhưng trả MỌI bài đã công bố của khoá học
--   (= các chương cùng subject_code với chương em làm gần nhất và chung ít nhất một lớp
--   với chương đó), để giao diện chuyển được: theo chương (đỉnh = bài), cả khoá (đỉnh = chương;
--   với khoá HSG KHTN 9 mỗi chương chính là một mảng Cơ / Nhiệt – Âm / Điện / Quang / Điện từ).
--   Thêm cột: chapter_sort, subject_code, is_latest (chương em làm gần nhất), earned, max
--   (để giao diện gộp % cả chương đúng theo Σearned/Σmax, không lấy trung bình của % bài).
-- Công thức mỗi bài giữ ĐÚNG get_my_chapter_mastery_pct / docs/mastery-rules.md.
-- Chỉ đọc theo auth.uid(), security invoker, không nới RLS. Không đổi bảng.
-- Cách chạy: bash scripts/run-migrations.sh
-- ============================================================================

begin;

create or replace function public.get_my_course_mastery_pct(p_before timestamptz default null)
returns table (
  chapter_id bigint,
  chapter_title text,
  chapter_sort integer,
  subject_code text,
  is_latest boolean,
  lesson_id bigint,
  lesson_title text,
  sort_order integer,
  answered_count integer,
  earned numeric,
  max numeric,
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
  course_chapters as (
    select c.id, c.title, c.sort_order, c.subject_code
    from public.chapters c
    where c.id = (select chapter_id from latest_chapter)
       or (
         c.subject_code is not distinct from
           (select c0.subject_code from public.chapters c0 where c0.id = (select chapter_id from latest_chapter))
         and exists (
           select 1
           from public.chapter_classes cc
           join public.chapter_classes cc0 on cc0.class_id = cc.class_id
           where cc.chapter_id = c.id
             and cc0.chapter_id = (select chapter_id from latest_chapter)
         )
       )
  ),
  course_lessons as (
    select l.id, l.title, l.sort_order, l.chapter_id
    from public.lessons l
    where l.chapter_id in (select id from course_chapters)
      and l.published
  ),
  groups as (
    select t.id as topic_id, t.lesson_id
    from public.question_topics t
    where t.lesson_id in (select id from course_lessons)
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
    cc.title,
    cc.sort_order,
    cc.subject_code,
    cl.chapter_id = (select chapter_id from latest_chapter),
    cl.id,
    cl.title,
    cl.sort_order,
    coalesce(p.answered_count, 0),
    coalesce(p.se, 0),
    coalesce(p.sm, 0),
    case when coalesce(p.sm, 0) = 0 then null else round(p.se / p.sm * 100)::int end,
    case
      when p.lesson_id is null or p.have_data = 0 then 'insufficient'
      when p.min_rnk = 0 then 'weak'
      when p.min_rnk = 1 then 'practicing'
      else 'mastered'
    end
  from course_lessons cl
  join course_chapters cc on cc.id = cl.chapter_id
  left join per_lesson p on p.lesson_id = cl.id
  order by cc.sort_order, cc.id, cl.sort_order;
$$;

revoke all on function public.get_my_course_mastery_pct(timestamptz) from public;
grant execute on function public.get_my_course_mastery_pct(timestamptz) to authenticated;

commit;

-- ============================================================================
-- ROLLBACK
-- drop function if exists public.get_my_course_mastery_pct(timestamptz);
-- ============================================================================
