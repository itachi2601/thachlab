-- Rollback 20261003100000_rank_gate_adaptive.sql
-- Trả lại 3 hàm về bản trước (rank_tier_needs_gate IMMUTABLE, rank_eval_gates, rank_status_of = 20260930130000),
-- rồi xoá hàm/bảng/cột mới. Mất toàn bộ lịch sử rank_gate_attempts. rank_gate_passes đã ghi giữ nguyên.
-- Nếu có HS đã đỗ bài thi thích ứng và lên bậc nhờ nó, sau rollback họ vẫn giữ rank_gate_passes (không bị tụt bậc).
begin;

CREATE OR REPLACE FUNCTION public.rank_tier_needs_gate(t rank_tiers)
 RETURNS boolean
 LANGUAGE sql
 IMMUTABLE
AS $$
  select t.required_title_count > 0 or t.challenge_exam_id is not null or t.code in ('cao_thu', 'thach_dau');
$$;

CREATE OR REPLACE FUNCTION public.rank_eval_gates(p_season bigint, p_student uuid)
 RETURNS void
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $$
declare
  t public.rank_tiers%rowtype;
  s public.rank_seasons%rowtype;
  v_titles int;
  v_pct int;
  v_titles_ok boolean;
  v_chal_ok boolean;
begin
  select * into s from public.rank_seasons where id = p_season;
  for t in select * from public.rank_tiers where season_id = p_season order by sort loop
    if not public.rank_tier_needs_gate(t) then continue; end if;
    if exists (select 1 from public.rank_gate_passes g where g.season_id = p_season and g.student_id = p_student and g.tier_code = t.code) then
      continue;
    end if;

    v_titles := public.rank_titles_at_level(p_student, coalesce(t.required_title_level, 'thuc_tinh'));
    v_titles_ok := v_titles >= t.required_title_count;

    if t.challenge_exam_id is null then
      -- Cao Thủ / Thách Đấu bắt buộc có thử thách; chưa gán -> chưa thể vượt.
      v_chal_ok := t.code not in ('cao_thu', 'thach_dau');
      v_pct := null;
    else
      v_pct := public.rank_best_pct(p_student, t.challenge_exam_id,
        (s.starts_on::timestamp) at time zone 'Asia/Ho_Chi_Minh',
        ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh');
      v_chal_ok := v_pct is not null and v_pct >= round(coalesce(t.challenge_pass_score, 8) * 10);
    end if;

    if v_titles_ok and v_chal_ok then
      insert into public.rank_gate_passes (season_id, student_id, tier_code, evidence)
      values (p_season, p_student, t.code, jsonb_build_object('titles', v_titles, 'challenge_pct', v_pct))
      on conflict do nothing;
    end if;
  end loop;
end; $$;

CREATE OR REPLACE FUNCTION public.rank_status_of(p_student uuid)
 RETURNS jsonb
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $$
declare
  v_season bigint;
  s public.rank_seasons%rowtype;
  m public.rank_student_seasons%rowtype;
  info record;
  nxt public.rank_tiers%rowtype;
  v_next jsonb := null;
  v_gate jsonb := null;
  v_titles int;
  v_pct int;
  v_chal_title text;
  v_passed boolean;
  v_week date := public.rank_week_start(now());
  v_week_done int;
  v_goal record;
  v_display jsonb := null;
  p public.profiles%rowtype;
  v_rp int := 0;
  v_code text := 'tan_binh';
  v_day date := public.rank_vn_date(now());
  v_sc record;
  v_fmax int;
begin
  if not public.rank_can_view(p_student) then return null; end if;
  select * into p from public.profiles where id = p_student;
  if p.display_title_code is not null then
    select jsonb_build_object('code', t.code, 'name', t.name, 'level', p.display_title_level, 'group', t.group_code)
    into v_display from public.rank_titles t where t.code = p.display_title_code;
  end if;

  v_season := public.rank_season_for_at(p_student, now());
  if v_season is null then
    return jsonb_build_object('season', null, 'display_title', v_display,
      'titles_count', (select count(distinct title_code) from public.rank_title_awards where student_id = p_student));
  end if;
  select * into s from public.rank_seasons where id = v_season;
  -- GĐ 1b #8: ngày của chuỗi đổi mốc khỏi 0h (rank_streak_day) + đóng băng
  v_day := public.rank_streak_day(v_season, now());
  select * into v_sc from public.rank_daily_streak_calc(v_season, p_student, now());
  v_fmax := public.rank_cfg(v_season, 'streak_freeze_per_week', 1)::int;
  select * into v_goal from public.rank_weekly_goal_of(v_season, p_student, v_week);
  select * into m from public.rank_student_seasons where season_id = v_season and student_id = p_student;
  if found then v_rp := m.rp; v_code := m.tier_code; end if;
  select * into info from public.rank_tier_info(v_season, v_code, v_rp);

  -- bậc kế tiếp + điều kiện còn thiếu
  select * into nxt from public.rank_tiers where season_id = v_season and sort = info.sort + 1;
  if found then
    v_passed := exists (select 1 from public.rank_gate_passes g where g.season_id = v_season and g.student_id = p_student and g.tier_code = nxt.code);
    if public.rank_tier_needs_gate(nxt) then
      v_titles := public.rank_titles_at_level(p_student, coalesce(nxt.required_title_level, 'thuc_tinh'));
      if nxt.challenge_exam_id is not null then
        select title into v_chal_title from public.exams where id = nxt.challenge_exam_id;
        v_pct := public.rank_best_pct(p_student, nxt.challenge_exam_id,
          (s.starts_on::timestamp) at time zone 'Asia/Ho_Chi_Minh',
          ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh');
      end if;
      v_gate := jsonb_build_object(
        'passed', v_passed,
        'required_title_count', nxt.required_title_count,
        'required_title_level', nxt.required_title_level,
        'titles_have', v_titles,
        'challenge_required', nxt.challenge_exam_id is not null or nxt.code in ('cao_thu', 'thach_dau'),
        'challenge_exam_id', nxt.challenge_exam_id,
        'challenge_title', v_chal_title,
        'challenge_pass_pct', round(coalesce(nxt.challenge_pass_score, 8) * 10),
        'challenge_best_pct', v_pct
      );
    end if;
    v_next := jsonb_build_object('code', nxt.code, 'name', nxt.name, 'min_rp', nxt.min_rp,
      'rp_needed', greatest(0, nxt.min_rp - v_rp), 'gate', v_gate);
  end if;

  select count(*) into v_week_done from (
    select er.exam_id from public.exam_results er
    join public.rank_sources rs on rs.season_id = v_season and rs.enabled and rs.source_kind = 'exam' and rs.source_id = er.exam_id
    where er.student_id = p_student and public.rank_week_start(er.created_at) = v_week
    group by er.exam_id having max(er.score) >= v_goal.min_score
    union all
    select ps.item_id from public.practice_sessions ps
    join public.rank_sources rs on rs.season_id = v_season and rs.enabled and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id
    where ps.student_id = p_student and public.rank_week_start(ps.created_at) = v_week
    group by ps.item_id having max(ps.score) >= v_goal.min_score
  ) x;

  return jsonb_build_object(
    'season', jsonb_build_object('id', s.id, 'name', s.name, 'starts_on', s.starts_on, 'ends_on', s.ends_on, 'status', s.status),
    'rp', v_rp,
    'tier', jsonb_build_object('code', info.code, 'name', info.name, 'sort', info.sort, 'tier_min', info.tier_min,
      'next_min', info.next_min, 'division', info.division, 'div_min', info.div_min, 'div_max', info.div_max,
      'paragon', v_code = 'thach_dau' and public.rank_is_paragon(p_student)),
    'next', v_next,
    'tier_reached_at', m.tier_reached_at,
    'joined_at', m.joined_at,
    'display_title', v_display,
    'titles_count', (select count(distinct title_code) from public.rank_title_awards where student_id = p_student),
    'weekly', jsonb_build_object('week_start', v_week, 'done', v_week_done,
      'target', v_goal.target,
      'min_score', v_goal.min_score,
      'personal', v_goal.personal,
      'rp', public.rank_cfg(v_season, 'weekly_goal_rp', 30)::int,
      'achieved', exists (select 1 from public.rank_rp_awards a where a.season_id = v_season and a.student_id = p_student and a.source_kind = 'weekly_goal' and a.source_ref = v_week::text and a.awarded > 0)),
    'daily', jsonb_build_object('date', v_day,
      'streak', v_sc.len,
      'reset_hour', public.rank_streak_offset(v_season),
      'freeze_per_week', v_fmax,
      'freeze_used_week', (select count(*) from unnest(v_sc.frozen) f where date_trunc('week', f) = date_trunc('week', v_day::timestamp))::int,
      'freeze_saved_recent', exists (select 1 from unnest(v_sc.frozen) f where f >= v_day - 1),
      'min_score', public.rank_cfg(v_season, 'weekly_goal_min_score', 7),
      'rp', public.rank_cfg(v_season, 'daily_streak_rp', 5)::int,
      'today_done', exists (select 1 from public.rank_rp_awards a where a.season_id = v_season and a.student_id = p_student and a.source_kind = 'daily_streak' and a.source_ref = v_day::text and a.awarded > 0))
  );
end; $$;

grant execute on function public.rank_status_of(uuid) to authenticated;

drop function if exists public.rank_gate_attempts_of(uuid, bigint);
drop function if exists public.rank_gate_finish(bigint);
drop function if exists public.rank_gate_answer(bigint, jsonb, bigint);
drop function if exists public.rank_gate_start(text);
drop function if exists public.rank_gate_current_payload(public.rank_gate_attempts);
drop function if exists public.rank_grade_question(jsonb, jsonb);
drop function if exists public.rank_gate_public_question(bigint, jsonb);
drop function if exists public.rank_gate_pick(bigint[], bigint[], text);
drop function if exists public.rank_gate_pool_ids(bigint, uuid, text);
drop function if exists public.rank_gate_pool_size(bigint, text);
drop function if exists public.rank_gate_grade(bigint, uuid);
drop function if exists public.rank_gate_rule(bigint, text);
drop function if exists public.rank_gate_mode(bigint);
drop function if exists public.rank_gate_adaptive_code(text);
drop function if exists public.rank_gate_lvl_name(int);
drop function if exists public.rank_gate_lvl(text);
drop table if exists public.rank_gate_attempts;
alter table public.rank_tiers
  drop column if exists gate_min_level_held,
  drop column if exists gate_min_hard_correct,
  drop column if exists gate_pass_pct;

commit;
