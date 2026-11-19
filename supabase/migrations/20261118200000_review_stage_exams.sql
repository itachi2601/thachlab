-- Báo lỗi #155 (18/11/2026): buổi ôn tập theo chặng tính lượt làm theo exam_id CHỤP lúc tạo buổi (review_sessions.stages).
-- `scripts/publish-theory-quiz.mts --replace` tạo đề "Kiểm tra nhanh" mới và đổi lesson_items.exam_ids (ví dụ item 219: [755] → [1182]),
-- nên lượt HS làm đề mới (vào từ trang bài học) không được tính: chặng hiện "Đang làm/Chưa làm", chặng sau bị khoá,
-- bảng điều phối báo thiếu (buổi 18 chặng 4: 28 HS làm đề mới, 0 đề cũ).
--
-- Sửa (chỉ thay/thêm HÀM, không đụng dữ liệu, không đụng bảng/RLS):
--  * review_stage_exams(stage)    [nội bộ] tập đề của chặng = {stage.exam_id} ∪ lesson_items.exam_ids của stage.item_id.
--  * review_stage_exam_now(stage) [nội bộ] đề hiện hành: stage.exam_id nếu item vẫn gắn đề đó (hoặc chặng không có item),
--                                 ngược lại đề mới nhất (id lớn nhất, còn tồn tại) trong lesson_items.exam_ids.
--  * review_student_stage: điểm tốt nhất / số lượt tính trên cả tập đề; lượt treo = lượt chưa nộp MỚI NHẤT trên cả tập đề và
--    bắt đầu SAU lần nộp gần nhất (lượt treo cũ trên đề cũ, như attempt 2691 của báo lỗi, không còn biến chặng thành "Đang làm");
--    trả thêm `open_exam_id` (đề của lượt treo). Số câu `total` theo đề của lượt treo, không có thì theo đề hiện hành.
--  * review_my_state: mỗi chặng trả `exam_id` = đề nên mở (đề của lượt treo nếu có, không thì đề hiện hành) để nút
--    "Vào làm / Tiếp tục làm" dẫn đúng đề; `exam_id_goc` = exam_id chụp lúc tạo buổi (chỉ khi khác). Số bạn đã nộp tính trên tập đề.
--  * review_board_stage: session.stages cũng đổi `exam_id` sang đề hiện hành (QR/mã đề trên màn chiếu, nút Chiếu, trích câu).
--    Câu sai nhiều nhất TÁCH THEO TỪNG ĐỀ (group by exam_id, question_index), mỗi dòng có `exam_id`; đề hiện hành xếp trước.
--    Nhãn dạng (dang_by_index) chỉ áp cho đề gốc của chặng (đề ôn dạng không có item nên không bao giờ đổi).
--  * review_wrong_students: tách theo (em, đề, câu), mỗi dòng có `exam_id`; `tries` đếm trên cả tập đề.
--  * review_roster: đã nộp / đang làm tính trên tập đề.
-- Quyền: hai hàm nội bộ revoke khỏi public/anon/authenticated; các hàm cũ giữ nguyên chữ ký nên giữ nguyên grant.
-- Chạy NGOÀI GIỜ HS LÀM BÀI (create or replace các hàm HS đang gọi mỗi 8–20 giây ở /lop-hoc/on-tap); nhẹ, không quét dữ liệu.
-- Rollback: perf/rollback/20261118200000_review_stage_exams.down.sql (dựng lại nguyên văn bản cũ của 5 hàm, rồi drop 2 hàm mới).
begin;

-- ---------- Hàm nội bộ mới ----------
create or replace function public.review_stage_exams(stage jsonb)
returns bigint[]
language sql stable security definer set search_path = public
as $$
  select coalesce(array_agg(distinct x order by x), '{}'::bigint[])
  from unnest(
    array[(stage ->> 'exam_id')::bigint]
    || coalesce((select li.exam_ids from public.lesson_items li where li.id = (stage ->> 'item_id')::bigint), '{}'::bigint[])
  ) as u(x)
  where x is not null
$$;
revoke execute on function public.review_stage_exams(jsonb) from public, anon, authenticated;

create or replace function public.review_stage_exam_now(stage jsonb)
returns bigint
language sql stable security definer set search_path = public
as $$
  select case
    when li.ids is null or cardinality(li.ids) = 0 or (stage ->> 'exam_id')::bigint = any(li.ids)
      then (stage ->> 'exam_id')::bigint
    else coalesce((select max(e.id) from public.exams e where e.id = any(li.ids)), (stage ->> 'exam_id')::bigint)
  end
  from (select (select l.exam_ids from public.lesson_items l where l.id = (stage ->> 'item_id')::bigint) as ids) li
