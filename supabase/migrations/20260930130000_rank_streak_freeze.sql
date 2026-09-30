-- ============================================================================
-- GĐ 1b #8 — Chuỗi ngày có đóng băng + mốc reset không phải 0h (30/9/2026)
--
-- 1. Mốc reset: "ngày" của chuỗi bắt đầu lúc streak_day_offset_hours (mặc định 3) giờ sáng giờ VN, không
--    phải 0h. Em học 23h–1h vẫn tính cùng một ngày; làm bài lúc 1h sáng tính cho ngày hôm trước.
--    Chỉnh qua rank_seasons.config: streak_day_offset_hours (0–6; 0 = như cũ, nửa đêm).
--    Chỉ áp cho chuỗi ngày; mục tiêu tuần / tuần thứ Hai vẫn tính theo lịch thường (0h).
-- 2. Đóng băng: tối đa streak_freeze_per_week (mặc định 1; 0 = tắt) ngày bỏ lỡ MỖI TUẦN (Thứ Hai–Chủ Nhật)
--    được "đóng băng" — chuỗi không gãy, ngày đó không cộng số ngày và không cộng RP. Tính tự động
--    khi đọc chuỗi (không cần bảng mới, không cần em bấm gì): chỉ bắc cầu qua ĐÚNG MỘT ngày trống.
-- 3. rank_status_of.daily thêm reset_hour, freeze_per_week, freeze_used_week, freeze_saved_recent
--    (client cũ bỏ qua khoá lạ).
--
-- Hàm mới: rank_streak_offset, rank_streak_day, rank_daily_streak_calc.
-- Định nghĩa lại: rank_eval_daily_streak (bản docs/supabase-migration-rank-daily-streak.sql),
--   rank_daily_streak_len (giữ chữ ký, gọi calc), rank_status_of (bản 20260929130000).
-- Lưu ý: RP chuỗi ngày đã cộng trước đây (khoá theo ngày lịch 0h) giữ nguyên, không tính lại.
-- Cách chạy: bash scripts/run-migrations.sh — giờ nào cũng được.
-- Rollback: perf/rollback/20260930130000_rank_streak_freeze.down.sql
-- ============================================================================

create or replace function public.rank_streak_offset(p_season bigint)
returns int language sql stable set search_path = public
as $$ select least(greatest(coalesce(public.rank_cfg(p_season, 'streak_day_offset_hours', 3), 3), 0), 6)::int; $$;

-- Ngày (giờ VN) của chuỗi tại thời điểm p_at, đã lùi theo mốc reset.
create or replace function public.rank_streak_day(p_season bigint, p_at timestamptz)
returns date language sql stable set search_path = public
as $$ select ((p_at at time zone 'Asia/Ho_Chi_Minh') - make_interval(hours => public.rank_streak_offset(p_season)))::date; $$;

create or replace function public.rank_eval_daily_streak(p_season bigint, p_student uuid, p_at timestamptz)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_off int := public.rank_streak_offset(p_season);
  v_day date := public.rank_streak_day(p_season, p_at);
  v_from timestamptz := ((v_day::timestamp + make_interval(hours => v_off)) at time zone 'Asia/Ho_Chi_Minh');
  v_to timestamptz := ((v_day::timestamp + make_interval(hours => v_off + 24)) at time zone 'Asia/Ho_Chi_Minh');
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

-- Chuỗi hiện tại + các ngày được đóng băng. Hôm nay chưa xong vẫn tính chuỗi từ hôm qua.
create or replace function public.rank_daily_streak_calc(p_season bigint, p_student uuid, p_at timestamptz)
returns table(len int, frozen date[])
language plpgsql stable security definer set search_path = public
as $$
declare
  v_cursor date := public.rank_streak_day(p_season, p_at);
  v_max int := greatest(coalesce(public.rank_cfg(p_season, 'streak_freeze_per_week', 1), 1)::int, 0);
  v_len int := 0;
  v_frozen date[] := '{}';
  v_used int;
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
    if r.d > v_cursor then
      continue;
    elsif r.d = v_cursor then
      v_len := v_len + 1;
      v_cursor := v_cursor - 1;
    elsif r.d = v_cursor - 1 and v_max > 0 then
      -- ngày trống duy nhất: v_cursor. Bắc cầu nếu tuần của ngày đó còn lượt đóng băng.
      select count(*) into v_used from unnest(v_frozen) f where date_trunc('week', f) = date_trunc('week', v_cursor::timestamp);
      exit when v_used >= v_max;
      v_frozen := v_frozen || v_cursor;
      v_len := v_len + 1;
      v_cursor := r.d - 1;
    else
      exit;
    end if;
  end loop;
  len := v_len; frozen := v_frozen;
  return next;
end; $$;
revoke all on function public.rank_daily_streak_calc(bigint, uuid, timestamptz) from public, anon, authenticated;

create or replace function public.rank_daily_streak_len(p_season bigint, p_student uuid, p_at timestamptz)
returns int
language sql stable security definer set search_path = public
as $$ select c.len from public.rank_daily_streak_calc(p_season, p_student, p_at) c; $$;

-- rank_status_of = bản 20260929130000 + chuỗi ngày mới (GĐ 1b #8)
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
