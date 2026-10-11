-- Hoàn tác 20261011190000: trả hai hàm về bản cũ (câu ok mất; cột ok_items giữ lại, vô hại)
-- ---------- 5. RPC Bắt đầu ôn tập câu sai ----------
create or replace function public.mistake_review_quiz_start(p_count int default 5)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_student uuid := auth.uid();
  v_season bigint;
  v_limit int := greatest(1, least(coalesce(p_count, 5), 10));
  v_mids bigint[];
  v_att public.student_mistake_review_attempts%rowtype;
  v_qs jsonb := '[]'::jsonb;
  r record;
  q jsonb;
begin
  if v_student is null then raise exception 'Cần đăng nhập'; end if;
  if not public.rank_is_student(v_student) then raise exception 'Chỉ học sinh mới có sổ tay câu sai'; end if;

  v_season := public.rank_season_for_at(v_student, now());

  -- Ưu tiên các câu đến hạn ôn (next_review_at <= now() và chưa cleared)
  select array_agg(id) into v_mids from (
    select id from public.student_mistakes
    where student_id = v_student and not cleared and next_review_at <= now()
    order by next_review_at asc
    limit v_limit
  ) s;

  -- Nếu chưa đủ câu đến hạn, bổ sung câu chưa cleared cũ nhất để em vẫn luyện được
  if cardinality(coalesce(v_mids, '{}')) < v_limit then
    select array_agg(id) into v_mids from (
      select id from public.student_mistakes
      where student_id = v_student and not cleared
      order by case when next_review_at <= now() then 0 else 1 end, next_review_at asc
      limit v_limit
    ) s2;
  end if;

  if cardinality(coalesce(v_mids, '{}')) = 0 then
    return jsonb_build_object('ok', false, 'reason', 'empty');
  end if;

  insert into public.student_mistake_review_attempts (
    student_id, season_id, mistake_ids, total, status
  )
  values (
    v_student, v_season, v_mids, cardinality(v_mids), 'open'
  )
  returning * into v_att;

  for r in
    select sm.id as mid, sm.exam_id, sm.question_index, sm.stage, e.questions -> sm.question_index as raw_q
    from public.student_mistakes sm
    join public.exams e on e.id = sm.exam_id
    where sm.id = any (v_mids)
  loop
    q := r.raw_q;
    if q is not null then
      v_qs := v_qs || jsonb_build_array(
        jsonb_build_object(
          'mistake_id', r.mid,
          'exam_id', r.exam_id,
          'question_index', r.question_index,
          'stage', r.stage,
          'type', q ->> 'type',
          'question', q ->> 'question',
          'options', coalesce(q -> 'options', '[]'::jsonb),
          'statements', case when jsonb_typeof(q -> 'statements') = 'array' then
            (select jsonb_agg(jsonb_build_object('text', s.v ->> 'text') order by s.i)
             from jsonb_array_elements(q -> 'statements') with ordinality as s (v, i))
            else '[]'::jsonb end
        )
      );
    end if;
  end loop;

  return jsonb_build_object(
    'ok', true,
    'attempt_id', v_att.id,
    'total', cardinality(v_mids),
    'questions', v_qs
  );
end; $$;

-- ---------- 6. RPC Nộp bài ôn tập câu sai ----------
create or replace function public.mistake_review_quiz_submit(p_attempt_id bigint, p_responses jsonb)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_student uuid := auth.uid();
  v_att public.student_mistake_review_attempts%rowtype;
  v_season bigint;
  v_total int;
  v_correct int := 0;
  v_rp_per_q int := 2;
  v_day_cap int := 10;
  v_day_used int := 0;
  v_avail_rp int := 0;
  v_rp_earned int := 0;
  v_results jsonb := '[]'::jsonb;
  v_answers_log jsonb := '[]'::jsonb;
  r record;
  q jsonb;
  resp jsonb;
  v_ok boolean;
  v_cleared boolean;
  v_next_interval interval;
