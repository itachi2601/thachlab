-- Cho phép giáo viên mở khoá thủ công việc chọn/đổi máy cho cả buổi, bỏ qua giới hạn
-- 6 tiếng và cả trạng thái buổi đã khoá — dùng khi cả lớp bị lỡ hạn hoặc có sự cố.
-- Chạy sau docs/supabase-migration-attendance-machine-checkin-window.sql.

alter table public.attendance_sessions add column if not exists machine_edit_override boolean not null default false;

create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text)
returns void language plpgsql security definer set search_path = public as $$
declare student_checked_in_at timestamptz; session_status text; session_override boolean;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_machine_code !~ '^(T[1-8]|P[1-8])$' then raise exception 'Mã máy không hợp lệ.'; end if;
  select status, machine_edit_override into session_status, session_override from public.attendance_sessions where id = p_session_id;
  if session_status is null then raise exception 'Không tìm thấy buổi điểm danh.'; end if;
  select checked_in_at into student_checked_in_at from public.attendance_records
    where session_id = p_session_id and student_id = auth.uid();
  if student_checked_in_at is null then raise exception 'Bạn chưa điểm danh buổi này.'; end if;
  if not session_override then
    if session_status = 'closed' then raise exception 'Buổi điểm danh đã bị khoá, không thể chọn/đổi máy.'; end if;
    if now() > student_checked_in_at + interval '6 hours' then
      raise exception 'Đã hết thời gian chọn/đổi máy (chỉ trong 6 tiếng kể từ lúc bạn điểm danh).';
    end if;
  end if;
  update public.attendance_records set machine_code = p_machine_code, machine_selected_at = now(), updated_at = now()
  where session_id = p_session_id and student_id = auth.uid();
end; $$;
revoke all on function public.select_attendance_machine(bigint, text) from public;
grant execute on function public.select_attendance_machine(bigint, text) to authenticated;

-- Cho giáo viên (authenticated) bật/tắt cờ này. RLS hiện có trên attendance_sessions
-- (nếu giáo viên đã update được cột status/note thì cũng update được cột này qua policy sẵn có).