$$;
revoke execute on function public.review_stage_exam_now(jsonb) from public, anon, authenticated;

-- ---------- review_student_stage (bản trước: 20261021120000_on_tap_theo_chang.sql) ----------
create or replace function public.review_student_stage(r public.review_sessions, p_student uuid, p_idx int)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_exams bigint[] := public.review_stage_exams(r.stages -> p_idx);
  v_now bigint := public.review_stage_exam_now(r.stages -> p_idx);
  v_total int;
  v_best numeric;
  v_tries int;
  v_last_sub timestamptz;
  v_open boolean;
  v_open_exam bigint;
  v_responses jsonb;
  v_saved timestamptz;
  v_started timestamptz;
  v_answered int := 0;
  v_state text;
  v_last int;
begin
  select max(er.score), count(*), max(er.created_at) into v_best, v_tries, v_last_sub
  from public.exam_results er
  where er.student_id = p_student and er.exam_id = any(v_exams) and er.created_at >= r.created_at;

  -- Lượt treo: mới nhất trên cả tập đề, bắt đầu sau lần nộp gần nhất (lượt bỏ dở trước đó coi như đã bỏ).
  select a.exam_id, a.responses, a.saved_at, a.started_at into v_open_exam, v_responses, v_saved, v_started
  from public.exam_attempts a
  where a.student_id = p_student and a.exam_id = any(v_exams) and a.submitted_at is null
    and a.started_at >= greatest(r.created_at, coalesce(v_last_sub, r.created_at))
  order by a.started_at desc
  limit 1;
  v_open := found;

  select coalesce(e.question_count, jsonb_array_length(e.questions)) into v_total
  from public.exams e where e.id = coalesce(v_open_exam, v_now);

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
    'idle_secs', v_last,
    'open_exam_id', v_open_exam
  );
end;
$$;
revoke execute on function public.review_student_stage(public.review_sessions, uuid, int) from public, anon, authenticated;

-- ---------- review_my_state (bản trước: 20261028100000_bai_tap_ngay_mo_theo_gio.sql) ----------
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
  v_exams bigint[];
  v_sub jsonb;
  v_go bigint;
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
      v_exams := public.review_stage_exams(r.stages -> i);
      select jsonb_build_object('class_submitted', count(distinct er.student_id)::int, 'class_total', v_total) into v_sub
      from public.exam_results er
      join public.user_classes uc on uc.user_id = er.student_id and uc.class_id = r.class_id and uc.status = 'active'
      where er.exam_id = any(v_exams) and er.created_at >= r.created_at;
    end if;
    -- Đề nút "Vào làm/Tiếp tục làm" mở: lượt treo của em (nếu có), không thì đề hiện hành của mục bài học.
    v_go := coalesce((v_mine ->> 'open_exam_id')::bigint, public.review_stage_exam_now(r.stages -> i));
    v_stages := v_stages || jsonb_build_array(
      (r.stages -> i)
      || jsonb_build_object('exam_id', v_go)
      || case when v_go is distinct from (r.stages -> i ->> 'exam_id')::bigint
           then jsonb_build_object('exam_id_goc', (r.stages -> i ->> 'exam_id')::bigint) else '{}'::jsonb end
      || jsonb_build_object('mine', v_mine, 'locked', v_locked) || coalesce(v_sub, '{}'::jsonb)
    );
    v_prev := v_mine;
  end loop;

  if v_idx >= 0 and r.mode = 'live' then
    v_exams := public.review_stage_exams(r.stages -> v_idx);
    select count(distinct er.student_id)::int into v_done
    from public.exam_results er
    join public.user_classes uc on uc.user_id = er.student_id and uc.class_id = r.class_id and uc.status = 'active'
    where er.exam_id = any(v_exams) and er.created_at >= r.created_at;
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

