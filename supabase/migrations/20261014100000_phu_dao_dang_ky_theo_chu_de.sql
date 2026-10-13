-- ============================================================================
-- 14/10/2026 — Đăng ký buổi phụ đạo THEO CHỦ ĐỀ (thầy chốt 14/10)
--
-- Em đăng ký buổi phải chọn 1–3 chủ đề (cấp bài học) mình cần học. Mỗi chủ đề phải có sẵn "bài kiểm tra tương ứng"
-- (≥ 12 câu trong question_bank, tính cả yêu cầu cần đạt con) để bài thoát cuối buổi và tính giờ cho trợ giảng chạy được.
--   * Hạn chốt đăng ký: 6 giờ trước giờ bắt đầu buổi (giờ Việt Nam). Huỷ không bị chặn ở đây.
--   * Trợ giảng phụ trách buổi + thầy cô của lớp nhận thông báo (chuông) ngay khi em đăng ký, kèm tên em và chủ đề.
--   * Hàng chờ giữ chủ đề của em; em được xếp từ hàng chờ vào buổi (huỷ/mở lượt tiếp) mang theo chủ đề đó, không xét lại hạn 6 giờ.
--   * RPC tutoring_ready_topics(class) liệt kê chủ đề của lớp kèm số câu bài kiểm tra — em chọn chủ đề; thầy thấy chủ đề còn thiếu bài.
-- Chỉ thêm cột/hàm; đăng ký cũ giữ nguyên (topic_ids = '{}'). Chạy giờ nào cũng được.
-- Rollback: perf/rollback/20261014100000_phu_dao_dang_ky_theo_chu_de.down.sql
-- ============================================================================

alter table public.tutoring_registrations add column if not exists topic_ids bigint[] not null default '{}';
alter table public.tutoring_waitlist add column if not exists topic_ids bigint[] not null default '{}';
-- Điểm danh (trợ giảng đặt qua RPC ở file 20261014110000); khai báo ở đây để trigger bên dưới luôn thấy cột.
alter table public.tutoring_registrations
  add column if not exists attended boolean,
  add column if not exists attended_at timestamptz;

-- Số câu trong ngân hàng cho một chủ đề cấp bài (tính cả các yêu cầu cần đạt con), chưa lưu trữ.
create or replace function public.tutoring_topic_question_count(p_topic bigint)
returns int
language sql stable security definer set search_path = public
as $$
  select count(*)::int
  from public.question_bank qb
  where qb.archived is not true
    and (qb.topic_id = p_topic
         or qb.topic_id in (select t.id from public.question_topics t where t.parent_id = p_topic));
$$;
revoke all on function public.tutoring_topic_question_count(bigint) from public, anon;
grant execute on function public.tutoring_topic_question_count(bigint) to authenticated;

-- Ngưỡng tối thiểu để chủ đề "có bài kiểm tra tương ứng".
create or replace function public.tutoring_topic_min_questions() returns int
language sql immutable as $$ select 12 $$;

-- Chủ đề cấp bài của lớp kèm số câu bài kiểm tra; ready = đủ để đăng ký.
create or replace function public.tutoring_ready_topics(p_class_id bigint)
returns table (topic_id bigint, topic_name text, lesson_id bigint, question_count int, ready boolean)
language plpgsql stable security definer set search_path = public
as $$
begin
  if not (
    exists (select 1 from public.user_classes uc
            where uc.user_id = auth.uid() and uc.class_id = p_class_id and uc.status = 'active')
    or public.manages_class(p_class_id) or public.assists_class(p_class_id) or public.is_admin()
  ) then
    raise exception 'Không có quyền xem chủ đề của lớp này.';
  end if;
  return query
    select t.id, t.name, t.lesson_id, c.n, c.n >= public.tutoring_topic_min_questions()
    from public.question_topics t
    cross join lateral (select public.tutoring_topic_question_count(t.id) as n) c
    where t.parent_id is null
      and t.chapter_id in (select cc.chapter_id from public.chapter_classes cc where cc.class_id = p_class_id)
    order by t.sort_order, t.id;
end; $$;
revoke all on function public.tutoring_ready_topics(bigint) from public, anon;
grant execute on function public.tutoring_ready_topics(bigint) to authenticated;

