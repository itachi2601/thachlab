-- Điểm danh offline theo từng khóa học và buổi học.
create table if not exists public.attendance_sessions (
  id bigint generated always as identity primary key,
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  created_by uuid references public.profiles(id) on delete set null,
  created_at timestamptz not null default now(), title text not null,
  session_date date not null, starts_at timestamptz not null, late_after timestamptz not null,
  closes_at timestamptz not null, code text not null check (code ~ '^[0-9]{6}$'),
  status text not null default 'open' check (status in ('open','closed')),
  note text not null default ''
);
alter table public.attendance_sessions add column if not exists note text not null default '';
create table if not exists public.attendance_records (
  session_id bigint not null references public.attendance_sessions(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  status text not null check (status in ('present','late','excused','absent')),
  checked_in_at timestamptz, note text not null default '', bonus_points integer not null default 0,
  marked_by uuid references public.profiles(id) on delete set null,
  updated_at timestamptz not null default now(), primary key(session_id, student_id)
);
alter table public.attendance_records add column if not exists bonus_points integer not null default 0;
create index if not exists attendance_sessions_course_date_idx on public.attendance_sessions(course_id, starts_at desc);
create index if not exists attendance_records_student_idx on public.attendance_records(student_id, session_id);
alter table public.attendance_sessions enable row level security;
alter table public.attendance_records enable row level security;
drop policy if exists "admins manage attendance sessions" on public.attendance_sessions;
create policy "admins manage attendance sessions" on public.attendance_sessions for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "students read course attendance sessions" on public.attendance_sessions;
create policy "students read course attendance sessions" on public.attendance_sessions for select to authenticated using (public.is_admin() or exists(select 1 from public.course_enrollments e where e.course_id=course_id and e.student_id=auth.uid() and e.status='active'));
drop policy if exists "admins manage attendance records" on public.attendance_records;
create policy "admins manage attendance records" on public.attendance_records for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "students read own attendance" on public.attendance_records;
create policy "students read own attendance" on public.attendance_records for select to authenticated using (student_id=auth.uid() or public.is_admin());

create or replace function public.submit_attendance_code(p_course_id bigint, p_code text)
returns jsonb language plpgsql security definer set search_path=public as $$
declare s public.attendance_sessions%rowtype; next_status text; checked_time timestamptz:=now();
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập để điểm danh.'; end if;
  if not exists(select 1 from public.course_enrollments where course_id=p_course_id and student_id=auth.uid() and status='active') then raise exception 'Bạn chưa thuộc khóa học này.'; end if;
  select * into s from public.attendance_sessions where course_id=p_course_id and code=trim(p_code) and status='open' order by created_at desc limit 1;
  if s.id is null then raise exception 'Mã điểm danh không đúng hoặc phiên đã đóng.'; end if;
  if checked_time < s.starts_at then raise exception 'Phiên điểm danh chưa bắt đầu.'; end if;
  if checked_time > s.closes_at then raise exception 'Phiên điểm danh đã hết thời gian.'; end if;
  next_status:=case when checked_time>s.late_after then 'late' else 'present' end;
  insert into public.attendance_records(session_id,student_id,status,checked_in_at,marked_by) values(s.id,auth.uid(),next_status,checked_time,auth.uid())
  on conflict(session_id,student_id) do update set status=excluded.status,checked_in_at=excluded.checked_in_at,updated_at=now();
  return jsonb_build_object('status',next_status,'session_title',s.title,'checked_in_at',checked_time);
end; $$;
revoke all on function public.submit_attendance_code(bigint,text) from public;
grant execute on function public.submit_attendance_code(bigint,text) to authenticated;
