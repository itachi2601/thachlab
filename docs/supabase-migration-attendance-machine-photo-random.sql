-- Thay "sinh viên đầu tiên chọn máy" bằng "chọn ngẫu nhiên 1 bạn phụ trách" cho ảnh máy,
-- và chọn ngẫu nhiên 1 bạn phụ trách ảnh toàn xưởng (thay vì ai nộp trước cũng được).
-- Ảnh thùng rác (RAC) vẫn mở cho cả buổi như trước.
-- Chạy sau docs/supabase-migration-attendance-machine-first.sql.

-- true nếu người gọi là bạn được CHỌN NGẪU NHIÊN trong nhóm dùng chung máy này để nộp ảnh.
-- Random ổn định: sắp theo hash(session+machine+student) nên kết quả không đổi giữa các lần gọi,
-- nhưng ai "thắng" thì không đoán trước được và không ưu tiên người chọn máy trước.
create or replace function public.is_photo_duty_machine(p_session_id bigint, p_machine_code text)
returns boolean language sql security definer set search_path = public stable as $$
  select auth.uid() = (
    select student_id from public.attendance_records
    where session_id = p_session_id and machine_code = p_machine_code
    order by md5(p_session_id::text || ':' || p_machine_code || ':' || student_id::text) asc
    limit 1
  );
$$;
revoke all on function public.is_photo_duty_machine(bigint, text) from public;
grant execute on function public.is_photo_duty_machine(bigint, text) to authenticated;

-- true nếu người gọi là bạn được CHỌN NGẪU NHIÊN trong cả buổi để nộp ảnh toàn xưởng.
create or replace function public.is_photo_duty_workshop(p_session_id bigint)
returns boolean language sql security definer set search_path = public stable as $$
  select auth.uid() = (
    select student_id from public.attendance_records
    where session_id = p_session_id and status in ('present', 'late')
    order by md5(p_session_id::text || ':workshop:' || student_id::text) asc
    limit 1
  );
$$;
revoke all on function public.is_photo_duty_workshop(bigint) from public;
grant execute on function public.is_photo_duty_workshop(bigint) to authenticated;

-- Chặn ở tầng server theo phân công ngẫu nhiên: ảnh máy chỉ bạn được chọn ngẫu nhiên trong nhóm
-- mới nộp được; ảnh toàn xưởng chỉ bạn được chọn ngẫu nhiên trong buổi; ảnh thùng rác vẫn mở tự do.
create or replace function public.submit_attendance_machine_photo(
  p_session_id bigint, p_machine_code text, p_checkpoint text, p_storage_path text, p_note text default ''
) returns void language plpgsql security definer set search_path = public as $$
declare own_machine text;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_checkpoint not in ('start','end') then raise exception 'Mốc kiểm tra không hợp lệ.'; end if;
  if p_machine_code = 'XUONG' then
    if not exists(select 1 from public.attendance_records where session_id = p_session_id and student_id = auth.uid()) then
      raise exception 'Bạn chưa điểm danh buổi này.';
    end if;
    if not public.is_photo_duty_workshop(p_session_id) then
      raise exception 'Chỉ bạn được chọn ngẫu nhiên mới được nộp ảnh toàn xưởng.';
    end if;
  elsif p_machine_code = 'RAC' then
    if not exists(select 1 from public.attendance_records where session_id = p_session_id and student_id = auth.uid()) then
      raise exception 'Bạn chưa điểm danh buổi này.';
    end if;
  else
    select machine_code into own_machine from public.attendance_records
      where session_id = p_session_id and student_id = auth.uid();
    if own_machine is null or own_machine <> p_machine_code then
      raise exception 'Bạn chưa chọn máy này trong buổi điểm danh.';
    end if;
    if not public.is_photo_duty_machine(p_session_id, p_machine_code) then
      raise exception 'Chỉ bạn được chọn ngẫu nhiên phụ trách máy này mới được nộp ảnh.';
    end if;
  end if;
  insert into public.attendance_machine_photos(session_id, machine_code, checkpoint, storage_path, note, uploaded_by)
  values (p_session_id, p_machine_code, p_checkpoint, p_storage_path, p_note, auth.uid())
  on conflict (session_id, machine_code, checkpoint) do nothing;
end; $$;
revoke all on function public.submit_attendance_machine_photo(bigint, text, text, text, text) from public;
grant execute on function public.submit_attendance_machine_photo(bigint, text, text, text, text) to authenticated;
