-- Chạy một lần trong Supabase SQL Editor để bật danh hiệu xếp hạng theo khóa.
create or replace function public.get_cnc_course_leaderboard(p_course_id bigint)
returns table(student_id uuid, first_activity_at timestamptz, completed_at timestamptz, accuracy numeric, passed_count bigint)
language sql security definer set search_path=public as $$
  with enrolled as (
    select ce.student_id from public.course_enrollments ce
    where ce.course_id=p_course_id and ce.status in ('active','completed')
  ), stats as (
    select e.student_id,min(r.last_activity_at) filter(where r.attempt_count>0) first_activity_at,
      case when count(*) filter(where r.completed)=17 then max(r.last_activity_at) filter(where r.completed) end completed_at,
      coalesce(round(avg(100.0*r.best_score/nullif(r.total_questions,0)) filter(where r.total_questions>0),1),0) accuracy,
      count(*) filter(where r.completed) passed_count
    from enrolled e left join public.cnc_learning_records r on r.student_id=e.student_id and r.course_id=p_course_id group by e.student_id
  ) select * from stats;
$$;
grant execute on function public.get_cnc_course_leaderboard(bigint) to authenticated;