-- Kiểm chủ đề đăng ký: 1–3 chủ đề khác nhau, cấp bài, thuộc chương của lớp, đủ câu bài kiểm tra.
create or replace function public.tutoring_check_topics(p_slot_id bigint, p_topics bigint[], p_check_deadline boolean, p_check_ready boolean default true)
returns void
language plpgsql stable security definer set search_path = public
as $$
declare
  s public.tutoring_slots;
  n int := coalesce(array_length(p_topics, 1), 0);
  t bigint;
  starts timestamptz;
begin
  select * into s from public.tutoring_slots where id = p_slot_id;
  if not found then raise exception 'Không tìm thấy buổi phụ đạo.'; end if;

  if n < 1 then raise exception 'Em chọn ít nhất 1 chủ đề muốn học trong buổi này.'; end if;
  if n > 3 then raise exception 'Mỗi buổi em chọn tối đa 3 chủ đề.'; end if;
  if (select count(distinct x) from unnest(p_topics) x) <> n then
    raise exception 'Chủ đề bị chọn trùng.';
  end if;

  foreach t in array p_topics loop
    if not p_check_ready then continue; end if; -- em đã được kiểm lúc vào hàng chờ; không làm hỏng việc huỷ của người khác
    if not exists (
      select 1 from public.question_topics q
      where q.id = t and q.parent_id is null
        and q.chapter_id in (select cc.chapter_id from public.chapter_classes cc where cc.class_id = s.class_id)
    ) then
      raise exception 'Chủ đề không thuộc chương trình của lớp.';
    end if;
    if public.tutoring_topic_question_count(t) < public.tutoring_topic_min_questions() then
      raise exception 'Chủ đề này chưa có đủ câu để kiểm tra cuối buổi, chưa đăng ký được.';
    end if;
  end loop;

  if p_check_deadline then
    starts := (s.work_date + s.start_time) at time zone 'Asia/Ho_Chi_Minh';
    if starts - interval '6 hours' < now() then
      raise exception 'Đã quá hạn đăng ký (chốt 6 giờ trước giờ học).';
    end if;
  end if;
end; $$;
revoke all on function public.tutoring_check_topics(bigint, bigint[], boolean, boolean) from public, anon, authenticated;

-- Đăng ký trực tiếp (độ sâu trigger 1) phải chọn chủ đề + còn hạn; xếp từ hàng chờ (độ sâu ≥ 2) chỉ kiểm chủ đề.
-- Tên bắt đầu bằng "trg_tutoring_reg_" để chạy TRƯỚC trg_tutoring_slot_register (tăng đếm).
create or replace function public.tutoring_registration_guard()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  new.attended := null; -- chỉ trợ giảng điểm danh (RPC tutoring_mark_attendance), học sinh không tự đặt được
  new.attended_at := null;
  perform public.tutoring_check_topics(
    new.slot_id, new.topic_ids,
    pg_trigger_depth() <= 1 and coalesce(current_setting('app.tutoring_skip_deadline', true), '') <> '1',
    pg_trigger_depth() <= 1 and coalesce(current_setting('app.tutoring_skip_deadline', true), '') <> '1'
  );
  return new;
end; $$;
drop trigger if exists trg_tutoring_reg_guard on public.tutoring_registrations;
create trigger trg_tutoring_reg_guard before insert on public.tutoring_registrations
  for each row execute function public.tutoring_registration_guard();

-- Hàng chờ cũng phải có chủ đề (để khi lên buổi, trợ giảng biết em cần gì).
create or replace function public.tutoring_waitlist_topics_guard()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  perform public.tutoring_check_topics(new.slot_id, new.topic_ids, true);
  return new;
end; $$;
drop trigger if exists trg_tutoring_waitlist_topics on public.tutoring_waitlist;
create trigger trg_tutoring_waitlist_topics before insert on public.tutoring_waitlist
  for each row execute function public.tutoring_waitlist_topics_guard();

-- Báo trợ giảng phụ trách buổi + thầy cô của lớp: "em X đăng ký buổi dd/mm hh:mm, chủ đề …".
create or replace function public.tutoring_registration_notify()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  s public.tutoring_slots;
  v_name text;
  v_topics text;
  v_title text;
  v_body text;
