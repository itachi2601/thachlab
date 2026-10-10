-- ============================================================================
-- fix(rank): thưởng tuần/tiến bộ không được quá cao cho điểm thấp (10/10/2026)
--
-- Sự cố: có em làm điểm thấp, bài kế tiếp 4,5 điểm mà ghi nhận tới ~90 RP. Truy sổ rank_rp_ledger 10/10:
--   * "Mùa thử nghiệm" (id 4) có config weekly_goal_rp = 90 (mặc định là 30) → mỗi lần đạt mục tiêu tuần = 90 RP.
--   * Mục tiêu tuần RIÊNG của em yếu bị kéo xuống sàn 4 điểm (weekly_goal_score_floor) → 4,5 điểm là "đạt".
--   * Tiến bộ tuần: mốc 2 tuần trước rất thấp thì nhích +5 điểm % cũng được 15–25 RP dù vẫn dưới 60%.
--   Cả ba cộng chồng cùng một ngày (có em 150–200 RP/ngày: weekly_goal 90 + progress 25 + streak 5 + practice).
--
-- Sửa (code + dữ liệu config, KHÔNG sửa RP đã cộng):
--   1. rank_eval_weekly_goal: ngưỡng điểm không dưới weekly_goal_abs_floor (mặc định 6) và RP không quá
--      weekly_goal_rp_max (mặc định 40), kể cả khi config mùa đặt cao hơn.
--   2. rank_eval_progress_week: chỉ thưởng khi tỉ lệ đúng tuần này >= progress_min_acc_pct (mặc định 60).
--   3. Hạ weekly_goal_rp 90 → 30 ở mùa 4 và đặt weekly_goal_score_floor = 6 ở mùa đang mở (merge config, giữ khoá khác).
-- Chuỗi ngày dùng weekly_goal_min_score = 7 nên không phải nguyên nhân.
--
-- Cách chạy: bash scripts/run-migrations.sh — giờ nào cũng được (định nghĩa lại 2 hàm + 1 UPDATE config).
-- Rollback: perf/rollback/20261010400000_rank_chan_thuong_qua_cao.down.sql
-- ============================================================================

create or replace function public.rank_eval_progress_week(p_season bigint, p_student uuid, p_at timestamptz)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_week date := public.rank_week_start(p_at);
  s public.rank_seasons%rowtype;
  v_min_gain numeric := public.rank_cfg(p_season, 'progress_min_gain_pct', 5);
  v_rp_base int := public.rank_cfg(p_season, 'progress_rp', 15)::int;
  v_rp_max int := public.rank_cfg(p_season, 'progress_rp_max', 25)::int;
  v_step_pct numeric := greatest(public.rank_cfg(p_season, 'progress_step_pct', 5), 0.1);
  v_step_rp int := public.rank_cfg(p_season, 'progress_step_rp', 5)::int;
  v_min_q int := public.rank_cfg(p_season, 'progress_min_questions', 15)::int;
  c record;
  v_need numeric;
  v_rp int;
  v_delta int;
  v_min_acc numeric := public.rank_cfg(p_season, 'progress_min_acc_pct', 60);
begin
  if not public.rank_is_student(p_student) then return 0; end if;
  select * into s from public.rank_seasons where id = p_season;
  if s.id is null or s.status <> 'active' then return 0; end if;
  if public.rank_vn_date(p_at) < s.starts_on or public.rank_vn_date(p_at) > s.ends_on then return 0; end if;

  select * into c from public.rank_progress_calc(p_student, v_week);
  if c.q_now < v_min_q or c.q_base < v_min_q or c.gain is null then return 0; end if;

  -- Chặn thưởng "tiến bộ" khi tuần này vẫn thấp: mốc cũ rất thấp thì nhích nhẹ cũng đạt +5 điểm %.
  if c.acc_now < v_min_acc then return 0; end if;

  v_need := least(v_min_gain, 100 - c.acc_base);
  if c.gain < v_need then return 0; end if;

  v_rp := least(v_rp_max, v_rp_base + (floor(greatest(c.gain - v_min_gain, 0) / v_step_pct)::int) * v_step_rp);
  v_delta := public.rank_award(p_season, p_student, 'progress_week', v_week::text, v_rp,
    'Tiến bộ tuần ' || to_char(v_week, 'DD/MM') || ': tỉ lệ đúng '
      || replace(c.acc_now::text, '.', ',') || '% (mốc 2 tuần trước '
      || replace(c.acc_base::text, '.', ',') || '%, +' || replace(c.gain::text, '.', ',') || ' điểm %)', null);
  -- GĐ 1b: thành tích Tiến Bộ Tuần (một lần, không thu hồi).
  perform public.rank_grant_title(p_student, 'tien_bo_tuan', 'don', p_season,
    jsonb_build_object('week', v_week, 'gain', c.gain, 'acc_now', c.acc_now, 'acc_base', c.acc_base));
  return v_delta;
end; $$;
revoke all on function public.rank_eval_progress_week(bigint, uuid, timestamptz) from public, anon, authenticated;

update public.rank_seasons
  set config = coalesce(config, '{}'::jsonb) || '{"weekly_goal_rp": 30}'::jsonb
  where id = 4 and (config ->> 'weekly_goal_rp')::int > 30;
-- Sàn điểm của mục tiêu RIÊNG đặt ở config để thẻ mục tiêu tuần hiện đúng con số em phải đạt (khớp với abs_floor trong hàm).
update public.rank_seasons
  set config = coalesce(config, '{}'::jsonb) || '{"weekly_goal_score_floor": 6}'::jsonb
  where status = 'active' and coalesce((config ->> 'weekly_goal_score_floor')::numeric, 0) < 6;

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
  v_rp int := least(public.rank_cfg(p_season, 'weekly_goal_rp', 30)::int, public.rank_cfg(p_season, 'weekly_goal_rp_max', 40)::int);
  v_count int;
  s public.rank_seasons%rowtype;
begin
  select * into s from public.rank_seasons where id = p_season;
  if v_week < s.starts_on or v_week > s.ends_on then
    return 0;
  end if;

  select w.target, w.min_score, w.personal into v_need, v_min, v_pers
  from public.rank_weekly_goal_of(p_season, p_student, v_week) w;
  -- Ngưỡng điểm tuyệt đối: mục tiêu riêng của em yếu không được tụt dưới mức này (chặn 4,5 điểm đã nhận cả thưởng tuần).
  v_min := greatest(v_min, public.rank_cfg(p_season, 'weekly_goal_abs_floor', 6));

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

