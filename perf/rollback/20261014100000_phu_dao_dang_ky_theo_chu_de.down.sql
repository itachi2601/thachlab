-- Hoàn tác đăng ký phụ đạo theo chủ đề: bỏ trigger/hàm/cột mới, khôi phục hai hàm hàng chờ bản 20261004120000.
drop trigger if exists trg_tutoring_reg_notify on public.tutoring_registrations;
drop trigger if exists trg_tutoring_reg_guard on public.tutoring_registrations;
drop trigger if exists trg_tutoring_waitlist_topics on public.tutoring_waitlist;
drop function if exists public.tutoring_registration_notify();
drop function if exists public.tutoring_registration_guard();
drop function if exists public.tutoring_waitlist_topics_guard();
drop function if exists public.tutoring_check_topics(bigint, bigint[], boolean, boolean);
drop function if exists public.tutoring_ready_topics(bigint);
drop function if exists public.tutoring_topic_min_questions();
drop function if exists public.tutoring_topic_question_count(bigint);
alter table public.tutoring_registrations drop column if exists topic_ids, drop column if exists attended_at, drop column if exists attended;
alter table public.tutoring_waitlist drop column if exists topic_ids;
-- Rồi chạy lại hai hàm tutoring_slot_unregister và tutoring_slot_open_next trong supabase/migrations/20261004120000_phu_dao_hang_cho.sql.
