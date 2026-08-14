alter table public.course_offerings
  add column if not exists open_lesson_ids text[] not null default array['lesson-1']::text[];

update public.course_offerings
set open_lesson_ids = array['lesson-1']::text[]
where open_lesson_ids is null or cardinality(open_lesson_ids) = 0;
