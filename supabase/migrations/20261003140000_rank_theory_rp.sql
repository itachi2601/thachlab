-- ============================================================================
-- RP cho bài LÝ THUYẾT tương tác (chỉ cộng RP, không đụng danh hiệu/YCCĐ).
--
-- Nguyên tắc: RP thưởng việc HIỂU bài (câu tự chấm), không thưởng việc MỞ bài. Chấm ở máy chủ.
--   * Bảng theory_quiz_keys: đáp án + mức ⭐ + thời gian đọc ước tính của từng bài lý thuyết (chỉ GV đọc được).
--     Bài chưa có dòng khoá (hoặc enabled = false) thì KHÔNG cộng RP — đăng khoá cùng lúc đăng bài.
--   * Bảng theory_sessions: mỗi (HS, bài) đúng MỘT dòng — lượt mở đầu + lượt nộp ĐẦU. Nộp lại = không cộng.
--   * rpc rank_theory_open(item)  : ghi giờ mở bài (lần đầu).
--   * rpc rank_theory_submit(item, answers jsonb): answers = {"q1":"B", ...} — đáp án LẦN ĐẦU từng câu.
--     Trả jsonb {ok, reason, awarded, correct, total, pct}.
--
-- Quy tắc cộng (mặc định, đổi bằng rank_seasons.config, đọc qua rank_cfg):
--   theory_rp 8            RP hoàn thành bài
--   theory_pass_pct 70     đúng >= 70% ở lượt đầu mới được cộng
--   theory_min_time_pct 40 thời gian từ lúc mở tới lúc nộp >= 40% thời gian đọc ước tính
--   theory_min_sec_per_q 4 và >= 4 giây/câu (chặn bấm mò)
--   theory_bonus2 2 / theory_bonus3 4   thưởng mỗi câu thử thách ⭐⭐ / ⭐⭐⭐ đúng lượt đầu
--   theory_day_cap 24 · theory_week_cap 60   trần RP lý thuyết mỗi ngày / tuần (giờ VN, tuần Thứ Hai–CN)
--   theory_season_cap_pct 25   tổng RP lý thuyết cả mùa <= 25% min_rp bậc cao nhất của mùa
-- Mỗi bài chỉ cộng 1 lần/mùa (khoá rank_rp_awards: season, student, 'theory', 'theory:<item>').
-- Loại GV/admin (rank_is_student). Không có mùa active cho HS => ghi nhận nhưng không cộng.
-- Cách chạy: bash scripts/run-migrations.sh — chạy lúc nào cũng được (chỉ thêm bảng/hàm mới + nới check constraint).
-- Rollback: perf/rollback/20261003140000_rank_theory_rp.down.sql
-- ============================================================================

alter table public.rank_rp_awards drop constraint if exists rank_rp_awards_source_kind_check;
alter table public.rank_rp_awards add constraint rank_rp_awards_source_kind_check
  check (source_kind in ('practice', 'fix', 'weekly_goal', 'daily_streak', 'manual', 'homework_check', 'progress_week', 'class_goal', 'theory'));

create table if not exists public.theory_quiz_keys (
  item_id bigint primary key references public.lesson_items (id) on delete cascade,
  enabled boolean not null default true,
  answers jsonb not null,                       -- {"q1":"B","q2":"C"} đáp án đúng
  challenge jsonb not null default '{}'::jsonb, -- {"q7":2,"q8":3} mức ⭐ của câu thử thách (không có = câu thường)
  est_read_seconds integer not null check (est_read_seconds > 0),
  updated_at timestamptz not null default now()
);
alter table public.theory_quiz_keys enable row level security;
drop policy if exists "staff manage theory keys" on public.theory_quiz_keys;
create policy "staff manage theory keys" on public.theory_quiz_keys
  for all using (public.rank_is_staff()) with check (public.rank_is_staff());

create table if not exists public.theory_sessions (
  student_id uuid not null references public.profiles (id) on delete cascade,
  item_id bigint not null references public.lesson_items (id) on delete cascade,
  opened_at timestamptz not null default now(),
  submitted_at timestamptz,
  correct integer,
  total integer,
  awarded integer,
  result text,
  primary key (student_id, item_id)
);
alter table public.theory_sessions enable row level security;
drop policy if exists "student reads own theory sessions" on public.theory_sessions;
create policy "student reads own theory sessions" on public.theory_sessions
  for select using (student_id = auth.uid() or public.rank_is_staff());

create or replace function public.rank_theory_open(p_item bigint)
returns void
language plpgsql security definer set search_path = public
as $$
begin
  if auth.uid() is null or not public.rank_is_student(auth.uid()) then return; end if;
  if not exists (select 1 from public.theory_quiz_keys where item_id = p_item and enabled) then return; end if;
  insert into public.theory_sessions (student_id, item_id) values (auth.uid(), p_item)
  on conflict (student_id, item_id) do nothing;
