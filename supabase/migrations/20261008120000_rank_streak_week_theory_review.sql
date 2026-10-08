-- ============================================================================
-- 8/10/2026 — (1) Dải chuỗi 7 ngày  (2) RP "XEM LẠI" bài lý thuyết (ôn cách quãng)
--
-- (1) rank_my_streak_days(p_days): trả {days:[{d:'YYYY-MM-DD', state:'done'|'frozen'|'none'}]}, cũ → mới, cuối là
--     "hôm nay" theo mốc reset của chuỗi. done = có dòng rank_rp_awards 'daily_streak' awarded > 0; frozen = ngày trống
--     được đóng băng (rank_daily_streak_calc). Không có mùa active → null. Chỉ đọc, không cộng gì.
--
-- (2) Quy tắc cộng RP khi em quay lại học lại một bài lý thuyết đã hoàn thành (bổ sung rank_theory_submit 3/10/2026,
--     vốn chỉ tính lượt ĐẦU). Nguyên tắc: thưởng việc ÔN CÁCH QUÃNG và HIỂU lại, không thưởng việc mở bài.
--       * Điều kiện: lượt đầu của bài đã nộp và đạt (theory_sessions.result = 'ok').
--       * Phải cách lượt trước (lượt đầu hoặc lần ôn trước) >= theory_review_gap_days (mặc định 3) ngày.
--       * Mở bài ôn bằng rank_theory_review_open(item) → làm lại bộ câu tự chấm → rank_theory_review_submit(item, answers).
--         Đáp án LẦN ĐẦU của lượt ôn mới tính; đúng >= theory_review_pass_pct (70)%; thời gian >= theory_review_min_time_pct (20)%
--         thời gian đọc ước tính và >= theory_min_sec_per_q giây/câu (chặn bấm mò).
--       * RP: theory_review_rp (mặc định 3, nhỏ hơn 8 của lượt đầu để không có lợi khi "cày" lại bài dễ).
--       * Tối đa theory_review_max_rounds (2) lần ôn có RP cho mỗi bài trong mùa.
--       * Dùng chung trần của RP lý thuyết (theory_day_cap 24 / theory_week_cap 60 / theory_season_cap_pct 25%)
--         vì ghi cùng nguồn 'theory' (khoá rank_rp_awards: season, student, 'theory', 'theory_review:<item>:<lần>').
--       * Ôn không đạt hoặc quá nhanh vẫn ghi nhận, tính là một lần (đặt lại khoảng cách), không cộng RP.
--     Cấu hình mới đọc qua rank_cfg (rank_seasons.config), sửa ở /quan-tri/xep-hang, không cần deploy.
--     CHƯA có giao diện gọi 2 RPC này (và RPC lượt đầu cũng chưa có giao diện / dòng khoá) — xem docs/STATE.md.
--
-- Không đổi hàm cũ, không đổi check constraint (dùng source_kind 'theory' đã có). Chạy giờ nào cũng được.
-- Rollback: perf/rollback/20261008120000_rank_streak_week_theory_review.down.sql
-- ============================================================================

create or replace function public.rank_my_streak_days(p_days int default 7)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_season bigint;
  v_today date;
  v_n int := least(greatest(coalesce(p_days, 7), 1), 31);
  v_frozen date[] := '{}';
  v_days jsonb;
begin
  if v_uid is null then return null; end if;
  v_season := public.rank_season_for_at(v_uid, now());
  if v_season is null then return null; end if;
  v_today := public.rank_streak_day(v_season, now());
  select c.frozen into v_frozen from public.rank_daily_streak_calc(v_season, v_uid, now()) c;

  select jsonb_agg(
           jsonb_build_object(
             'd', g.d::text,
             'state', case
               when exists (
                 select 1 from public.rank_rp_awards a
                 where a.season_id = v_season and a.student_id = v_uid and a.source_kind = 'daily_streak'
                   and a.source_ref = g.d::text and a.awarded > 0
               ) then 'done'
               when g.d = any (coalesce(v_frozen, '{}')) then 'frozen'
               else 'none' end)
           order by g.d)
    into v_days
    from (select (v_today - s)::date as d from generate_series(0, v_n - 1) s) g;

  return jsonb_build_object('days', coalesce(v_days, '[]'::jsonb));
