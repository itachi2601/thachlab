-- Ôn tập theo chặng — trợ giảng xem lại chặng cũ và biết EM NÀO đang sai câu/dạng nào (24/10/2026).
--   * review_board_stage(p_session, p_stage): bảng điều phối của MỘT chặng bất kỳ (null = chặng hiện tại).
--     Giống review_board bản 20261023120000 (students, wrongest, by_dang) + `students_wrong` cho mỗi câu
--     (số em ĐANG sai = lượt làm mới nhất của em vẫn sai) và `viewed_stage` trong session. Số "lượt" giữ nguyên.
--   * review_board(p_session): giữ tên cũ, chỉ gọi review_board_stage(p_session, null) — client cũ vẫn chạy.
--   * review_wrong_students(p_session, p_stage): mọi cặp (em, câu) mà lượt làm MỚI NHẤT của em ở câu đó vẫn sai,
--     kèm nhãn dạng. Em đã làm lại và đúng thì không còn trong danh sách.
-- Chỉ nhân sự (is_staff) gọi được. Chỉ tạo hàm, không đụng dữ liệu. Chạy lúc nào cũng được.

begin;

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
  v_exam bigint;
  v_map jsonb;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  select * into r from public.review_sessions where id = p_session;
  if not found then raise exception 'not_found'; end if;
  n := jsonb_array_length(r.stages);
  v_idx := coalesce(p_stage, r.current_stage);
  if v_idx >= n or (p_stage is not null and p_stage < 0) then raise exception 'stage_invalid'; end if;

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
    v_map := r.stages -> v_idx -> 'dang_by_index';

    -- Câu sai: số lượt (mọi lần nộp) + số em đang sai (lượt mới nhất). Không cắt ở 8 câu: câu sai ít vẫn phải thấy.
    select coalesce(jsonb_agg(t order by t.pct desc, t.total desc, t.idx), '[]'::jsonb) into v_wrong
    from (
      select q.question_index as idx,
             case when jsonb_typeof(v_map) = 'array' then v_map ->> q.question_index end as dang,
             count(*)::int as total,
             count(*) filter (where q.is_correct is false)::int as wrong,
             round(100.0 * count(*) filter (where q.is_correct is false) / count(*))::int as pct,
             (select count(*)::int from (
                select distinct on (q2.student_id) q2.student_id, q2.is_correct
                from public.exam_question_results q2
                join public.exam_results er2 on er2.id = q2.exam_result_id
                join public.user_classes uc2 on uc2.user_id = q2.student_id and uc2.class_id = r.class_id and uc2.status = 'active'
                where q2.exam_id = v_exam and q2.question_index = q.question_index
                  and er2.created_at >= r.created_at and q2.is_correct is not null and q2.max > 0
                order by q2.student_id, er2.created_at desc, er2.id desc
              ) l where l.is_correct is false) as students_wrong
      from public.exam_question_results q
      join public.exam_results er on er.id = q.exam_result_id
      join public.user_classes uc on uc.user_id = q.student_id and uc.class_id = r.class_id and uc.status = 'active'
      where q.exam_id = v_exam and er.created_at >= r.created_at and q.is_correct is not null and q.max > 0
      group by q.question_index
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
      'secs_left', public.review_secs_left(r), 'stages', r.stages
    ),
    'students', v_students,
    'wrongest', v_wrong,
    'by_dang', v_dang
  );
end;
$$;

-- Giữ tên và chữ ký cũ để client chưa deploy vẫn gọi được.
create or replace function public.review_board(p_session bigint)
returns jsonb
language sql stable security definer set search_path = public
as $$ select public.review_board_stage(p_session, null) $$;

create or replace function public.review_wrong_students(p_session bigint, p_stage int default null)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  r public.review_sessions;
  v_idx int;
  v_exam bigint;
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
  v_map := r.stages -> v_idx -> 'dang_by_index';

  select coalesce(jsonb_agg(jsonb_build_object(
           'student_id', t.student_id,
           'name', t.full_name,
           'idx', t.question_index,
           'dang', case when jsonb_typeof(v_map) = 'array' then v_map ->> t.question_index end,
           'earned', t.earned,
           'max', t.max,
           'tries', t.tries
         ) order by t.question_index, t.full_name), '[]'::jsonb)
  into v_out
  from (
    select l.*, p.full_name,
           (select count(*)::int from public.exam_results e3
             where e3.student_id = l.student_id and e3.exam_id = v_exam and e3.created_at >= r.created_at) as tries
    from (
      select distinct on (q.student_id, q.question_index)
             q.student_id, q.question_index, q.is_correct, q.earned, q.max
      from public.exam_question_results q
      join public.exam_results er on er.id = q.exam_result_id
      join public.user_classes uc on uc.user_id = q.student_id and uc.class_id = r.class_id and uc.status = 'active'
      where q.exam_id = v_exam and er.created_at >= r.created_at and q.is_correct is not null and q.max > 0
      order by q.student_id, q.question_index, er.created_at desc, er.id desc
    ) l
    join public.profiles p on p.id = l.student_id and coalesce(p.is_test, false) = false
    where l.is_correct is false
  ) t;

  return v_out;
end;
$$;

revoke execute on function public.review_board_stage(bigint, int) from public, anon;
revoke execute on function public.review_wrong_students(bigint, int) from public, anon;
grant execute on function public.review_board_stage(bigint, int) to authenticated;
grant execute on function public.review_wrong_students(bigint, int) to authenticated;

commit;

-- ROLLBACK (cũng ở perf/rollback/20261024170000_on_tap_xem_lai_chang_em_sai.down.sql):
-- begin;
-- drop function if exists public.review_wrong_students(bigint, int);
-- -- khôi phục review_board bản cũ: chạy lại hàm review_board trong 20261023120000_on_tap_dang_bai_tap.sql
-- --   (create or replace đè bản gọi review_board_stage), rồi mới drop hàm dưới đây.
-- drop function if exists public.review_board_stage(bigint, int);
-- commit;
