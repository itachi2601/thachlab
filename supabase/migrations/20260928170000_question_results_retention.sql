-- ============================================================
-- Giữ database không phình vô hạn (28/9/2026, đợt rà hạn mức Supabase Free).
--
-- Bảng phình theo học sinh là exam_question_results (~28 dòng mỗi lượt nộp) và
-- practice_question_results. Phân tích lớp, cảnh báo phụ đạo, mastery, sửa sai... đều chỉ cần
-- dữ liệu gần đây; chỉ danh hiệu chuyên môn (rank_title_stats) cộng dồn cả đời.
--
-- Cơ chế:
--   1. Bảng gộp question_result_rollups: mỗi học sinh × nguồn (đề/luyện tập) × chủ đề × dạng ×
--      loại câu × độ khó → số câu làm, số câu đúng, điểm. Vài nghìn dòng, không phình theo lượt làm.
--   2. Hàm rollup_question_results(p_before, p_dry): gộp dòng lẻ của các lượt làm cũ hơn p_before
--      (mặc định 12 tháng) vào bảng gộp rồi xoá dòng lẻ; đánh dấu exam_results/practice_sessions
--      .results_rolled_up_at để script backfill không dựng lại. Lượt nộp có câu tự luận (qtype
--      'essay') được GIỮ NGUYÊN để không mất điểm chấm tay. Cùng lúc xoá đáp án JSON tạm trong
--      exam_attempts đã nộp (bản chính đã nằm ở exam_results.detail).
--   3. rank_title_stats cộng thêm phần đã gộp → danh hiệu chuyên môn không tụt tiến độ.
--   4. Nếu pg_cron bật được: chạy tự động 3:00 sáng (giờ VN) ngày 1 hằng tháng. Không thì chạy tay:
--        select public.rollup_question_results();                 -- ghi thật
--        select public.rollup_question_results(now() - interval '12 months', true);  -- chỉ đếm thử
--
-- Mất gì sau khi gộp (chấp nhận được, chỉ với dữ liệu > 12 tháng):
--   - Bảng phân tích từng câu / ma trận chủ đề của GV cho đề cũ > 1 năm sẽ trống.
--   - Mastery "10 lượt gần nhất" và thành tích Lật Kèo chỉ nhìn dữ liệu còn lại.
--   - Danh hiệu đã trao không bị thu hồi (rank_title_awards giữ nguyên).
-- Chạy giờ nào cũng được: chỉ tạo bảng/hàm, KHÔNG tự xoá dữ liệu lúc migration.
-- ============================================================

begin;

-- ---------- 1. Bảng gộp ----------
create table if not exists public.question_result_rollups (
  id          bigint generated always as identity primary key,
  student_id  uuid not null references public.profiles(id) on delete cascade,
  source      text not null check (source in ('exam', 'practice')),
  topic_id    bigint references public.question_topics(id) on delete set null,
  topic_name  text,
  form        text,
  qtype       text,
  difficulty  text,
  attempted   integer not null default 0,
  correct     integer not null default 0,
  earned      numeric not null default 0,
  max         numeric not null default 0,
  first_at    timestamptz,
  last_at     timestamptz,
  updated_at  timestamptz not null default now(),
  unique nulls not distinct (student_id, source, topic_id, topic_name, form, qtype, difficulty)
);
create index if not exists question_result_rollups_student_idx on public.question_result_rollups (student_id);
create index if not exists question_result_rollups_topic_idx on public.question_result_rollups (topic_id);

alter table public.question_result_rollups enable row level security;
drop policy if exists "rollups: own, staff, parent read" on public.question_result_rollups;
create policy "rollups: own, staff, parent read" on public.question_result_rollups
  for select to authenticated
  using (student_id = (select auth.uid()) or public.is_staff() or public.is_parent_of(student_id));
-- Không có policy insert/update/delete cho client: chỉ hàm security definer ghi.

-- ---------- 2. Cột đánh dấu đã gộp ----------
alter table public.exam_results      add column if not exists results_rolled_up_at timestamptz;
alter table public.practice_sessions add column if not exists results_rolled_up_at timestamptz;

