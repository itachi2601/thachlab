-- Hoàn tác 20261009100000_notify_exam_assigned.sql. Thông báo đã gửi giữ nguyên (xoá tay nếu cần: delete from notifications where kind in ('assessment_new','homework_new')).
drop trigger if exists trg_notify_homework_assigned on public.class_announcements;
drop trigger if exists trg_notify_assessment_assigned on public.class_assessments;
drop function if exists public.trg_notify_homework_assigned();
drop function if exists public.trg_notify_assessment_assigned();
drop function if exists public.notify_class_students(bigint, text, text, text, text);
