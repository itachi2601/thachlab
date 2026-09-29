-- Rollback cho supabase/migrations/20260930100000_tutoring_exit_cooldown.sql (trả lại giới hạn 3 lượt)
create or replace function public.tutoring_exit_attempt_guard()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  v_need public.tutoring_needs%rowtype;
  v_count int;
begin
  select * into v_need from public.tutoring_needs where id = new.tutoring_need_id;
  if not found or v_need.student_id <> new.student_id then
    raise exception 'Không tìm thấy mục cần phụ đạo của em';
  end if;
  if v_need.status not in ('open', 'assigned', 'tutored') then
    raise exception 'Chủ đề này không còn cần phụ đạo';
  end if;
  select count(*) into v_count from public.tutoring_exit_attempts
    where tutoring_need_id = new.tutoring_need_id and student_id = new.student_id;
  if v_count >= 3 then
    raise exception 'Em đã dùng hết 3 lượt tự kiểm tra cho chủ đề này — hãy đăng ký buổi phụ đạo.';
  end if;
  new.topic_id := v_need.topic_id;
  new.form := v_need.form;
  new.pct := round(new.correct * 100.0 / new.total)::int;
  new.passed := new.pct >= 80;
  return new;
end; $$;
