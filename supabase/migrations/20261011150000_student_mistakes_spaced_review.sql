-- ============================================================================
-- Sổ tay câu sai & Ôn cách quãng (Spaced Mistake Review)
--
-- 1. Bảng student_mistakes: tự động gom các câu học sinh làm sai ở bài kiểm tra
--    (exam_question_results) và bài luyện tập (practice_question_results).
-- 2. Chu kỳ ôn cách quãng:
--    * Mới sai: stage 0, next_review_at = now() + 2 ngày.
--    * Ôn đúng lần 1: stage 1, next_review_at = now() + 4 ngày (+2 RP).
--    * Ôn đúng lần 2: stage 2, cleared = true (xoá bẫy thành công, +2 RP).
--    * Ôn sai: reset về stage 0, tăng mistake_count, next_review_at = now() + 2 ngày.
-- 3. Giới hạn RP thưởng: tối đa mistake_review_day_cap (mặc định 10 RP/ngày)
--    ghi vào sổ cái rank qua nguồn 'fix' (source_ref = 'mistake_review:<attempt_id>').
-- ============================================================================

-- ---------- 1. Bảng lưu câu sai ----------
create table if not exists public.student_mistakes (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.profiles (id) on delete cascade,
  exam_id bigint not null references public.exams (id) on delete cascade,
  question_index int not null,
  topic_id bigint references public.question_topics (id) on delete set null,
  form text not null default '',
  difficulty text not null default '',
  mistake_count int not null default 1,
  consecutive_correct int not null default 0,
  stage int not null default 0,
  cleared boolean not null default false,
  last_wrong_at timestamptz not null default now(),
  last_reviewed_at timestamptz,
  next_review_at timestamptz not null default (now() + interval '2 days'),
  created_at timestamptz not null default now(),
  constraint student_mistakes_unique unique (student_id, exam_id, question_index)
);

create index if not exists student_mistakes_student_due_idx
  on public.student_mistakes (student_id, cleared, next_review_at);
create index if not exists student_mistakes_topic_idx
  on public.student_mistakes (topic_id);

alter table public.student_mistakes enable row level security;
revoke all on public.student_mistakes from anon, authenticated;
drop policy if exists "read own student_mistakes" on public.student_mistakes;
create policy "read own student_mistakes" on public.student_mistakes
  for select to authenticated
  using (student_id = (select auth.uid()) or public.rank_is_staff() or public.teaches_student(student_id));

-- ---------- 2. Bảng lượt ôn câu sai ----------
create table if not exists public.student_mistake_review_attempts (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.profiles (id) on delete cascade,
  season_id bigint references public.rank_seasons (id) on delete set null,
  mistake_ids bigint[] not null default '{}',
  answers jsonb not null default '[]'::jsonb,
  correct_count int not null default 0,
  total int not null default 0,
  rp_awarded int not null default 0,
  status text not null default 'open' check (status in ('open', 'done')),
  created_at timestamptz not null default now(),
  submitted_at timestamptz
);

create index if not exists student_mistake_review_attempts_student_idx
  on public.student_mistake_review_attempts (student_id, created_at desc);

alter table public.student_mistake_review_attempts enable row level security;
revoke all on public.student_mistake_review_attempts from anon, authenticated;
drop policy if exists "read own student_mistake_review_attempts" on public.student_mistake_review_attempts;
create policy "read own student_mistake_review_attempts" on public.student_mistake_review_attempts
  for select to authenticated
  using (student_id = (select auth.uid()) or public.rank_is_staff() or public.teaches_student(student_id));

-- ---------- 3. Triggers tự động gom câu sai ----------
create or replace function public.trg_ingest_exam_question_mistake()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if not new.is_correct and coalesce(new.qtype, '') <> 'essay' and new.exam_id is not null then
    insert into public.student_mistakes (
      student_id, exam_id, question_index, topic_id, form, difficulty,
      mistake_count, consecutive_correct, stage, cleared, last_wrong_at, next_review_at
    )
    values (
      new.student_id, new.exam_id, new.question_index, new.topic_id,
      coalesce(new.form, ''), coalesce(new.difficulty, ''),
      1, 0, 0, false, coalesce(new.created_at, now()),
      coalesce(new.created_at, now()) + interval '2 days'
    )
    on conflict (student_id, exam_id, question_index) do update
      set mistake_count = public.student_mistakes.mistake_count + 1,
          consecutive_correct = 0,
          stage = 0,
          cleared = false,
          last_wrong_at = excluded.last_wrong_at,
          next_review_at = excluded.next_review_at;
  end if;
  return new;
