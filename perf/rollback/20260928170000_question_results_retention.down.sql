-- Rollback cho 20260928170000_question_results_retention.sql
-- Lưu ý: dòng lẻ đã gộp+xoá bởi rollup_question_results() không khôi phục được.
begin;
do $$
begin
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'question-results-rollup';
  end if;
end $$;

drop function if exists public.rollup_question_results(timestamptz, boolean);

-- rank_title_stats: bản 20260928100000 (chỉ đọc dòng lẻ)
create or replace function public.rank_title_stats(p_student uuid, p_title text)
returns table(n int, correct int, covered int, total_topics int, acc int, de_correct int, tb_correct int, kho_correct int)
language sql stable set search_path = public
as $$
  with topics as (
    select tt.topic_id from public.rank_title_topics tt where tt.title_code = p_title
  ),
  rows_ as (
    select coalesce(t.parent_id, t.id) as lesson_topic, eqr.is_correct, eqr.difficulty
    from public.exam_question_results eqr
    join public.question_topics t on t.id = eqr.topic_id
    where eqr.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
    union all
    select coalesce(t.parent_id, t.id) as lesson_topic, pqr.is_correct, pqr.difficulty
    from public.practice_question_results pqr
    join public.question_topics t on t.id = pqr.topic_id
    where pqr.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
  ),
  per_topic as (
    select lesson_topic, count(*) as c from rows_ group by lesson_topic
  )
  select
    (select count(*) from rows_)::int,
    (select count(*) filter (where is_correct) from rows_)::int,
    (select count(*) from per_topic where c >= 3)::int,
    (select count(*) from topics)::int,
    case when (select count(*) from rows_) > 0
      then round((select count(*) filter (where is_correct) from rows_) * 100.0 / (select count(*) from rows_))::int
      else 0 end,
    (select count(*) filter (where is_correct and difficulty = 'de') from rows_)::int,
    (select count(*) filter (where is_correct and difficulty = 'trung-binh') from rows_)::int,
    (select count(*) filter (where is_correct and difficulty = 'kho') from rows_)::int;
$$;

drop table if exists public.question_result_rollups;
alter table public.exam_results      drop column if exists results_rolled_up_at;
alter table public.practice_sessions drop column if exists results_rolled_up_at;
commit;
