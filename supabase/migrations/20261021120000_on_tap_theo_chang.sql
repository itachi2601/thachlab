-- Buổi ÔN TẬP THEO CHẶNG (21/10/2026) — thầy/trợ giảng chọn lớp + một dãy đề (mỗi đề là một chặng, thường là
-- "Kiểm tra nhanh" cuối bài), mở từng chặng có đồng hồ; học sinh thấy chặng hiện tại trên điện thoại; bảng điều phối
-- cho thầy/trợ giảng thấy từng em chưa mở / đang làm / chưa đạt / đạt, và câu sai nhiều nhất.
--
-- Thiết kế:
--  * Không có bảng tiến độ riêng: tiến độ đọc từ exam_attempts (đáp án tự lưu khi làm) và exam_results (điểm khi nộp),
--    chỉ tính các lượt từ lúc buổi ôn được tạo (review_sessions.created_at) nên bài làm cũ không lẫn vào.
--  * "Đạt" = điểm tốt nhất ≥ ngưỡng % (mặc định 80). Ngưỡng chỉ là mốc hiển thị, KHÔNG khoá máy chủ: em chưa đạt vẫn làm lại được.
--  * Học sinh không đọc trực tiếp bảng nào; mọi thứ đi qua RPC security definer. Học sinh chỉ thấy số liệu chung (ẩn danh),
--    tên từng em chỉ trả cho nhân sự (is_staff: admin/giảng viên/trợ giảng).
--
-- Chạy lúc nào cũng được: chỉ thêm bảng và hàm mới, không đụng dữ liệu cũ.
-- Rollback ở cuối file và perf/rollback/20261021120000_on_tap_theo_chang.down.sql.
begin;

-- ---------- Bảng ----------
create table if not exists public.review_sessions (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  class_id bigint not null references public.classes (id) on delete cascade,
  created_by uuid references public.profiles (id) on delete set null default auth.uid(),
  title text not null check (length(btrim(title)) between 1 and 120),
  threshold int not null default 80 check (threshold between 1 and 100),
  -- [{ "exam_id": 770, "item_id": 123|null, "title": "…", "minutes": 12 }, …]
  stages jsonb not null check (jsonb_typeof(stages) = 'array' and jsonb_array_length(stages) between 1 and 12),
  current_stage int not null default -1,
  stage_started_at timestamptz,
  extra_seconds int not null default 0 check (extra_seconds between 0 and 7200),
  status text not null default 'ready' check (status in ('ready', 'running', 'finished'))
);

create index if not exists review_sessions_class_created_idx on public.review_sessions (class_id, created_at desc);

alter table public.review_sessions enable row level security;
revoke all on public.review_sessions from anon, authenticated;

-- ---------- Hàm nội bộ ----------
-- Trạng thái MỘT học sinh ở MỘT chặng: idle (chưa mở) | doing (đang làm) | failed (đã nộp, chưa đạt) | passed (đạt).
create or replace function public.review_student_stage(r public.review_sessions, p_student uuid, p_idx int)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_exam bigint := (r.stages -> p_idx ->> 'exam_id')::bigint;
  v_total int;
  v_best numeric;
  v_tries int;
  v_open boolean;
  v_responses jsonb;
  v_saved timestamptz;
  v_started timestamptz;
  v_answered int := 0;
  v_state text;
  v_last int;