end; $$;
revoke all on function public.rank_my_streak_days(int) from public, anon;
grant execute on function public.rank_my_streak_days(int) to authenticated;

-- ---------------------------------------------------------------------------
-- RP xem lại bài lý thuyết
-- ---------------------------------------------------------------------------
create table if not exists public.theory_reviews (
  student_id uuid not null references public.profiles (id) on delete cascade,
  item_id bigint not null references public.lesson_items (id) on delete cascade,
  round int not null check (round >= 1),
  opened_at timestamptz not null default now(),
  submitted_at timestamptz,
  correct integer,
  total integer,
  awarded integer,
  result text,
  primary key (student_id, item_id, round)
);
alter table public.theory_reviews enable row level security;
revoke all on public.theory_reviews from anon, authenticated;
grant select on public.theory_reviews to authenticated;
drop policy if exists "student reads own theory reviews" on public.theory_reviews;
create policy "student reads own theory reviews" on public.theory_reviews
  for select using (student_id = auth.uid() or public.rank_is_staff());

-- Mở lượt ôn. Trả {ok, reason, round, available_at}. reason: ok | not_student | no_key | no_season | no_first_pass | too_soon | max_rounds
create or replace function public.rank_theory_review_open(p_item bigint)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_season bigint;
  v_ses public.theory_sessions%rowtype;
  v_last timestamptz;
  v_avail timestamptz;
  v_round int;
  v_done int;
begin
  if v_uid is null or not public.rank_is_student(v_uid) then
    return jsonb_build_object('ok', false, 'reason', 'not_student');
  end if;
  if not exists (select 1 from public.theory_quiz_keys where item_id = p_item and enabled) then
    return jsonb_build_object('ok', false, 'reason', 'no_key');
  end if;
  v_season := public.rank_season_for_at(v_uid, now());
  if v_season is null then return jsonb_build_object('ok', false, 'reason', 'no_season'); end if;

  perform pg_advisory_xact_lock(hashtextextended('theory_review:' || v_uid || ':' || p_item, 0));
  select * into v_ses from public.theory_sessions where student_id = v_uid and item_id = p_item;
  if not found or v_ses.submitted_at is null or v_ses.result is distinct from 'ok' then
    return jsonb_build_object('ok', false, 'reason', 'no_first_pass');
  end if;

  select count(*) into v_done from public.rank_rp_awards
    where season_id = v_season and student_id = v_uid and source_kind = 'theory'
      and source_ref like 'theory\_review:' || p_item || ':%' and awarded > 0;
  if v_done >= public.rank_cfg(v_season, 'theory_review_max_rounds', 2) then
    return jsonb_build_object('ok', false, 'reason', 'max_rounds', 'round', v_done);
  end if;

  select max(submitted_at) into v_last from public.theory_reviews
    where student_id = v_uid and item_id = p_item and submitted_at is not null;
  v_last := greatest(v_ses.submitted_at, coalesce(v_last, v_ses.submitted_at));
  v_avail := v_last + make_interval(days => public.rank_cfg(v_season, 'theory_review_gap_days', 3)::int);
  if now() < v_avail then
    return jsonb_build_object('ok', false, 'reason', 'too_soon', 'available_at', v_avail);
  end if;

  -- lượt đang mở dở thì dùng lại, không thì mở lượt mới
  select round into v_round from public.theory_reviews
    where student_id = v_uid and item_id = p_item and submitted_at is null order by round desc limit 1;
  if v_round is null then
    select coalesce(max(round), 0) + 1 into v_round from public.theory_reviews where student_id = v_uid and item_id = p_item;
    insert into public.theory_reviews (student_id, item_id, round) values (v_uid, p_item, v_round);
  end if;
  return jsonb_build_object('ok', true, 'reason', 'ok', 'round', v_round);
end; $$;

-- Nộp lượt ôn. Trả {ok, reason, awarded, correct, total, pct}. reason: ok | not_opened | below_pass | too_fast | capped | ...
create or replace function public.rank_theory_review_submit(p_item bigint, p_answers jsonb)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_key public.theory_quiz_keys%rowtype;
  v_rev public.theory_reviews%rowtype;
  v_season bigint;
  v_total int; v_correct int := 0; v_pct int;
  v_elapsed numeric; v_need numeric;
  v_value int; v_day_used int; v_week_used int; v_season_used int; v_season_max int; v_room int;
  v_award int := 0; v_reason text := 'ok'; v_title text;
  k text;
