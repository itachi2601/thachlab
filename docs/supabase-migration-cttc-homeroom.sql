-- Trang "Lớp chủ nhiệm" cho giáo viên chủ nhiệm CTTC.
--
-- Mô hình: 1 lớp chủ nhiệm = 1 course_offering dưới môn 'gddd-ptnn'
-- ("Giáo dục đạo đức và phát triển nghề nghiệp"). GVCN được gán qua course_instructors
-- (dùng lại can_manage_course()), roster = course_enrollments, điểm danh = attendance_sessions
-- / attendance_records có sẵn (bonus_points dùng làm điểm nề nếp).
--
-- Bảng mới duy nhất: homeroom_term_records — điểm kiểm tra học kì (thang 10) + xếp loại
-- hạnh kiểm theo từng học kì. Điểm tổng kết môn tính ở client (TB 2 học kì) hoặc GV ghi đè
-- vào term = 'ca_nam'.
--
-- Chạy sau supabase-migration-course-instructors.sql. Idempotent.

-- ---------- Môn học ----------
insert into public.subjects (code, name, area, is_practicum)
values ('gddd-ptnn', 'Giáo dục đạo đức và phát triển nghề nghiệp', 'cttc', false)
on conflict (code) do update set
  name = excluded.name,
  area = excluded.area,
  active = true;

-- ---------- Bảng điểm học kì + hạnh kiểm ----------
create table if not exists public.homeroom_term_records (
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  term text not null check (term in ('hk1', 'hk2', 'ca_nam')),
  exam_score numeric(4, 2) check (exam_score >= 0 and exam_score <= 10),
  conduct text check (conduct in ('tot', 'kha', 'tb', 'yeu')),
  note text not null default '',
  updated_by uuid references public.profiles(id) on delete set null,
  updated_at timestamptz not null default now(),
  primary key (course_id, student_id, term)
);

create index if not exists homeroom_term_records_student_idx
  on public.homeroom_term_records(student_id, course_id);

alter table public.homeroom_term_records enable row level security;

drop policy if exists "admins manage homeroom term records" on public.homeroom_term_records;
create policy "admins manage homeroom term records" on public.homeroom_term_records
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "instructors manage assigned homeroom term records" on public.homeroom_term_records;
create policy "instructors manage assigned homeroom term records" on public.homeroom_term_records
  for all to authenticated
  using (public.can_manage_course(course_id))
  with check (public.can_manage_course(course_id));

drop policy if exists "students read own homeroom term records" on public.homeroom_term_records;
create policy "students read own homeroom term records" on public.homeroom_term_records
  for select to authenticated using (student_id = auth.uid() or public.is_admin());
