-- Bộ bài tập mỗi ngày (HSG KHTN 9): chặng của buổi tự học mở theo giờ, bảng tên bạn đã nộp / chưa nộp, chuông mỗi sáng.
--  * stages[i].open_at (tuỳ chọn, ISO): chặng khoá tới giờ đó (review_my_state trả locked=true). Chặng không có open_at chạy như cũ.
--  * review_open_due_stages(): mỗi 10 phút (pg_cron), chặng nào tới giờ thì bật published cho đề của chặng và gửi chuông cho cả lớp;
--    đánh dấu stages[i].opened=true để không gửi hai lần. Đề của chặng chưa tới giờ được tạo published=false nên chưa hiện ở danh sách bài kiểm tra.
--  * review_roster(p_session): em trong lớp (hoặc nhân sự) xem từng bạn đã nộp / đang làm / chưa làm từng chặng — KHÔNG có điểm, không xếp hạng.
-- Thêm hàm + thay review_my_state (chỉ thêm điều kiện khoá theo giờ). Buổi ôn cũ chạy y như trước. Chạy lúc nào cũng được.
-- Rollback ở cuối file và perf/rollback/20261028100000_bai_tap_ngay_mo_theo_gio.down.sql.
begin;

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
    v_locked := (r.mode = 'self' and r.sequential and i > 0
      and coalesce(v_prev ->> 'state', 'idle') <> 'passed'
      and coalesce((v_prev ->> 'tries')::int, 0) < 2)
      or coalesce(nullif(r.stages -> i ->> 'open_at', '')::timestamptz > now(), false);
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

create or replace function public.review_roster(p_session bigint)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_uid uuid := (select auth.uid());
  r public.review_sessions;
  n int;
begin
  if v_uid is null then raise exception 'not_authenticated'; end if;
  select * into r from public.review_sessions where id = p_session;
  if not found then return null; end if;
  if not public.is_staff() and not exists (
    select 1 from public.user_classes uc where uc.user_id = v_uid and uc.class_id = r.class_id and uc.status = 'active'
  ) then
    raise exception 'forbidden';
  end if;
  n := jsonb_array_length(r.stages);
  return jsonb_build_object(
    'now', now(),
    'students', coalesce((
      select jsonb_agg(jsonb_build_object(
        'id', p.id,
        'name', p.full_name,
        'me', p.id = v_uid,
        'st', (
          select jsonb_agg(
            case
              when exists (
                select 1 from public.exam_results er
                where er.student_id = p.id and er.exam_id = (r.stages -> g.i ->> 'exam_id')::bigint and er.created_at >= r.created_at
              ) then 'done'
              when exists (
                select 1 from public.exam_attempts a
                where a.student_id = p.id and a.exam_id = (r.stages -> g.i ->> 'exam_id')::bigint
                  and a.submitted_at is null and a.started_at >= r.created_at
              ) then 'doing'
              else 'none'
            end order by g.i)
          from generate_series(0, n - 1) as g(i)
        )
      ) order by regexp_replace(btrim(p.full_name), '^.*\s', ''), p.full_name)
      from public.user_classes uc
      join public.profiles p on p.id = uc.user_id
      where uc.class_id = r.class_id and uc.status = 'active' and p.role = 'student' and coalesce(p.is_test, false) = false
    ), '[]'::jsonb)
  );
end;
$$;

create or replace function public.review_open_due_stages()
returns int
language plpgsql security definer set search_path = public
as $$
declare
  r public.review_sessions;
  i int;
  v_opened int := 0;
  u record;
begin
  for r in select * from public.review_sessions where mode = 'self' and status <> 'finished' loop
    for i in 0 .. jsonb_array_length(r.stages) - 1 loop
      if (r.stages -> i ->> 'open_at') is not null
         and (r.stages -> i ->> 'open_at')::timestamptz <= now()
         and coalesce((r.stages -> i ->> 'opened')::boolean, false) = false then
        update public.exams set published = true where id = (r.stages -> i ->> 'exam_id')::bigint;
        update public.review_sessions
          set stages = jsonb_set(stages, array[i::text, 'opened'], 'true'::jsonb)
          where id = r.id;
        for u in
          select uc.user_id from public.user_classes uc
          join public.profiles p on p.id = uc.user_id
          where uc.class_id = r.class_id and uc.status = 'active' and p.role = 'student'
        loop
          perform public.notify_user(
            u.user_id, 'review_self_new', 'Bài tập hôm nay: ' || (r.stages -> i ->> 'title'),
            coalesce(r.stages -> i ->> 'brief', '4 bài, khoảng 30–45 phút') || ' · bấm để vào làm và xem bạn nào đã nộp.',
            '/lop-hoc/on-tap/');
        end loop;
        v_opened := v_opened + 1;
      end if;
    end loop;
  end loop;
  return v_opened;
end;
$$;

revoke execute on function public.review_roster(bigint) from public, anon;
grant execute on function public.review_roster(bigint) to authenticated;
revoke execute on function public.review_open_due_stages() from public, anon, authenticated;

commit;

do $$
begin
  begin
    create extension if not exists pg_cron;
  exception when others then
    raise notice 'pg_cron không bật được (%): gọi tay select public.review_open_due_stages(); mỗi sáng', sqlerrm;
  end;
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'review-open-due-stages';
    perform cron.schedule('review-open-due-stages', '*/10 * * * *', 'select public.review_open_due_stages();');
    raise notice 'Đã đặt lịch pg_cron review-open-due-stages (mỗi 10 phút)';
  end if;
end $$;

-- ROLLBACK (cũng ở perf/rollback/20261028100000_bai_tap_ngay_mo_theo_gio.down.sql):
-- do $$ begin
--   if exists (select 1 from pg_extension where extname = 'pg_cron') then
--     perform cron.unschedule(jobid) from cron.job where jobname = 'review-open-due-stages';
--   end if;
-- end $$;
-- drop function if exists public.review_open_due_stages();
-- drop function if exists public.review_roster(bigint);
-- rồi chạy lại phần create or replace review_my_state trong 20261025100000_on_tap_tu_hoc_ve_nha.sql
