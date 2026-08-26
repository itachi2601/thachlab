-- Điểm danh offline cho khối lớp THPT (lý thuyết), song song với attendance_sessions/
-- attendance_records đã có cho CTTC (course_offerings) nhưng gắn theo class_id thay vì
-- course_id, và không có phần máy móc/ảnh 5S/bonus điểm vì lớp lý thuyết không cần.

create table if not exists public.thpt_attendance_sessions (
  id bigint generated always as identity primary key,
  class_id bigint not null references public.classes(id) on delete cascade,
  created_by uuid references public.profiles(id) on delete set null,
  created_at timestamptz not null default now(),
  title text not null,
  session_date date not null,
  starts_at timestamptz not null default now(),
  note text not null default ''
);

create table if not exists public.thpt_attendance_records (
  session_id bigint not null references public.thpt_attendance_sessions(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  status text not null check (status in ('present', 'late', 'excused', 'absent')),
  note text not null default '',
  marked_by uuid references public.profiles(id) on delete set null,
  marked_at timestamptz not null default now(),
  primary key (session_id, student_id)
);

create index if not exists thpt_attendance_sessions_class_date_idx
  on public.thpt_attendance_sessions(class_id, starts_at desc);
create index if not exists thpt_attendance_records_student_idx
  on public.thpt_attendance_records(student_id, session_id);

alter table public.thpt_attendance_sessions enable row level security;
alter table public.thpt_attendance_records enable row level security;

drop policy if exists "admins manage thpt attendance sessions" on public.thpt_attendance_sessions;
create policy "admins manage thpt attendance sessions" on public.thpt_attendance_sessions
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "assigned instructors manage thpt attendance sessions" on public.thpt_attendance_sessions;
create policy "assigned instructors manage thpt attendance sessions" on public.thpt_attendance_sessions
  for all to authenticated
  using (exists (select 1 from public.class_instructors ci where ci.class_id = thpt_attendance_sessions.class_id and ci.instructor_id = auth.uid()))
  with check (exists (select 1 from public.class_instructors ci where ci.class_id = thpt_attendance_sessions.class_id and ci.instructor_id = auth.uid()));

drop policy if exists "students read own class thpt attendance sessions" on public.thpt_attendance_sessions;
create policy "students read own class thpt attendance sessions" on public.thpt_attendance_sessions
  for select to authenticated
  using (exists (select 1 from public.user_classes uc where uc.class_id = thpt_attendance_sessions.class_id and uc.user_id = auth.uid()));

drop policy if exists "admins manage thpt attendance records" on public.thpt_attendance_records;
create policy "admins manage thpt attendance records" on public.thpt_attendance_records
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "assigned instructors manage thpt attendance records" on public.thpt_attendance_records;
create policy "assigned instructors manage thpt attendance records" on public.thpt_attendance_records
  for all to authenticated
  using (exists (
    select 1 from public.thpt_attendance_sessions s
    join public.class_instructors ci on ci.class_id = s.class_id
    where s.id = thpt_attendance_records.session_id and ci.instructor_id = auth.uid()
  ))
  with check (exists (
    select 1 from public.thpt_attendance_sessions s
    join public.class_instructors ci on ci.class_id = s.class_id
    where s.id = thpt_attendance_records.session_id and ci.instructor_id = auth.uid()
  ));

drop policy if exists "students read own thpt attendance" on public.thpt_attendance_records;
create policy "students read own thpt attendance" on public.thpt_attendance_records
  for select to authenticated using (student_id = auth.uid() or public.is_admin());
