-- Rollback 20260929100000_rank_restore_daily_streak.sql: về lại rank_on_result của 20260926110000
-- (không cộng chuỗi ngày). Không xoá dòng daily_streak đã cộng.

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

  perform public.rank_eval_gates(v_season, p_student);
  perform public.rank_eval_achievements(v_season, p_student, p_at);
  perform public.rank_refresh_student(v_season, p_student);
end; $$;
