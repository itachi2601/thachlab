-- ============================================================================
-- Kho bẫy: mỗi lượt ôn trộn CÂU BẪY (đến hạn) với CÂU EM ĐÃ LÀM ĐÚNG (11/10/2026)
-- Lý do: lượt toàn câu sai kéo tỉ lệ đúng xuống ~40–60% → dễ nản; vùng học tốt nhất ~85% đúng
-- (Wilson 2019), mở/đóng bằng câu làm được (peak-end, Kahneman), nhớ lại điều đã biết cũng củng cố trí nhớ (Roediger & Karpicke).
-- Tỉ lệ bẫy thích ứng theo 2 lượt gần nhất (config mùa, mặc định):
--   mặc định 0.6 · lượt gần nhất đúng < 50% hoặc đang có > 15 bẫy tồn → 0.4 · 2 lượt liền đúng > 80% → 0.7
-- Câu đầu và câu cuối của lượt luôn là câu "ok" (nếu có ≥ 2 câu ok).
-- Câu ok: lấy từ câu em từng làm đúng (bài kiểm tra + luyện tập), ưu tiên làm đúng cách đây ≥ 3 ngày,
-- không phải bẫy chưa xoá; KHÔNG cộng RP, KHÔNG đổi lịch ôn của bẫy; nếu làm sai thì trở thành bẫy mới.
-- Thêm cột attempts.ok_items; định nghĩa lại mistake_review_quiz_start / _submit. Câu ok mang mistake_id âm (-1, -2…),
-- thêm trường kind = 'trap' | 'ok' (client cũ bỏ qua).
-- Cách chạy: bash scripts/run-migrations.sh — giờ nào cũng được.
-- Rollback: perf/rollback/20261011190000_mistake_review_mix_ok.down.sql
-- ============================================================================

alter table public.student_mistake_review_attempts
  add column if not exists ok_items jsonb not null default '[]'::jsonb;

-- JSON câu hỏi đưa cho học sinh (không lộ đáp án)
create or replace function public.mistake_q_public(p_key bigint, p_exam bigint, p_idx int, p_stage int, p_kind text, q jsonb)
returns jsonb
language sql immutable set search_path = public
as $$
  select jsonb_build_object(
    'mistake_id', p_key, 'exam_id', p_exam, 'question_index', p_idx, 'stage', p_stage, 'kind', p_kind,
    'type', q ->> 'type', 'question', q ->> 'question',
    'options', coalesce(q -> 'options', '[]'::jsonb),
    'statements', case when jsonb_typeof(q -> 'statements') = 'array' then
      (select jsonb_agg(jsonb_build_object('text', s.v ->> 'text') order by s.i)
       from jsonb_array_elements(q -> 'statements') with ordinality as s (v, i))
      else '[]'::jsonb end);
$$;

create or replace function public.mistake_review_quiz_start(p_count int default 5)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_student uuid := auth.uid();
  v_season bigint;
  v_limit int := greatest(1, least(coalesce(p_count, 5), 10));
  v_share numeric;
  v_active int;
  v_trap_avail int;
  v_n_trap int;
  v_n_ok int;
  v_mids bigint[] := '{}';
  v_ok jsonb := '[]'::jsonb;
  v_att public.student_mistake_review_attempts%rowtype;
  v_last numeric;
  v_prev numeric;
  r record;
  q jsonb;
  v_traps jsonb[] := '{}';
  v_oks jsonb[] := '{}';
  v_seq jsonb[] := '{}';
  v_mid jsonb[];
  v_i int;
  v_k int := 0;
  v_mid_ok int;
  v_gap int;
