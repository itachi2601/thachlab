-- Rubric chấm thi thực hành tổng hợp CNC (Lập trình → Mô phỏng → Cài đặt dao/phôi → Gia công),
-- 4 mức E/G/P/F theo tiêu chí, chấm 2 lượt: sinh viên tự đánh giá (role='self', không tính điểm
-- chính thức) và giáo viên chấm chính thức (role='teacher', ghi vào cnc_learning_records với
-- lesson_id='lesson-5' (tiện) / 'lesson-6' (phay) và assessment_id='rubric-exam').
create table if not exists public.rubric_exam_attempts (
  id bigint generated always as identity primary key,
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  machine text not null check (machine in ('tien', 'phay')),
  role text not null check (role in ('self', 'teacher')),
  grader_id uuid references public.profiles(id) on delete set null,
  item_levels jsonb not null default '{}'::jsonb,
  zero_tolerance_confirmed jsonb not null default '{}'::jsonb,
  ky_thuat_score numeric not null default 0,
  thanh_phan_score numeric not null default 0,
  total_score numeric not null default 0,
  xep_loai text not null default '',
  notes text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (course_id, student_id, machine, role)
);

create index if not exists rubric_exam_attempts_course_idx
  on public.rubric_exam_attempts(course_id, machine);

alter table public.rubric_exam_attempts enable row level security;

drop policy if exists "admins manage rubric exam attempts" on public.rubric_exam_attempts;
create policy "admins manage rubric exam attempts" on public.rubric_exam_attempts
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "students read own rubric exam attempts" on public.rubric_exam_attempts;
create policy "students read own rubric exam attempts" on public.rubric_exam_attempts
  for select to authenticated using (student_id = auth.uid() or public.is_admin());

drop policy if exists "students manage own self rubric attempt" on public.rubric_exam_attempts;
create policy "students manage own self rubric attempt" on public.rubric_exam_attempts
  for insert to authenticated with check (student_id = auth.uid() and role = 'self' and grader_id is null);
drop policy if exists "students update own self rubric attempt" on public.rubric_exam_attempts;
create policy "students update own self rubric attempt" on public.rubric_exam_attempts
  for update to authenticated using (student_id = auth.uid() and role = 'self')
  with check (student_id = auth.uid() and role = 'self' and grader_id is null);

do $$ begin
  alter publication supabase_realtime add table public.rubric_exam_attempts;
exception when duplicate_object then null;
end $$;
