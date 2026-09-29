-- ============================================================
-- Migration: chuỗi ngày (streak) + gợi ý "nhiệm vụ hôm nay"
-- Chạy SAU: supabase-migration-rank-system.sql
-- Idempotent — chạy lại được (create or replace function).
--
-- Thêm nguồn RP mới 'daily_streak': mỗi ngày hoàn thành >= 1 bài tính RP đạt từ điểm tối thiểu
-- (dùng chung ngưỡng weekly_goal_min_score) thì +daily_streak_rp (mặc định 5). Chuỗi = số ngày
-- liên tiếp có 'daily_streak' — hôm nay chưa xong vẫn tính chuỗi từ hôm qua (không gãy giữa ngày,
-- kiểu Duolingo/Snapchat). Hai danh hiệu mới: Chuỗi 7 Ngày / Chuỗi 30 Ngày.
-- Sau khi chạy: gọi rank_recompute_season(<id mùa>) để backfill chuỗi cho hoạt động cũ trong mùa.
-- ============================================================

-- Cho phép source_kind mới trong rank_rp_awards / rank_rp_ledger.
alter table public.rank_rp_awards drop constraint if exists rank_rp_awards_source_kind_check;
alter table public.rank_rp_awards add constraint rank_rp_awards_source_kind_check
  check (source_kind in ('practice', 'fix', 'weekly_goal', 'daily_streak', 'manual'));

-- ============================================================
-- 5b. Chuỗi ngày
-- ============================================================
-- Ngày (giờ VN). Đạt khi có >= 1 bài tính RP mà điểm >= ngưỡng weekly_goal_min_score.
-- Cộng một lần/ngày (source_ref = ngày, dạng 'YYYY-MM-DD').
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


-- ============================================================
-- 8. Danh hiệu thành tích (thêm Chuỗi 7 Ngày / Chuỗi 30 Ngày)
-- ============================================================
create or replace function public.rank_eval_achievements(p_season bigint, p_student uuid, p_at timestamptz)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  s public.rank_seasons%rowtype;
  v_week date := public.rank_week_start(p_at);
  v_this int;
  v_prev numeric;
  v_prev_weeks int;
  v_streak int;
  v_day_streak int;
  v_n int;
  v_pct int;
  r record;
  v_from timestamptz;
  v_to timestamptz;
