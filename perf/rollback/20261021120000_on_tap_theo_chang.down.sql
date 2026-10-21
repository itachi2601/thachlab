-- Hoàn tác Buổi ôn tập theo chặng. Buổi ôn chỉ là dữ liệu tạm; điểm/bài làm của học sinh nằm ở exam_results, không bị đụng.
begin;
drop function if exists public.review_my_state(bigint);
drop function if exists public.review_board(bigint);
drop function if exists public.review_extend(bigint, int);
drop function if exists public.review_set_stage(bigint, int);
drop function if exists public.review_list(bigint);
drop function if exists public.review_create(bigint, text, int, jsonb);
drop function if exists public.review_secs_left(public.review_sessions);
drop function if exists public.review_student_stage(public.review_sessions, uuid, int);
drop table if exists public.review_sessions;
commit;
