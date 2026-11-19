-- Rollback 20261118150000_get_lesson_page_student: bỏ RPC gộp trang bài học (client phải quay về 7 truy vấn cũ trước).
drop function if exists public.get_lesson_page_student(bigint);
