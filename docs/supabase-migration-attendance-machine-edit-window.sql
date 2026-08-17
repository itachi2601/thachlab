-- Giới hạn chọn/đổi máy trong vòng 6 tiếng kể từ lúc mở buổi điểm danh (starts_at).
-- Chạy sau docs/supabase-migration-attendance-machine-first.sql.

create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text)
returns void language plpgsql security definer set search_path = public as $$
declare session_starts_at timestamptz;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_machine_code !~ '^(T[1-8]|P[1-8])$' then raise exception 'Mã máy không hợp lệ.'; end if;
  select starts_at into session_starts_at from public.attendance_sessions where id = p_session_id;
  if session_starts_at is null then raise exception 'Không tìm thấy buổi điểm danh.'; end if;
  if now() > session_starts_at + interval '6 hours' then
    raise exception 'Đã hết thời gian chọn/đổi máy (chỉ trong 6 tiếng kể từ lúc mở điểm danh).';
  end if;
  update public.attendance_records set machine_code = p_machine_code, machine_selected_at = now(), updated_at = now()
  where session_id = p_session_id and student_id = auth.uid();
  if not found then raise exception 'Bạn chưa điểm danh buổi này.'; end if;
end; $$;
revoke all on function public.select_attendance_machine(bigint, text) from public;
grant execute on function public.select_attendance_machine(bigint, text) to authenticated;
