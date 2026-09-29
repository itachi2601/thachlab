-- ============================================================================
-- GĐ 1b #3 — Kênh phụ đạo: thay giới hạn 3 lượt tự kiểm tra bằng thời gian chờ 24 giờ giữa 2 lượt
-- cùng một chủ đề (để kịp ôn lại đoạn lý thuyết trước lượt sau). Chỉ thay hàm guard, không đổi bảng.
-- Hằng số 24 giờ khớp EXIT_COOLDOWN_HOURS trong services/tutoring.ts.
--
-- Cách chạy: supabase db query --linked -f supabase/migrations/20260930100000_tutoring_exit_cooldown.sql
-- Rollback:  supabase db query --linked -f perf/rollback/20260930100000_tutoring_exit_cooldown.down.sql
-- ============================================================================
create or replace function public.tutoring_exit_attempt_guard()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  v_need public.tutoring_needs%rowtype;
  v_last timestamptz;
begin
  select * into v_need from public.tutoring_needs where id = new.tutoring_need_id;
  if not found or v_need.student_id <> new.student_id then
    raise exception 'Không tìm thấy mục cần phụ đạo của em';
  end if;
  if v_need.status not in ('open', 'assigned', 'tutored') then
    raise exception 'Chủ đề này không còn cần phụ đạo';
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
