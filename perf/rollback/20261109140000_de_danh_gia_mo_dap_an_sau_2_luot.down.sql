-- Rollback 20261109140000: trả ngưỡng mở đáp án về 3 lượt, bỏ hàm gợi ý.
drop function if exists public.get_exam_wrong_notes(bigint);
create or replace function public.exam_answers_revealed(p_exam_id bigint, p_uid uuid)
returns boolean
language sql stable security definer set search_path = public
as $$
  select not public.exam_is_assessment(p_exam_id)
      or exists (select 1 from public.lesson_items li
                 where li.kind = 'ly_thuyet' and p_exam_id = any (li.exam_ids))
      or (select count(*) from public.exam_results er where er.exam_id = p_exam_id and er.student_id = p_uid) >= 3
      or exists (select 1 from public.exam_results er join public.exams e on e.id = er.exam_id
                 where er.exam_id = p_exam_id and er.student_id = p_uid
                   and e.pass_score is not null and er.score >= e.pass_score)
$$;
