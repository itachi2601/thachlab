-- Tiến độ và điểm CNC dùng chung cho dashboard sinh viên và giáo viên.
create table if not exists public.cnc_learning_records (
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  lesson_id text not null,
  assessment_id text not null default 'final',
  completed boolean not null default false,
  latest_score integer,
  best_score integer,
  total_questions integer,
  attempt_count integer not null default 0,
  last_activity_at timestamptz not null default now(),
  primary key (course_id, student_id, lesson_id, assessment_id),
  check (latest_score is null or latest_score >= 0),
  check (best_score is null or best_score >= 0),
  check (total_questions is null or total_questions > 0)
);

-- Nâng cấp an toàn nếu bảng phiên bản cũ đã tồn tại.
alter table public.cnc_learning_records add column if not exists assessment_id text not null default 'final';
alter table public.cnc_learning_records drop constraint if exists cnc_learning_records_pkey;
alter table public.cnc_learning_records add primary key (course_id, student_id, lesson_id, assessment_id);

create index if not exists cnc_learning_records_course_student_idx
  on public.cnc_learning_records(course_id, student_id);

alter table public.cnc_learning_records enable row level security;
drop policy if exists "students read own cnc learning records" on public.cnc_learning_records;
create policy "students read own cnc learning records" on public.cnc_learning_records
  for select to authenticated using (student_id = auth.uid() or public.is_admin());
drop policy if exists "admins manage cnc learning records" on public.cnc_learning_records;
create policy "admins manage cnc learning records" on public.cnc_learning_records
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

create or replace function public.record_cnc_learning_result(
  p_course_id bigint,
  p_lesson_id text,
  p_assessment_id text default 'final',
  p_score integer default null,
  p_total integer default null,
  p_completed boolean default false
) returns void
language plpgsql security definer set search_path = public
as $$
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if not exists (
    select 1 from public.course_enrollments
    where course_id = p_course_id and student_id = auth.uid() and status = 'active'
  ) then raise exception 'Bạn chưa được duyệt vào khóa học này.'; end if;

  insert into public.cnc_learning_records (
    course_id, student_id, lesson_id, assessment_id, completed, latest_score, best_score,
    total_questions, attempt_count, last_activity_at
  ) values (
    p_course_id, auth.uid(), p_lesson_id, p_assessment_id, p_completed, p_score, p_score,
    p_total, case when p_score is null then 0 else 1 end, now()
  )
  on conflict (course_id, student_id, lesson_id, assessment_id) do update set
    completed = cnc_learning_records.completed or excluded.completed,
    latest_score = coalesce(excluded.latest_score, cnc_learning_records.latest_score),
    best_score = case
      when excluded.best_score is null then cnc_learning_records.best_score
      else greatest(coalesce(cnc_learning_records.best_score, 0), excluded.best_score)
    end,
    total_questions = coalesce(excluded.total_questions, cnc_learning_records.total_questions),
    attempt_count = cnc_learning_records.attempt_count + case when p_score is null then 0 else 1 end,
    last_activity_at = now();
end;
$$;
revoke all on function public.record_cnc_learning_result(bigint,text,text,integer,integer,boolean) from public;
grant execute on function public.record_cnc_learning_result(bigint,text,text,integer,integer,boolean) to authenticated;

do $$ begin
  alter publication supabase_realtime add table public.cnc_learning_records;
exception when duplicate_object then null;
end $$;
