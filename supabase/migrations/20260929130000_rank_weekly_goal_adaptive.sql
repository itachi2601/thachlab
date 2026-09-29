-- ============================================================================
-- feat(rank): mục tiêu tuần THÍCH ỨNG theo từng em — giai đoạn 1b, việc 2 (29/9/2026)
--
-- Bỏ "N bài >= X điểm" chung cho cả lớp. Mỗi tuần, mục tiêu của từng em được đặt từ 2 tuần liền
-- trước của chính em (cố định suốt tuần):
--   Số bài  = nhịp làm bài 2 tuần qua x weekly_goal_pace_pct (75%), trong [count_min 1, count_max 5].
--   Ngưỡng  = điểm mà ~80% bài gần đây của chính em đạt tới (phân vị 20 của điểm tốt nhất mỗi bài/tuần),
--             làm tròn 0,5, trong [sàn 4, trần 8,5]. Nhắm ~80-85% em đạt mục tiêu mỗi tuần (Bandura & Schunk).
--   Chưa đủ lịch sử (< weekly_goal_min_history = 3 bài trong 2 tuần) hoặc weekly_goal_personal = 0
--     -> dùng mục tiêu chung của mùa như cũ (weekly_goal_count / weekly_goal_min_score).
--   Thưởng RP, khoá chống cộng đôi (một lần/tuần) và thành tích "Chiến Binh Bất Diệt" giữ nguyên.
--
-- Lưu ý cách đọc yêu cầu gốc: ROADMAP viết "ngưỡng nhỉnh hơn trung bình" và "nhắm ~80-85% thành
-- công" — hai ý lệch nhau. Ở đây ưu tiên tỉ lệ thành công (ngưỡng thấp hơn trung bình một chút);
-- muốn thử thách hơn thì hạ weekly_goal_success_pct. Tất cả chỉnh được qua rank_seasons.config, không sửa code:
--   weekly_goal_personal (1) · weekly_goal_min_history (3) · weekly_goal_pace_pct (75) ·
--   weekly_goal_success_pct (80) · weekly_goal_count_min (1) · weekly_goal_count_max (5) ·
--   weekly_goal_score_floor (4) · weekly_goal_score_cap (8.5)
--
-- Thay đổi hệ thống hiện có (định nghĩa lại đúng 2 hàm, còn lại giữ nguyên bản đang chạy):
--   rank_eval_weekly_goal (bản docs/supabase-migration-rank-system.sql) và rank_status_of
--   (bản 20260926100000_rank_paragon.sql). rank_status_of.weekly thêm khoá 'personal' (client cũ bỏ qua).
-- Chuỗi ngày (daily) vẫn dùng weekly_goal_min_score chung của mùa — chưa đổi.
--
-- Cách chạy: bash scripts/run-migrations.sh   (giờ nào cũng được; chỉ thêm 1 hàm và định nghĩa lại 2 hàm)
-- Rollback:  supabase db query --linked -f perf/rollback/20260929130000_rank_weekly_goal_adaptive.down.sql
-- ============================================================================

do $$
begin
  if to_regprocedure('public.rank_award(bigint,uuid,text,text,integer,text,bigint)') is null then
    raise exception 'Thiếu rank_award: schema rank chưa đúng, dừng lại';
  end if;
end $$;

