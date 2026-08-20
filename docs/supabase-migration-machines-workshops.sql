-- Sửa lại danh mục máy cho đúng sổ tài sản thật (3 xưởng thực tập: CNC C1.2, Tiện–Phay C1.1,
-- Tiện–Phay F1.2) và bổ sung dữ liệu cho trang "Tổng quan tình trạng máy". Seed C1.1 ở
-- docs/supabase-migration-machines.sql là SAI so với thực tế (12 EMCOMAT 17D / 12 FB 450 MC / 4
-- CNC lớn không khớp sổ tài sản) — migration này sửa lại đúng.
-- Chạy sau docs/supabase-migration-equipment-breakdown-v2.sql.

alter table public.machines add column if not exists workshop text not null default '';
alter table public.machines add column if not exists status text not null default 'ok' check (status in ('ok', 'broken'));
alter table public.machines add column if not exists note text not null default '';

alter table public.machines drop constraint if exists machines_machine_type_check;
alter table public.machines add constraint machines_machine_type_check
  check (machine_type in ('cnc_turn', 'cnc_mill', 'manual_turn', 'manual_mill', 'auxiliary'));

create index if not exists machines_workshop_idx on public.machines(workshop);

-- Xưởng CNC C1.2: cập nhật nhãn hiệu thật + tình trạng thật (T7, T8, P2 đang hỏng).
update public.machines set label = 'Máy tiện CNC Emco Turn 55 số 1 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'T1';
update public.machines set label = 'Máy tiện CNC Emco Turn 55 số 2 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'T2';
update public.machines set label = 'Máy tiện CNC Emco Turn 55 số 3 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'T3';
update public.machines set label = 'Máy tiện CNC Emco Turn 55 số 4 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'T4';
update public.machines set label = 'Máy tiện CNC Emco Turn 60 số 5 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'T5';
update public.machines set label = 'Máy tiện CNC Emco Turn 60 số 6 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'T6';
update public.machines set label = 'Máy tiện CNC Emco Turn 60 số 7 — Xưởng C1.2', workshop = 'C1.2', status = 'broken', note = 'Hư biến tần' where code = 'T7';
update public.machines set label = 'Máy tiện CNC Emco Turn 60 số 8 — Xưởng C1.2', workshop = 'C1.2', status = 'broken', note = 'Báo lỗi "spindle beros"' where code = 'T8';
update public.machines set label = 'Máy phay CNC Emco Mill 55 số 1 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'P1';
update public.machines set label = 'Máy phay CNC Emco Mill 55 số 2 — Xưởng C1.2', workshop = 'C1.2', status = 'broken', note = 'Thường báo lỗi "device not found"' where code = 'P2';
update public.machines set label = 'Máy phay CNC Emco Mill 55 số 3 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'P3';
update public.machines set label = 'Máy phay CNC Emco Mill 55 số 4 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'P4';
update public.machines set label = 'Máy phay CNC Emco Mill 55 số 5 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'P5';
update public.machines set label = 'Máy phay CNC Emco Mill 55 số 6 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'P6';
update public.machines set label = 'Máy phay CNC Emco Mill 55 số 7 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'P7';
update public.machines set label = 'Máy phay CNC Emco Mill 55 số 8 — Xưởng C1.2', workshop = 'C1.2', status = 'ok', note = '' where code = 'P8';

-- Xưởng C1.1: sửa lại đúng số liệu thật theo sổ tài sản (thay cho seed sai trước đó).
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 01 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT01';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 02 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT02';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 03 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT03';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 04 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT04';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 05 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT05';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 06 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT06';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 07 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT07';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 08 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT08';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 09 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT09';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 10 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT10';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 11 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT11';
update public.machines set label = 'Tiện vạn năng Emcomat 14 số 12 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'TT12';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 01 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT01';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 02 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT02';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 03 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT03';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 04 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT04';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 05 — Xưởng C1.1', workshop = 'C1.1', status = 'broken', note = 'NG theo sổ tài sản' where code = 'PT05';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 06 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT06';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 07 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT07';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 08 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT08';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 09 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT09';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 10 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT10';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 11 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT11';
update public.machines set label = 'Phay vạn năng Emco FB-3 số 12 — Xưởng C1.1', workshop = 'C1.1', status = 'ok', note = '' where code = 'PT12';
update public.machines set label = 'Phay CNC Emco 450MC số 01 — Xưởng C1.1', machine_type = 'cnc_mill', workshop = 'C1.1', status = 'ok', note = '' where code = 'PC01';
update public.machines set label = 'Phay CNC Emco 450MC số 02 — Xưởng C1.1', machine_type = 'cnc_mill', workshop = 'C1.1', status = 'ok', note = '' where code = 'PC02';
update public.machines set label = 'Phay CNC Emco 450MC số 03 — Xưởng C1.1', machine_type = 'cnc_mill', workshop = 'C1.1', status = 'ok', note = '' where code = 'PC03';
update public.machines set label = 'Phay CNC Emco 155 Mill (cũ) — Xưởng C1.1', machine_type = 'cnc_mill', workshop = 'C1.1', status = 'broken', note = 'NG, giá trị còn 30%' where code = 'PC04';

-- Xưởng C1.1: thêm các máy còn thiếu trong seed cũ.
insert into public.machines (code, label, machine_type, workshop, status, note, is_active) values
  ('TT13', 'Tiện vạn năng Emcomat 17D — Xưởng C1.1', 'manual_turn', 'C1.1', 'broken', 'NG theo sổ tài sản', true),
  ('TC01', 'Tiện CNC Emco 155 Turn (cũ) — Xưởng C1.1', 'cnc_turn', 'C1.1', 'ok', '', true),
  ('AUX-C11-NENKHI', 'Máy nén khí Garner-Denver — Xưởng C1.1', 'auxiliary', 'C1.1', 'ok', '', false),
  ('AUX-C11-MAISHOWA', 'Máy mài 2 đá Showa — Xưởng C1.1', 'auxiliary', 'C1.1', 'ok', '', false)
