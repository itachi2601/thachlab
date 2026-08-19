-- Thêm danh mục máy thật (bảng machines) thay cho whitelist mã máy hardcode bằng regex
-- trong select_attendance_machine, và nạp dữ liệu máy cho Xưởng C1.1: 12 tiện vạn năng
-- EMCOMAT 17D + 12 phay vạn năng EMCOMAT FB 450 MC (truyền thống) + 4 phay CNC EMCO cỡ lớn.
-- Giữ nguyên mã máy cũ (T1-8 tiện CNC / P1-8 phay CNC) của xưởng hiện có để không phá dữ liệu
-- điểm danh/ảnh 5S/báo hỏng đã lưu theo các mã đó.
-- Chạy sau docs/supabase-migration-attendance-machine-selection-redesign.sql.

create table if not exists public.machines (
  code text primary key,
  label text not null,
  machine_type text not null check (machine_type in ('cnc_turn','cnc_mill','manual_turn','manual_mill')),
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

alter table public.machines enable row level security;

drop policy if exists "admins manage machines" on public.machines;
create policy "admins manage machines" on public.machines
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "authenticated read machines" on public.machines;
create policy "authenticated read machines" on public.machines
  for select to authenticated using (true);

-- Nạp lại mã máy CNC hiện có (xưởng cũ) để tương thích ngược với select_attendance_machine mới.
insert into public.machines (code, label, machine_type) values
  ('T1','Máy tiện CNC số 1','cnc_turn'),('T2','Máy tiện CNC số 2','cnc_turn'),('T3','Máy tiện CNC số 3','cnc_turn'),
  ('T4','Máy tiện CNC số 4','cnc_turn'),('T5','Máy tiện CNC số 5','cnc_turn'),('T6','Máy tiện CNC số 6','cnc_turn'),
  ('T7','Máy tiện CNC số 7','cnc_turn'),('T8','Máy tiện CNC số 8','cnc_turn'),
  ('P1','Máy phay CNC số 1','cnc_mill'),('P2','Máy phay CNC số 2','cnc_mill'),('P3','Máy phay CNC số 3','cnc_mill'),
  ('P4','Máy phay CNC số 4','cnc_mill'),('P5','Máy phay CNC số 5','cnc_mill'),('P6','Máy phay CNC số 6','cnc_mill'),
  ('P7','Máy phay CNC số 7','cnc_mill'),('P8','Máy phay CNC số 8','cnc_mill')
on conflict (code) do nothing;

-- Xưởng C1.1: 12 tiện vạn năng EMCOMAT 17D + 12 phay vạn năng EMCOMAT FB 450 MC + 4 phay CNC EMCO cỡ lớn.
insert into public.machines (code, label, machine_type) values
  ('TT01','Tiện EMCOMAT 17D số 01 — Xưởng C1.1','manual_turn'),('TT02','Tiện EMCOMAT 17D số 02 — Xưởng C1.1','manual_turn'),
  ('TT03','Tiện EMCOMAT 17D số 03 — Xưởng C1.1','manual_turn'),('TT04','Tiện EMCOMAT 17D số 04 — Xưởng C1.1','manual_turn'),
  ('TT05','Tiện EMCOMAT 17D số 05 — Xưởng C1.1','manual_turn'),('TT06','Tiện EMCOMAT 17D số 06 — Xưởng C1.1','manual_turn'),
  ('TT07','Tiện EMCOMAT 17D số 07 — Xưởng C1.1','manual_turn'),('TT08','Tiện EMCOMAT 17D số 08 — Xưởng C1.1','manual_turn'),
  ('TT09','Tiện EMCOMAT 17D số 09 — Xưởng C1.1','manual_turn'),('TT10','Tiện EMCOMAT 17D số 10 — Xưởng C1.1','manual_turn'),
  ('TT11','Tiện EMCOMAT 17D số 11 — Xưởng C1.1','manual_turn'),('TT12','Tiện EMCOMAT 17D số 12 — Xưởng C1.1','manual_turn'),
  ('PT01','Phay EMCOMAT FB 450 MC số 01 — Xưởng C1.1','manual_mill'),('PT02','Phay EMCOMAT FB 450 MC số 02 — Xưởng C1.1','manual_mill'),
  ('PT03','Phay EMCOMAT FB 450 MC số 03 — Xưởng C1.1','manual_mill'),('PT04','Phay EMCOMAT FB 450 MC số 04 — Xưởng C1.1','manual_mill'),
  ('PT05','Phay EMCOMAT FB 450 MC số 05 — Xưởng C1.1','manual_mill'),('PT06','Phay EMCOMAT FB 450 MC số 06 — Xưởng C1.1','manual_mill'),
  ('PT07','Phay EMCOMAT FB 450 MC số 07 — Xưởng C1.1','manual_mill'),('PT08','Phay EMCOMAT FB 450 MC số 08 — Xưởng C1.1','manual_mill'),
  ('PT09','Phay EMCOMAT FB 450 MC số 09 — Xưởng C1.1','manual_mill'),('PT10','Phay EMCOMAT FB 450 MC số 10 — Xưởng C1.1','manual_mill'),
  ('PT11','Phay EMCOMAT FB 450 MC số 11 — Xưởng C1.1','manual_mill'),('PT12','Phay EMCOMAT FB 450 MC số 12 — Xưởng C1.1','manual_mill'),
  ('PC01','Phay CNC EMCO số 01 — Xưởng C1.1','cnc_mill'),('PC02','Phay CNC EMCO số 02 — Xưởng C1.1','cnc_mill'),
  ('PC03','Phay CNC EMCO số 03 — Xưởng C1.1','cnc_mill'),('PC04','Phay CNC EMCO số 04 — Xưởng C1.1','cnc_mill')
on conflict (code) do nothing;

-- select_attendance_machine: đổi kiểm tra mã máy từ regex cố định (T[1-8]/P[1-8]) sang tra bảng
-- machines đang hoạt động, để có thể thêm/tắt máy (kể cả máy truyền thống) mà không cần sửa RPC.
create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text)
returns void language plpgsql security definer set search_path = public as $$
declare student_checked_in_at timestamptz; session_open boolean;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if not exists(select 1 from public.machines where code = p_machine_code and is_active) then
    raise exception 'Mã máy không hợp lệ.';
  end if;
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
