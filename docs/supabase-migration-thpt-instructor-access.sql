-- Mở quyền đọc cho giảng viên THPT được phân công (class_instructors) xem được hồ sơ,
-- danh sách lớp và điểm của ĐÚNG học sinh thuộc khối lớp mình phụ trách — cần cho dashboard
-- giáo viên THPT (/dashboard-thpt): Tổng quan, Bảng điểm, Hồ sơ học sinh. Trước migration này,
-- "read own profile"/"student reads own results"/"read own user classes" chỉ cho phép chính
-- học sinh hoặc admin (role='admin') đọc — giảng viên (role='instructor') bị chặn.

drop policy if exists "assigned instructors read student profiles" on public.profiles;
create policy "assigned instructors read student profiles" on public.profiles
  for select to authenticated
  using (exists (
    select 1 from public.user_classes uc
    join public.class_instructors ci on ci.class_id = uc.class_id
    where uc.user_id = profiles.id and ci.instructor_id = auth.uid()
  ));

drop policy if exists "assigned instructors read class rosters" on public.user_classes;
create policy "assigned instructors read class rosters" on public.user_classes
  for select to authenticated
  using (exists (
    select 1 from public.class_instructors ci
    where ci.class_id = user_classes.class_id and ci.instructor_id = auth.uid()
  ));

drop policy if exists "assigned instructors read student results" on public.exam_results;
create policy "assigned instructors read student results" on public.exam_results
  for select to authenticated
  using (exists (
    select 1 from public.user_classes uc
    join public.class_instructors ci on ci.class_id = uc.class_id
    where uc.user_id = exam_results.student_id and ci.instructor_id = auth.uid()
  ));