on conflict (code) do update set label = excluded.label, machine_type = excluded.machine_type, workshop = excluded.workshop, status = excluded.status, note = excluded.note, is_active = excluded.is_active;

-- Xưởng F1.2 (xưởng cũ, thiết bị đa dạng) — chỉ hiển thị ở trang tổng quan, chưa dùng cho điểm danh.
insert into public.machines (code, label, machine_type, workshop, status, note, is_active) values
  ('F12-C02', 'Máy cưa TSUNE (C02) — Xưởng F1.2', 'auxiliary', 'F1.2', 'ok', '', false),
  ('F12-C01', 'Máy cưa H-250SA (C01) — Xưởng F1.2', 'auxiliary', 'F1.2', 'ok', '', false),
  ('F12-M04', 'Máy mài 2 đá Nhật (M04) — Xưởng F1.2', 'auxiliary', 'F1.2', 'ok', '', false),
  ('F12-M03', 'Máy mài 2 đá SGB-T (M03) — Xưởng F1.2', 'auxiliary', 'F1.2', 'ok', '', false),
  ('F12-M02', 'Máy mài tròn Seibu Kiki 1964 (M02) — Xưởng F1.2', 'auxiliary', 'F1.2', 'ok', '', false),
  ('F12-M01', 'Máy mài phẳng Brownshape (M01) — Xưởng F1.2', 'auxiliary', 'F1.2', 'ok', '', false),
  ('F12-B01', 'Máy bào Uchidasu-610 (B01) — Xưởng F1.2', 'auxiliary', 'F1.2', 'ok', '', false),
  ('F12-B02', 'Máy bào Handahor II (B02) — Xưởng F1.2', 'auxiliary', 'F1.2', 'ok', '', false),
  ('F12-P08', 'Máy phay Shizoka (P08) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P09', 'Máy phay Makino 1983 (P09) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P07', 'Máy phay Makino (P07) — Xưởng F1.2', 'manual_mill', 'F1.2', 'broken', '', false),
  ('F12-P19', 'Máy phay Makino (P19) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P18', 'Máy phay Makino (P18) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P17', 'Máy phay Makino (P17) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P16', 'Máy phay Makino (P16) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P15', 'Máy phay Makino (P15) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P14', 'Máy phay Makino (P14) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P13', 'Máy phay Makino (P13) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P12', 'Máy phay Makino (P12) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P11', 'Máy phay Makino (P11) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P10', 'Máy phay Makino (P10) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-P01', 'Máy phay Topone (P01) — Xưởng F1.2', 'manual_mill', 'F1.2', 'broken', '', false),
  ('F12-P02', 'Máy phay Topone (P02) — Xưởng F1.2', 'manual_mill', 'F1.2', 'broken', '', false),
  ('F12-P03', 'Máy phay Topone (P03) — Xưởng F1.2', 'manual_mill', 'F1.2', 'ok', '', false),
  ('F12-T20', 'Máy tiện Wasino 1970 (T20) — Xưởng F1.2', 'manual_turn', 'F1.2', 'broken', '', false),
  ('F12-T07', 'Máy tiện Keiyoseiki 1988 (T07) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T06', 'Máy tiện Keiyoseiki 1988 (T06) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T05', 'Máy tiện Keiyoseiki 1988 (T05) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T04', 'Máy tiện Keiyoseiki 1988 (T04) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T03', 'Máy tiện Keiyoseiki 1957 (T03) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T02', 'Máy tiện Keiyoseiki 1948 (T02) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T01', 'Máy tiện Takisawa 1980 (T01) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T00', 'Máy tiện Takisawa 1982 (T00) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T21', 'Máy tiện Takisawa 1972 (T21) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T17', 'Máy tiện Takisawa 1970 (T17) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T14', 'Máy tiện Takisawa 1970 (T14) — Xưởng F1.2', 'manual_turn', 'F1.2', 'broken', '', false),
  ('F12-T11', 'Máy tiện Mazak Junior (T11) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T10', 'Máy tiện Mazak Junior (T10) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T09', 'Máy tiện Mazak Junior (T09) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T13', 'Máy tiện Dainichi (T13) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T15', 'Máy tiện Hamatu (T15) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T16', 'Máy tiện Hamatu (T16) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T12', 'Máy tiện Mazak Junior (T12) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false),
  ('F12-T19', 'Máy tiện Howasangyo (T19) — Xưởng F1.2', 'manual_turn', 'F1.2', 'ok', '', false)
on conflict (code) do update set label = excluded.label, machine_type = excluded.machine_type, workshop = excluded.workshop, status = excluded.status, note = excluded.note, is_active = excluded.is_active;

-- Chặn chọn máy khi trạng thái tồn kho ghi nhận đang hỏng (không chỉ dựa vào báo hỏng theo khóa
-- học như trước) — hai nguồn trạng thái (machines.status và equipment_breakdown_reports) đều
-- chặn được, phòng trường hợp máy hỏng nhưng chưa có báo cáo hỏng cho khóa học đang chọn.
create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text)
returns void language plpgsql security definer set search_path = public as $$
declare student_checked_in_at timestamptz; session_open boolean; session_course_id bigint; machine_status text;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  select status into machine_status from public.machines where code = p_machine_code and is_active;
  if machine_status is null then raise exception 'Mã máy không hợp lệ.'; end if;
  if machine_status = 'broken' then raise exception 'Máy đang hỏng, không thể chọn.'; end if;
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
