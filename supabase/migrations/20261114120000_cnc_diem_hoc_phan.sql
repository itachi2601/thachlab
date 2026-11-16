-- Điểm học phần CNC: mỗi SV có 2 điểm (module 'tien' = Tiện, 'phay' = Phay) trong mỗi lớp.
-- SV chỉ ĐỌC được dòng của mình; ghi qua service role (script nạp điểm) hoặc giảng viên admin.
-- Rollback: perf/rollback/20261114120000_cnc_diem_hoc_phan.down.sql
begin;

create table if not exists public.cnc_grades (
  course_id   int8 not null references public.course_offerings(id) on delete cascade,
  student_id  uuid not null references public.profiles(id) on delete cascade,
  module      text not null check (module in ('tien', 'phay')),
  ky_thuat    numeric(4,2),            -- nhóm I (tối đa 7)
  thanh_phan  numeric(4,2),            -- nhóm II (tối đa 3)
  total       numeric(4,2) not null default 0,
  grade       text,                    -- Xuất sắc / Khá / Đạt / Không đạt ...
  detail      jsonb not null default '{}'::jsonb,  -- {criteria:[{name,level,points,max}], violations:[text]}
  graded_at   timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  primary key (course_id, student_id, module)
);

alter table public.cnc_grades enable row level security;
revoke all on public.cnc_grades from anon, authenticated;
grant select on public.cnc_grades to authenticated;

create policy "student reads own cnc grades" on public.cnc_grades
  for select to authenticated
  using (student_id = (select auth.uid()) or (select public.is_admin()));

commit;
