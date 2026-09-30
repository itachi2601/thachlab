-- Rollback 20260930130000_rank_streak_freeze.sql: trả 3 hàm về bản trước, bỏ hàm mới.
create or replace function public.rank_eval_daily_streak(p_season bigint, p_student uuid, p_at timestamptz)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_day date := public.rank_vn_date(p_at);
  v_from timestamptz := (v_day::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to timestamptz := ((v_day + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_min numeric := public.rank_cfg(p_season, 'weekly_goal_min_score', 7);
  v_rp int := public.rank_cfg(p_season, 'daily_streak_rp', 5)::int;
  v_done boolean;
  s public.rank_seasons%rowtype;
begin
  select * into s from public.rank_seasons where id = p_season;
  if v_day < s.starts_on or v_day > s.ends_on then
    return 0;
  end if;

  select exists (
    select 1 from public.exam_results er
    join public.rank_sources rs on rs.season_id = p_season and rs.enabled and rs.source_kind = 'exam' and rs.source_id = er.exam_id
    where er.student_id = p_student and er.created_at >= v_from and er.created_at < v_to and er.score >= v_min
    union all
    select 1 from public.practice_sessions ps
    join public.rank_sources rs on rs.season_id = p_season and rs.enabled and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id
    where ps.student_id = p_student and ps.created_at >= v_from and ps.created_at < v_to and ps.score >= v_min
  ) into v_done;

  if v_done then
    return public.rank_award(p_season, p_student, 'daily_streak', v_day::text, v_rp,
      'Chuỗi ngày ' || to_char(v_day, 'DD/MM') || ': hoàn thành 1 bài đạt từ ' || replace(v_min::text, '.', ','), null);
  end if;
  return 0;
end; $$;

-- Số ngày liên tiếp hiện tại (kể từ hôm nay nếu đã xong, ngược lại kể từ hôm qua — không gãy chuỗi giữa ngày).
create or replace function public.rank_daily_streak_len(p_season bigint, p_student uuid, p_at timestamptz)
returns int
language plpgsql stable security definer set search_path = public
as $$
declare
  v_cursor date := public.rank_vn_date(p_at);
  v_streak int := 0;
  r record;
begin
  if not exists (
    select 1 from public.rank_rp_awards
    where season_id = p_season and student_id = p_student and source_kind = 'daily_streak'
      and source_ref = v_cursor::text and awarded > 0
  ) then
    v_cursor := v_cursor - 1;
  end if;

  for r in
    select source_ref::date as d from public.rank_rp_awards
    where season_id = p_season and student_id = p_student and source_kind = 'daily_streak' and awarded > 0
    order by 1 desc
  loop
    if r.d = v_cursor then
      v_streak := v_streak + 1;
      v_cursor := v_cursor - 1;
    elsif r.d < v_cursor then
      exit;
    end if;
  end loop;
  return v_streak;
end; $$;



create or replace function public.rank_status_of(p_student uuid)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
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
      'streak', public.rank_daily_streak_len(v_season, p_student, now()),
      'min_score', public.rank_cfg(v_season, 'weekly_goal_min_score', 7),
      'rp', public.rank_cfg(v_season, 'daily_streak_rp', 5)::int,
      'today_done', exists (select 1 from public.rank_rp_awards a where a.season_id = v_season and a.student_id = p_student and a.source_kind = 'daily_streak' and a.source_ref = v_day::text and a.awarded > 0))
  );
end; $$;
grant execute on function public.rank_status_of(uuid) to authenticated;

drop function if exists public.rank_daily_streak_calc(bigint, uuid, timestamptz);
drop function if exists public.rank_streak_day(bigint, timestamptz);
drop function if exists public.rank_streak_offset(bigint);
