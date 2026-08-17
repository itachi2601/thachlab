-- Chỉ sinh viên đầu tiên chọn 1 máy mới được nộp ảnh đầu ca/cuối ca cho máy đó.
-- Chạy sau docs/supabase-migration-attendance-machine-duty.sql.

alter table public.attendance_records add column if not exists machine_selected_at timestamptz;

create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_machine_code !~ '^(T[1-8]|P[1-8])$' then raise exception 'Mã máy không hợp lệ.'; end if;
  update public.attendance_records set machine_code = p_machine_code, machine_selected_at = now(), updated_at = now()
  where session_id = p_session_id and student_id = auth.uid();
  if not found then raise exception 'Bạn chưa điểm danh buổi này.'; end if;
end; $$;
revoke all on function public.select_attendance_machine(bigint, text) from public;
grant execute on function public.select_attendance_machine(bigint, text) to authenticated;

-- true nếu người gọi là sinh viên đầu tiên chọn đúng máy này trong buổi (được phép nộp ảnh).
create or replace function public.is_first_on_machine(p_session_id bigint, p_machine_code text)
returns boolean language sql security definer set search_path = public stable as $$
  select auth.uid() = (
    select student_id from public.attendance_records
    where session_id = p_session_id and machine_code = p_machine_code
    order by machine_selected_at asc nulls last, student_id asc
    limit 1
  );
$$;
revoke all on function public.is_first_on_machine(bigint, text) from public;
grant execute on function public.is_first_on_machine(bigint, text) to authenticated;

-- Chặn luôn ở tầng server: chỉ người đến trước với đúng máy mới nộp được ảnh (XUONG/RAC vẫn mở cho cả buổi).
create or replace function public.submit_attendance_machine_photo(
  p_session_id bigint, p_machine_code text, p_checkpoint text, p_storage_path text, p_note text default ''
) returns void language plpgsql security definer set search_path = public as $$
declare own_machine text;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_checkpoint not in ('start','end') then raise exception 'Mốc kiểm tra không hợp lệ.'; end if;
  if p_machine_code not in ('XUONG','RAC') then
    select machine_code into own_machine from public.attendance_records
      where session_id = p_session_id and student_id = auth.uid();
    if own_machine is null or own_machine <> p_machine_code then
      raise exception 'Bạn chưa chọn máy này trong buổi điểm danh.';
    end if;
    if not public.is_first_on_machine(p_session_id, p_machine_code) then
      raise exception 'Chỉ bạn đầu tiên chọn máy này mới được nộp ảnh.';
    end if;
  else
    if not exists(select 1 from public.attendance_records where session_id = p_session_id and student_id = auth.uid()) then
      raise exception 'Bạn chưa điểm danh buổi này.';
    end if;
  end if;
  insert into public.attendance_machine_photos(session_id, machine_code, checkpoint, storage_path, note, uploaded_by)
  values (p_session_id, p_machine_code, p_checkpoint, p_storage_path, p_note, auth.uid())
  on conflict (session_id, machine_code, checkpoint) do nothing;
end; $$;
revoke all on function public.submit_attendance_machine_photo(bigint, text, text, text, text) from public;
grant execute on function public.submit_attendance_machine_photo(bigint, text, text, text, text) to authenticated;