begin
  if v_student is null then raise exception 'Cần đăng nhập'; end if;
  if not public.rank_is_student(v_student) then raise exception 'Chỉ học sinh mới có sổ tay câu sai'; end if;

  v_season := public.rank_season_for_at(v_student, now());

  select count(*) into v_active from public.student_mistakes where student_id = v_student and not cleared;
  v_trap_avail := v_active;
  if v_trap_avail = 0 then
    return jsonb_build_object('ok', false, 'reason', 'empty');
  end if;

  -- Tỉ lệ bẫy thích ứng theo 2 lượt gần nhất
  select max(case when rn = 1 then acc end), max(case when rn = 2 then acc end) into v_last, v_prev
  from (select correct_count::numeric / nullif(total, 0) as acc,
               row_number() over (order by submitted_at desc) as rn
        from public.student_mistake_review_attempts
        where student_id = v_student and status = 'done' order by submitted_at desc limit 2) a;

  v_share := coalesce(public.rank_cfg(v_season, 'mistake_review_trap_share', 0.6), 0.6);
  if (v_last is not null and v_last < 0.5) or v_active > 15 then
    v_share := least(v_share, 0.4);
  elsif v_last is not null and v_prev is not null and v_last > 0.8 and v_prev > 0.8 then
    v_share := greatest(v_share, 0.7);
  end if;

  v_n_trap := greatest(1, round(v_limit * v_share)::int);
  v_n_ok := v_limit - v_n_trap;

  -- Câu ok: từng làm đúng, không phải bẫy chưa xoá, ưu tiên làm đúng cách đây >= 3 ngày
  if v_n_ok > 0 then
    with good as (
      select exam_id, question_index as qi, created_at from public.exam_question_results
      where student_id = v_student and is_correct and coalesce(qtype, '') <> 'essay' and exam_id is not null
      union all
      select exam_id, coalesce(source_index, question_index), created_at from public.practice_question_results
      where student_id = v_student and is_correct and coalesce(qtype, '') <> 'essay' and exam_id is not null
    ), g as (
      select exam_id, qi, max(created_at) as last_ok from good group by 1, 2
    ), pick as (
      select g.exam_id, g.qi from g
      join public.exams e on e.id = g.exam_id and jsonb_typeof(e.questions) = 'array' and e.questions -> g.qi is not null
      where not exists (select 1 from public.student_mistakes sm
                        where sm.student_id = v_student and sm.exam_id = g.exam_id and sm.question_index = g.qi and not sm.cleared)
      order by (g.last_ok <= now() - interval '3 days') desc, random()
      limit v_n_ok
    )
    select coalesce(jsonb_agg(jsonb_build_object('exam_id', exam_id, 'qi', qi)), '[]'::jsonb) into v_ok from pick;
  end if;

  v_n_ok := jsonb_array_length(v_ok);
  v_n_trap := least(v_limit - v_n_ok, v_trap_avail);

  select array_agg(id) into v_mids from (
    select id from public.student_mistakes
    where student_id = v_student and not cleared
    order by case when next_review_at <= now() then 0 else 1 end, next_review_at asc
    limit v_n_trap
  ) s;

  -- gán khoá âm cho câu ok
  select coalesce(jsonb_agg(x.v || jsonb_build_object('key', -x.n) order by x.n), '[]'::jsonb) into v_ok
  from (select value as v, ordinality as n from jsonb_array_elements(v_ok) with ordinality) x;

  insert into public.student_mistake_review_attempts (student_id, season_id, mistake_ids, ok_items, total, status)
  values (v_student, v_season, coalesce(v_mids, '{}'), v_ok, cardinality(coalesce(v_mids, '{}')) + v_n_ok, 'open')
  returning * into v_att;

  for r in
    select sm.id as mid, sm.exam_id, sm.question_index, sm.stage, e.questions -> sm.question_index as raw_q
    from public.student_mistakes sm join public.exams e on e.id = sm.exam_id
    where sm.id = any (coalesce(v_mids, '{}'))
    order by case when sm.next_review_at <= now() then 0 else 1 end, sm.next_review_at
  loop
    if r.raw_q is not null then
      v_traps := v_traps || public.mistake_q_public(r.mid, r.exam_id, r.question_index, r.stage, 'trap', r.raw_q);
    end if;
  end loop;

  for r in
    select (o ->> 'key')::bigint as k, (o ->> 'exam_id')::bigint as exam_id, (o ->> 'qi')::int as qi,
           e.questions -> (o ->> 'qi')::int as raw_q
    from jsonb_array_elements(v_ok) o join public.exams e on e.id = (o ->> 'exam_id')::bigint
    order by (o ->> 'key')::bigint desc
  loop
    if r.raw_q is not null then
      v_oks := v_oks || public.mistake_q_public(r.k, r.exam_id, r.qi, 0, 'ok', r.raw_q);
    end if;
  end loop;

  -- Thứ tự: câu ok đầu, bẫy xen câu ok giữa, câu ok cuối
  if coalesce(array_length(v_oks, 1), 0) >= 2 then
    v_seq := array[v_oks[1]];
    v_mid_ok := array_length(v_oks, 1) - 2;
    v_gap := case when v_mid_ok > 0 then greatest(1, ceil(coalesce(array_length(v_traps, 1), 0)::numeric / (v_mid_ok + 1))::int) else 0 end;
    v_k := 0;
    for v_i in 1..coalesce(array_length(v_traps, 1), 0) loop
      v_seq := v_seq || v_traps[v_i];
      if v_gap > 0 and v_i % v_gap = 0 and v_k < v_mid_ok then
        v_k := v_k + 1;
        v_seq := v_seq || v_oks[1 + v_k];
      end if;
    end loop;
    while v_k < v_mid_ok loop
      v_k := v_k + 1;
      v_seq := v_seq || v_oks[1 + v_k];
    end loop;
    v_seq := v_seq || v_oks[array_length(v_oks, 1)];
  elsif coalesce(array_length(v_oks, 1), 0) = 1 then
    v_seq := array[v_oks[1]] || v_traps;
  else
    v_seq := v_traps;
  end if;

  if coalesce(array_length(v_seq, 1), 0) = 0 then
    return jsonb_build_object('ok', false, 'reason', 'empty');
  end if;

  return jsonb_build_object('ok', true, 'attempt_id', v_att.id, 'total', array_length(v_seq, 1),
    'questions', to_jsonb(v_seq));