-- ---------- review_roster (bản trước: 20261028100000_bai_tap_ngay_mo_theo_gio.sql) ----------
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
      with st as materialized (
        select g.i, public.review_stage_exams(r.stages -> g.i) as ex from generate_series(0, n - 1) as g(i)
      )
      select jsonb_agg(jsonb_build_object(
        'id', p.id,
        'name', p.full_name,
        'me', p.id = v_uid,
        'st', (
          select jsonb_agg(
            case
              when exists (
                select 1 from public.exam_results er
                where er.student_id = p.id and er.exam_id = any(st.ex) and er.created_at >= r.created_at
              ) then 'done'
              when exists (
                select 1 from public.exam_attempts a
                where a.student_id = p.id and a.exam_id = any(st.ex)
                  and a.submitted_at is null and a.started_at >= r.created_at
              ) then 'doing'
              else 'none'
            end order by st.i)
          from st
        )
      ) order by regexp_replace(btrim(p.full_name), '^.*\s', ''), p.full_name)
      from public.user_classes uc
      join public.profiles p on p.id = uc.user_id
      where uc.class_id = r.class_id and uc.status = 'active' and p.role = 'student' and coalesce(p.is_test, false) = false
    ), '[]'::jsonb)
  );
end;
$$;

-- ---------- review_board_stage (bản trước: 20261024170000_on_tap_xem_lai_chang_em_sai.sql) ----------
create or replace function public.review_board_stage(p_session bigint, p_stage int default null)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  r public.review_sessions;
  n int;
  v_idx int;
  v_students jsonb;
  v_wrong jsonb := '[]'::jsonb;
  v_dang jsonb := '[]'::jsonb;
  v_exam bigint;      -- đề chụp lúc tạo buổi (nhãn dạng gắn với đề này)
  v_now bigint;       -- đề hiện hành của mục bài học
  v_exams bigint[];   -- mọi đề tính cho chặng
  v_map jsonb;
  v_stages_out jsonb;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  select * into r from public.review_sessions where id = p_session;
  if not found then raise exception 'not_found'; end if;
  n := jsonb_array_length(r.stages);
  v_idx := coalesce(p_stage, r.current_stage);
  if v_idx >= n or (p_stage is not null and p_stage < 0) then raise exception 'stage_invalid'; end if;

  -- Màn chiếu/QR/nút Chiếu dùng stages[i].exam_id → trả đề hiện hành; exam_id_goc giữ đề chụp lúc tạo (chỉ khi khác).
  select coalesce(jsonb_agg(
    s.v || jsonb_build_object('exam_id', public.review_stage_exam_now(s.v))
        || case when public.review_stage_exam_now(s.v) is distinct from (s.v ->> 'exam_id')::bigint
             then jsonb_build_object('exam_id_goc', (s.v ->> 'exam_id')::bigint) else '{}'::jsonb end
    order by s.ord), '[]'::jsonb)
  into v_stages_out
  from jsonb_array_elements(r.stages) with ordinality as s(v, ord);

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
    v_now := public.review_stage_exam_now(r.stages -> v_idx);
    v_exams := public.review_stage_exams(r.stages -> v_idx);
    v_map := r.stages -> v_idx -> 'dang_by_index';

    -- Câu sai: TÁCH theo (đề, câu) — đề mới xáo ý/đổi số câu nên câu số k của hai đề là hai câu khác nhau.
    select coalesce(jsonb_agg(t order by (t.exam_id = v_now) desc, t.pct desc, t.total desc, t.exam_id desc, t.idx), '[]'::jsonb)
    into v_wrong
    from (
      select q.exam_id,
             q.question_index as idx,
             case when jsonb_typeof(v_map) = 'array' and q.exam_id = v_exam then v_map ->> q.question_index end as dang,
             count(*)::int as total,
             count(*) filter (where q.is_correct is false)::int as wrong,
             round(100.0 * count(*) filter (where q.is_correct is false) / count(*))::int as pct,
             (select count(*)::int from (
                select distinct on (q2.student_id) q2.student_id, q2.is_correct
                from public.exam_question_results q2
                join public.exam_results er2 on er2.id = q2.exam_result_id
                join public.user_classes uc2 on uc2.user_id = q2.student_id and uc2.class_id = r.class_id and uc2.status = 'active'
                where q2.exam_id = q.exam_id and q2.question_index = q.question_index
                  and er2.created_at >= r.created_at and q2.is_correct is not null and q2.max > 0
                order by q2.student_id, er2.created_at desc, er2.id desc
              ) l where l.is_correct is false) as students_wrong
      from public.exam_question_results q
      join public.exam_results er on er.id = q.exam_result_id
      join public.user_classes uc on uc.user_id = q.student_id and uc.class_id = r.class_id and uc.status = 'active'
      where q.exam_id = any(v_exams) and er.created_at >= r.created_at and q.is_correct is not null and q.max > 0
      group by q.exam_id, q.question_index
      having count(*) filter (where q.is_correct is false) > 0
    ) t;

    if jsonb_typeof(v_map) = 'array' then
      select coalesce(jsonb_agg(t order by t.pct desc, t.total desc), '[]'::jsonb) into v_dang
      from (
        select v_map ->> q.question_index as label,
               count(*)::int as total,
               count(*) filter (where q.is_correct is false)::int as wrong,
               round(100.0 * count(*) filter (where q.is_correct is false) / count(*))::int as pct,
               count(distinct q.student_id) filter (where q.is_correct is false)::int as students_wrong,
               count(distinct q.student_id)::int as students
        from public.exam_question_results q
        join public.exam_results er on er.id = q.exam_result_id
        join public.user_classes uc on uc.user_id = q.student_id and uc.class_id = r.class_id and uc.status = 'active'
        where q.exam_id = v_exam and er.created_at >= r.created_at and q.is_correct is not null and q.max > 0
          and v_map ->> q.question_index is not null
        group by v_map ->> q.question_index
      ) t;
    end if;
  end if;

  return jsonb_build_object(
    'now', now(),
    'session', jsonb_build_object(
      'id', r.id, 'title', r.title, 'class_id', r.class_id, 'threshold', r.threshold, 'status', r.status,
      'current_stage', r.current_stage, 'viewed_stage', v_idx, 'stage_started_at', r.stage_started_at,
      'secs_left', public.review_secs_left(r), 'stages', v_stages_out
    ),
    'students', v_students,
    'wrongest', v_wrong,
    'by_dang', v_dang
  );
