-- Cho phép giáo viên hiệu chỉnh trực tiếp điểm tổng kết mà không sửa/xóa lịch sử
-- bài kiểm tra, rubric hoặc điểm danh gốc. Giá trị ghi đè nằm trong thang 0–10.

create table if not exists public.course_grade_overrides (
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  grade_key text not null,
  score numeric(4,2) not null check (score >= -10 and score <= 10),
  updated_by uuid references public.profiles(id) on delete set null,
  updated_at timestamptz not null default now(),
  primary key (course_id, student_id, grade_key)
);

alter table public.course_grade_overrides drop constraint if exists course_grade_overrides_score_check;
alter table public.course_grade_overrides add constraint course_grade_overrides_score_check
  check (score >= -10 and score <= 10);

create index if not exists course_grade_overrides_student_idx
  on public.course_grade_overrides(student_id, course_id);

alter table public.course_grade_overrides enable row level security;
drop policy if exists "admins manage course grade overrides" on public.course_grade_overrides;
create policy "admins manage course grade overrides" on public.course_grade_overrides
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "students read own course grade overrides" on public.course_grade_overrides;
create policy "students read own course grade overrides" on public.course_grade_overrides
  for select to authenticated using (student_id = auth.uid() or public.is_admin());
