-- Rollback cho supabase/migrations/20260926110000_rank_exclude_staff.sql
--
-- Khôi phục lại 3 hàm về bản KHÔNG chặn theo role (hành vi trước migration).
-- LƯU Ý: không khôi phục được dữ liệu rank_student_seasons/rank_rp_awards/…
-- đã xoá của tài khoản không phải học sinh — nhưng đó là dữ liệu rác (0 RP
-- thật, phát sinh khi GV/admin tự test bài), không cần khôi phục.
--
-- Chạy: supabase db query --linked -f perf/rollback/20260926110000_rank_exclude_staff.down.sql

create or replace function public.rank_ensure_member(p_season bigint, p_student uuid)
returns void
language sql security definer set search_path = public
as $$
  insert into public.rank_student_seasons (season_id, student_id)
  values (p_season, p_student)
  on conflict (season_id, student_id) do nothing;
$$;

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
  end if;

  perform public.rank_eval_gates(v_season, p_student);
  perform public.rank_eval_achievements(v_season, p_student, p_at);
  perform public.rank_refresh_student(v_season, p_student);
end; $$;

create or replace function public.trg_rank_question_results()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  r record;
  v_season bigint;
begin
  for r in select distinct student_id from inserted loop
    begin
      v_season := public.rank_season_for_at(r.student_id, now());
      perform public.rank_eval_titles(r.student_id, v_season);
      if v_season is not null then
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

drop function if exists public.rank_is_student(uuid);
