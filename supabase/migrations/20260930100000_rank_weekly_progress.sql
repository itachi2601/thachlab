-- ============================================================================
-- GĐ 1b #1 — Trục "tiến bộ so với chính em" (ROADMAP, thầy chốt 28/09/2026)
--   * rank_progress_stats(student, tuần): số câu + số đúng của tuần đó và của 2 tuần liền trước.
--   * rank_eval_progress(season, student, at): tuần này đúng nhiều hơn 2 tuần trước
--     >= progress_min_gain điểm % (mặc định 5), mỗi bên >= progress_min_questions câu (mặc định 10)
--     -> cộng RP 'progress_week' (mặc định 20, theo tuần, idempotent qua rank_award).
--   * rank_progress_top(grade): "Tiến bộ nhất tuần" của khối (tên đã rút gọn theo honor_visibility).
--   * rank_public_honor v3 = v2 + khoá 'progress' cho mỗi khối (không thêm round-trip ở trang chủ).
--   * Gắn vào rank_on_result + trg_rank_question_results (mọi lượt làm bài đều xét lại, không tính thừa).
-- Không đổi bảng. Client cũ bỏ qua khoá 'progress'.
-- Cấu hình mùa (rank_seasons.config): progress_rp, progress_min_gain, progress_min_questions.
--
-- Cách chạy: supabase db query --linked -f supabase/migrations/20260930100000_rank_weekly_progress.sql
-- Rollback:  supabase db query --linked -f perf/rollback/20260930100000_rank_weekly_progress.down.sql
-- ============================================================================

