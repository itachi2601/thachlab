-- ============================================================================
-- Cộng bù RP cho 25 lượt làm Kiểm tra nhanh ngày 19/10/2026 (đề #1003, #979, #1032)
--
-- 3 đề tạo ngày 18–19/10, sau đợt bật 20261017235000 nên chưa có dòng rank_sources → các lượt nộp không được RP.
-- Bật 10 RP (như mọi Kiểm tra nhanh khác) cho mùa nào có học sinh đã nộp đề, rồi rank_recompute_season để cộng bù.
-- Sao lưu dòng thêm mới: rank_sources_backup_20261020. Rollback: perf/rollback/20261020090000_rank_bat_nguon_kiem_tra_nhanh_19_10.down.sql
-- ============================================================================
create table if not exists public.rank_sources_backup_20261020 (
  season_id bigint, source_kind text, source_id bigint, max_rp int, backed_up_at timestamptz default now()
);
alter table public.rank_sources_backup_20261020 enable row level security;
revoke all on public.rank_sources_backup_20261020 from anon, authenticated;

do $$
declare
  s public.rank_seasons%rowtype;
  v_admin uuid; v_n int; v_students int;
begin
  select id into v_admin from public.profiles where role = 'admin' order by created_at limit 1;
  if v_admin is null then raise exception 'Không tìm thấy admin để tính lại'; end if;

  for s in select * from public.rank_seasons where status = 'active' order by id loop
    with ins as (
      insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
      select s.id, 'exam', e.id, 10, true
      from public.exams e
      where e.id in (1003, 979, 1032)
        and exists (select 1 from public.exam_results er
                    join public.rank_student_seasons ss on ss.student_id = er.student_id and ss.season_id = s.id
                    where er.exam_id = e.id)
        and not exists (select 1 from public.rank_sources rs
                        where rs.season_id = s.id and rs.source_kind = 'exam' and rs.source_id = e.id)
      returning source_kind, source_id, max_rp
    )
    insert into public.rank_sources_backup_20261020 (season_id, source_kind, source_id, max_rp)
    select s.id, source_kind, source_id, max_rp from ins;
    get diagnostics v_n = row_count;

    if v_n > 0 then
      perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);
      v_students := public.rank_recompute_season(s.id);
    else
      v_students := 0;
    end if;
    raise notice 'Mùa %: bật % đề (10 RP); tính lại % học sinh', s.id, v_n, v_students;
  end loop;
end $$;
