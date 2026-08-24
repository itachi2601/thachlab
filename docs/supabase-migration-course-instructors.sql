-- Vai trò "giảng viên": quản lý (admin) phân công giảng viên vào từng khóa học thực tập
-- (course_instructors); giảng viên được phân công vào /dashboard chỉ thấy đúng các môn được
-- đánh dấu is_practicum và các khóa mình được gán, với đầy đủ quyền thao tác như quản lý đang
-- làm cho CNC (điểm danh, năng lực, checklist, rubric, bản vẽ, điểm tổng kết, báo hỏng máy)
-- nhưng chỉ trong phạm vi khóa được gán. Chạy sau tất cả các migration hiện có.

alter table public.profiles drop constraint if exists profiles_role_check;
alter table public.profiles add constraint profiles_role_check check (role in ('student', 'admin', 'instructor'));

-- Trước đây chỉ có "update own profile" (tự sửa, không tự thăng quyền); thêm quyền cho quản lý
-- gán/thu hồi vai trò giảng viên cho người khác ngay trong trang quản trị (không cần chạy SQL tay).
drop policy if exists "admins manage profiles" on public.profiles;
create policy "admins manage profiles" on public.profiles
  for update to authenticated using (public.is_admin()) with check (public.is_admin());

alter table public.subjects add column if not exists is_practicum boolean not null default false;
update public.subjects set is_practicum = true where code in ('cnc', 'tien-phay');

-- Phân công: 1 khóa có thể có nhiều giảng viên, 1 giảng viên có thể phụ trách nhiều khóa.
create table if not exists public.course_instructors (
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  instructor_id uuid not null references public.profiles(id) on delete cascade,
  assigned_by uuid references public.profiles(id) on delete set null,
  assigned_at timestamptz not null default now(),
  primary key (course_id, instructor_id)
);
create index if not exists course_instructors_instructor_idx on public.course_instructors(instructor_id, course_id);
alter table public.course_instructors enable row level security;
drop policy if exists "admins manage course instructors" on public.course_instructors;
create policy "admins manage course instructors" on public.course_instructors
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "instructors read own assignments" on public.course_instructors;
create policy "instructors read own assignments" on public.course_instructors
  for select to authenticated using (instructor_id = auth.uid() or public.is_admin());

-- true nếu là admin, hoặc giảng viên được phân công cho đúng khóa này.
create or replace function public.can_manage_course(p_course_id bigint)
returns boolean language sql security definer stable set search_path = public
as $$
  select public.is_admin() or exists (
    select 1 from public.course_instructors
    where course_id = p_course_id and instructor_id = auth.uid()
  );
$$;

-- Giảng viên thấy tên/lớp của học sinh trong các khóa mình phụ trách (cần cho mọi join tới
-- profiles từ course_enrollments/attendance_records/checklist_attempts/... trong dashboard).
drop policy if exists "instructors read enrolled student profiles" on public.profiles;
create policy "instructors read enrolled student profiles" on public.profiles
  for select to authenticated using (
    exists (
      select 1 from public.course_enrollments e
      join public.course_instructors ci on ci.course_id = e.course_id
      where e.student_id = profiles.id and ci.instructor_id = auth.uid()
    )
  );

-- ---------- Quyền theo khóa được phân công (mirror quyền admin, thu hẹp theo can_manage_course) ----------

drop policy if exists "instructors read assigned course offerings" on public.course_offerings;
create policy "instructors read assigned course offerings" on public.course_offerings
  for select to authenticated using (public.can_manage_course(id));
drop policy if exists "instructors update assigned course offerings" on public.course_offerings;
create policy "instructors update assigned course offerings" on public.course_offerings
  for update to authenticated using (public.can_manage_course(id)) with check (public.can_manage_course(id));

drop policy if exists "instructors read assigned course enrollments" on public.course_enrollments;
create policy "instructors read assigned course enrollments" on public.course_enrollments
  for select to authenticated using (public.can_manage_course(course_id));