begin
  select coalesce(e.question_count, jsonb_array_length(e.questions)) into v_total from public.exams e where e.id = v_exam;

  select max(er.score), count(*) into v_best, v_tries
  from public.exam_results er
  where er.student_id = p_student and er.exam_id = v_exam and er.created_at >= r.created_at;

  select a.responses, a.saved_at, a.started_at into v_responses, v_saved, v_started
  from public.exam_attempts a
  where a.student_id = p_student and a.exam_id = v_exam and a.submitted_at is null and a.started_at >= r.created_at
  order by a.started_at desc
  limit 1;
  v_open := found;

  if v_open and v_responses is not null and jsonb_typeof(v_responses) = 'array' then
    select count(*) into v_answered
    from jsonb_array_elements(v_responses) e
    where case jsonb_typeof(e)
      when 'null' then false
      when 'array' then exists (select 1 from jsonb_array_elements(e) x where jsonb_typeof(x) <> 'null')
      when 'string' then btrim(e #>> '{}') <> ''
      else true
    end;
  end if;

  if v_best is not null and v_best * 10 >= r.threshold then
    v_state := 'passed';
  elsif v_open then
    v_state := 'doing';
  elsif v_best is not null then
    v_state := 'failed';
  else
    v_state := 'idle';
  end if;

  if v_state in ('passed', 'failed') and not v_open then v_answered := coalesce(v_total, 0); end if;
  if v_open then v_last := greatest(0, extract(epoch from (now() - coalesce(v_saved, v_started)))::int); end if;

  return jsonb_build_object(
    'state', v_state,
    'answered', v_answered,
    'total', coalesce(v_total, 0),
    'best_pct', case when v_best is null then null else round(v_best * 10)::int end,
    'tries', coalesce(v_tries, 0),
    'idle_secs', v_last
  );
end;
$$;
revoke execute on function public.review_student_stage(public.review_sessions, uuid, int) from public, anon, authenticated;

-- Còn bao nhiêu giây ở chặng hiện tại (null khi chưa mở chặng).
create or replace function public.review_secs_left(r public.review_sessions)
returns int
language sql stable security definer set search_path = public
as $$
  select case
    when r.current_stage < 0 or r.stage_started_at is null or r.status <> 'running' then null
    else greatest(0,
      coalesce((r.stages -> r.current_stage ->> 'minutes')::int, 10) * 60 + r.extra_seconds
      - extract(epoch from (now() - r.stage_started_at))::int)
  end;
$$;
revoke execute on function public.review_secs_left(public.review_sessions) from public, anon, authenticated;

-- ---------- Nhân sự: tạo / điều khiển ----------
create or replace function public.review_create(p_class bigint, p_title text, p_threshold int, p_stages jsonb)
returns bigint
language plpgsql security definer set search_path = public
as $$
declare
  v_id bigint;
  s jsonb;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  if jsonb_typeof(p_stages) <> 'array' or jsonb_array_length(p_stages) not between 1 and 12 then
    raise exception 'stages_invalid';
  end if;
  for s in select * from jsonb_array_elements(p_stages) loop
    if not exists (select 1 from public.exams e where e.id = (s ->> 'exam_id')::bigint) then
      raise exception 'exam_not_found:%', s ->> 'exam_id';
    end if;
  end loop;
  insert into public.review_sessions (class_id, title, threshold, stages)
  values (p_class, btrim(p_title), coalesce(p_threshold, 80), p_stages)
  returning id into v_id;
  return v_id;
end;
$$;

create or replace function public.review_list(p_class bigint default null)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  return coalesce((
    select jsonb_agg(jsonb_build_object(
      'id', s.id, 'title', s.title, 'class_id', s.class_id, 'class_name', c.name,
      'status', s.status, 'current_stage', s.current_stage,
      'stage_count', jsonb_array_length(s.stages), 'created_at', s.created_at
    ) order by s.created_at desc)
    from (
      select * from public.review_sessions
      where p_class is null or class_id = p_class
      order by created_at desc limit 20
    ) s
    join public.classes c on c.id = s.class_id
  ), '[]'::jsonb);
end;
$$;

-- Mở chặng p_stage (0..n-1), p_stage = -1 đưa về "chưa bắt đầu", p_stage ≥ n kết thúc buổi.
create or replace function public.review_set_stage(p_session bigint, p_stage int)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  r public.review_sessions;
  n int;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  select * into r from public.review_sessions where id = p_session for update;
  if not found then raise exception 'not_found'; end if;
  n := jsonb_array_length(r.stages);
  if p_stage >= n then
    update public.review_sessions set status = 'finished' where id = p_session;
  elsif p_stage < 0 then
    update public.review_sessions
    set current_stage = -1, stage_started_at = null, extra_seconds = 0, status = 'ready'
    where id = p_session;
  else
    update public.review_sessions
    set current_stage = p_stage, stage_started_at = now(), extra_seconds = 0, status = 'running'
    where id = p_session;
  end if;
end;
$$;

create or replace function public.review_extend(p_session bigint, p_seconds int)
returns void
language plpgsql security definer set search_path = public
as $$
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  update public.review_sessions
  set extra_seconds = least(7200, greatest(0, extra_seconds + coalesce(p_seconds, 0)))
  where id = p_session and status = 'running';
end;
$$;

-- Bảng điều phối: từng em ở chặng hiện tại + câu sai nhiều nhất (chỉ nhân sự).
create or replace function public.review_board(p_session bigint)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  r public.review_sessions;
  v_idx int;
  v_students jsonb;
  v_wrong jsonb := '[]'::jsonb;
  v_exam bigint;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  select * into r from public.review_sessions where id = p_session;
  if not found then raise exception 'not_found'; end if;
  v_idx := r.current_stage;

  select coalesce(jsonb_agg(
    jsonb_build_object('id', p.id, 'name', p.full_name)
    || case when v_idx >= 0
         then public.review_student_stage(r, p.id, v_idx)
         else jsonb_build_object('state', 'idle', 'answered', 0, 'total', 0, 'best_pct', null, 'tries', 0, 'idle_secs', null)
       end
  ), '[]'::jsonb)
  into v_students
  from public.user_classes uc
  join public.profiles p on p.id = uc.user_id
  where uc.class_id = r.class_id and uc.status = 'active' and p.role = 'student' and coalesce(p.is_test, false) = false;

  if v_idx >= 0 then
    v_exam := (r.stages -> v_idx ->> 'exam_id')::bigint;
    select coalesce(jsonb_agg(t order by t.pct desc, t.total desc), '[]'::jsonb) into v_wrong
    from (
      select q.question_index as idx,
             count(*)::int as total,
             count(*) filter (where q.is_correct is false)::int as wrong,
             round(100.0 * count(*) filter (where q.is_correct is false) / count(*))::int as pct
      from public.exam_question_results q
      join public.exam_results er on er.id = q.exam_result_id
      join public.user_classes uc on uc.user_id = q.student_id and uc.class_id = r.class_id and uc.status = 'active'
      where q.exam_id = v_exam and er.created_at >= r.created_at and q.is_correct is not null and q.max > 0
      group by q.question_index
      having count(*) filter (where q.is_correct is false) > 0
      order by pct desc, total desc
      limit 8
    ) t;
  end if;

  return jsonb_build_object(
    'now', now(),
    'session', jsonb_build_object(
      'id', r.id, 'title', r.title, 'class_id', r.class_id, 'threshold', r.threshold, 'status', r.status,
      'current_stage', r.current_stage, 'stage_started_at', r.stage_started_at,
      'secs_left', public.review_secs_left(r), 'stages', r.stages
    ),
    'students', v_students,
    'wrongest', v_wrong
  );
end;
$$;

-- ---------- Học sinh ----------
-- Buổi ôn đang diễn ra của lớp em (p_session null → tự tìm buổi chưa kết thúc, tạo trong 12 giờ qua).
-- Trả null nếu không có. Chỉ số liệu chung (không tên bạn).
create or replace function public.review_my_state(p_session bigint default null)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_uid uuid := (select auth.uid());
  r public.review_sessions;
  n int;
  v_idx int;
  v_stages jsonb := '[]'::jsonb;
  i int;
  v_mine jsonb;
  v_total int;
  v_done int;
  v_cur jsonb := null;
  v_exam bigint;
begin
  if v_uid is null then raise exception 'not_authenticated'; end if;

  if p_session is null then
    select * into r
    from public.review_sessions s
    where s.status <> 'finished' and s.created_at > now() - interval '12 hours'
      and exists (select 1 from public.user_classes uc where uc.user_id = v_uid and uc.class_id = s.class_id and uc.status = 'active')
    order by s.created_at desc
    limit 1;
    if not found then return null; end if;
  else
    select * into r from public.review_sessions where id = p_session;
    if not found then return null; end if;
    if not public.is_staff() and not exists (
      select 1 from public.user_classes uc where uc.user_id = v_uid and uc.class_id = r.class_id and uc.status = 'active'
    ) then
      raise exception 'forbidden';
    end if;
  end if;

  n := jsonb_array_length(r.stages);
  v_idx := r.current_stage;

  for i in 0 .. n - 1 loop
    v_mine := case when i <= v_idx then public.review_student_stage(r, v_uid, i) else null end;
    v_stages := v_stages || jsonb_build_array(
      (r.stages -> i) || jsonb_build_object('mine', v_mine)
    );
  end loop;

  if v_idx >= 0 then
    v_exam := (r.stages -> v_idx ->> 'exam_id')::bigint;
    select count(*)::int into v_total
    from public.user_classes uc join public.profiles p on p.id = uc.user_id
    where uc.class_id = r.class_id and uc.status = 'active' and p.role = 'student' and coalesce(p.is_test, false) = false;
    select count(distinct er.student_id)::int into v_done
    from public.exam_results er
    join public.user_classes uc on uc.user_id = er.student_id and uc.class_id = r.class_id and uc.status = 'active'
    where er.exam_id = v_exam and er.created_at >= r.created_at;
    v_cur := jsonb_build_object('submitted', v_done, 'total', v_total);
  end if;

  return jsonb_build_object(
    'now', now(),
    'id', r.id,
    'title', r.title,
    'threshold', r.threshold,
    'status', r.status,
    'current_stage', v_idx,
    'secs_left', public.review_secs_left(r),
    'stages', v_stages,
    'class', v_cur
  );
end;
$$;

-- ---------- Quyền gọi ----------
revoke execute on function public.review_create(bigint, text, int, jsonb) from public, anon;
revoke execute on function public.review_list(bigint) from public, anon;
revoke execute on function public.review_set_stage(bigint, int) from public, anon;
revoke execute on function public.review_extend(bigint, int) from public, anon;
revoke execute on function public.review_board(bigint) from public, anon;
revoke execute on function public.review_my_state(bigint) from public, anon;
grant execute on function public.review_create(bigint, text, int, jsonb) to authenticated;
grant execute on function public.review_list(bigint) to authenticated;
grant execute on function public.review_set_stage(bigint, int) to authenticated;
grant execute on function public.review_extend(bigint, int) to authenticated;
grant execute on function public.review_board(bigint) to authenticated;
grant execute on function public.review_my_state(bigint) to authenticated;

commit;

-- ROLLBACK (cũng ở perf/rollback/20261021120000_on_tap_theo_chang.down.sql):
-- begin;
-- drop function if exists public.review_my_state(bigint);
-- drop function if exists public.review_board(bigint);
-- drop function if exists public.review_extend(bigint, int);
-- drop function if exists public.review_set_stage(bigint, int);
-- drop function if exists public.review_list(bigint);
-- drop function if exists public.review_create(bigint, text, int, jsonb);
-- drop function if exists public.review_secs_left(public.review_sessions);
-- drop function if exists public.review_student_stage(public.review_sessions, uuid, int);
-- drop table if exists public.review_sessions;
-- commit;
