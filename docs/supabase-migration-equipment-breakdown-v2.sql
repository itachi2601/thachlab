-- Nâng cấp báo hỏng máy theo yêu cầu thực tế của quản lý xưởng:
-- - Giờ hư (tương đối, giáo viên tự nhập khi báo, mặc định là lúc báo).
-- - Ảnh 2 giai đoạn: lúc phát hiện hỏng (bắt buộc khi báo) + lúc khắc phục xong (bắt buộc khi đóng).
-- - Trạng thái 3 bước open → in_progress → resolved thay vì chỉ open/resolved.
-- - Trạng thái máy giờ lấy từ báo hỏng đang mở (bền vững qua nhiều buổi), không dùng cột
--   equipment_status theo từng buổi trong attendance_machine_scores nữa (giữ cột lại cho lịch sử
--   cũ, không xoá, chỉ ngừng đọc/ghi từ ứng dụng).
-- - Chặn sinh viên chọn máy đang có báo hỏng chưa đóng (open/in_progress).
-- Chạy sau docs/supabase-migration-machines.sql.

alter table public.equipment_breakdown_reports rename column storage_path to broken_photo_path;
alter table public.equipment_breakdown_reports add column if not exists resolved_photo_path text;
alter table public.equipment_breakdown_reports add column if not exists broken_at timestamptz not null default now();
-- Backfill 1 lần cho các báo cáo cũ: coi giờ báo cáo là giờ hư (không có dữ liệu chính xác hơn).
update public.equipment_breakdown_reports set broken_at = created_at;

alter table public.equipment_breakdown_reports drop constraint if exists equipment_breakdown_reports_status_check;
alter table public.equipment_breakdown_reports add constraint equipment_breakdown_reports_status_check
  check (status in ('open', 'in_progress', 'resolved'));

drop function if exists public.report_equipment_breakdown(bigint, bigint, text, text, text);
create or replace function public.report_equipment_breakdown(
  p_course_id bigint, p_session_id bigint, p_machine_code text, p_description text, p_storage_path text,
  p_broken_at timestamptz default now()
) returns bigint language plpgsql security definer set search_path = public as $$
declare new_id bigint;
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được báo hỏng máy.'; end if;
  insert into public.equipment_breakdown_reports(course_id, session_id, machine_code, description, broken_photo_path, broken_at, reported_by)
  values (p_course_id, p_session_id, p_machine_code, p_description, p_storage_path, p_broken_at, auth.uid())
  returning id into new_id;
  return new_id;
end; $$;
revoke all on function public.report_equipment_breakdown(bigint, bigint, text, text, text, timestamptz) from public;
grant execute on function public.report_equipment_breakdown(bigint, bigint, text, text, text, timestamptz) to authenticated;

-- Chuyển báo cáo sang "đang sửa" — bước trung gian tuỳ chọn giữa báo hỏng và khắc phục xong.
create or replace function public.start_equipment_repair(p_id bigint)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được cập nhật báo cáo.'; end if;
  update public.equipment_breakdown_reports set status = 'in_progress' where id = p_id and status = 'open';
end; $$;
revoke all on function public.start_equipment_repair(bigint) from public;
grant execute on function public.start_equipment_repair(bigint) to authenticated;

drop function if exists public.resolve_equipment_breakdown(bigint, text);
create or replace function public.resolve_equipment_breakdown(p_id bigint, p_note text, p_resolved_photo_path text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được cập nhật báo cáo.'; end if;
  update public.equipment_breakdown_reports
  set status = 'resolved', resolved_by = auth.uid(), resolved_at = now(), resolved_note = p_note, resolved_photo_path = p_resolved_photo_path
  where id = p_id;
end; $$;
revoke all on function public.resolve_equipment_breakdown(bigint, text, text) from public;
grant execute on function public.resolve_equipment_breakdown(bigint, text, text) to authenticated;

-- Chặn chọn máy đang có báo hỏng chưa đóng (open/in_progress) — trạng thái hỏng giờ bền vững
-- qua nhiều buổi thay vì chỉ nằm trong 1 buổi điểm danh.
create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text)
returns void language plpgsql security definer set search_path = public as $$
declare student_checked_in_at timestamptz; session_open boolean; session_course_id bigint;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if not exists(select 1 from public.machines where code = p_machine_code and is_active) then
    raise exception 'Mã máy không hợp lệ.';
  end if;
  select machine_selection_open, course_id into session_open, session_course_id
    from public.attendance_sessions where id = p_session_id;
  if session_open is null then raise exception 'Không tìm thấy buổi điểm danh.'; end if;
  if not session_open then raise exception 'Giáo viên đã khoá chọn máy cho buổi này.'; end if;
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
