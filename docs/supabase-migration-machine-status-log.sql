-- Lịch sử tình trạng máy — khác với báo hỏng theo khóa học ở equipment_breakdown_reports (dùng
-- trong luồng điểm danh hằng ngày). Bảng này phục vụ trang Tổng quan tình trạng máy: mỗi lần
-- giáo viên cập nhật trạng thái/ghi chú của 1 máy đều lưu thành 1 dòng lịch sử, xem và sửa được
-- trực tiếp khi click vào máy. Dòng lịch sử mới nhất của mỗi máy luôn đồng bộ vào machines.status/note.
-- Chạy sau docs/supabase-migration-machines-workshops.sql.

create table if not exists public.machine_status_log (
  id bigint generated always as identity primary key,
  machine_code text not null references public.machines(code) on delete cascade,
  status text not null check (status in ('ok', 'broken')),
  note text not null default '',
  created_by uuid references public.profiles(id) on delete set null,
  updated_by uuid references public.profiles(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists machine_status_log_machine_idx on public.machine_status_log(machine_code, created_at desc);

alter table public.machine_status_log enable row level security;
drop policy if exists "admins manage machine status log" on public.machine_status_log;
create policy "admins manage machine status log" on public.machine_status_log
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- Ghi 1 dòng lịch sử mới + đồng bộ trạng thái hiện tại của máy.
create or replace function public.add_machine_status_log(p_machine_code text, p_status text, p_note text)
returns bigint language plpgsql security definer set search_path = public as $$
declare new_id bigint;
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được cập nhật tình trạng máy.'; end if;
  if p_status not in ('ok','broken') then raise exception 'Trạng thái không hợp lệ.'; end if;
  insert into public.machine_status_log(machine_code, status, note, created_by, updated_by)
  values (p_machine_code, p_status, p_note, auth.uid(), auth.uid())
  returning id into new_id;
  update public.machines set status = p_status, note = p_note where code = p_machine_code;
  return new_id;
end; $$;
revoke all on function public.add_machine_status_log(text, text, text) from public;
grant execute on function public.add_machine_status_log(text, text, text) to authenticated;

-- Sửa 1 dòng lịch sử đã có; nếu là dòng mới nhất của máy đó thì đồng bộ lại machines.status/note.
create or replace function public.update_machine_status_log(p_id bigint, p_status text, p_note text)
returns void language plpgsql security definer set search_path = public as $$
declare target_code text; latest_id bigint;
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được cập nhật tình trạng máy.'; end if;
  if p_status not in ('ok','broken') then raise exception 'Trạng thái không hợp lệ.'; end if;
  select machine_code into target_code from public.machine_status_log where id = p_id;
  if target_code is null then raise exception 'Không tìm thấy dòng lịch sử.'; end if;
  update public.machine_status_log set status = p_status, note = p_note, updated_by = auth.uid(), updated_at = now()
  where id = p_id;
  select id into latest_id from public.machine_status_log where machine_code = target_code order by created_at desc limit 1;
  if latest_id = p_id then
    update public.machines set status = p_status, note = p_note where code = target_code;
  end if;
end; $$;
revoke all on function public.update_machine_status_log(bigint, text, text) from public;
grant execute on function public.update_machine_status_log(bigint, text, text) to authenticated;

-- Khởi tạo 1 dòng lịch sử ban đầu từ tình trạng hiện có trong machines, để máy nào cũng có
-- ít nhất 1 dòng lịch sử (chạy 1 lần, không lặp nhờ điều kiện not exists).
insert into public.machine_status_log (machine_code, status, note, created_at)
select code, status, note, now() from public.machines
where not exists (select 1 from public.machine_status_log l where l.machine_code = public.machines.code);
