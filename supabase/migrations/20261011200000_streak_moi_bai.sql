-- ============================================================================
-- Chuỗi ngày tính MỌI bài (thầy chốt 11/10/2026)
-- Trước: chỉ bài thuộc nguồn RP (rank_sources) mới giữ chuỗi — hôm 11/10 chỉ 16/36 lượt luyện được tính, nhiều em
-- làm bài mà chuỗi không tăng. Nay: bài kiểm tra hoặc luyện tập NÀO đạt từ weekly_goal_min_score (mặc định 7) trong
-- ngày đều giữ chuỗi và nhận daily_streak_rp. RP của từng bài vẫn chỉ cho bài thuộc nguồn.
-- Định nghĩa lại: rank_eval_daily_streak (bỏ ràng buộc nguồn), rank_on_result (gọi chuỗi ngoài khối nguồn).
-- Không tính lại ngày cũ (RP/chuỗi đã có giữ nguyên).
-- Cách chạy: bash scripts/run-migrations.sh — nên ngoài giờ học sinh làm bài (create or replace hàm chạy sau mỗi lần nộp).
-- Rollback: perf/rollback/20261011200000_streak_moi_bai.down.sql
-- ============================================================================

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
    where er.student_id = p_student and er.created_at >= v_from and er.created_at < v_to and er.score >= v_min
    union all
    select 1 from public.practice_sessions ps
    where ps.student_id = p_student and ps.created_at >= v_from and ps.created_at < v_to and ps.score >= v_min
  ) into v_done;

  if v_done then
    return public.rank_award(p_season, p_student, 'daily_streak', v_day::text, v_rp,
      'Chuỗi ngày ' || to_char(v_day, 'DD/MM') || ': hoàn thành 1 bài đạt từ ' || replace(v_min::text, '.', ','), null);
  end if;
  return 0;
end; $$;


CREATE OR REPLACE FUNCTION public.rank_on_result(p_student uuid, p_kind text, p_source_id bigint, p_score numeric, p_at timestamp with time zone, p_result_ref bigint)
 RETURNS void
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $$
declare
  v_season bigint;
  v_src public.rank_sources%rowtype;
  v_title text;
  v_ref text;
  v_seen boolean := false;
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
    v_ref := p_kind || ':' || p_source_id;
    -- RP của một bài = LƯỢT ĐẦU trong mùa (không phải điểm tốt nhất): đã có dòng nhận RP cho bài này thì bỏ qua
    -- phần cộng RP (mục tiêu tuần / chuỗi ngày / cửa / thành tích bên dưới vẫn chạy). Tắt bằng config mùa
    -- rp_first_attempt_only = 0. Khoá tư vấn để hai lượt nộp đồng thời không cùng thấy "chưa có dòng".
    if public.rank_cfg(v_season, 'rp_first_attempt_only', 1) >= 1 then
      perform pg_advisory_xact_lock(hashtextextended('rank_first:' || v_season || ':' || p_student || ':' || v_ref, 0));
      v_seen := exists (
        select 1 from public.rank_rp_awards a
        where a.season_id = v_season and a.student_id = p_student and a.source_kind = 'practice' and a.source_ref = v_ref);
    end if;
    if not v_seen then
      perform public.rank_award(v_season, p_student, 'practice', v_ref,
        public.rank_score_to_rp(p_score, v_src.max_rp),
        'Bài luyện tập: ' || coalesce(v_title, '#' || p_source_id) || ' (' || replace(to_char(p_score, 'FM990.0'), '.', ',') || ' điểm)',
        p_result_ref);
    end if;
    perform public.rank_eval_weekly_goal(v_season, p_student, p_at);
  end if;
  -- Chuỗi ngày tính MỌI bài đạt điểm tối thiểu (thầy chốt 11/10/2026), không chỉ bài thuộc nguồn RP.
  perform public.rank_eval_daily_streak(v_season, p_student, p_at);

  perform public.rank_eval_gates(v_season, p_student);
  perform public.rank_eval_achievements(v_season, p_student, p_at);
  perform public.rank_refresh_student(v_season, p_student);
end; $$;
