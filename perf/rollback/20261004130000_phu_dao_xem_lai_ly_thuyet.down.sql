-- Hoàn tác 20261004130000_phu_dao_xem_lai_ly_thuyet.sql: trả guard về bản 20261003150000 (không đòi xem lại lý thuyết),
-- rồi gỡ RPC + bảng lượt xem lại.
begin;
create or replace function public.tutoring_exit_attempt_guard()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  v_need public.tutoring_needs%rowtype;
  v_win public.tutoring_exit_windows%rowtype;
  v_last timestamptz;
begin
  select * into v_need from public.tutoring_needs where id = new.tutoring_need_id;
  if not found or v_need.student_id <> new.student_id then
    raise exception 'Không tìm thấy mục cần phụ đạo của em';
  end if;
  if v_need.status not in ('open', 'assigned', 'tutored') then
    raise exception 'Chủ đề này không còn cần phụ đạo';
  end if;

  if new.window_id is not null then
    select * into v_win from public.tutoring_exit_windows where id = new.window_id;
    if not found or not (new.student_id = any (v_win.student_ids))
       or not (v_need.topic_id = any (v_win.topic_ids)) then
      raise exception 'Bài kiểm tra cuối buổi này không dành cho em hoặc chủ đề này';
    end if;
    if now() > v_win.closes_at + interval '30 seconds' then
      raise exception 'Cửa sổ kiểm tra cuối buổi đã đóng';
    end if;
    new.topic_id := v_need.topic_id;
    new.form := v_need.form;
    new.pct := round(new.correct * 100.0 / new.total)::int;
    new.passed := new.pct >= 70;
    return new;
  end if;

  select max(created_at) into v_last from public.tutoring_exit_attempts
    where tutoring_need_id = new.tutoring_need_id and student_id = new.student_id;
  if v_last is not null and v_last > now() - interval '24 hours' then
    raise exception 'Lượt tự kiểm tra tiếp theo của chủ đề này mở sau 24 giờ kể từ lượt trước — em ôn lại lý thuyết rồi quay lại nhé.';
  end if;

  new.topic_id := v_need.topic_id;
  new.form := v_need.form;
  new.pct := round(new.correct * 100.0 / new.total)::int;
  new.passed := new.pct >= 80;
  return new;
end; $$;
drop function if exists public.tutoring_review_ping(bigint, int, int, int);
drop function if exists public.tutoring_review_start(bigint, int, int, int);
drop function if exists public.tutoring_theory_item(bigint);
drop table if exists public.tutoring_theory_reviews;
commit;