-- Mục tiêu tuần của MỘT học sinh trong MỘT tuần (p_week = ngày Thứ Hai), tính từ 2 tuần liền trước.
-- Cố định suốt tuần (chỉ dùng dữ liệu trước tuần đó). Chưa đủ lịch sử hoặc tắt cấu hình -> dùng mục
-- tiêu chung của mùa (weekly_goal_count / weekly_goal_min_score) như cũ.
create or replace function public.rank_weekly_goal_of(p_season bigint, p_student uuid, p_week date)
returns table(target int, min_score numeric, personal boolean, n_items int, avg_items numeric)
language plpgsql stable security definer set search_path = public
as $$
declare
  v_from timestamptz := ((p_week - 14)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to timestamptz := (p_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_def_count int := public.rank_cfg(p_season, 'weekly_goal_count', 3)::int;
  v_def_min numeric := public.rank_cfg(p_season, 'weekly_goal_min_score', 7);
  v_on boolean := public.rank_cfg(p_season, 'weekly_goal_personal', 1) <> 0;
  v_hist int := public.rank_cfg(p_season, 'weekly_goal_min_history', 3)::int;
  v_pace numeric := public.rank_cfg(p_season, 'weekly_goal_pace_pct', 75) / 100.0;
  v_succ numeric := least(greatest(public.rank_cfg(p_season, 'weekly_goal_success_pct', 80), 50), 95) / 100.0;
  v_cmin int := public.rank_cfg(p_season, 'weekly_goal_count_min', 1)::int;
  v_cmax int := public.rank_cfg(p_season, 'weekly_goal_count_max', 5)::int;
  v_floor numeric := public.rank_cfg(p_season, 'weekly_goal_score_floor', 4);
  v_cap numeric := public.rank_cfg(p_season, 'weekly_goal_score_cap', 8.5);
  v_n int;
  v_pct numeric;
begin
  select count(*), percentile_cont(1 - v_succ) within group (order by b.best)
  into v_n, v_pct
  from (
    select max(a.score) as best
    from (
      select 'exam' as k, er.exam_id as id, er.score, public.rank_week_start(er.created_at) as wk
      from public.exam_results er
      join public.rank_sources rs on rs.season_id = p_season and rs.enabled and rs.source_kind = 'exam' and rs.source_id = er.exam_id
      where er.student_id = p_student and er.created_at >= v_from and er.created_at < v_to and er.score is not null
      union all
      select 'practice_item', ps.item_id, ps.score, public.rank_week_start(ps.created_at)
      from public.practice_sessions ps
      join public.rank_sources rs on rs.season_id = p_season and rs.enabled and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id
      where ps.student_id = p_student and ps.created_at >= v_from and ps.created_at < v_to and ps.score is not null
    ) a
    group by a.k, a.id, a.wk
  ) b;

  n_items := coalesce(v_n, 0);
  avg_items := round(n_items / 2.0, 1);
  if not v_on or n_items < v_hist or v_pct is null then
    target := v_def_count; min_score := v_def_min; personal := false;
    return next; return;
  end if;
  -- Số bài = nhịp làm bài 2 tuần qua x hệ số (mặc định 75%), trong [min, max].
  target := least(v_cmax, greatest(v_cmin, round(n_items / 2.0 * v_pace)::int));
  -- Ngưỡng điểm = mức mà ~80% bài gần đây của CHÍNH em đạt tới (phân vị 20), làm tròn 0,5, trong [sàn, trần].
  min_score := least(v_cap, greatest(v_floor, round(v_pct * 2) / 2))::numeric(3,1);
  personal := true;
  return next;
end; $$;
revoke all on function public.rank_weekly_goal_of(bigint, uuid, date) from public, anon, authenticated;

create or replace function public.rank_eval_weekly_goal(p_season bigint, p_student uuid, p_at timestamptz)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_week date := public.rank_week_start(p_at);
  v_from timestamptz := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to timestamptz := ((v_week + 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_need int;
  v_min numeric;
  v_pers boolean;
  v_rp int := public.rank_cfg(p_season, 'weekly_goal_rp', 30)::int;
  v_count int;
  s public.rank_seasons%rowtype;
begin
  select * into s from public.rank_seasons where id = p_season;
  if v_week < s.starts_on or v_week > s.ends_on then
    return 0;
  end if;

  select w.target, w.min_score, w.personal into v_need, v_min, v_pers
  from public.rank_weekly_goal_of(p_season, p_student, v_week) w;

  select count(*) into v_count from (
    select 'exam' as k, er.exam_id as id
    from public.exam_results er
    join public.rank_sources rs on rs.season_id = p_season and rs.enabled and rs.source_kind = 'exam' and rs.source_id = er.exam_id
    where er.student_id = p_student and er.created_at >= v_from and er.created_at < v_to
    group by er.exam_id having max(er.score) >= v_min
    union
    select 'practice_item', ps.item_id
    from public.practice_sessions ps
    join public.rank_sources rs on rs.season_id = p_season and rs.enabled and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id
    where ps.student_id = p_student and ps.created_at >= v_from and ps.created_at < v_to
    group by ps.item_id having max(ps.score) >= v_min
  ) x;

  if v_count >= v_need then
    return public.rank_award(p_season, p_student, 'weekly_goal', v_week::text, v_rp,
      'Mục tiêu tuần ' || to_char(v_week, 'DD/MM') || ': ' || v_count || ' bài đạt từ ' || replace(v_min::text, '.', ',')
        || case when v_pers then ' (mục tiêu riêng theo 2 tuần trước)' else '' end, null);
  end if;
  return 0;
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