-- ---------- 3. Hàm gộp + xoá ----------
create or replace function public.rollup_question_results(
  p_before timestamptz default now() - interval '12 months',
  p_dry boolean default false
)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_er int; v_eqr int; v_ps int; v_pqr int; v_att int;
begin
  -- Lượt nộp đề đủ điều kiện: cũ hơn mốc, chưa gộp, không có câu tự luận.
  create temp table _er on commit drop as
    select r.id from public.exam_results r
    where r.created_at < p_before
      and r.results_rolled_up_at is null
      and not exists (
        select 1 from public.exam_question_results q
        where q.exam_result_id = r.id and q.qtype = 'essay'
      );
  create temp table _ps on commit drop as
    select s.id from public.practice_sessions s
    where s.created_at < p_before and s.results_rolled_up_at is null;

  select count(*) into v_er from _er;
  select count(*) into v_ps from _ps;
  select count(*) into v_eqr from public.exam_question_results q join _er on _er.id = q.exam_result_id;
  select count(*) into v_pqr from public.practice_question_results q join _ps on _ps.id = q.session_id;
  select count(*) into v_att from public.exam_attempts a
    where a.submitted_at is not null and (a.responses is not null or a.seconds_left is not null);

  if p_dry then
    return jsonb_build_object('dry', true, 'before', p_before,
      'exam_results', v_er, 'exam_question_results', v_eqr,
      'practice_sessions', v_ps, 'practice_question_results', v_pqr,
      'exam_attempts_to_clean', v_att);
  end if;

  -- 3a. Gộp kết quả đề
  insert into public.question_result_rollups
    (student_id, source, topic_id, topic_name, form, qtype, difficulty,
     attempted, correct, earned, max, first_at, last_at)
  select q.student_id, 'exam', q.topic_id, q.topic_name, q.form, q.qtype, q.difficulty,
         count(*), count(*) filter (where q.is_correct),
         coalesce(sum(q.earned), 0), coalesce(sum(q.max), 0), min(q.created_at), max(q.created_at)
  from public.exam_question_results q join _er on _er.id = q.exam_result_id
  group by q.student_id, q.topic_id, q.topic_name, q.form, q.qtype, q.difficulty
  on conflict (student_id, source, topic_id, topic_name, form, qtype, difficulty) do update set
    attempted = question_result_rollups.attempted + excluded.attempted,
    correct   = question_result_rollups.correct   + excluded.correct,
    earned    = question_result_rollups.earned    + excluded.earned,
    max       = question_result_rollups.max       + excluded.max,
    first_at  = least(question_result_rollups.first_at, excluded.first_at),
    last_at   = greatest(question_result_rollups.last_at, excluded.last_at),
    updated_at = now();

  delete from public.exam_question_results q using _er where _er.id = q.exam_result_id;
  update public.exam_results r set results_rolled_up_at = now() from _er where _er.id = r.id;

  -- 3b. Gộp kết quả luyện tập
  insert into public.question_result_rollups
    (student_id, source, topic_id, topic_name, form, qtype, difficulty,
     attempted, correct, earned, max, first_at, last_at)
  select q.student_id, 'practice', q.topic_id, q.topic_name, q.form, q.qtype, q.difficulty,
         count(*), count(*) filter (where q.is_correct),
         coalesce(sum(q.earned), 0), coalesce(sum(q.max), 0), min(q.created_at), max(q.created_at)
  from public.practice_question_results q join _ps on _ps.id = q.session_id
  group by q.student_id, q.topic_id, q.topic_name, q.form, q.qtype, q.difficulty
  on conflict (student_id, source, topic_id, topic_name, form, qtype, difficulty) do update set
    attempted = question_result_rollups.attempted + excluded.attempted,
    correct   = question_result_rollups.correct   + excluded.correct,
    earned    = question_result_rollups.earned    + excluded.earned,
    max       = question_result_rollups.max       + excluded.max,
    first_at  = least(question_result_rollups.first_at, excluded.first_at),
    last_at   = greatest(question_result_rollups.last_at, excluded.last_at),
    updated_at = now();

  delete from public.practice_question_results q using _ps where _ps.id = q.session_id;
  update public.practice_sessions s set results_rolled_up_at = now() from _ps where _ps.id = s.id;

  -- 3c. Dọn đáp án JSON tạm của lượt làm đã nộp (bản chính ở exam_results.detail)
  update public.exam_attempts set responses = null, seconds_left = null
  where submitted_at is not null and (responses is not null or seconds_left is not null);

  return jsonb_build_object('dry', false, 'before', p_before,
    'exam_results', v_er, 'exam_question_results', v_eqr,
    'practice_sessions', v_ps, 'practice_question_results', v_pqr,
    'exam_attempts_cleaned', v_att);
