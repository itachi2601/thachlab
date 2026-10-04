-- Hàng chờ cho buổi phụ đạo đã đủ chỗ (trần 4 em/buổi theo quy chế trợ giảng 10/2026).
-- Em vào hàng chờ khi buổi đầy; có người huỷ thì em đầu hàng tự được lên; trợ giảng bấm
-- "Mở lượt tiếp" để tạo buổi mới cùng chủ đề và chuyển tối đa `capacity` em đầu hàng sang.
-- Idempotent. Chạy lúc nào cũng được (chỉ thêm bảng/hàm mới; thay hàm tutoring_slot_unregister).
-- Phụ thuộc: docs/supabase-migration-tutoring-slots.sql, docs/supabase-migration-bu-bai.sql (is_parent_of).

create table if not exists public.tutoring_waitlist (
  id bigint generated always as identity primary key,
  slot_id bigint not null references public.tutoring_slots (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  created_at timestamptz not null default now(),
  unique (slot_id, student_id)
);
create index if not exists tutoring_waitlist_slot_idx on public.tutoring_waitlist (slot_id, created_at);
create index if not exists tutoring_waitlist_student_idx on public.tutoring_waitlist (student_id);

alter table public.tutoring_waitlist enable row level security;

drop policy if exists "waitlist join self or child" on public.tutoring_waitlist;
create policy "waitlist join self or child" on public.tutoring_waitlist
  for insert to authenticated
  with check (
    (student_id = auth.uid() or public.is_parent_of(student_id))
    and exists (
      select 1 from public.tutoring_slots s
      join public.user_classes uc on uc.class_id = s.class_id and uc.user_id = student_id and uc.status = 'active'
      where s.id = slot_id
    )
  );

drop policy if exists "waitlist leave self or child" on public.tutoring_waitlist;
create policy "waitlist leave self or child" on public.tutoring_waitlist
  for delete to authenticated
  using (student_id = auth.uid() or public.is_parent_of(student_id));

drop policy if exists "waitlist read own" on public.tutoring_waitlist;
create policy "waitlist read own" on public.tutoring_waitlist
  for select to authenticated
  using (student_id = auth.uid() or public.is_parent_of(student_id));

drop policy if exists "waitlist staff read" on public.tutoring_waitlist;
create policy "waitlist staff read" on public.tutoring_waitlist
  for select to authenticated
  using (exists (
    select 1 from public.tutoring_slots s
    where s.id = slot_id and (public.manages_class(s.class_id) or public.assists_class(s.class_id) or public.is_admin())
  ));

-- Chỉ cho vào hàng chờ khi buổi còn mở, em chưa đăng ký, và buổi thật sự đã đầy.
create or replace function public.tutoring_waitlist_guard()
returns trigger language plpgsql security definer set search_path = public
as $$
declare s public.tutoring_slots;
begin
  select * into s from public.tutoring_slots where id = new.slot_id;
  if not found or s.status <> 'open' then
    raise exception 'Buổi phụ đạo không còn nhận đăng ký.';
  end if;
  if exists (select 1 from public.tutoring_registrations where slot_id = new.slot_id and student_id = new.student_id) then
    raise exception 'Em đã đăng ký buổi này rồi.';
  end if;
  if s.registered_count < s.capacity then
    raise exception 'Buổi này còn chỗ, hãy đăng ký trực tiếp.';
  end if;
  return new;
end; $$;
drop trigger if exists trg_tutoring_waitlist_guard on public.tutoring_waitlist;
create trigger trg_tutoring_waitlist_guard before insert on public.tutoring_waitlist
  for each row execute function public.tutoring_waitlist_guard();

-- Có người huỷ đăng ký → em đầu hàng chờ tự được lên (nếu buổi còn mở và chưa qua).
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
      insert into public.tutoring_registrations (slot_id, student_id) values (w.slot_id, w.student_id)
        on conflict (slot_id, student_id) do nothing;
    end if;
  end if;
  return old;
end; $$;

-- Vị trí của em (hoặc con của phụ huynh) trong hàng chờ từng buổi.
create or replace function public.tutoring_waitlist_mine(p_student uuid)
returns table (slot_id bigint, position int, total int)
language plpgsql stable security definer set search_path = public
as $$
begin
  if p_student is distinct from auth.uid() and not public.is_parent_of(p_student) then
    raise exception 'Không có quyền xem hàng chờ này.';
  end if;
  return query
    select w.slot_id,
           (select count(*)::int from public.tutoring_waitlist x
              where x.slot_id = w.slot_id and (x.created_at, x.id) <= (w.created_at, w.id)),
           (select count(*)::int from public.tutoring_waitlist x where x.slot_id = w.slot_id)
    from public.tutoring_waitlist w
    where w.student_id = p_student;
end; $$;
grant execute on function public.tutoring_waitlist_mine(uuid) to authenticated;

-- Trợ giảng "Mở lượt tiếp": tạo buổi mới giống buổi cũ (lớp, chủ đề, sức chứa) vào ngày giờ
-- mới và chuyển tối đa `capacity` em đầu hàng chờ sang. Trả về id buổi mới.
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

  insert into public.tutoring_slots (assistant_id, class_id, work_date, start_time, end_time, topic_ids, capacity, note)
    values (s.assistant_id, s.class_id, p_work_date, p_start, p_end, s.topic_ids, s.capacity, s.note)
    returning id into new_id;

  for w in
    select id, student_id from public.tutoring_waitlist
      where slot_id = p_slot_id order by created_at, id limit s.capacity
  loop
    delete from public.tutoring_waitlist where id = w.id;
    insert into public.tutoring_registrations (slot_id, student_id) values (new_id, w.student_id);
  end loop;
  return new_id;
end; $$;
grant execute on function public.tutoring_slot_open_next(bigint, date, time, time) to authenticated;

-- ROLLBACK (khôi phục hàm huỷ đăng ký bản cũ, gỡ phần hàng chờ):
--   drop function if exists public.tutoring_slot_open_next(bigint, date, time, time);
--   drop function if exists public.tutoring_waitlist_mine(uuid);
--   drop trigger if exists trg_tutoring_waitlist_guard on public.tutoring_waitlist;
--   drop function if exists public.tutoring_waitlist_guard();
--   drop table if exists public.tutoring_waitlist;
--   create or replace function public.tutoring_slot_unregister() returns trigger language plpgsql security definer set search_path = public
--   as $f$ begin update public.tutoring_slots set registered_count = greatest(0, registered_count - 1) where id = old.slot_id; return old; end; $f$;