drop policy if exists "instructors update assigned course enrollments" on public.course_enrollments;
create policy "instructors update assigned course enrollments" on public.course_enrollments
  for update to authenticated using (public.can_manage_course(course_id)) with check (public.can_manage_course(course_id));

drop policy if exists "instructors read assigned learning records" on public.cnc_learning_records;
create policy "instructors read assigned learning records" on public.cnc_learning_records
  for select to authenticated using (public.can_manage_course(course_id));

drop policy if exists "instructors manage assigned competency permissions" on public.cnc_competency_permissions;
create policy "instructors manage assigned competency permissions" on public.cnc_competency_permissions
  for all to authenticated using (public.can_manage_course(course_id)) with check (public.can_manage_course(course_id));

drop policy if exists "instructors manage assigned attendance sessions" on public.attendance_sessions;
create policy "instructors manage assigned attendance sessions" on public.attendance_sessions
  for all to authenticated using (public.can_manage_course(course_id)) with check (public.can_manage_course(course_id));

drop policy if exists "instructors manage assigned attendance records" on public.attendance_records;
create policy "instructors manage assigned attendance records" on public.attendance_records
  for all to authenticated using (
    exists (select 1 from public.attendance_sessions s where s.id = session_id and public.can_manage_course(s.course_id))
  ) with check (
    exists (select 1 from public.attendance_sessions s where s.id = session_id and public.can_manage_course(s.course_id))
  );

drop policy if exists "instructors read assigned attendance machine photos" on public.attendance_machine_photos;
create policy "instructors read assigned attendance machine photos" on public.attendance_machine_photos
  for select to authenticated using (
    exists (select 1 from public.attendance_sessions s where s.id = session_id and public.can_manage_course(s.course_id))
  );

drop policy if exists "instructors manage assigned attendance machine scores" on public.attendance_machine_scores;
create policy "instructors manage assigned attendance machine scores" on public.attendance_machine_scores
  for all to authenticated using (
    exists (select 1 from public.attendance_sessions s where s.id = session_id and public.can_manage_course(s.course_id))
  ) with check (
    exists (select 1 from public.attendance_sessions s where s.id = session_id and public.can_manage_course(s.course_id))
  );

drop policy if exists "instructors read assigned equipment breakdown reports" on public.equipment_breakdown_reports;
create policy "instructors read assigned equipment breakdown reports" on public.equipment_breakdown_reports
  for select to authenticated using (public.can_manage_course(course_id));

drop policy if exists "instructors manage assigned course grade overrides" on public.course_grade_overrides;
create policy "instructors manage assigned course grade overrides" on public.course_grade_overrides
  for all to authenticated using (public.can_manage_course(course_id)) with check (public.can_manage_course(course_id));

drop policy if exists "instructors read assigned rubric exam attempts" on public.rubric_exam_attempts;
create policy "instructors read assigned rubric exam attempts" on public.rubric_exam_attempts
  for select to authenticated using (public.can_manage_course(course_id));

drop policy if exists "instructors manage assigned checklist sessions" on public.checklist_sessions;
create policy "instructors manage assigned checklist sessions" on public.checklist_sessions
  for all to authenticated using (public.can_manage_course(course_id)) with check (public.can_manage_course(course_id));

drop policy if exists "instructors read assigned checklist attempts" on public.checklist_attempts;
create policy "instructors read assigned checklist attempts" on public.checklist_attempts
  for select to authenticated using (public.can_manage_course(course_id));

drop policy if exists "instructors read assigned cnc drawings" on public.cnc_drawing_submissions;
create policy "instructors read assigned cnc drawings" on public.cnc_drawing_submissions
  for select to authenticated using (course_id is not null and public.can_manage_course(course_id));
