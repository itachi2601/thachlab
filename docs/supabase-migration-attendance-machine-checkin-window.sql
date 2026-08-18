-- Sửa: tính giới hạn 6 tiếng chọn/đổi máy từ lúc HỌC SINH tự điểm danh (checked_in_at),
-- thay vì từ lúc giáo viên mở buổi điểm danh (starts_at) — tránh việc cả lớp bị khóa
-- chọn máy nếu buổi điểm danh mở từ sớm hoặc kéo dài hơn 6 tiếng.
-- Đồng thời chặn hẳn việc chọn/đổi máy khi buổi điểm danh đã bị giáo viên khoá (status = 'closed'),
-- vì trước đây học sinh vẫn đổi được máy sau khi khoá miễn còn trong 6 tiếng.
-- Chạy sau docs/supabase-migration-attendance-machine-edit-window.sql.

create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text)
returns void language plpgsql security definer set search_path = public as $$
declare student_checked_in_at timestamptz; session_status text;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_machine_code !~ '^(T[1-8]|P[1-8])$' then raise exception 'Mã máy không hợp lệ.'; end if;
  select status into session_status from public.attendance_sessions where id = p_session_id;
  if session_status is null then raise exception 'Không tìm thấy buổi điểm danh.'; end if;
  if session_status = 'closed' then raise exception 'Buổi điểm danh đã bị khoá, không thể chọn/đổi máy.'; end if;
  select checked_in_at into student_checked_in_at from public.attendance_records
    where session_id = p_session_id and student_id = auth.uid();
  if student_checked_in_at is null then raise exception 'Bạn chưa điểm danh buổi này.'; end if;
  if now() > student_checked_in_at + interval '6 hours' then
    raise exception 'Đã hết thời gian chọn/đổi máy (chỉ trong 6 tiếng kể từ lúc bạn điểm danh).';
  end if;
  update public.attendance_records set machine_code = p_machine_code, machine_selected_at = now(), updated_at = now()
  where session_id = p_session_id and student_id = auth.uid();
end; $$;
revoke all on function public.select_attendance_machine(bigint, text) from public;
grant execute on function public.select_attendance_machine(bigint, text) to authenticated;
