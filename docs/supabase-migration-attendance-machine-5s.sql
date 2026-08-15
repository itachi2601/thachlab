-- Nâng cấp attendance_machine_scores sang chấm điểm 5S theo tiêu chí + trạng thái thiết bị.
-- Chạy sau docs/supabase-migration-attendance-machine-duty.sql.

alter table public.attendance_machine_scores add column if not exists sang_loc boolean not null default false;
alter table public.attendance_machine_scores add column if not exists sap_xep boolean not null default false;
alter table public.attendance_machine_scores add column if not exists sach_se boolean not null default false;
alter table public.attendance_machine_scores add column if not exists san_soc boolean not null default false;
alter table public.attendance_machine_scores add column if not exists san_sang boolean not null default false;
alter table public.attendance_machine_scores add column if not exists equipment_status text not null default 'normal';
alter table public.attendance_machine_scores drop constraint if exists attendance_machine_scores_equipment_status_check;
alter table public.attendance_machine_scores add constraint attendance_machine_scores_equipment_status_check
  check (equipment_status in ('normal', 'maintenance', 'broken'));