exception when others then
  return new;
end; $$;

drop trigger if exists trg_exam_question_results_mistake on public.exam_question_results;
create trigger trg_exam_question_results_mistake
  after insert on public.exam_question_results
  for each row execute function public.trg_ingest_exam_question_mistake();

create or replace function public.trg_ingest_practice_question_mistake()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  v_idx int;
begin
  if not new.is_correct and coalesce(new.qtype, '') <> 'essay' and new.exam_id is not null then
    v_idx := coalesce(new.source_index, new.question_index);
    insert into public.student_mistakes (
      student_id, exam_id, question_index, topic_id, form, difficulty,
      mistake_count, consecutive_correct, stage, cleared, last_wrong_at, next_review_at
    )
    values (
      new.student_id, new.exam_id, v_idx, new.topic_id,
      coalesce(new.form, ''), coalesce(new.difficulty, ''),
      1, 0, 0, false, coalesce(new.created_at, now()),
      coalesce(new.created_at, now()) + interval '2 days'
    )
    on conflict (student_id, exam_id, question_index) do update
      set mistake_count = public.student_mistakes.mistake_count + 1,
          consecutive_correct = 0,
          stage = 0,
          cleared = false,
          last_wrong_at = excluded.last_wrong_at,
          next_review_at = excluded.next_review_at;
  end if;
  return new;
exception when others then
  return new;
end; $$;

drop trigger if exists trg_practice_question_results_mistake on public.practice_question_results;
create trigger trg_practice_question_results_mistake
  after insert on public.practice_question_results
  for each row execute function public.trg_ingest_practice_question_mistake();

-- ---------- 4. RPC thống kê Sổ tay câu sai ----------
create or replace function public.mistake_stats_of(p_student uuid default auth.uid())
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_total int;
  v_due int;
  v_cleared int;
  v_topics jsonb;
begin
  if p_student is null then return null; end if;
  if not (p_student = auth.uid() or public.rank_is_staff() or public.teaches_student(p_student)) then
    return null;
  end if;

  select count(*) filter (where not cleared),
         count(*) filter (where not cleared and next_review_at <= now()),
         count(*) filter (where cleared)
  into v_total, v_due, v_cleared
  from public.student_mistakes
  where student_id = p_student;

  select coalesce(jsonb_agg(jsonb_build_object(
    'topic_id', x.tid, 'name', x.name, 'count', x.cnt
  ) order by x.cnt desc), '[]'::jsonb)
  into v_topics
  from (
    select coalesce(t.parent_id, t.id) as tid, coalesce(max(pt.name), max(t.name)) as name, count(*) as cnt
    from public.student_mistakes sm
    join public.question_topics t on t.id = sm.topic_id
    left join public.question_topics pt on pt.id = t.parent_id
    where sm.student_id = p_student and not sm.cleared
    group by coalesce(t.parent_id, t.id)
    order by cnt desc
    limit 3
  ) x;

  return jsonb_build_object(
    'total_active', coalesce(v_total, 0),
    'due_count', coalesce(v_due, 0),
    'cleared_count', coalesce(v_cleared, 0),
    'weak_topics', coalesce(v_topics, '[]'::jsonb)
  );
end; $$;

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

revoke execute on function public.mistake_stats_of(uuid) from public, anon;
revoke execute on function public.mistake_review_quiz_start(int) from public, anon;
revoke execute on function public.mistake_review_quiz_submit(bigint, jsonb) from public, anon;
grant execute on function public.mistake_stats_of(uuid) to authenticated;
grant execute on function public.mistake_review_quiz_start(int) to authenticated;
grant execute on function public.mistake_review_quiz_submit(bigint, jsonb) to authenticated;
