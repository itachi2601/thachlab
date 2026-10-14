-- Rollback 20261014150000: gỡ nút Giao trợ giảng. Mục phụ đạo đã tự gán giữ nguyên (assigned_to/status đã ghi).
drop trigger if exists trg_tutoring_needs_handoff_assign on public.tutoring_needs;
drop function if exists public.tutoring_needs_handoff_assign();
drop function if exists public.ta_handoff_clear(uuid);
drop function if exists public.ta_handoff_assign(uuid, uuid, bigint);
drop function if exists public.ta_handoff_options(uuid);
drop function if exists public.ta_handoff_can_assign(uuid);
drop table if exists public.ta_student_handoffs;
