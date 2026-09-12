-- ============================================================
-- Migration: Thứ hạng học sinh (theo từng đề + theo bài kiểm tra định kỳ)
-- Chạy SAU: supabase-migration-classes.sql, supabase-migration-user-classes-approval.sql,
--           supabase-migration-exam-analytics.sql
-- Idempotent — chạy lại được.
--
-- RLS của exam_results/exam_question_results chỉ cho học sinh đọc bài của CHÍNH MÌNH,
-- nên không thể tính hạng ở phía trình duyệt. Hai hàm dưới đây chạy security definer
-- (bỏ qua RLS nội bộ) nhưng chỉ trả về DÒNG CỦA NGƯỜI GỌI (auth.uid()) — không lộ tên/
-- điểm của bạn khác, giống cách sweep_missed_assessments/evaluate_student_alerts đang làm.
-- ============================================================

-- Hạng của học sinh hiện tại trong MỘT đề cụ thể, so với các bạn đang active cùng
-- (ít nhất một) lớp với mình và đã làm đề đó (tính điểm cao nhất mỗi bạn).
create or replace function public.get_exam_rank(p_exam_id bigint)
returns table(rnk int, total int, my_best numeric)
language plpgsql security definer stable set search_path = public
as $$
declare
  v_student uuid := auth.uid();
begin
  return query
  with my_classes as (
    select class_id from public.user_classes
    where user_id = v_student and status = 'active'
  ),
  classmates as (
    select distinct uc.user_id
    from public.user_classes uc
    where uc.class_id in (select class_id from my_classes)
      and uc.status = 'active'
  ),
  best_scores as (
    select er.student_id, max(er.score) as best
    from public.exam_results er
    where er.exam_id = p_exam_id
      and er.student_id in (select user_id from classmates)
    group by er.student_id
  ),
  ranked as (
    select student_id, best, rank() over (order by best desc) as rnk
    from best_scores
  )
  select r.rnk::int, (select count(*)::int from best_scores), r.best
  from ranked r
  where r.student_id = v_student;
end;
$$;

grant execute on function public.get_exam_rank(bigint) to authenticated;

-- Hạng của học sinh hiện tại theo điểm TRUNG BÌNH các bài kiểm tra định kỳ (class_assessments)
-- của MỘT lớp cụ thể — bài chưa làm bị bỏ qua (không tính 0), giống logic cảnh báo phụ đạo.
create or replace function public.get_periodic_rank(p_class_id bigint)
returns table(rnk int, total int, my_avg numeric, class_avg numeric)
language plpgsql security definer stable set search_path = public
as $$
declare
  v_student uuid := auth.uid();
begin
  -- chỉ tính hạng cho lớp mà chính học sinh đang active — không cho dò lớp khác
  if not exists (
    select 1 from public.user_classes
    where user_id = v_student and class_id = p_class_id and status = 'active'
  ) then
    return;
  end if;

  return query
  with classmates as (
    select user_id from public.user_classes
    where class_id = p_class_id and status = 'active'
  ),
  scores as (
    select c.user_id as student_id,
           (select max(er.score) from public.exam_results er
              where er.student_id = c.user_id and er.exam_id = ca.exam_id) as best
    from classmates c
    cross join public.class_assessments ca
    where ca.class_id = p_class_id
  ),
  avgs as (
    select student_id, avg(best) as avg_score
    from scores
    where best is not null
    group by student_id
  ),
  ranked as (
    select student_id, avg_score, rank() over (order by avg_score desc) as rnk
    from avgs
  )
  select r.rnk::int, (select count(*)::int from avgs), r.avg_score,
         (select avg(avg_score) from avgs)
  from ranked r
  where r.student_id = v_student;
end;
$$;

grant execute on function public.get_periodic_rank(bigint) to authenticated;
