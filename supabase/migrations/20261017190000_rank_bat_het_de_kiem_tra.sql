-- ============================================================================
-- feat(rank): bật làm nguồn RP MỌI đề kiểm tra / BTVN còn thiếu + đề học sinh đã nộp, tính lại mùa 4 và 5 (17/10/2026)
--
-- Thầy chốt 17/10: điểm kiểm tra trên lớp là điểm thật, phải được tính RP. Hiện mùa 4 còn ~360 đề, mùa 5 còn 1 đề trong
-- mục Kiểm tra/BTVN của chương lớp chưa có trong rank_sources; thêm 6 đề đã có lượt nộp (128 lượt) nhưng chưa tính.
--   1. Bật làm nguồn RP: (a) mọi đề trong mục BTVN/Kiểm tra của chương gắn với lớp của mùa; (b) mọi đề học sinh mùa đã nộp
--      từ ngày mở mùa; (c) mọi đề định kỳ (class_assessments) của lớp mùa. "Kiểm tra nhanh" tối đa 10 RP, còn lại 20 RP.
--      Không đụng dòng rank_sources đã có (giữ nguyên max_rp/enabled).
--   2. Tính lại mùa 4 và 5 (rank_recompute_season) để các lượt đã nộp được cộng RP bù (theo cấu hình mùa:
--      mùa 4/5 đang rp_first_attempt_only = 0).
-- Sao lưu dòng thêm mới vào rank_sources_backup_20261017.
-- Cách chạy: bash scripts/run-migrations.sh — ngoài giờ học sinh làm bài (recompute nặng hơn một chút).
-- Rollback: perf/rollback/20261017190000_rank_bat_het_de_kiem_tra.down.sql (RP đã cộng bù không tự thu hồi)
-- ============================================================================

create table if not exists public.rank_sources_backup_20261017 (
  season_id bigint, source_kind text, source_id bigint, max_rp int, backed_up_at timestamptz default now()
);
alter table public.rank_sources_backup_20261017 enable row level security;
revoke all on public.rank_sources_backup_20261017 from anon, authenticated;

do $$
declare
  s public.rank_seasons%rowtype;
  v_admin uuid;
  v_exam int; v_n int;
begin
  select id into v_admin from public.profiles where role = 'admin' order by created_at limit 1;
  if v_admin is null then raise exception 'Không tìm thấy admin để tính lại'; end if;

  for s in select * from public.rank_seasons where id in (4, 5) and status = 'active' order by id loop
    with todo as (
      select e.id, e.title from public.exams e where e.id in (
        select unnest(li.exam_ids) from public.lesson_items li
        join public.lessons l on l.id = li.lesson_id
        join public.chapter_classes cc on cc.chapter_id = l.chapter_id and cc.class_id = any (s.class_ids)
        where li.kind in ('bai_tap_ve_nha', 'kiem_tra')
        union
        select er.exam_id from public.exam_results er
        where er.created_at >= s.starts_on::timestamp
          and er.student_id in (select uc.user_id from public.user_classes uc
            where uc.status = 'active' and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids)))
        union
        select ca.exam_id from public.class_assessments ca where ca.class_id = any (s.class_ids))
      and not exists (select 1 from public.rank_sources rs
        where rs.season_id = s.id and rs.source_kind = 'exam' and rs.source_id = e.id)
    ), ins as (
      insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
      select s.id, 'exam', id, case when title ilike 'Kiểm tra nhanh%' then 10 else 20 end, true from todo
      returning source_kind, source_id, max_rp
    )
    insert into public.rank_sources_backup_20261017 (season_id, source_kind, source_id, max_rp)
    select s.id, source_kind, source_id, max_rp from ins;
    get diagnostics v_exam = row_count;

    perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);
    v_n := public.rank_recompute_season(s.id);

    raise notice 'Mùa %: bật % đề; tính lại % học sinh', s.id, v_exam, v_n;
  end loop;
end $$;
