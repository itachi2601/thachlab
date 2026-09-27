-- Rollback cho 20260927140000_class_review_homework.sql.

drop policy if exists "students read class review homework" on public.class_review_homework;
drop policy if exists "staff delete review homework" on public.class_review_homework;
drop policy if exists "staff read review homework" on public.class_review_homework;
drop policy if exists "staff create review homework" on public.class_review_homework;
drop table if exists public.class_review_homework;
