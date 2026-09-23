-- Vai trò cán bộ lớp (lớp trưởng / lớp phó 1 / lớp phó 2) trong course_enrollments —
-- cho phép các bạn này tự mở phiên điểm danh cho cả lớp, không cần đợi giáo viên/giảng viên.
--
-- Chạy sau supabase-migration-course-enrollments.sql và supabase-migration-course-attendance.sql.
-- Idempotent.

alter table public.course_enrollments
  add column if not exists class_role text not null default 'member'
  check (class_role in ('member', 'lop_truong', 'lop_pho_1', 'lop_pho_2'));

-- Mỗi khóa chỉ có 1 lớp trưởng, 1 lớp phó 1, 1 lớp phó 2.
create unique index if not exists course_enrollments_class_role_unique_idx
  on public.course_enrollments (course_id, class_role)
  where class_role <> 'member';

create or replace function public.is_class_officer(p_course_id bigint)
returns boolean language sql security definer stable set search_path = public
as $$
  select exists (
    select 1 from public.course_enrollments
    where course_id = p_course_id and student_id = auth.uid() and status = 'active'
      and class_role in ('lop_truong', 'lop_pho_1', 'lop_pho_2')
  );
$$;
revoke all on function public.is_class_officer(bigint) from public;
grant execute on function public.is_class_officer(bigint) to authenticated;

drop policy if exists "class officers open attendance sessions" on public.attendance_sessions;
create policy "class officers open attendance sessions" on public.attendance_sessions
  for insert to authenticated
  with check (created_by = auth.uid() and public.is_class_officer(course_id));