begin
  if v_uid is null or not public.rank_is_student(v_uid) then
    return jsonb_build_object('ok', false, 'reason', 'not_student');
  end if;
  select * into v_key from public.theory_quiz_keys where item_id = p_item and enabled;
  if not found then return jsonb_build_object('ok', false, 'reason', 'no_key'); end if;

  perform pg_advisory_xact_lock(hashtextextended('theory_review:' || v_uid || ':' || p_item, 0));
  select * into v_rev from public.theory_reviews
    where student_id = v_uid and item_id = p_item and submitted_at is null order by round desc limit 1;
  if not found then return jsonb_build_object('ok', false, 'reason', 'not_opened'); end if;

  select count(*) into v_total from jsonb_object_keys(v_key.answers);
  for k in select jsonb_object_keys(v_key.answers) loop
    if (p_answers ->> k) is not distinct from (v_key.answers ->> k) then v_correct := v_correct + 1; end if;
  end loop;
  v_pct := case when v_total > 0 then round(100.0 * v_correct / v_total) else 0 end;
  v_elapsed := extract(epoch from (now() - v_rev.opened_at));

  v_season := public.rank_season_for_at(v_uid, now());
  if v_season is null then
    v_reason := 'no_season';
  else
    v_need := greatest(v_key.est_read_seconds * public.rank_cfg(v_season, 'theory_review_min_time_pct', 20) / 100.0,
                       v_total * public.rank_cfg(v_season, 'theory_min_sec_per_q', 4));
    if v_pct < public.rank_cfg(v_season, 'theory_review_pass_pct', 70) then
      v_reason := 'below_pass';
    elsif v_elapsed < v_need then
      v_reason := 'too_fast';
    else
      v_value := public.rank_cfg(v_season, 'theory_review_rp', 3)::int;
      select coalesce(sum(amount), 0) into v_day_used from public.rank_rp_ledger
        where season_id = v_season and student_id = v_uid and source_kind = 'theory'
          and public.rank_vn_date(created_at) = public.rank_vn_date(now());
      select coalesce(sum(amount), 0) into v_week_used from public.rank_rp_ledger
        where season_id = v_season and student_id = v_uid and source_kind = 'theory'
          and public.rank_week_start(created_at) = public.rank_week_start(now());
      select coalesce(sum(amount), 0) into v_season_used from public.rank_rp_ledger
        where season_id = v_season and student_id = v_uid and source_kind = 'theory';
      select coalesce(max(min_rp), 0) * public.rank_cfg(v_season, 'theory_season_cap_pct', 25) / 100.0
        into v_season_max from public.rank_tiers where season_id = v_season;
      v_room := least(public.rank_cfg(v_season, 'theory_day_cap', 24) - v_day_used,
                      public.rank_cfg(v_season, 'theory_week_cap', 60) - v_week_used,
                      floor(v_season_max) - v_season_used);
      v_value := greatest(0, least(v_value, v_room));
      if v_value <= 0 then
        v_reason := 'capped';
      else
        select title into v_title from public.lesson_items where id = p_item;
        perform public.rank_ensure_member(v_season, v_uid);
        v_award := public.rank_award(v_season, v_uid, 'theory', 'theory_review:' || p_item || ':' || v_rev.round, v_value,
          'Ôn lại bài lý thuyết: ' || coalesce(v_title, '#' || p_item) || ' (' || v_correct || '/' || v_total || ' câu đúng)', null);
        perform public.rank_eval_gates(v_season, v_uid);
        perform public.rank_refresh_student(v_season, v_uid);
      end if;
    end if;
  end if;

  update public.theory_reviews
    set submitted_at = now(), correct = v_correct, total = v_total, awarded = v_award, result = v_reason
    where student_id = v_uid and item_id = p_item and round = v_rev.round;

  return jsonb_build_object('ok', true, 'reason', v_reason, 'awarded', v_award,
    'correct', v_correct, 'total', v_total, 'pct', v_pct);
end; $$;

revoke all on function public.rank_theory_review_open(bigint) from public, anon;
revoke all on function public.rank_theory_review_submit(bigint, jsonb) from public, anon;
grant execute on function public.rank_theory_review_open(bigint) to authenticated;
grant execute on function public.rank_theory_review_submit(bigint, jsonb) to authenticated;