begin
  if v_student is null then raise exception 'Cần đăng nhập'; end if;

  select * into v_att from public.student_mistake_review_attempts
  where id = p_attempt_id and student_id = v_student for update;
  if not found then raise exception 'Không tìm thấy phiên ôn tập'; end if;
  if v_att.status = 'done' then raise exception 'Phiên này đã hoàn thành rồi'; end if;

  v_season := coalesce(v_att.season_id, public.rank_season_for_at(v_student, now()));
  if v_season is not null then
    v_rp_per_q := public.rank_cfg(v_season, 'mistake_review_rp', 2)::int;
    v_day_cap := public.rank_cfg(v_season, 'mistake_review_day_cap', 10)::int;
  end if;

  v_total := cardinality(v_att.mistake_ids);

  for r in
    select sm.id as mid, sm.exam_id, sm.question_index, sm.stage, sm.consecutive_correct,
           sm.mistake_count, e.questions -> sm.question_index as raw_q
    from public.student_mistakes sm
    join public.exams e on e.id = sm.exam_id
    where sm.id = any (v_att.mistake_ids)
  loop
    q := r.raw_q;
    resp := p_responses -> (r.mid::text);
    v_ok := public.rank_grade_question(coalesce(q, '{}'::jsonb), resp);

    if v_ok then
      v_correct := v_correct + 1;
      v_cleared := (r.stage + 1 >= 2);
      v_next_interval := case when v_cleared then interval '7 days' else interval '4 days' end;

      update public.student_mistakes
        set consecutive_correct = r.consecutive_correct + 1,
            stage = r.stage + 1,
            cleared = v_cleared,
            last_reviewed_at = now(),
            next_review_at = now() + v_next_interval
      where id = r.mid;
    else
      update public.student_mistakes
        set consecutive_correct = 0,
            stage = 0,
            mistake_count = r.mistake_count + 1,
            last_reviewed_at = now(),
            next_review_at = now() + interval '2 days'
      where id = r.mid;
    end if;

    v_answers_log := v_answers_log || jsonb_build_array(
      jsonb_build_object('mistake_id', r.mid, 'correct', v_ok)
    );

    v_results := v_results || jsonb_build_array(
      jsonb_build_object(
        'mistake_id', r.mid,
        'correct', v_ok,
        'answer', q -> 'answer',
        'explanation', coalesce(q ->> 'explanation', '')
      )
    );
  end loop;

  -- Tính thưởng RP trong mùa
  if v_season is not null and v_correct > 0 then
    select coalesce(sum(amount), 0) into v_day_used from public.rank_rp_ledger
    where season_id = v_season and student_id = v_student
      and source_kind = 'fix' and source_ref like 'mistake_review:%'
      and public.rank_vn_date(created_at) = public.rank_vn_date(now());

    v_avail_rp := greatest(0, v_day_cap - v_day_used);
    v_rp_earned := least(v_correct * v_rp_per_q, v_avail_rp);

    if v_rp_earned > 0 then
      perform public.rank_award(
        v_season, v_student, 'fix', 'mistake_review:' || v_att.id, v_rp_earned,
        'Xoá bẫy Vật lí: ôn đúng ' || v_correct || '/' || v_total || ' câu', null
      );
      perform public.rank_refresh_student(v_season, v_student);
    end if;
  end if;

  update public.student_mistake_review_attempts
    set status = 'done', correct_count = v_correct, answers = v_answers_log,
        rp_awarded = v_rp_earned, submitted_at = now()
  where id = v_att.id;

  return jsonb_build_object(
    'ok', true,
    'correct', v_correct,
    'total', v_total,
    'rp_awarded', v_rp_earned,
    'results', v_results
  );
end; $$;

drop function if exists public.mistake_q_public(bigint, bigint, int, int, text, jsonb);
grant execute on function public.mistake_review_quiz_start(int) to authenticated;
grant execute on function public.mistake_review_quiz_submit(bigint, jsonb) to authenticated;
