-- Ôn tập theo chặng — chế độ TỰ HỌC Ở NHÀ (25/10/2026).
-- Buổi ôn trên lớp (mode 'live') chạy đồng bộ: thầy mở từng chặng, có đồng hồ chung, học sinh chỉ thấy buổi ôn tạo trong 12 giờ qua.
-- Chế độ 'self' dùng cùng bảng/đề/bảng điều phối nhưng:
--   * mọi chặng mở sẵn (current_stage = n-1), KHÔNG có đồng hồ (secs_left = null) — ở nhà đồng hồ đếm lùi chỉ thêm lo âu;
--   * có hạn nộp `due_at` (gợi ý, không khoá máy chủ): học sinh còn thấy buổi ôn tới hạn + 3 ngày;
--   * `sequential` = chặng sau chỉ mở khi chặng trước đạt ngưỡng, hoặc em đã nộp ≥2 lượt (không kẹt cứng, bỏ qua có ghi nhận);
--     khoá chỉ ở giao diện + RPC trả cờ `locked`, đề vẫn được gán cho lớp như cũ.
--   * học sinh thấy số bạn đã nộp từng chặng (ẩn danh), không có tên.
-- Bảng điều phối (review_board_stage) dùng nguyên: chọn chặng nào xem chặng đó.
-- Chỉ thêm cột (có mặc định) và thay hàm; buổi ôn 'live' cũ chạy y như trước. Chạy lúc nào cũng được.
-- Rollback ở cuối file và perf/rollback/20261025100000_on_tap_tu_hoc_ve_nha.down.sql.
begin;

alter table public.review_sessions
  add column if not exists mode text not null default 'live' check (mode in ('live', 'self')),
  add column if not exists due_at timestamptz,
  add column if not exists sequential boolean not null default false;

-- Chế độ tự học không có đồng hồ.
create or replace function public.review_secs_left(r public.review_sessions)
returns int
language sql stable security definer set search_path = public
as $$
  select case
    when r.mode = 'self' then null
    when r.current_stage < 0 or r.stage_started_at is null or r.status <> 'running' then null
    else greatest(0,
      coalesce((r.stages -> r.current_stage ->> 'minutes')::int, 10) * 60 + r.extra_seconds
      - extract(epoch from (now() - r.stage_started_at))::int)
  end;
$$;
revoke execute on function public.review_secs_left(public.review_sessions) from public, anon, authenticated;

-- Tạo buổi tự học: mọi chặng mở ngay.
create or replace function public.review_create_self(
  p_class bigint, p_title text, p_threshold int, p_stages jsonb, p_due_at timestamptz, p_sequential boolean
)
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
  if p_due_at is null or p_due_at <= now() then raise exception 'due_invalid'; end if;
  for s in select * from jsonb_array_elements(p_stages) loop
    if not exists (select 1 from public.exams e where e.id = (s ->> 'exam_id')::bigint) then
      raise exception 'exam_not_found:%', s ->> 'exam_id';
    end if;
  end loop;
  insert into public.review_sessions (class_id, title, threshold, stages, mode, due_at, sequential,
                                      current_stage, stage_started_at, status)
  values (p_class, btrim(p_title), coalesce(p_threshold, 80), p_stages, 'self', p_due_at, coalesce(p_sequential, false),
          jsonb_array_length(p_stages) - 1, now(), 'running')
  returning id into v_id;
  return v_id;
end;
$$;

-- Thông tin chế độ của một buổi ôn (bảng điều phối cần để ẩn đồng hồ và nút mở chặng).
create or replace function public.review_session_meta(p_session bigint)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  r public.review_sessions;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  select * into r from public.review_sessions where id = p_session;
  if not found then raise exception 'not_found'; end if;
  return jsonb_build_object('mode', r.mode, 'due_at', r.due_at, 'sequential', r.sequential);
end;
$$;

-- Danh sách buổi ôn: thêm mode, due_at.
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
      'stage_count', jsonb_array_length(s.stages), 'created_at', s.created_at,
      'mode', s.mode, 'due_at', s.due_at
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

-- Buổi tự học: không mở/đóng từng chặng, chỉ kết thúc cả buổi (p_stage ≥ n).
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
  elsif r.mode = 'self' then
    raise exception 'stage_invalid';
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

-- Học sinh: buổi ôn của lớp em. Live: tạo trong 12 giờ qua. Self: chưa kết thúc và chưa quá hạn + 3 ngày.
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
  v_prev jsonb := null;
  v_locked boolean;
  v_total int;
  v_done int;
  v_cur jsonb := null;
  v_exam bigint;
  v_sub jsonb;
begin
  if v_uid is null then raise exception 'not_authenticated'; end if;

  if p_session is null then
    select * into r
    from public.review_sessions s
    where s.status <> 'finished'
      and ((s.mode = 'live' and s.created_at > now() - interval '12 hours')
        or (s.mode = 'self' and (s.due_at is null or s.due_at > now() - interval '3 days')))
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

  select count(*)::int into v_total
  from public.user_classes uc join public.profiles p on p.id = uc.user_id
  where uc.class_id = r.class_id and uc.status = 'active' and p.role = 'student' and coalesce(p.is_test, false) = false;

  for i in 0 .. n - 1 loop
    v_mine := case when i <= v_idx then public.review_student_stage(r, v_uid, i) else null end;
    v_locked := r.mode = 'self' and r.sequential and i > 0
      and coalesce(v_prev ->> 'state', 'idle') <> 'passed'
      and coalesce((v_prev ->> 'tries')::int, 0) < 2;
    v_sub := null;
    if r.mode = 'self' then
      v_exam := (r.stages -> i ->> 'exam_id')::bigint;
      select jsonb_build_object('class_submitted', count(distinct er.student_id)::int, 'class_total', v_total) into v_sub
      from public.exam_results er
      join public.user_classes uc on uc.user_id = er.student_id and uc.class_id = r.class_id and uc.status = 'active'
      where er.exam_id = v_exam and er.created_at >= r.created_at;
    end if;
    v_stages := v_stages || jsonb_build_array(
      (r.stages -> i) || jsonb_build_object('mine', v_mine, 'locked', v_locked) || coalesce(v_sub, '{}'::jsonb)
    );
    v_prev := v_mine;
  end loop;

  if v_idx >= 0 and r.mode = 'live' then
    v_exam := (r.stages -> v_idx ->> 'exam_id')::bigint;
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
    'mode', r.mode,
    'due_at', r.due_at,
    'sequential', r.sequential,
    'current_stage', v_idx,
    'secs_left', public.review_secs_left(r),
    'stages', v_stages,
    'class', v_cur
  );
end;
$$;

revoke execute on function public.review_create_self(bigint, text, int, jsonb, timestamptz, boolean) from public, anon;
revoke execute on function public.review_session_meta(bigint) from public, anon;
grant execute on function public.review_create_self(bigint, text, int, jsonb, timestamptz, boolean) to authenticated;
grant execute on function public.review_session_meta(bigint) to authenticated;

commit;

-- ROLLBACK (cũng ở perf/rollback/20261025100000_on_tap_tu_hoc_ve_nha.down.sql). Buổi 'live' chạy y như trước nên chỉ
-- cần bỏ hai hàm mới; cột mode/due_at/sequential để lại vô hại (các hàm đã thay đọc chúng):
-- begin;
-- drop function if exists public.review_session_meta(bigint);
-- drop function if exists public.review_create_self(bigint, text, int, jsonb, timestamptz, boolean);
-- commit;
