-- Thiết kế lại quyền chọn/đổi máy: bỏ cửa sổ 6 tiếng tự động (nguồn gây lỗi ẩn) và
-- tách hẳn khỏi trạng thái khoá điểm danh. Giờ chỉ còn MỘT cờ do giáo viên bật/tắt:
-- machine_selection_open (đổi tên từ machine_edit_override, mặc định TRUE — mở sẵn khi
-- tạo buổi, giáo viên tự khoá khi xong).
-- Chạy sau docs/supabase-migration-attendance-machine-manual-unlock.sql.

alter table public.attendance_sessions rename column machine_edit_override to machine_selection_open;
alter table public.attendance_sessions alter column machine_selection_open set default true;
-- Buổi đang mở điểm danh: chuyển sang cho phép chọn máy (thay thế quyền theo cửa sổ 6h cũ).
-- Buổi đã khoá điểm danh mà chưa từng được mở khoá chọn máy: giữ nguyên khoá.
update public.attendance_sessions set machine_selection_open = true where status = 'open';

create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text)
returns void language plpgsql security definer set search_path = public as $$
declare student_checked_in_at timestamptz; session_open boolean;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_machine_code !~ '^(T[1-8]|P[1-8])$' then raise exception 'Mã máy không hợp lệ.'; end if;
  select machine_selection_open into session_open from public.attendance_sessions where id = p_session_id;
  if session_open is null then raise exception 'Không tìm thấy buổi điểm danh.'; end if;
  if not session_open then raise exception 'Giáo viên đã khoá chọn máy cho buổi này.'; end if;
  select checked_in_at into student_checked_in_at from public.attendance_records
    where session_id = p_session_id and student_id = auth.uid();
  if student_checked_in_at is null then raise exception 'Bạn chưa điểm danh buổi này.'; end if;
  update public.attendance_records set machine_code = p_machine_code, machine_selected_at = now(), updated_at = now()
  where session_id = p_session_id and student_id = auth.uid();
end; $$;
revoke all on function public.select_attendance_machine(bigint, text) from public;
grant execute on function public.select_attendance_machine(bigint, text) to authenticated;
