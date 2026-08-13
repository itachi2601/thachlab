-- Quản lý học sinh theo môn, khóa và năm học (thử nghiệm đầu tiên với CNC).

create table if not exists public.subjects (
  id bigint generated always as identity primary key,
  code text not null unique,
  name text not null,
  area text not null check (area in ('physics', 'cttc')),
  active boolean not null default true
);

create table if not exists public.course_offerings (
  id bigint generated always as identity primary key,
  subject_id bigint not null references public.subjects (id) on delete restrict,
  created_by uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now(),
  name text not null,
  class_label text not null default '',
  school_year text not null,
  join_code text not null,
  enrollment_mode text not null default 'approval'
    check (enrollment_mode in ('approval', 'automatic', 'closed')),
  starts_at date,
  ends_at date,
  status text not null default 'active'
    check (status in ('draft', 'active', 'completed', 'archived')),
  unique (join_code)
);

create table if not exists public.course_enrollments (
  course_id bigint not null references public.course_offerings (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  enrolled_at timestamptz not null default now(),
  status text not null default 'pending'
    check (status in ('pending', 'active', 'rejected', 'suspended', 'completed', 'left')),
  approved_at timestamptz,
  approved_by uuid references public.profiles (id) on delete set null,
  primary key (course_id, student_id)
);

create index if not exists course_offerings_subject_year_idx
  on public.course_offerings (subject_id, school_year desc);
create index if not exists course_enrollments_student_idx
  on public.course_enrollments (student_id, course_id);
create unique index if not exists course_offerings_join_code_upper_idx
  on public.course_offerings (upper(join_code));

insert into public.subjects (code, name, area)
values ('cnc', 'Gia công CNC', 'cttc')
on conflict (code) do update set name = excluded.name, area = excluded.area, active = true;

alter table public.subjects enable row level security;
alter table public.course_offerings enable row level security;
alter table public.course_enrollments enable row level security;

drop policy if exists "authenticated reads subjects" on public.subjects;
create policy "authenticated reads subjects" on public.subjects
  for select to authenticated using (active or public.is_admin());
drop policy if exists "admins manage subjects" on public.subjects;
create policy "admins manage subjects" on public.subjects
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "admins manage course offerings" on public.course_offerings;
create policy "admins manage course offerings" on public.course_offerings
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "students read joined courses" on public.course_offerings;
create policy "students read joined courses" on public.course_offerings
  for select to authenticated using (
    public.is_admin() or exists (
      select 1 from public.course_enrollments e
      where e.course_id = id and e.student_id = auth.uid()
    )
  );

drop policy if exists "admins manage course enrollments" on public.course_enrollments;
create policy "admins manage course enrollments" on public.course_enrollments
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "students read own enrollment" on public.course_enrollments;
create policy "students read own enrollment" on public.course_enrollments
  for select to authenticated using (student_id = auth.uid() or public.is_admin());

create or replace function public.request_course_enrollment(p_join_code text)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  selected_course public.course_offerings%rowtype;
  selected_subject public.subjects%rowtype;
  next_status text;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập trước khi tham gia khóa học.'; end if;
  select * into selected_course from public.course_offerings
    where upper(join_code) = upper(trim(p_join_code)) and status = 'active' limit 1;
  if selected_course.id is null then raise exception 'Mã khóa học không đúng hoặc khóa đã kết thúc.'; end if;
  select * into selected_subject from public.subjects where id = selected_course.subject_id;
  if selected_course.enrollment_mode = 'closed' then raise exception 'Khóa học đã đóng đăng ký.'; end if;
  next_status := case when selected_course.enrollment_mode = 'automatic' then 'active' else 'pending' end;
  insert into public.course_enrollments (course_id, student_id, status, approved_at)
  values (selected_course.id, auth.uid(), next_status, case when next_status = 'active' then now() end)
  on conflict (course_id, student_id) do update
    set status = case when course_enrollments.status = 'active' then 'active' else excluded.status end,
        enrolled_at = now();
  return jsonb_build_object('course_id', selected_course.id, 'course_name', selected_course.name,
    'subject_code', selected_subject.code, 'school_year', selected_course.school_year, 'status', next_status);
end;
$$;
revoke all on function public.request_course_enrollment(text) from public;
grant execute on function public.request_course_enrollment(text) to authenticated;

alter table if exists public.cnc_milling_quiz_attempts
  add column if not exists course_id bigint references public.course_offerings (id) on delete set null;
alter table if exists public.cnc_drawing_submissions
  add column if not exists course_id bigint references public.course_offerings (id) on delete set null;
alter table if exists public.cnc_drawing_submissions
  drop constraint if exists cnc_drawing_submissions_student_id_lesson_id_key;
do $$
begin
  if to_regclass('public.cnc_drawing_submissions') is not null then
    create unique index if not exists cnc_drawing_submissions_student_course_lesson_idx
      on public.cnc_drawing_submissions (student_id, course_id, lesson_id)
      where course_id is not null;
  end if;
end;
$$;
alter table if exists public.exam_results
  add column if not exists course_id bigint references public.course_offerings (id) on delete set null;
alter table if exists public.lesson_progress
  add column if not exists course_id bigint references public.course_offerings (id) on delete set null;