begin
  select * into s from public.rank_seasons where id = p_season;
  v_from := (s.starts_on::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to := ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh';

  -- Bứt Phá Thần Tốc: RP tuần này >= 60 và >= 2× trung bình 3 tuần liền trước (đủ 3 tuần trong mùa, TB >= 10).
  if v_week - 21 >= s.starts_on then
    select coalesce(sum(amount), 0) into v_this from public.rank_rp_ledger
      where season_id = p_season and student_id = p_student and source_kind <> 'manual'
        and public.rank_week_start(created_at) = v_week;
    select coalesce(sum(amount), 0) / 3.0 into v_prev from public.rank_rp_ledger
      where season_id = p_season and student_id = p_student and source_kind <> 'manual'
        and public.rank_week_start(created_at) between v_week - 21 and v_week - 7;
    if v_this >= 60 and v_prev >= 10 and v_this >= 2 * v_prev then
      perform public.rank_grant_title(p_student, 'but_pha_than_toc', 'don', p_season, jsonb_build_object('week', v_week, 'rp', v_this, 'prev_avg', round(v_prev)));
    end if;
  end if;

  -- Chiến Binh Bất Diệt: đạt mục tiêu 4 tuần liên tiếp.
  v_streak := 0;
  for r in
    select source_ref::date as w from public.rank_rp_awards
    where season_id = p_season and student_id = p_student and source_kind = 'weekly_goal' and awarded > 0
    order by 1 desc
  loop
    if v_streak = 0 or r.w = v_week - 7 * v_streak then
      v_week := case when v_streak = 0 then r.w else v_week end;
      v_streak := v_streak + 1;
    else
      exit;
    end if;
  end loop;
  if v_streak >= 4 then
    perform public.rank_grant_title(p_student, 'chien_binh_bat_diet', 'don', p_season, jsonb_build_object('weeks', v_streak));
  end if;

  -- Chuỗi 7 Ngày / Chuỗi 30 Ngày: số ngày liên tiếp hoàn thành mục tiêu ngày.
  v_day_streak := public.rank_daily_streak_len(p_season, p_student, p_at);
  if v_day_streak >= 7 then
    perform public.rank_grant_title(p_student, 'chuoi_7_ngay', 'don', p_season, jsonb_build_object('days', v_day_streak));
  end if;
  if v_day_streak >= 30 then
    perform public.rank_grant_title(p_student, 'chuoi_30_ngay', 'don', p_season, jsonb_build_object('days', v_day_streak));
  end if;

  -- Bách Phát Bách Trúng: >= 3 đề thử thách (bậc / Huyền Thoại / trùm) đạt 100% trong mùa.
  select count(*) into v_n from (
    select e.exam_id from (
      select challenge_exam_id as exam_id from public.rank_tiers where season_id = p_season and challenge_exam_id is not null
      union select legend_challenge_exam_id from public.rank_titles where legend_challenge_exam_id is not null
      union select s.boss_exam_id where s.boss_exam_id is not null
    ) e
    where public.rank_best_pct(p_student, e.exam_id, v_from, v_to) >= 100
  ) x;
  if v_n >= 3 then
    perform public.rank_grant_title(p_student, 'bach_phat_bach_trung', 'don', p_season, jsonb_build_object('exams', v_n));
  end if;

  -- Lật Kèo Ngoạn Mục: một chủ đề tầng bài từng <50% (8 câu đầu) rồi >=80% (8 câu gần nhất, tổng >=16);
  -- hoặc đã tự thoát phụ đạo bằng bài kiểm tra.
  if exists (
    select 1 from public.tutoring_needs n
    where n.student_id = p_student and n.status = 'cleared' and n.note like 'Tự kiểm tra%'
  ) or exists (
    with rows_ as (
      select coalesce(t.parent_id, t.id) as lt, eqr.is_correct,
             row_number() over (partition by coalesce(t.parent_id, t.id) order by eqr.created_at, eqr.question_index) as rn,
             count(*) over (partition by coalesce(t.parent_id, t.id)) as cnt
      from public.exam_question_results eqr
      join public.question_topics t on t.id = eqr.topic_id
      where eqr.student_id = p_student
    )
    select lt from rows_ where cnt >= 16 group by lt
    having avg(case when rn <= 8 then (is_correct)::int end) < 0.5
       and avg(case when rn > cnt - 8 then (is_correct)::int end) >= 0.8
  ) then
    perform public.rank_grant_title(p_student, 'lat_keo_ngoan_muc', 'don', p_season, '{}'::jsonb);
  end if;

  -- Phá Đảo Chuyên Đề: một chương mà mọi chủ đề tầng bài đều >= 5 câu, >= 85% đúng, và có cả lý thuyết lẫn bài tập.
  for r in
    with lt as (
      select t.id as topic_id, t.chapter_id from public.question_topics t where t.parent_id is null and t.chapter_id is not null
    ),
    per as (
      select lt.chapter_id, lt.topic_id,
             count(eqr.*) as n,
             count(*) filter (where eqr.is_correct) as c,
             count(distinct eqr.form) filter (where eqr.form in ('ly_thuyet', 'bai_tap')) as forms
      from lt
      left join public.question_topics ch on coalesce(ch.parent_id, ch.id) = lt.topic_id
      left join public.exam_question_results eqr on eqr.topic_id = ch.id and eqr.student_id = p_student
      group by lt.chapter_id, lt.topic_id
    )
    select chapter_id from per
    group by chapter_id
    having bool_and(n >= 5 and c * 100 >= n * 85) and max(forms) = 2
    limit 1
  loop
    perform public.rank_grant_title(p_student, 'pha_dao_chuyen_de', 'don', p_season, jsonb_build_object('chapter_id', r.chapter_id));
  end loop;

  -- Trùm Cuối: vượt đề khó nhất mùa.
  if s.boss_exam_id is not null then
    v_pct := public.rank_best_pct(p_student, s.boss_exam_id, v_from, v_to);
    if v_pct is not null and v_pct >= round(coalesce(s.boss_pass_score, 8) * 10) then
      perform public.rank_grant_title(p_student, 'trum_cuoi', 'don', p_season, jsonb_build_object('exam_id', s.boss_exam_id, 'pct', v_pct));
    end if;
  end if;

  -- Huyền Thoại Đấu Trường: Chí Tôn ở >= 2 mùa đã đóng.
  select count(*) into v_n from public.rank_season_results where student_id = p_student and tier_code = 'thach_dau';
  if v_n >= 2 then
    perform public.rank_grant_title(p_student, 'huyen_thoai_dau_truong', 'don', p_season, jsonb_build_object('seasons', v_n));
  end if;
end; $$;


-- ============================================================
-- 9. Xử lý một lần nộp bài (thêm gọi rank_eval_daily_streak)
-- ============================================================
create or replace function public.rank_on_result(
  p_student uuid, p_kind text, p_source_id bigint, p_score numeric, p_at timestamptz, p_result_ref bigint
)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_season bigint := public.rank_season_for_at(p_student, p_at);
  v_src public.rank_sources%rowtype;
  v_title text;
begin
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
    perform public.rank_eval_daily_streak(v_season, p_student, p_at);
  end if;

  perform public.rank_eval_gates(v_season, p_student);
  perform public.rank_eval_achievements(v_season, p_student, p_at);
  perform public.rank_refresh_student(v_season, p_student);
end; $$;


-- ============================================================
-- 10. Trạng thái rank (thêm khối 'daily' — chuỗi ngày hôm nay)
-- ============================================================
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


-- ============================================================
-- Seed danh hiệu mới
-- ============================================================
insert into public.rank_titles (code, group_code, kind, name, description, sort) values
  ('chuoi_7_ngay',  'thanh_tich', 'achievement', 'Chuỗi 7 Ngày',  'Hoàn thành mục tiêu ngày 7 ngày liên tiếp', 15),
  ('chuoi_30_ngay', 'thanh_tich', 'achievement', 'Chuỗi 30 Ngày', 'Hoàn thành mục tiêu ngày 30 ngày liên tiếp', 16)
on conflict (code) do update set group_code = excluded.group_code, kind = excluded.kind, name = excluded.name,
  description = excluded.description, sort = excluded.sort;
