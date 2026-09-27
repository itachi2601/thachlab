-- Rollback cho supabase/migrations/20260927150000_exam_class_access.sql
-- Gỡ 3 policy restrictive + 2 hàm helper, đưa exams/exam_results/
-- exam_question_results về đúng hành vi RLS trước khi vá (chỉ permissive
-- policy cũ còn hiệu lực).

begin;

drop policy if exists "students insert question results only for own-class exams" on public.exam_question_results;
drop policy if exists "students insert results only for own-class exams" on public.exam_results;
drop policy if exists "students only see own-class exams" on public.exams;

drop function if exists public.exam_open_to_student(bigint, uuid);
drop function if exists public.is_staff();

commit;