end; $$;

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
  v_trap_correct int := 0;
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

  v_total := cardinality(v_att.mistake_ids) + jsonb_array_length(v_att.ok_items);

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
      v_trap_correct := v_trap_correct + 1;
      v_cleared := (r.stage + 1 >= 2);
      v_next_interval := case when v_cleared then interval '7 days' else interval '4 days' end;

      update public.student_mistakes
        set consecutive_correct = r.consecutive_correct + 1, stage = r.stage + 1, cleared = v_cleared,
            last_reviewed_at = now(), next_review_at = now() + v_next_interval
      where id = r.mid;
    else
      update public.student_mistakes
        set consecutive_correct = 0, stage = 0, mistake_count = r.mistake_count + 1,
            last_reviewed_at = now(), next_review_at = now() + interval '2 days'
      where id = r.mid;
    end if;

    v_answers_log := v_answers_log || jsonb_build_array(jsonb_build_object('mistake_id', r.mid, 'correct', v_ok));
    v_results := v_results || jsonb_build_array(jsonb_build_object(
      'mistake_id', r.mid, 'kind', 'trap', 'correct', v_ok, 'answer', q -> 'answer',
      'explanation', coalesce(q ->> 'explanation', '')));
  end loop;

  -- Câu ok: không cộng RP; sai thì thành bẫy mới
  for r in
    select (o ->> 'key')::bigint as k, (o ->> 'exam_id')::bigint as exam_id, (o ->> 'qi')::int as qi,
           e.questions -> (o ->> 'qi')::int as raw_q
    from jsonb_array_elements(v_att.ok_items) o join public.exams e on e.id = (o ->> 'exam_id')::bigint
  loop
    q := r.raw_q;
    resp := p_responses -> (r.k::text);
    v_ok := public.rank_grade_question(coalesce(q, '{}'::jsonb), resp);
    if v_ok then
      v_correct := v_correct + 1;
    else
      insert into public.student_mistakes (student_id, exam_id, question_index, topic_id, form, difficulty,
        mistake_count, consecutive_correct, stage, cleared, last_wrong_at, next_review_at)
      select v_student, r.exam_id, r.qi,
             (select topic_id from public.exam_question_results x where x.student_id = v_student and x.exam_id = r.exam_id and x.question_index = r.qi limit 1),
             '', '', 1, 0, 0, false, now(), now() + interval '2 days'
      on conflict (student_id, exam_id, question_index) do update
        set mistake_count = public.student_mistakes.mistake_count + 1, consecutive_correct = 0, stage = 0,
            cleared = false, last_wrong_at = now(), next_review_at = now() + interval '2 days';
    end if;
    v_answers_log := v_answers_log || jsonb_build_array(jsonb_build_object('mistake_id', r.k, 'correct', v_ok, 'kind', 'ok'));
    v_results := v_results || jsonb_build_array(jsonb_build_object(
      'mistake_id', r.k, 'kind', 'ok', 'correct', v_ok, 'answer', q -> 'answer',
      'explanation', coalesce(q ->> 'explanation', '')));
  end loop;

  if v_season is not null and v_trap_correct > 0 then
    select coalesce(sum(amount), 0) into v_day_used from public.rank_rp_ledger
    where season_id = v_season and student_id = v_student
      and source_kind = 'fix' and source_ref like 'mistake_review:%'
      and public.rank_vn_date(created_at) = public.rank_vn_date(now());

    v_avail_rp := greatest(0, v_day_cap - v_day_used);
    v_rp_earned := least(v_trap_correct * v_rp_per_q, v_avail_rp);

    if v_rp_earned > 0 then
      perform public.rank_award(v_season, v_student, 'fix', 'mistake_review:' || v_att.id, v_rp_earned,
        'Xoá bẫy Vật lí: ôn đúng ' || v_trap_correct || ' câu bẫy', null);
      perform public.rank_refresh_student(v_season, v_student);
    end if;
  end if;

  update public.student_mistake_review_attempts
    set status = 'done', correct_count = v_correct, total = v_total, answers = v_answers_log,
        rp_awarded = v_rp_earned, submitted_at = now()
  where id = v_att.id;

  return jsonb_build_object('ok', true, 'correct', v_correct, 'total', v_total,
    'rp_awarded', v_rp_earned, 'results', v_results);
end; $$;

revoke execute on function public.mistake_q_public(bigint, bigint, int, int, text, jsonb) from public, anon;
revoke execute on function public.mistake_review_quiz_start(int) from public, anon;
revoke execute on function public.mistake_review_quiz_submit(bigint, jsonb) from public, anon;
grant execute on function public.mistake_review_quiz_start(int) to authenticated;
grant execute on function public.mistake_review_quiz_submit(bigint, jsonb) to authenticated;
