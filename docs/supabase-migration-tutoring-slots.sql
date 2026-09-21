-- ============================================================
-- Lịch phụ đạo trong tuần: trợ giảng đăng buổi sắp tới, học sinh tự đăng ký
-- ============================================================
-- Chạy SAU:
--   docs/supabase-migration-tutoring-needs.sql   (assists_class, manages_class, question_topics)
-- Idempotent — chạy lại được.
--
-- Khác với ta_sessions ("phiếu ghi buổi" — trợ giảng ghi LẠI sau khi đã dạy, dùng để
-- tính lương): đây là lịch ĐĂNG TRƯỚC để học sinh biết mà đăng ký. Sau khi dạy xong,
-- trợ giảng vẫn ghi buổi ở /tro-giang/ghi như cũ — hai bảng không tự động nối nhau.
-- ============================================================

create table if not exists public.tutoring_slots (
  id bigint generated always as identity primary key,
  assistant_id uuid not null references public.ta_assistants (id) on delete cascade,
  class_id bigint not null references public.classes (id) on delete cascade,
  work_date date not null,
  start_time time not null,
  end_time time not null,
  topic_ids bigint[] not null default '{}',
  capacity int not null default 6 check (capacity > 0),
  registered_count int not null default 0,
  note text not null default '',
  status text not null default 'open' check (status in ('open', 'cancelled')),
  created_at timestamptz not null default now(),
  check (end_time > start_time)
);
create index if not exists tutoring_slots_class_idx
  on public.tutoring_slots (class_id, work_date, start_time);

alter table public.tutoring_slots enable row level security;

drop policy if exists "assistant manages own slots" on public.tutoring_slots;
create policy "assistant manages own slots" on public.tutoring_slots
  for all to authenticated
  using (
    exists (select 1 from public.ta_assistants a where a.id = assistant_id and a.user_id = auth.uid())
    or public.is_admin()
  )
  with check (
    exists (select 1 from public.ta_assistants a where a.id = assistant_id and a.user_id = auth.uid())
    or public.is_admin()
  );

drop policy if exists "class reads own slots" on public.tutoring_slots;
create policy "class reads own slots" on public.tutoring_slots
  for select to authenticated
  using (
    exists (
      select 1 from public.user_classes uc
      where uc.user_id = auth.uid() and uc.class_id = tutoring_slots.class_id and uc.status = 'active'
    )
    or public.manages_class(class_id) or public.assists_class(class_id) or public.is_admin()
  );


create table if not exists public.tutoring_registrations (
  id bigint generated always as identity primary key,
  slot_id bigint not null references public.tutoring_slots (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  created_at timestamptz not null default now(),
  unique (slot_id, student_id)
);
create index if not exists tutoring_registrations_slot_idx on public.tutoring_registrations (slot_id);
create index if not exists tutoring_registrations_student_idx on public.tutoring_registrations (student_id);

alter table public.tutoring_registrations enable row level security;

drop policy if exists "student registers self" on public.tutoring_registrations;
create policy "student registers self" on public.tutoring_registrations
  for insert to authenticated
  with check (
    student_id = auth.uid()
    and exists (
      select 1 from public.tutoring_slots s
      join public.user_classes uc on uc.class_id = s.class_id and uc.user_id = auth.uid() and uc.status = 'active'
      where s.id = slot_id
    )
  );

drop policy if exists "student cancels self" on public.tutoring_registrations;
create policy "student cancels self" on public.tutoring_registrations
  for delete to authenticated
  using (student_id = auth.uid());

drop policy if exists "student reads own registration" on public.tutoring_registrations;
create policy "student reads own registration" on public.tutoring_registrations
  for select to authenticated
  using (student_id = auth.uid());

drop policy if exists "staff reads registrations" on public.tutoring_registrations;
create policy "staff reads registrations" on public.tutoring_registrations
  for select to authenticated
  using (exists (
    select 1 from public.tutoring_slots s
    where s.id = slot_id and (public.manages_class(s.class_id) or public.assists_class(s.class_id) or public.is_admin())
  ));

-- Giữ sức chứa và số đã đăng ký nhất quán: kiểm tra + tăng đếm khi đăng ký (chặn
-- đăng ký nếu buổi đã đủ hoặc không còn mở), giảm đếm khi huỷ.
create or replace function public.tutoring_slot_register()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  update public.tutoring_slots
    set registered_count = registered_count + 1
    where id = new.slot_id and status = 'open' and registered_count < capacity;
  if not found then
    raise exception 'Buổi phụ đạo đã đủ số lượng hoặc không còn nhận đăng ký.';
  end if;
  return new;
end; $$;
drop trigger if exists trg_tutoring_slot_register on public.tutoring_registrations;
create trigger trg_tutoring_slot_register before insert on public.tutoring_registrations
  for each row execute function public.tutoring_slot_register();

create or replace function public.tutoring_slot_unregister()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  update public.tutoring_slots
    set registered_count = greatest(0, registered_count - 1)
    where id = old.slot_id;
  return old;
end; $$;
drop trigger if exists trg_tutoring_slot_unregister on public.tutoring_registrations;
create trigger trg_tutoring_slot_unregister after delete on public.tutoring_registrations
  for each row execute function public.tutoring_slot_unregister();