drop policy if exists "instructors review assigned cnc drawings" on public.cnc_drawing_submissions;
create policy "instructors review assigned cnc drawings" on public.cnc_drawing_submissions
  for update to authenticated using (course_id is not null and public.can_manage_course(course_id))
  with check (course_id is not null and public.can_manage_course(course_id));

-- ---------- Storage: ảnh báo hỏng máy / ảnh 5S / file bản vẽ theo khóa được phân công ----------

drop policy if exists "instructors upload equipment breakdown photos" on storage.objects;
create policy "instructors upload equipment breakdown photos" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'equipment-breakdown-photos' and public.can_manage_course(((storage.foldername(name))[1])::bigint));
drop policy if exists "instructors read equipment breakdown photos" on storage.objects;
create policy "instructors read equipment breakdown photos" on storage.objects
  for select to authenticated
  using (bucket_id = 'equipment-breakdown-photos' and public.can_manage_course(((storage.foldername(name))[1])::bigint));

drop policy if exists "instructors read attendance machine photos" on storage.objects;
create policy "instructors read attendance machine photos" on storage.objects
  for select to authenticated
  using (
    bucket_id = 'attendance-machine-photos'
    and exists (select 1 from public.attendance_sessions s where s.id::text = (storage.foldername(name))[1] and public.can_manage_course(s.course_id))
  );

drop policy if exists "instructors read assigned cnc drawing files" on storage.objects;
create policy "instructors read assigned cnc drawing files" on storage.objects
  for select to authenticated
  using (
    bucket_id = 'cnc-drawings'
    and exists (select 1 from public.cnc_drawing_submissions d where d.storage_path = name and d.course_id is not null and public.can_manage_course(d.course_id))
  );

-- ---------- RPC: đổi kiểm tra is_admin() thuần sang can_manage_course() theo khóa ----------

create or replace function public.report_equipment_breakdown(
  p_course_id bigint, p_session_id bigint, p_machine_code text, p_description text, p_storage_path text,
  p_broken_at timestamptz default now()
) returns bigint language plpgsql security definer set search_path = public as $$
declare new_id bigint;
begin
  if not public.can_manage_course(p_course_id) then raise exception 'Chỉ giảng viên phụ trách khóa mới được báo hỏng máy.'; end if;
  insert into public.equipment_breakdown_reports(course_id, session_id, machine_code, description, broken_photo_path, broken_at, reported_by)
  values (p_course_id, p_session_id, p_machine_code, p_description, p_storage_path, p_broken_at, auth.uid())
  returning id into new_id;
  return new_id;
end; $$;

create or replace function public.start_equipment_repair(p_id bigint)
returns void language plpgsql security definer set search_path = public as $$
declare v_course_id bigint;
begin
  select course_id into v_course_id from public.equipment_breakdown_reports where id = p_id;
  if v_course_id is null or not public.can_manage_course(v_course_id) then raise exception 'Chỉ giảng viên phụ trách khóa mới được cập nhật báo cáo.'; end if;
  update public.equipment_breakdown_reports set status = 'in_progress' where id = p_id and status = 'open';
end; $$;

create or replace function public.resolve_equipment_breakdown(p_id bigint, p_note text, p_resolved_photo_path text)
returns void language plpgsql security definer set search_path = public as $$
declare v_course_id bigint;
begin
  select course_id into v_course_id from public.equipment_breakdown_reports where id = p_id;
  if v_course_id is null or not public.can_manage_course(v_course_id) then raise exception 'Chỉ giảng viên phụ trách khóa mới được cập nhật báo cáo.'; end if;
  update public.equipment_breakdown_reports
  set status = 'resolved', resolved_by = auth.uid(), resolved_at = now(), resolved_note = p_note, resolved_photo_path = p_resolved_photo_path
  where id = p_id;
end; $$;

