drop policy if exists "class officers open attendance sessions" on public.attendance_sessions;
drop function if exists public.is_class_officer(bigint);
drop index if exists public.course_enrollments_class_role_unique_idx;
alter table public.course_enrollments drop column if exists class_role;
