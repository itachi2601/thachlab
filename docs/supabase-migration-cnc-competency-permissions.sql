-- Giáo viên xác nhận quyền thực hành sau khi sinh viên đạt chốt chặn lý thuyết.
create table if not exists public.cnc_competency_permissions (
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  competency_id text not null check (competency_id in ('turn-operation','turn-tool-setup','mill-operation','mill-tool-setup')),
  status text not null check (status in ('approved','revoked')),
  note text not null default '', approved_by uuid references public.profiles(id) on delete set null,
  approved_at timestamptz, updated_at timestamptz not null default now(),
  primary key(course_id,student_id,competency_id)
);
create index if not exists cnc_competency_permissions_student_idx on public.cnc_competency_permissions(student_id,course_id);
alter table public.cnc_competency_permissions enable row level security;
drop policy if exists "admins manage competency permissions" on public.cnc_competency_permissions;
create policy "admins manage competency permissions" on public.cnc_competency_permissions for all to authenticated using(public.is_admin()) with check(public.is_admin());
drop policy if exists "students read own competency permissions" on public.cnc_competency_permissions;
create policy "students read own competency permissions" on public.cnc_competency_permissions for select to authenticated using(student_id=auth.uid() or public.is_admin());
