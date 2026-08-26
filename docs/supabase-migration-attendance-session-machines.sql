-- Cho phép giảng viên chọn xưởng thực tập + danh sách máy dùng trong từng buổi điểm danh,
-- thay cho việc sinh viên được chọn tự do trong toàn bộ máy active của xưởng cố định theo môn
-- học (services/subjects.ts). Sinh viên chỉ được chọn máy nằm trong danh sách này.
-- Đồng thời bỏ tính năng "Ảnh toàn xưởng"/"Ảnh thùng rác" (mã XUONG/RAC) — không xoá dữ liệu ảnh
-- cũ đã nộp, chỉ không còn UI/luồng nộp mới cho 2 mã này.

alter table public.attendance_sessions add column if not exists workshop text;

create table if not exists public.attendance_session_machines (
  session_id bigint not null references public.attendance_sessions(id) on delete cascade,
  machine_code text not null references public.machines(code),
  primary key (session_id, machine_code)
);
alter table public.attendance_session_machines enable row level security;

drop policy if exists "admins manage session machines" on public.attendance_session_machines;
create policy "admins manage session machines" on public.attendance_session_machines
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "instructors manage assigned session machines" on public.attendance_session_machines;
create policy "instructors manage assigned session machines" on public.attendance_session_machines
  for all to authenticated using (
    exists (select 1 from public.attendance_sessions s where s.id = session_id and public.can_manage_course(s.course_id))
  ) with check (
    exists (select 1 from public.attendance_sessions s where s.id = session_id and public.can_manage_course(s.course_id))
  );

drop policy if exists "authenticated read session machines" on public.attendance_session_machines;
create policy "authenticated read session machines" on public.attendance_session_machines
  for select to authenticated using (true);

-- Chặn sinh viên chọn máy ngoài danh sách giảng viên đã chọn cho buổi (nếu giảng viên chưa
-- cấu hình máy nào cho buổi, không có máy nào chọn được).
create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text)
returns void language plpgsql security definer set search_path = public as $$
declare student_checked_in_at timestamptz; session_open boolean; session_course_id bigint; machine_status text;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  select status into machine_status from public.machines where code = p_machine_code and is_active;
  if machine_status is null then raise exception 'Mã máy không hợp lệ.'; end if;
  if machine_status = 'broken' then raise exception 'Máy đang hỏng, không thể chọn.'; end if;
  select machine_selection_open, course_id into session_open, session_course_id
    from public.attendance_sessions where id = p_session_id;
  if session_open is null then raise exception 'Không tìm thấy buổi điểm danh.'; end if;
  if not session_open then raise exception 'Giáo viên đã khoá chọn máy cho buổi này.'; end if;
  if not exists(
    select 1 from public.attendance_session_machines
    where session_id = p_session_id and machine_code = p_machine_code
  ) then raise exception 'Máy này không có trong danh sách giảng viên đã chọn cho buổi học.'; end if;
  if exists(
    select 1 from public.equipment_breakdown_reports
    where course_id = session_course_id and machine_code = p_machine_code and status in ('open', 'in_progress')
  ) then raise exception 'Máy đang chờ sửa, không thể chọn.'; end if;
  select checked_in_at into student_checked_in_at from public.attendance_records
    where session_id = p_session_id and student_id = auth.uid();
  if student_checked_in_at is null then raise exception 'Bạn chưa điểm danh buổi này.'; end if;
  update public.attendance_records set machine_code = p_machine_code, machine_selected_at = now(), updated_at = now()
  where session_id = p_session_id and student_id = auth.uid();
end; $$;
revoke all on function public.select_attendance_machine(bigint, text) from public;
grant execute on function public.select_attendance_machine(bigint, text) to authenticated;
