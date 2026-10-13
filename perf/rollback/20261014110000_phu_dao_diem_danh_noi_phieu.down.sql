-- Hoàn tác điểm danh + nối phiếu/kiểm tra với buổi phụ đạo.
drop function if exists public.tutoring_followup_report(bigint, int);
drop trigger if exists trg_tutoring_exit_window_slot_guard on public.tutoring_exit_windows;
drop function if exists public.tutoring_exit_window_slot_guard();
drop trigger if exists trg_ta_session_slot_guard on public.ta_sessions;
drop function if exists public.ta_session_slot_guard();
drop function if exists public.tutoring_mark_attendance(bigint, uuid, boolean);
alter table public.tutoring_exit_windows drop column if exists slot_id;
drop index if exists public.ta_sessions_slot_unique;
alter table public.ta_sessions drop column if exists slot_id;
alter table public.tutoring_registrations drop column if exists attended_at, drop column if exists attended;
