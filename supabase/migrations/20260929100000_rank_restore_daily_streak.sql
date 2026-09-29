-- ============================================================================
-- fix(rank): khôi phục cộng RP "chuỗi ngày" (daily_streak) bị mất từ 26/9/2026
-- 29/9/2026.
--
-- Nguyên nhân: docs/supabase-migration-rank-daily-streak.sql thêm dòng
--   perform public.rank_eval_daily_streak(...)
-- vào rank_on_result. Migration 20260926110000_rank_exclude_staff.sql (chạy sau) định nghĩa lại
-- rank_on_result từ bản TRƯỚC khi có chuỗi ngày nên làm rơi dòng đó.
-- Bằng chứng trên production: rank_rp_ledger có 29 dòng daily_streak ngày 25/9, dòng cuối lúc
-- 26/9 00:03 giờ VN; từ đó tới 29/9 KHÔNG còn dòng nào dù có hơn 230 lượt luyện tập được cộng RP.
--
-- Migration này chỉ định nghĩa lại rank_on_result = bản 20260926110000 + đúng 1 dòng gọi chuỗi ngày.
-- Không đổi bảng, không đổi quyền, không chạm dữ liệu.
--
-- SAU KHI CHẠY (tuỳ chọn, thầy quyết): chuỗi ngày của 26–29/9 chưa được cộng. Muốn cộng bù:
--   select public.rank_recompute_season(4);  select public.rank_recompute_season(5);
-- (idempotent: rank_award chỉ cộng phần chênh, chạy lại không cộng đôi; nhưng RP của các em sẽ tăng
--  ngay, nên cân nhắc trước khi chạy giữa mùa.)
--
-- Cách chạy: bash scripts/run-migrations.sh
-- Rollback:  supabase db query --linked -f perf/rollback/20260929100000_rank_restore_daily_streak.down.sql
-- ============================================================================

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
    perform public.rank_eval_daily_streak(v_season, p_student, p_at);
  end if;

  perform public.rank_eval_gates(v_season, p_student);
  perform public.rank_eval_achievements(v_season, p_student, p_at);
  perform public.rank_refresh_student(v_season, p_student);
end; $$;