end;
$$;

-- ---------- review_wrong_students (bản trước: 20261024170000_on_tap_xem_lai_chang_em_sai.sql) ----------
create or replace function public.review_wrong_students(p_session bigint, p_stage int default null)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  r public.review_sessions;
  v_idx int;
  v_exam bigint;
  v_now bigint;
  v_exams bigint[];
  v_map jsonb;
  v_out jsonb;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  select * into r from public.review_sessions where id = p_session;
  if not found then raise exception 'not_found'; end if;
  v_idx := coalesce(p_stage, r.current_stage);
  if v_idx < 0 then return '[]'::jsonb; end if;
  if v_idx >= jsonb_array_length(r.stages) then raise exception 'stage_invalid'; end if;
  v_exam := (r.stages -> v_idx ->> 'exam_id')::bigint;
  v_now := public.review_stage_exam_now(r.stages -> v_idx);
  v_exams := public.review_stage_exams(r.stages -> v_idx);
  v_map := r.stages -> v_idx -> 'dang_by_index';

  select coalesce(jsonb_agg(jsonb_build_object(
           'student_id', t.student_id,
           'name', t.full_name,
           'exam_id', t.exam_id,
           'idx', t.question_index,
           'dang', case when jsonb_typeof(v_map) = 'array' and t.exam_id = v_exam then v_map ->> t.question_index end,
           'earned', t.earned,
           'max', t.max,
           'tries', t.tries
         ) order by (t.exam_id = v_now) desc, t.exam_id desc, t.question_index, t.full_name), '[]'::jsonb)
  into v_out
  from (
    select l.*, p.full_name,
           (select count(*)::int from public.exam_results e3
             where e3.student_id = l.student_id and e3.exam_id = any(v_exams) and e3.created_at >= r.created_at) as tries
    from (
      select distinct on (q.student_id, q.exam_id, q.question_index)
             q.student_id, q.exam_id, q.question_index, q.is_correct, q.earned, q.max
      from public.exam_question_results q
      join public.exam_results er on er.id = q.exam_result_id
      join public.user_classes uc on uc.user_id = q.student_id and uc.class_id = r.class_id and uc.status = 'active'
      where q.exam_id = any(v_exams) and er.created_at >= r.created_at and q.is_correct is not null and q.max > 0
      order by q.student_id, q.exam_id, q.question_index, er.created_at desc, er.id desc
    ) l
    join public.profiles p on p.id = l.student_id and coalesce(p.is_test, false) = false
    where l.is_correct is false
  ) t;

  return v_out;
end;
$$;

commit;

-- ROLLBACK: supabase db query --linked -f perf/rollback/20261118200000_review_stage_exams.down.sql
-- (dựng lại nguyên văn review_student_stage 20261021120000, review_my_state + review_roster 20261028100000,
--  review_board_stage + review_wrong_students 20261024170000, rồi drop review_stage_exams / review_stage_exam_now).
