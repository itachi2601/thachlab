-- ============================================================================
-- Bật nguồn RP 10 cho MỌI đề "Kiểm tra nhanh" / "Kiểm tra hiểu bài" / "Luyện tập" lẻ (thầy chốt 17/10/2026)
--
-- Sau 20261017190000 chỉ các đề loại này ĐÃ CÓ lượt nộp mới được bật (10 RP), đề cùng loại chưa ai làm thì không →
-- em làm Kiểm tra nhanh bài này có RP, bài kia không. Nay bật đồng loạt cho đề published, gán lớp thuộc lớp của mùa
-- đang mở, KHÔNG nằm trong mục Luyện tập của bài học (mục đó đã tính RP qua nguồn practice_item, tránh tính hai lần).
-- Không đụng dòng rank_sources đã có (3 đề #206, #209 mùa 4 và #7 mùa 5 đang 20 RP giữ nguyên).
-- Tính lại mùa (rank_recompute_season) để em đã nộp các đề này được cộng bù, như 20261017190000.
-- Sao lưu dòng thêm mới: rank_sources_backup_20261017b. Chạy: bash scripts/run-migrations.sh --only N.
-- Rollback: perf/rollback/20261017235000_rank_bat_kiem_tra_nhanh_10rp.down.sql (RP đã cộng bù không tự thu hồi)
-- ============================================================================

create table if not exists public.rank_sources_backup_20261017b (
  season_id bigint, source_kind text, source_id bigint, max_rp int, backed_up_at timestamptz default now()
);
alter table public.rank_sources_backup_20261017b enable row level security;
revoke all on public.rank_sources_backup_20261017b from anon, authenticated;

do $$
declare
  s public.rank_seasons%rowtype;
  v_admin uuid;
  v_n int; v_students int;
begin
  select id into v_admin from public.profiles where role = 'admin' order by created_at limit 1;
  if v_admin is null then raise exception 'Không tìm thấy admin để tính lại'; end if;

  for s in select * from public.rank_seasons where status = 'active' order by id loop
    with todo as (
      select e.id from public.exams e
      where e.published
        and (e.title ilike 'Kiểm tra nhanh%' or e.title ilike 'Kiểm tra hiểu bài%' or e.title ilike 'Luyện tập%')
        and exists (select 1 from public.exam_classes ec where ec.exam_id = e.id and ec.class_id = any (s.class_ids))
        and not exists (select 1 from public.lesson_items li where li.kind = 'luyen_tap' and e.id = any (li.exam_ids))
        and not exists (select 1 from public.rank_sources rs
                        where rs.season_id = s.id and rs.source_kind = 'exam' and rs.source_id = e.id)
    ), ins as (
      insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
      select s.id, 'exam', id, 10, true from todo
      returning source_kind, source_id, max_rp
    )
    insert into public.rank_sources_backup_20261017b (season_id, source_kind, source_id, max_rp)
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
