-- Cho phép sửa ngày giờ (created_at) của 1 dòng lịch sử tình trạng máy, ngoài trạng thái/ghi chú.
-- Chạy sau docs/supabase-migration-machine-status-log.sql.

-- Sửa 1 dòng lịch sử đã có, có thể đổi cả ngày giờ; nếu dòng đó là mới nhất (theo created_at
-- sau khi sửa) của máy thì đồng bộ lại machines.status/note.
create or replace function public.update_machine_status_log(p_id bigint, p_status text, p_note text, p_created_at timestamptz default null)
returns void language plpgsql security definer set search_path = public as $$
declare target_code text; latest_id bigint;
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được cập nhật tình trạng máy.'; end if;
  if p_status not in ('ok','broken') then raise exception 'Trạng thái không hợp lệ.'; end if;
  select machine_code into target_code from public.machine_status_log where id = p_id;
  if target_code is null then raise exception 'Không tìm thấy dòng lịch sử.'; end if;
  update public.machine_status_log
  set status = p_status, note = p_note, updated_by = auth.uid(), updated_at = now(),
      created_at = coalesce(p_created_at, created_at)
  where id = p_id;
  select id into latest_id from public.machine_status_log where machine_code = target_code order by created_at desc limit 1;
  if latest_id = p_id then
    update public.machines set status = p_status, note = p_note where code = target_code;
  end if;
end; $$;
revoke all on function public.update_machine_status_log(bigint, text, text, timestamptz) from public;
grant execute on function public.update_machine_status_log(bigint, text, text, timestamptz) to authenticated;

-- Xoá chữ ký cũ (không còn tham số ngày giờ) để tránh gọi nhầm bản thiếu tham số.
drop function if exists public.update_machine_status_log(bigint, text, text);
