-- Rollback 20260929110000_rank_progress_week.sql
-- Xoá RP tiến bộ đã cộng (awards + ledger), trigger/hàm mới, khôi phục trg_rank_question_results
-- và ràng buộc source_kind như trước. Sau đó tính lại RP các em bị ảnh hưởng bằng
--   select public.rank_recompute_season(<id mùa>);  (hoặc chờ lượt làm kế tiếp tự làm mới)

drop trigger if exists trg_rank_progress_practice on public.practice_question_results;
drop function if exists public.trg_rank_progress_practice();

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

drop function if exists public.rank_eval_progress_week(bigint, uuid, timestamptz);
drop function if exists public.rank_progress_calc(uuid, date);

delete from public.rank_rp_ledger where source_kind = 'progress_week';
delete from public.rank_rp_awards where source_kind = 'progress_week';

alter table public.rank_rp_awards drop constraint if exists rank_rp_awards_source_kind_check;
alter table public.rank_rp_awards add constraint rank_rp_awards_source_kind_check
  check (source_kind in ('practice', 'fix', 'weekly_goal', 'daily_streak', 'manual', 'homework_check'));

-- Chỉ mục giữ lại (vô hại). Muốn bỏ:
--   drop index if exists public.exam_question_results_student_time_idx;
--   drop index if exists public.practice_question_results_student_time_idx;