end;
$$;
revoke all on function public.rollup_question_results(timestamptz, boolean) from public, anon, authenticated;
grant execute on function public.rollup_question_results(timestamptz, boolean) to service_role, postgres;

-- ---------- 4. rank_title_stats: cộng thêm phần đã gộp ----------
-- Cùng chữ ký với bản 20260928100000 → create or replace được.
create or replace function public.rank_title_stats(p_student uuid, p_title text)
returns table(n int, correct int, covered int, total_topics int, acc int, de_correct int, tb_correct int, kho_correct int)
language sql stable set search_path = public
as $$
  with topics as (
    select tt.topic_id from public.rank_title_topics tt where tt.title_code = p_title
  ),
  rows_ as (
    select coalesce(t.parent_id, t.id) as lesson_topic, eqr.is_correct, eqr.difficulty
    from public.exam_question_results eqr
    join public.question_topics t on t.id = eqr.topic_id
    where eqr.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
    union all
    select coalesce(t.parent_id, t.id) as lesson_topic, pqr.is_correct, pqr.difficulty
    from public.practice_question_results pqr
    join public.question_topics t on t.id = pqr.topic_id
    where pqr.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
  ),
  agg as (
    select lesson_topic,
      count(*)::int as n,
      (count(*) filter (where is_correct))::int as c,
      (count(*) filter (where is_correct and difficulty = 'de'))::int as de,
      (count(*) filter (where is_correct and difficulty = 'trung-binh'))::int as tb,
      (count(*) filter (where is_correct and difficulty = 'kho'))::int as kho
    from rows_ group by lesson_topic
    union all
    select coalesce(t.parent_id, t.id),
      sum(r.attempted)::int,
      sum(r.correct)::int,
      coalesce(sum(r.correct) filter (where r.difficulty = 'de'), 0)::int,
      coalesce(sum(r.correct) filter (where r.difficulty = 'trung-binh'), 0)::int,
      coalesce(sum(r.correct) filter (where r.difficulty = 'kho'), 0)::int
    from public.question_result_rollups r
    join public.question_topics t on t.id = r.topic_id
    where r.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
    group by coalesce(t.parent_id, t.id)
  ),
  per_topic as (
    select lesson_topic, sum(n) as c from agg group by lesson_topic
  ),
  tot as (
    select coalesce(sum(n), 0)::int as n, coalesce(sum(c), 0)::int as c,
           coalesce(sum(de), 0)::int as de, coalesce(sum(tb), 0)::int as tb, coalesce(sum(kho), 0)::int as kho
    from agg
  )
  select
    tot.n,
    tot.c,
    (select count(*) from per_topic where c >= 3)::int,
    (select count(*) from topics)::int,
    case when tot.n > 0 then round(tot.c * 100.0 / tot.n)::int else 0 end,
    tot.de, tot.tb, tot.kho
  from tot;
$$;

-- ---------- 5. Dọn ngay đáp án JSON tạm của các lượt đã nộp (nhỏ, an toàn) ----------
update public.exam_attempts set responses = null, seconds_left = null
where submitted_at is not null and (responses is not null or seconds_left is not null);

-- ---------- 6. Lịch tự động (nếu pg_cron bật được) ----------
do $$
begin
  begin
    create extension if not exists pg_cron;
  exception when others then
    raise notice 'pg_cron không bật được (%): chạy tay select public.rollup_question_results(); mỗi học kì', sqlerrm;
  end;
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'question-results-rollup';
    -- 20:00 UTC ngày 1 hằng tháng = 3:00 sáng giờ VN
    perform cron.schedule('question-results-rollup', '0 20 1 * *', 'select public.rollup_question_results();');
    raise notice 'Đã đặt lịch pg_cron question-results-rollup (3:00 VN ngày 1 hằng tháng)';
  end if;
end $$;

commit;

-- ---------- ROLLBACK ----------
-- perf/rollback/20260928170000_question_results_retention.down.sql
-- Xoá lịch, hàm, bảng gộp, cột đánh dấu và trả rank_title_stats về bản 20260928100000.
-- Dòng lẻ đã bị hàm rollup xoá KHÔNG khôi phục được (chỉ còn trong bảng gộp).
