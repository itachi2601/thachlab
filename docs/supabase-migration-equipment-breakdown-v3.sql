-- Cho chọn "giảng viên báo hỏng" và "giảng viên phụ trách sửa" từ danh sách tài khoản giáo viên
-- (role=admin) thay vì luôn gán cứng theo tài khoản đang bấm nút — vì người bấm gửi báo cáo/đóng
-- báo cáo trên máy dùng chung của xưởng có thể không phải là giảng viên thực sự phát hiện hoặc
-- phụ trách sửa máy đó.
-- Chạy sau docs/supabase-migration-equipment-breakdown-v2.sql.

alter table public.equipment_breakdown_reports add column if not exists assigned_to uuid references public.profiles(id) on delete set null;

-- report_equipment_breakdown: thêm p_reported_by (mặc định người đang đăng nhập nếu không truyền).
drop function if exists public.report_equipment_breakdown(bigint, bigint, text, text, text, timestamptz);
create or replace function public.report_equipment_breakdown(
  p_course_id bigint, p_session_id bigint, p_machine_code text, p_description text, p_storage_path text,
  p_broken_at timestamptz default now(), p_reported_by uuid default null
) returns bigint language plpgsql security definer set search_path = public as $$
declare new_id bigint; reporter uuid;
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được báo hỏng máy.'; end if;
  reporter := coalesce(p_reported_by, auth.uid());
  if not exists(select 1 from public.profiles where id = reporter and role = 'admin') then
    raise exception 'Giảng viên báo hỏng không hợp lệ.';
  end if;
  insert into public.equipment_breakdown_reports(course_id, session_id, machine_code, description, broken_photo_path, broken_at, reported_by)
  values (p_course_id, p_session_id, p_machine_code, p_description, p_storage_path, p_broken_at, reporter)
  returning id into new_id;
  return new_id;
end; $$;
revoke all on function public.report_equipment_breakdown(bigint, bigint, text, text, text, timestamptz, uuid) from public;
grant execute on function public.report_equipment_breakdown(bigint, bigint, text, text, text, timestamptz, uuid) to authenticated;

-- start_equipment_repair: gán/đổi giảng viên phụ trách sửa (assigned_to) ngay khi chuyển "đang sửa".
drop function if exists public.start_equipment_repair(bigint);
create or replace function public.start_equipment_repair(p_id bigint, p_assigned_to uuid default null)
returns void language plpgsql security definer set search_path = public as $$
declare assignee uuid;
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được cập nhật báo cáo.'; end if;
  assignee := coalesce(p_assigned_to, auth.uid());
  if not exists(select 1 from public.profiles where id = assignee and role = 'admin') then
    raise exception 'Giảng viên phụ trách sửa không hợp lệ.';
  end if;
  update public.equipment_breakdown_reports set status = 'in_progress', assigned_to = assignee where id = p_id and status = 'open';
end; $$;
revoke all on function public.start_equipment_repair(bigint, uuid) from public;
grant execute on function public.start_equipment_repair(bigint, uuid) to authenticated;

-- resolve_equipment_breakdown: thêm p_resolved_by (mặc định người đang đăng nhập nếu không truyền);
-- nếu báo cáo chưa từng được gán (bỏ qua bước "Bắt đầu sửa"), lưu luôn assigned_to = người đóng.
drop function if exists public.resolve_equipment_breakdown(bigint, text, text);
create or replace function public.resolve_equipment_breakdown(p_id bigint, p_note text, p_resolved_photo_path text, p_resolved_by uuid default null)
returns void language plpgsql security definer set search_path = public as $$
declare resolver uuid;
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được cập nhật báo cáo.'; end if;
  resolver := coalesce(p_resolved_by, auth.uid());
  if not exists(select 1 from public.profiles where id = resolver and role = 'admin') then
    raise exception 'Giảng viên sửa chữa không hợp lệ.';
  end if;
  update public.equipment_breakdown_reports
  set status = 'resolved', resolved_by = resolver, resolved_at = now(), resolved_note = p_note, resolved_photo_path = p_resolved_photo_path,
      assigned_to = coalesce(assigned_to, resolver)
  where id = p_id;
end; $$;
revoke all on function public.resolve_equipment_breakdown(bigint, text, text, uuid) from public;
grant execute on function public.resolve_equipment_breakdown(bigint, text, text, uuid) to authenticated;
