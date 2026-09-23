-- ============================================================
-- Ghép cặp buổi cho lớp học 2 buổi/tuần (vd 12L1: 1 buổi A + 1 buổi B,
-- mỗi buổi lại có 2 khung giờ để chọn — xem docs/supabase-seed-lop-vatly-thpt-thach-2026.sql).
--
-- Mỗi khung giờ là một dòng thpt_courses riêng để phụ huynh chọn được giờ,
-- nhưng phải chặn không cho đăng ký 2 khoá cùng nhóm (2 buổi A, hoặc 2 buổi
-- B) — trước đây không có gì ngăn việc này.
--
-- pair_key: định danh lớp gộp (vd '12L1'). pair_slot: 'A' / 'B'. Lớp học
-- 1 buổi/tuần (10L3, 11L4…) để cả hai cột null — không bị chặn gì thêm.
--
-- Cần chạy SAU: supabase-migration-khoa-hoc-thpt.sql.
-- Idempotent — chạy lại được. Chạy trong Supabase → SQL Editor.
-- ============================================================

alter table public.thpt_courses add column if not exists pair_key text;
alter table public.thpt_courses add column if not exists pair_slot text check (pair_slot is null or pair_slot in ('A', 'B'));
create index if not exists thpt_courses_pair_idx on public.thpt_courses (pair_key, pair_slot) where pair_key is not null;

create or replace function public.thpt_register(
  p_course_id bigint,
  p_student_id uuid default null,
  p_child_name text default '',
  p_contact text default '',
  p_note text default ''
)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_user uuid := auth.uid();
  c public.thpt_courses%rowtype;
  v_taken int;
  v_late boolean;
  v_status text;
  v_id bigint;
  v_student_role text;
begin
  if v_user is null then
    raise exception 'Bạn cần đăng nhập trước khi đăng ký.';
  end if;

  select * into c from public.thpt_courses where id = p_course_id;
  if c.id is null or c.status <> 'active' or not (c.is_public or public.manages_class(c.class_id)) then
    raise exception 'Khoá học không còn mở đăng ký.';
  end if;

  if p_student_id is not null then
    if p_student_id <> v_user and not public.is_parent_of(p_student_id) then
      raise exception 'Bạn chỉ đăng ký được cho chính mình hoặc cho con đã nối với tài khoản.';
    end if;
    select role into v_student_role from public.profiles where id = p_student_id;
    if v_student_role in ('admin', 'instructor', 'tro_giang') then
      raise exception 'Tài khoản này không phải tài khoản học sinh.';
    end if;
  elsif coalesce(trim(p_child_name), '') = '' then
    raise exception 'Nhập họ tên của con.';
  end if;

  -- Lớp 2 buổi/tuần (12L1…): chặn đăng ký 2 khoá cùng nhóm buổi (2 buổi A hoặc 2 buổi B).
  if c.pair_key is not null then
    if p_student_id is not null then
      if exists (
        select 1 from public.thpt_registrations r
        join public.thpt_courses c2 on c2.id = r.course_id
        where r.student_id = p_student_id
          and r.status in ('pending', 'catchup', 'active')
          and c2.pair_key = c.pair_key and c2.pair_slot = c.pair_slot
          and c2.id <> c.id
      ) then
        raise exception 'Đã đăng ký một lớp buổi % rồi — chọn lớp buổi % để đủ lịch tuần, không đăng ký 2 lớp cùng buổi %.',
          c.pair_slot, (case when c.pair_slot = 'A' then 'B' else 'A' end), c.pair_slot;
      end if;
    elsif coalesce(trim(p_child_name), '') <> '' and exists (
      select 1 from public.thpt_registrations r
      join public.thpt_courses c2 on c2.id = r.course_id
      where r.student_id is null and r.registered_by = v_user
        and lower(trim(r.child_name)) = lower(trim(p_child_name))
        and r.status in ('pending', 'catchup', 'active')
        and c2.pair_key = c.pair_key and c2.pair_slot = c.pair_slot
        and c2.id <> c.id
    ) then
      raise exception 'Con đã đăng ký một lớp buổi % rồi — chọn lớp buổi % để đủ lịch tuần, không đăng ký 2 lớp cùng buổi %.',
        c.pair_slot, (case when c.pair_slot = 'A' then 'B' else 'A' end), c.pair_slot;
    end if;
  end if;

  if c.capacity is not null then
    select count(*) into v_taken from public.thpt_registrations
    where course_id = c.id and status in ('pending', 'catchup', 'active')
      and (p_student_id is null or student_id is distinct from p_student_id);
    if v_taken >= c.capacity then
      raise exception 'Lớp đã đủ chỗ (%/%). Nhắn giáo viên để xếp lớp khác.', v_taken, c.capacity;
    end if;
  end if;

  v_late := c.starts_at is not null and c.starts_at < current_date;
  v_status := 'pending';

  if p_student_id is not null then
    insert into public.thpt_registrations
      (course_id, student_id, registered_by, child_name, contact, note, status, joined_late)
    values
      (c.id, p_student_id, v_user, coalesce(trim(p_child_name), ''), coalesce(trim(p_contact), ''),
       coalesce(trim(p_note), ''), v_status, v_late)
    on conflict (course_id, student_id) where student_id is not null do update
      set status = case
                     when public.thpt_registrations.status in ('rejected', 'left') then excluded.status
                     else public.thpt_registrations.status
                   end,
          joined_late = case
                     when public.thpt_registrations.status in ('rejected', 'left') then excluded.joined_late
                     else public.thpt_registrations.joined_late
                   end,
          note = case when excluded.note <> '' then excluded.note else public.thpt_registrations.note end,
          contact = case when excluded.contact <> '' then excluded.contact else public.thpt_registrations.contact end,
          created_at = case
                     when public.thpt_registrations.status in ('rejected', 'left') then now()
                     else public.thpt_registrations.created_at
                   end
    returning id, status into v_id, v_status;

    -- Vào đúng hàng chờ duyệt của khối — /tai-khoan của em hiện "Đang chờ giáo viên duyệt",
    -- tab Nhập danh sách / trang Học sinh của giáo viên vẫn thấy như học sinh tự xin vào lớp.
    if v_status = 'pending' then
      insert into public.user_classes (user_id, class_id, status)
      values (p_student_id, c.class_id, 'pending')
      on conflict (user_id, class_id) do update
        set status = case when public.user_classes.status = 'rejected' then 'pending' else public.user_classes.status end,
            requested_at = case when public.user_classes.status = 'rejected' then now() else public.user_classes.requested_at end;
    end if;
  else
    insert into public.thpt_registrations
      (course_id, student_id, registered_by, child_name, contact, note, status, joined_late)
    values
      (c.id, null, v_user, trim(p_child_name), coalesce(trim(p_contact), ''), coalesce(trim(p_note), ''),
       v_status, v_late)
    returning id into v_id;
  end if;

  return jsonb_build_object(
    'registration_id', v_id,
    'status', v_status,
    'joined_late', v_late,
    'course_name', c.name
  );
end;
$$;
revoke all on function public.thpt_register(bigint, uuid, text, text, text) from public, anon;
grant execute on function public.thpt_register(bigint, uuid, text, text, text) to authenticated;
