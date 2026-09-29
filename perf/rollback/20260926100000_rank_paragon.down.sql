-- Rollback cho 20260926100000_rank_paragon.sql — khôi phục 2 hàm bản gốc rồi bỏ rank_is_paragon.
-- Chạy: supabase db query --linked -f perf/rollback/20260926100000_rank_paragon.down.sql

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
    group by er.exam_id having max(er.score) >= public.rank_cfg(v_season, 'weekly_goal_min_score', 7)
    union all
    select ps.item_id from public.practice_sessions ps
    join public.rank_sources rs on rs.season_id = v_season and rs.enabled and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id
    where ps.student_id = p_student and public.rank_week_start(ps.created_at) = v_week
    group by ps.item_id having max(ps.score) >= public.rank_cfg(v_season, 'weekly_goal_min_score', 7)
  ) x;

  return jsonb_build_object(
    'season', jsonb_build_object('id', s.id, 'name', s.name, 'starts_on', s.starts_on, 'ends_on', s.ends_on, 'status', s.status),
    'rp', v_rp,
    'tier', jsonb_build_object('code', info.code, 'name', info.name, 'sort', info.sort, 'tier_min', info.tier_min,
      'next_min', info.next_min, 'division', info.division, 'div_min', info.div_min, 'div_max', info.div_max),
    'next', v_next,
    'tier_reached_at', m.tier_reached_at,
    'joined_at', m.joined_at,
    'display_title', v_display,
    'titles_count', (select count(distinct title_code) from public.rank_title_awards where student_id = p_student),
    'weekly', jsonb_build_object('week_start', v_week, 'done', v_week_done,
      'target', public.rank_cfg(v_season, 'weekly_goal_count', 3)::int,
      'min_score', public.rank_cfg(v_season, 'weekly_goal_min_score', 7),
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

create or replace function public.rank_class_board(p_class_id bigint)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_me uuid := auth.uid();
  v_season bigint;
  s public.rank_seasons%rowtype;
  v_week date := public.rank_week_start(now());
  v_from timestamptz := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_prev_from timestamptz := ((v_week - 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_top jsonb;
  v_total int;
  v_me_json jsonb;
  v_improved jsonb;
  v_weekly jsonb;
begin
  if not (public.manages_class(p_class_id) or exists (
    select 1 from public.user_classes where user_id = v_me and class_id = p_class_id and status = 'active'
  )) then
    return null;
  end if;

  select rs.id into v_season from public.rank_seasons rs
  where rs.status = 'active' and public.rank_vn_date(now()) between rs.starts_on and rs.ends_on
    and (cardinality(rs.class_ids) = 0 or p_class_id = any (rs.class_ids))
  order by rs.starts_on desc limit 1;
  if v_season is null then return jsonb_build_object('season', null); end if;
  select * into s from public.rank_seasons where id = v_season;

  with members as (
    select uc.user_id, p.full_name, p.avatar_url, m.tier_code, m.division
    from public.user_classes uc
    join public.profiles p on p.id = uc.user_id
    left join public.rank_student_seasons m on m.season_id = v_season and m.student_id = uc.user_id
    where uc.class_id = p_class_id and uc.status = 'active' and p.role = 'student'
  ),
  wk as (
    select mm.*,
      coalesce((select sum(l.amount) from public.rank_rp_ledger l
                where l.season_id = v_season and l.student_id = mm.user_id and l.created_at >= v_from), 0)::int as rp_week,
      coalesce((select sum(l.amount) from public.rank_rp_ledger l
                where l.season_id = v_season and l.student_id = mm.user_id
                  and l.created_at >= v_prev_from and l.created_at < v_from), 0)::int as rp_prev
    from members mm
  ),
  ranked as (
    select w.*, rank() over (order by w.rp_week desc) as pos from wk w
  )
  select
    (select coalesce(jsonb_agg(jsonb_build_object(
        'pos', t.pos, 'name', t.full_name, 'avatar', t.avatar_url, 'rp_week', t.rp_week,
        'tier_code', t.tier_code, 'division', t.division, 'is_me', t.user_id = v_me
      ) order by t.pos, t.full_name), '[]'::jsonb)
     from (select * from ranked where rp_week > 0 order by pos, full_name limit 3) t),
    (select count(*) from ranked),
    (select jsonb_build_object(
        'pos', r.pos, 'rp_week', r.rp_week,
        'tied', (select count(*) from ranked x where x.rp_week = r.rp_week) - 1,
        'above', (select jsonb_build_object('name', x.full_name, 'avatar', x.avatar_url, 'rp_week', x.rp_week)
                  from ranked x where x.rp_week > r.rp_week order by x.rp_week asc, x.full_name limit 1),
        'below', (select jsonb_build_object('name', x.full_name, 'avatar', x.avatar_url, 'rp_week', x.rp_week)
                  from ranked x where x.rp_week < r.rp_week order by x.rp_week desc, x.full_name limit 1)
      ) from ranked r where r.user_id = v_me),
    (select jsonb_build_object('name', t.full_name, 'avatar', t.avatar_url, 'rp_week', t.rp_week, 'delta', t.rp_week - t.rp_prev)
     from ranked t where t.rp_week > 0 and t.rp_week - t.rp_prev > 0 and t.pos > 3
     order by (t.rp_week - t.rp_prev) desc, t.full_name limit 1)
  into v_top, v_total, v_me_json, v_improved;

  with members as (
    select uc.user_id, p.full_name from public.user_classes uc join public.profiles p on p.id = uc.user_id
    where uc.class_id = p_class_id and uc.status = 'active' and p.role = 'student'
  ),
  ev as (
    select mm.full_name, 'weekly_goal' as kind, 'đạt mục tiêu tuần' as label, l.created_at as happened_at
    from public.rank_rp_ledger l join members mm on mm.user_id = l.student_id
    where l.season_id = v_season and l.source_kind = 'weekly_goal' and l.created_at >= v_from
    union all
    select mm.full_name, 'tier_up', 'lên bậc ' || t.name, m.tier_reached_at
    from public.rank_student_seasons m join members mm on mm.user_id = m.student_id
    join public.rank_tiers t on t.season_id = m.season_id and t.code = m.tier_code
    where m.season_id = v_season and m.tier_reached_at >= v_from and m.tier_sort > 1
    union all
    select mm.full_name, 'title', 'nhận danh hiệu ' || rt.name || case a.level when 'thuc_tinh' then ' · Thức Tỉnh' when 'lam_chu' then ' · Làm Chủ' when 'huyen_thoai' then ' · Huyền Thoại' else '' end, a.awarded_at
    from public.rank_title_awards a join members mm on mm.user_id = a.student_id
    join public.rank_titles rt on rt.code = a.title_code
    where a.awarded_at >= v_from
  )
  select coalesce(jsonb_agg(jsonb_build_object('name', e.full_name, 'kind', e.kind, 'label', e.label, 'at', e.happened_at) order by e.happened_at desc), '[]'::jsonb)
  into v_weekly from (select * from ev order by happened_at desc limit 20) e;

  return jsonb_build_object(
    'season', jsonb_build_object('id', s.id, 'name', s.name, 'starts_on', s.starts_on, 'ends_on', s.ends_on),
    'week_start', v_week,
    'total', v_total,
    'top_week', v_top,
    'me', v_me_json,
    'improved', v_improved,
    'weekly', v_weekly
  );
end; $$;
grant execute on function public.rank_class_board(bigint) to authenticated;

drop function if exists public.rank_is_paragon(uuid);