create or replace function public.cleanup_old_machine_photos(p_course_id bigint, p_keep_session_id bigint)
returns text[] language plpgsql security definer set search_path = public as $$
declare deleted_paths text[];
begin
  if not public.can_manage_course(p_course_id) then raise exception 'Không có quyền.'; end if;
  with stale as (
    delete from public.attendance_machine_photos amp
    using public.attendance_sessions s
    where amp.session_id = s.id and s.course_id = p_course_id and s.id <> p_keep_session_id
    returning amp.storage_path
  )
  select coalesce(array_agg(storage_path), array[]::text[]) into deleted_paths from stale;
  return deleted_paths;
end; $$;

create or replace function public.submit_checklist_result(
  p_course_id bigint,
  p_code text,
  p_student_id uuid,
  p_lesson_id text,
  p_item_results jsonb,
  p_score numeric,
  p_critical_ok boolean,
  p_zero_tolerance_ok boolean,
  p_passed boolean
) returns jsonb
language plpgsql security definer set search_path = public
as $$
declare s public.checklist_sessions%rowtype; v_grader_role text; now_time timestamptz := now();
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_student_id = auth.uid() then raise exception 'Không thể tự chấm cho chính mình.'; end if;

  select * into s from public.checklist_sessions
    where course_id = p_course_id and lesson_id = p_lesson_id and code = trim(p_code) and status = 'open'
    order by created_at desc limit 1;
  if s.id is null then raise exception 'Mã phiên chấm không đúng hoặc phiên đã đóng.'; end if;
  if now_time < s.starts_at then raise exception 'Phiên chấm chưa bắt đầu.'; end if;
  if now_time > s.closes_at then raise exception 'Phiên chấm đã hết thời gian.'; end if;

  if not exists (
    select 1 from public.course_enrollments where course_id = p_course_id and student_id = p_student_id and status = 'active'
  ) then raise exception 'Học sinh được chấm không thuộc khóa học này.'; end if;

  if public.can_manage_course(p_course_id) then
    v_grader_role := 'teacher';
  else
    if not exists (
      select 1 from public.course_enrollments where course_id = p_course_id and student_id = auth.uid() and status = 'active'
    ) then raise exception 'Bạn chưa thuộc khóa học này.'; end if;
    if not exists (
      select 1 from public.cnc_learning_records
      where course_id = p_course_id and student_id = auth.uid() and lesson_id = p_lesson_id
        and assessment_id in ('machine-operation','tool-setup') and completed = true
      group by student_id having count(distinct assessment_id) = 2
    ) then raise exception 'Bạn cần đạt cả 2 bài kiểm tra vận hành máy và cài đặt dao trước khi được chấm chéo cho bạn khác.'; end if;
    v_grader_role := 'peer';
  end if;

  insert into public.checklist_attempts (
    session_id, course_id, lesson_id, student_id, grader_id, grader_role,
    item_results, score, total, critical_ok, zero_tolerance_ok, passed
  ) values (
    s.id, p_course_id, p_lesson_id, p_student_id, auth.uid(), v_grader_role,
    coalesce(p_item_results, '{}'::jsonb), p_score, 10, p_critical_ok, p_zero_tolerance_ok, p_passed
  );

  insert into public.cnc_learning_records (
    course_id, student_id, lesson_id, assessment_id, completed, latest_score, best_score,
    total_questions, attempt_count, last_activity_at
  ) values (
    p_course_id, p_student_id, p_lesson_id, 'checklist', p_passed, round(p_score), round(p_score),
    10, 1, now_time
  )
  on conflict (course_id, student_id, lesson_id, assessment_id) do update set
    completed = cnc_learning_records.completed or excluded.completed,
    latest_score = excluded.latest_score,
    best_score = greatest(coalesce(cnc_learning_records.best_score, 0), excluded.best_score),
    total_questions = excluded.total_questions,
    attempt_count = cnc_learning_records.attempt_count + 1,
    last_activity_at = now_time;

  return jsonb_build_object('passed', p_passed, 'score', p_score, 'grader_role', v_grader_role, 'session_title', s.title);
end;
$$;
