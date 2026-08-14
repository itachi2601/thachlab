-- Chấm chéo checklist thực hành CNC (phiên có mã, giống điểm danh) + ghi nhận vào cnc_learning_records.
create table if not exists public.checklist_sessions (
  id bigint generated always as identity primary key,
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  lesson_id text not null check (lesson_id in ('lesson-4-turn','lesson-4-mill')),
  created_by uuid references public.profiles(id) on delete set null,
  created_at timestamptz not null default now(),
  title text not null,
  starts_at timestamptz not null,
  closes_at timestamptz not null,
  code text not null check (code ~ '^[0-9]{6}$'),
  status text not null default 'open' check (status in ('open','closed'))
);

create table if not exists public.checklist_attempts (
  id bigint generated always as identity primary key,
  session_id bigint not null references public.checklist_sessions(id) on delete cascade,
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  lesson_id text not null,
  student_id uuid not null references public.profiles(id) on delete cascade,
  grader_id uuid references public.profiles(id) on delete set null,
  grader_role text not null check (grader_role in ('teacher','peer')),
  item_results jsonb not null default '{}'::jsonb,
  score numeric not null,
  total numeric not null default 10,
  critical_ok boolean not null,
  zero_tolerance_ok boolean not null,
  passed boolean not null,
  created_at timestamptz not null default now()
);

create index if not exists checklist_sessions_course_idx on public.checklist_sessions(course_id, lesson_id, status);
create index if not exists checklist_attempts_student_idx on public.checklist_attempts(student_id, created_at desc);
create index if not exists checklist_attempts_session_idx on public.checklist_attempts(session_id);

alter table public.checklist_sessions enable row level security;
alter table public.checklist_attempts enable row level security;

drop policy if exists "admins manage checklist sessions" on public.checklist_sessions;
create policy "admins manage checklist sessions" on public.checklist_sessions
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "students read course checklist sessions" on public.checklist_sessions;
create policy "students read course checklist sessions" on public.checklist_sessions
  for select to authenticated using (public.is_admin() or exists(
    select 1 from public.course_enrollments e where e.course_id = checklist_sessions.course_id and e.student_id = auth.uid() and e.status = 'active'
  ));

drop policy if exists "admins manage checklist attempts" on public.checklist_attempts;
create policy "admins manage checklist attempts" on public.checklist_attempts
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "students read own or graded checklist attempts" on public.checklist_attempts;
create policy "students read own or graded checklist attempts" on public.checklist_attempts
  for select to authenticated using (public.is_admin() or student_id = auth.uid() or grader_id = auth.uid());

-- Trả về danh sách bạn học cùng khóa (không gồm bản thân) để chọn người chấm chéo.
create or replace function public.list_cnc_course_classmates(p_course_id bigint)
returns table(student_id uuid, full_name text, class_name text)
language plpgsql security definer set search_path = public
as $$
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if not exists (
    select 1 from public.course_enrollments where course_id = p_course_id and student_id = auth.uid() and status = 'active'
  ) then raise exception 'Bạn chưa thuộc khóa học này.'; end if;

  return query
    select e.student_id, p.full_name, p.class_name
    from public.course_enrollments e
    join public.profiles p on p.id = e.student_id
    where e.course_id = p_course_id and e.status = 'active' and e.student_id <> auth.uid()
    order by p.full_name;
end;
$$;
revoke all on function public.list_cnc_course_classmates(bigint) from public;
grant execute on function public.list_cnc_course_classmates(bigint) to authenticated;

-- Nộp kết quả chấm checklist (giáo viên hoặc bạn học chấm chéo) trong 1 phiên đang mở, đồng thời ghi vào cnc_learning_records
-- với assessment_id='checklist' để hiển thị/đếm lượt y hệt các bài kiểm tra khác trong tab Điểm & tiến độ.
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

  if public.is_admin() then
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
revoke all on function public.submit_checklist_result(bigint,text,uuid,text,jsonb,numeric,boolean,boolean,boolean) from public;
grant execute on function public.submit_checklist_result(bigint,text,uuid,text,jsonb,numeric,boolean,boolean,boolean) to authenticated;

do $$ begin
  alter publication supabase_realtime add table public.checklist_attempts;
exception when duplicate_object then null;
end $$;