begin
  select * into s from public.tutoring_slots where id = new.slot_id;
  select coalesce(full_name, 'Một em') into v_name from public.profiles where id = new.student_id;
  select string_agg(q.name, ', ' order by q.name) into v_topics
    from public.question_topics q where q.id = any(new.topic_ids);
  v_title := v_name || ' đăng ký phụ đạo ' || to_char(s.work_date, 'DD/MM') || ' ' || to_char(s.start_time, 'HH24:MI');
  v_body := 'Chủ đề: ' || coalesce(v_topics, '—');

  insert into public.notifications (user_id, kind, title, body, href)
  select a.user_id, 'phu_dao_dang_ky', v_title, v_body, '/tro-giang/phu-dao?tab=slots'
    from public.ta_assistants a where a.id = s.assistant_id and a.user_id is not null;

  insert into public.notifications (user_id, kind, title, body, href)
  select ci.instructor_id, 'phu_dao_dang_ky', v_title, v_body, '/dashboard-thpt'
    from public.class_instructors ci where ci.class_id = s.class_id;
  return new;
end; $$;
drop trigger if exists trg_tutoring_reg_notify on public.tutoring_registrations;
create trigger trg_tutoring_reg_notify after insert on public.tutoring_registrations
  for each row execute function public.tutoring_registration_notify();

-- Xếp từ hàng chờ vào buổi: mang chủ đề của em theo.
create or replace function public.tutoring_slot_unregister()
returns trigger language plpgsql security definer set search_path = public
as $$
declare w public.tutoring_waitlist;
begin
  update public.tutoring_slots
    set registered_count = greatest(0, registered_count - 1)
    where id = old.slot_id;

  if exists (
    select 1 from public.tutoring_slots
    where id = old.slot_id and status = 'open' and work_date >= current_date and registered_count < capacity
  ) then
    select * into w from public.tutoring_waitlist
      where slot_id = old.slot_id order by created_at, id limit 1 for update skip locked;
    if found then
      delete from public.tutoring_waitlist where id = w.id;
      insert into public.tutoring_registrations (slot_id, student_id, topic_ids)
        values (w.slot_id, w.student_id, w.topic_ids)
        on conflict (slot_id, student_id) do nothing;
    end if;
  end if;
  return old;
end; $$;

-- "Mở lượt tiếp": chuyển em đầu hàng chờ sang buổi mới, mang chủ đề theo.
create or replace function public.tutoring_slot_open_next(
  p_slot_id bigint, p_work_date date, p_start time, p_end time
) returns bigint
language plpgsql security definer set search_path = public
as $$
declare
  s public.tutoring_slots;
  new_id bigint;
  w record;
begin
  select * into s from public.tutoring_slots where id = p_slot_id for update;
  if not found then raise exception 'Không tìm thấy buổi phụ đạo.'; end if;
  if not (
    exists (select 1 from public.ta_assistants a where a.id = s.assistant_id and a.user_id = auth.uid())
    or public.is_admin()
  ) then
    raise exception 'Chỉ trợ giảng phụ trách buổi này mới mở lượt tiếp.';
  end if;
  if p_end <= p_start then raise exception 'Giờ kết thúc phải sau giờ bắt đầu.'; end if;
  if not exists (select 1 from public.tutoring_waitlist where slot_id = p_slot_id) then
    raise exception 'Buổi này không có em nào đang chờ.';
  end if;

  perform set_config('app.tutoring_skip_deadline', '1', true); -- em đã đăng ký từ trước, không xét lại hạn 6 giờ
  insert into public.tutoring_slots (assistant_id, class_id, work_date, start_time, end_time, topic_ids, capacity, note)
    values (s.assistant_id, s.class_id, p_work_date, p_start, p_end, s.topic_ids, s.capacity, s.note)
    returning id into new_id;

  for w in
    select id, student_id, topic_ids from public.tutoring_waitlist
      where slot_id = p_slot_id order by created_at, id limit s.capacity
  loop
    delete from public.tutoring_waitlist where id = w.id;
    insert into public.tutoring_registrations (slot_id, student_id, topic_ids) values (new_id, w.student_id, w.topic_ids);
  end loop;
  return new_id;
end; $$;
grant execute on function public.tutoring_slot_open_next(bigint, date, time, time) to authenticated;