create or replace function public.rank_progress_stats(p_student uuid, p_week date default null)
returns table (cur_n int, cur_ok int, base_n int, base_ok int)
language sql stable security definer set search_path = public
as $$
  with w as (
    select coalesce(p_week, public.rank_week_start(now())) as wk
  ),
  b as (
    select ((wk - 14)::timestamp) at time zone 'Asia/Ho_Chi_Minh' as t0,
           ((wk)::timestamp) at time zone 'Asia/Ho_Chi_Minh' as t1,
           ((wk + 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh' as t2
    from w
  ),
  q as (
    select created_at, is_correct from public.exam_question_results
    where student_id = p_student and is_correct is not null
      and created_at >= (select t0 from b) and created_at < (select t2 from b)
    union all
    select created_at, is_correct from public.practice_question_results
    where student_id = p_student and is_correct is not null
      and created_at >= (select t0 from b) and created_at < (select t2 from b)
  )
  select
    count(*) filter (where created_at >= (select t1 from b))::int,
    count(*) filter (where created_at >= (select t1 from b) and is_correct)::int,
    count(*) filter (where created_at < (select t1 from b))::int,
    count(*) filter (where created_at < (select t1 from b) and is_correct)::int
  from q;
$$;
grant execute on function public.rank_progress_stats(uuid, date) to authenticated;

create or replace function public.rank_eval_progress(p_season bigint, p_student uuid, p_at timestamptz)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_week date := public.rank_week_start(p_at);
  v_min_n int := public.rank_cfg(p_season, 'progress_min_questions', 10)::int;
  v_min_gain numeric := public.rank_cfg(p_season, 'progress_min_gain', 5);
  v_rp int := public.rank_cfg(p_season, 'progress_rp', 20)::int;
  st record;
  v_gain numeric;
  s public.rank_seasons%rowtype;
begin
  select * into s from public.rank_seasons where id = p_season;
  if v_week < s.starts_on or v_week > s.ends_on then return 0; end if;

  select * into st from public.rank_progress_stats(p_student, v_week);
  if st.cur_n < v_min_n or st.base_n < v_min_n then return 0; end if;

  v_gain := 100.0 * st.cur_ok / st.cur_n - 100.0 * st.base_ok / st.base_n;
  if v_gain < v_min_gain then return 0; end if;

  return public.rank_award(p_season, p_student, 'progress_week', v_week::text, v_rp,
    'Tiến bộ tuần ' || to_char(v_week, 'DD/MM') || ': tỉ lệ đúng tăng ' || round(v_gain)::text || ' điểm % so với 2 tuần trước', null);
end; $$;

-- "Tiến bộ nhất tuần" của một khối: tăng điểm % lớn nhất, đủ số câu; chỉ HS không ẩn tên.
create or replace function public.rank_progress_top(p_grade text)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_week date := public.rank_week_start(now());
  v_res jsonb;
begin
  select jsonb_build_object('name', public.rank_honor_name(x.full_name, x.honor_visibility),
                            'avatar', x.avatar_url, 'gain', round(x.gain)::int,
                            'from_pct', round(x.p0)::int, 'to_pct', round(x.p1)::int)
  into v_res
  from (
    select p.full_name, p.honor_visibility, p.avatar_url,
           100.0 * st.cur_ok / st.cur_n as p1, 100.0 * st.base_ok / st.base_n as p0,
           100.0 * st.cur_ok / st.cur_n - 100.0 * st.base_ok / st.base_n as gain
    from (
      select distinct uc.user_id
      from public.classes c
      join public.user_classes uc on uc.class_id = c.id and uc.status = 'active'
      where substring(c.name from '\d+') = p_grade
    ) m
    join public.profiles p on p.id = m.user_id and p.role = 'student' and p.honor_visibility <> 'hidden'
    cross join lateral public.rank_progress_stats(m.user_id, v_week) st
    where st.cur_n >= 10 and st.base_n >= 10
  ) x
  where x.gain >= 5
  order by x.gain desc, x.full_name
  limit 1;
  return v_res;
end; $$;

-- Gắn vào luồng chấm RP hiện có (giữ nguyên thân hàm, chỉ thêm 1 lời gọi).
create or replace function public.rank_on_result(
  p_student uuid, p_kind text, p_source_id bigint, p_score numeric, p_at timestamptz, p_result_ref bigint
)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_season bigint;
  v_src public.rank_sources%rowtype;
  v_title text;
begin
  if not public.rank_is_student(p_student) then return; end if;

  v_season := public.rank_season_for_at(p_student, p_at);
  if v_season is null then return; end if;

  select * into v_src from public.rank_sources
  where season_id = v_season and source_kind = p_kind and source_id = p_source_id and enabled;

  perform public.rank_ensure_member(v_season, p_student);

  if v_src.season_id is not null then
    if p_kind = 'exam' then
      select title into v_title from public.exams where id = p_source_id;
    else
      select li.title into v_title from public.lesson_items li where li.id = p_source_id;
    end if;
    perform public.rank_award(v_season, p_student, 'practice', p_kind || ':' || p_source_id,
      public.rank_score_to_rp(p_score, v_src.max_rp),
      'Bài luyện tập: ' || coalesce(v_title, '#' || p_source_id) || ' (' || replace(to_char(p_score, 'FM990.0'), '.', ',') || ' điểm)',
      p_result_ref);
    perform public.rank_eval_weekly_goal(v_season, p_student, p_at);
  end if;

  begin
    perform public.rank_eval_progress(v_season, p_student, p_at);
  exception when others then
    raise warning 'rank: bỏ qua lỗi tiến bộ tuần cho %: %', p_student, sqlerrm;
  end;

  perform public.rank_eval_gates(v_season, p_student);
  perform public.rank_eval_achievements(v_season, p_student, p_at);
  perform public.rank_refresh_student(v_season, p_student);
end; $$;

-- Trigger câu hỏi: xét thêm tiến bộ tuần (điểm câu có thể ghi sau rank_on_result).
create or replace function public.trg_rank_question_results()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  r record;
  v_season bigint;
begin
  for r in select distinct student_id from inserted loop
    if not public.rank_is_student(r.student_id) then continue; end if;
    begin
      v_season := public.rank_season_for_at(r.student_id, now());
      perform public.rank_eval_titles(r.student_id, v_season);
      if v_season is not null then
        perform public.rank_eval_progress(v_season, r.student_id, now());
        perform public.rank_eval_gates(v_season, r.student_id);
        perform public.rank_eval_achievements(v_season, r.student_id, now());
        perform public.rank_refresh_student(v_season, r.student_id);
      end if;
    exception when others then
      raise warning 'rank: bỏ qua lỗi khi xét danh hiệu cho %: %', r.student_id, sqlerrm;
    end;
  end loop;
  return null;
end; $$;

-- rank_public_honor v3 (= v2 + 'progress')
create or replace function public.rank_public_honor()
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_week date := public.rank_week_start(now());
  v_from timestamptz := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_prev_from timestamptz := ((v_week - 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_today date := public.rank_vn_date(now());
  v_grades jsonb;
begin
  with cls as (
    select c.id as class_id, substring(c.name from '\d+') as grade
    from public.classes c
    where c.name ~ '\d'
  ),
  seas as (
    select cl.class_id, cl.grade, rs.id as season_id, rs.name as season_name, rs.ends_on
    from cls cl
    join lateral (
      select rs.* from public.rank_seasons rs
      where rs.status = 'active' and v_today between rs.starts_on and rs.ends_on
        and (cardinality(rs.class_ids) = 0 or cl.class_id = any (rs.class_ids))
      order by rs.starts_on desc limit 1
    ) rs on true
  ),
  members as (
    select distinct on (s.grade, uc.user_id)
      s.grade, s.season_id, uc.user_id, p.full_name, p.avatar_url, p.honor_visibility,
      p.display_title_code, p.display_title_level,
      m.tier_code, m.tier_sort, m.division, m.tier_reached_at
    from seas s
    join public.user_classes uc on uc.class_id = s.class_id and uc.status = 'active'
    join public.profiles p on p.id = uc.user_id and p.role = 'student'
    left join public.rank_student_seasons m on m.season_id = s.season_id and m.student_id = uc.user_id
    where p.honor_visibility <> 'hidden'
    order by s.grade, uc.user_id, s.season_id desc
  ),
  wk as (
    select mm.*,
      coalesce((select sum(l.amount) from public.rank_rp_ledger l
                where l.season_id = mm.season_id and l.student_id = mm.user_id and l.created_at >= v_from), 0)::int as rp_cur,
      coalesce((select sum(l.amount) from public.rank_rp_ledger l
                where l.season_id = mm.season_id and l.student_id = mm.user_id
                  and l.created_at >= v_prev_from and l.created_at < v_from), 0)::int as rp_prev
    from members mm
  ),
  gmode as (
    select grade, (max(rp_cur) = 0 and max(rp_prev) > 0) as use_prev from wk group by grade
  ),
  eff as (
    select w.*, g.use_prev,
      case when g.use_prev then w.rp_prev else w.rp_cur end as rp_week,
      case when g.use_prev then 0 else w.rp_prev end as rp_before,
      case when g.use_prev then v_prev_from else v_from end as win_from,
      case when g.use_prev then v_from else now() + interval '1 day' end as win_to
    from wk w join gmode g on g.grade = w.grade
  ),
  ranked as (
    select e.*, rank() over (partition by e.grade order by e.rp_week desc) as pos from eff e
  )
  select coalesce(jsonb_agg(jsonb_build_object(
      'grade', g.grade,
      'use_prev', g.use_prev,
      'season', (select jsonb_build_object('id', s.season_id, 'name', s.season_name, 'ends_on', s.ends_on)
                 from seas s where s.grade = g.grade order by s.ends_on desc limit 1),
      'total', (select count(*) from ranked r where r.grade = g.grade),
      'top', (select coalesce(jsonb_agg(jsonb_build_object(
                'pos', t.pos,
                'name', public.rank_honor_name(t.full_name, t.honor_visibility),
                'avatar', t.avatar_url,
                'rp_week', t.rp_week,
                'tier_code', t.tier_code, 'division', t.division,
                'paragon', t.tier_code = 'thach_dau' and public.rank_is_paragon(t.user_id),
                'title', (select jsonb_build_object('code', rt.code, 'name', rt.name, 'level', t.display_title_level)
                          from public.rank_titles rt where rt.code = t.display_title_code)
              ) order by t.pos, t.full_name), '[]'::jsonb)
              from (select * from ranked r where r.grade = g.grade and r.rp_week > 0 and r.pos <= 3
                    order by r.pos, r.full_name limit 5) t),
      'top_more', greatest(0, (select count(*) from ranked r where r.grade = g.grade and r.rp_week > 0 and r.pos <= 3) - 5),
      'improved', (select jsonb_build_object(
                     'name', public.rank_honor_name(t.full_name, t.honor_visibility),
                     'avatar', t.avatar_url, 'delta', t.rp_week - t.rp_before, 'rp_week', t.rp_week)
                   from ranked t
                   where t.grade = g.grade and not g.use_prev and t.pos > 3 and t.rp_week > 0 and t.rp_week - t.rp_before > 0
                   order by (t.rp_week - t.rp_before) desc, t.full_name limit 1),
      'progress', public.rank_progress_top(g.grade),
      'tier_ups', (select coalesce(jsonb_agg(jsonb_build_object(
                     'name', public.rank_honor_name(t.full_name, t.honor_visibility),
                     'tier_code', t.tier_code, 'division', t.division) order by t.tier_reached_at desc), '[]'::jsonb)
                   from (select * from ranked r
                         where r.grade = g.grade and r.tier_sort > 1
                           and r.tier_reached_at >= r.win_from and r.tier_reached_at < r.win_to
                         order by r.tier_reached_at desc limit 4) t),
      'streak', (select jsonb_build_object('name', public.rank_honor_name(s.full_name, s.honor_visibility), 'days', s.days)
                 from (select r.full_name, r.honor_visibility,
                              public.rank_daily_streak_len(r.season_id, r.user_id, now()) as days
                       from ranked r
                       where r.grade = g.grade and exists (
                         select 1 from public.rank_rp_awards a
                         where a.season_id = r.season_id and a.student_id = r.user_id
                           and a.source_kind = 'daily_streak' and a.awarded > 0
                           and a.source_ref in (v_today::text, (v_today - 1)::text))
                      ) s
                 where s.days >= 3 order by s.days desc, s.full_name limit 1)
    ) order by g.grade::int), '[]'::jsonb)
  into v_grades
  from (select distinct grade, use_prev from ranked) g;

  return jsonb_build_object('week_start', v_week, 'grades', v_grades);
end; $$;
grant execute on function public.rank_public_honor() to anon, authenticated;

-- ============================================================================
-- ROLLBACK: perf/rollback/20260930100000_rank_weekly_progress.down.sql
-- ============================================================================
