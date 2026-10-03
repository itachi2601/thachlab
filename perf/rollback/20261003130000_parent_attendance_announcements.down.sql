drop function if exists public.parent_attendance_summary(uuid, integer);
drop policy if exists "parents read child class announcements" on public.class_announcements;