end; $$;

create or replace function public.rank_theory_submit(p_item bigint, p_answers jsonb)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_key public.theory_quiz_keys%rowtype;
  v_ses public.theory_sessions%rowtype;
  v_season bigint;
  v_total int; v_correct int := 0; v_bonus int := 0; v_pct int;
  v_elapsed numeric; v_need numeric;
  v_value int; v_day_used int; v_week_used int; v_season_used int; v_season_max int;
  v_room int; v_award int := 0; v_reason text := 'ok'; v_title text; v_ref text;
  k text; v_lvl int;
begin
  if v_uid is null or not public.rank_is_student(v_uid) then
    return jsonb_build_object('ok', false, 'reason', 'not_student');
  end if;
  select * into v_key from public.theory_quiz_keys where item_id = p_item and enabled;
  if not found then return jsonb_build_object('ok', false, 'reason', 'no_key'); end if;

  -- khoá theo (HS, bài) để hai lần nộp đồng thời không cùng thấy "chưa nộp"
  perform pg_advisory_xact_lock(hashtextextended('theory:' || v_uid || ':' || p_item, 0));
  insert into public.theory_sessions (student_id, item_id) values (v_uid, p_item)
  on conflict (student_id, item_id) do nothing;
  select * into v_ses from public.theory_sessions where student_id = v_uid and item_id = p_item;
  if v_ses.submitted_at is not null then
    return jsonb_build_object('ok', true, 'reason', 'already', 'awarded', 0,
      'correct', v_ses.correct, 'total', v_ses.total,
      'pct', case when v_ses.total > 0 then round(100.0 * v_ses.correct / v_ses.total) else 0 end);
  end if;

  select count(*) into v_total from jsonb_object_keys(v_key.answers);
  for k in select jsonb_object_keys(v_key.answers) loop
    if (p_answers ->> k) is not distinct from (v_key.answers ->> k) then
      v_correct := v_correct + 1;
    end if;
  end loop;
  v_pct := case when v_total > 0 then round(100.0 * v_correct / v_total) else 0 end;
  v_elapsed := extract(epoch from (now() - v_ses.opened_at));

  v_season := public.rank_season_for_at(v_uid, now());
  if v_season is null then
    v_reason := 'no_season';
  else
    -- thưởng câu thử thách theo config của mùa
    for k in select jsonb_object_keys(v_key.answers) loop
      if (p_answers ->> k) is not distinct from (v_key.answers ->> k) then
        v_lvl := coalesce((v_key.challenge ->> k)::int, 1);
        if v_lvl = 2 then v_bonus := v_bonus + public.rank_cfg(v_season, 'theory_bonus2', 2)::int; end if;
        if v_lvl = 3 then v_bonus := v_bonus + public.rank_cfg(v_season, 'theory_bonus3', 4)::int; end if;
      end if;
    end loop;

    v_need := greatest(v_key.est_read_seconds * public.rank_cfg(v_season, 'theory_min_time_pct', 40) / 100.0,
                       v_total * public.rank_cfg(v_season, 'theory_min_sec_per_q', 4));
    if v_pct < public.rank_cfg(v_season, 'theory_pass_pct', 70) then
      v_reason := 'below_pass';
    elsif v_elapsed < v_need then
      v_reason := 'too_fast';
    else
      v_value := public.rank_cfg(v_season, 'theory_rp', 8)::int + v_bonus;
      v_ref := 'theory:' || p_item;
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
        v_award := public.rank_award(v_season, v_uid, 'theory', v_ref, v_value,
          'Bài lý thuyết: ' || coalesce(v_title, '#' || p_item) || ' (' || v_correct || '/' || v_total || ' câu đúng)', null);
        perform public.rank_eval_gates(v_season, v_uid);
        perform public.rank_refresh_student(v_season, v_uid);
      end if;
    end if;
  end if;

  update public.theory_sessions
    set submitted_at = now(), correct = v_correct, total = v_total, awarded = v_award, result = v_reason
    where student_id = v_uid and item_id = p_item;

  return jsonb_build_object('ok', true, 'reason', v_reason, 'awarded', v_award,
    'correct', v_correct, 'total', v_total, 'pct', v_pct);
end; $$;

revoke all on function public.rank_theory_open(bigint) from public;
revoke all on function public.rank_theory_submit(bigint, jsonb) from public;
grant execute on function public.rank_theory_open(bigint) to authenticated;
grant execute on function public.rank_theory_submit(bigint, jsonb) to authenticated;
