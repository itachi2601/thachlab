-- ============================================================================
-- fix(rank): lớp 10 (mùa 5 "Alpha test") làm nhiều không được cộng RP (11/10/2026)
--
-- Lớp 10 (class 16, 67 HS) thuộc mùa 5, mùa này chỉ có 2 đề làm nguồn RP và chưa có mục luyện tập nào; migration
-- 20261011160000 chỉ sửa mùa 4 (lớp 11–12). Áp dụng cùng cách cho mùa 5:
--   1. Bật làm nguồn RP: (a) mọi đề / mục luyện tập học sinh mùa 5 đã nộp từ ngày mở mùa; (b) mọi mục Luyện tập,
--      BTVN, Kiểm tra trong các chương của lớp 10 (chapter_classes) để thông báo "tính RP" ở màn vào bài đúng
--      với thực tế. Kiểm tra nhanh tối đa 10 RP, còn lại 20 RP.
--   2. rp_first_attempt_only = 0 (làm lại thưởng phần chênh lệch).
--   3. Tính lại mùa 5.
-- Sao lưu dòng thêm mới vào rank_sources_backup_20261011 (cùng bảng với migration mùa 4, cột season_id phân biệt).
-- Cách chạy: bash scripts/run-migrations.sh — ngoài giờ học sinh làm bài.
-- Rollback: perf/rollback/20261011170000_rank_lop10_bat_nguon.down.sql
-- ============================================================================

create table if not exists public.rank_sources_backup_20261011 (
  season_id bigint, source_kind text, source_id bigint, max_rp int, backed_up_at timestamptz default now()
);
alter table public.rank_sources_backup_20261011 enable row level security;
revoke all on public.rank_sources_backup_20261011 from anon, authenticated;

do $$
declare
  s public.rank_seasons%rowtype;
  v_admin uuid;
  v_exam int; v_item int; v_n int;
begin
  select * into s from public.rank_seasons where id = 5 and status = 'active';
  if s.id is null then raise exception 'Mùa 5 không còn active — dừng'; end if;

  -- 1a. Đề: đã nộp bởi HS mùa 5, hoặc nằm trong mục BTVN/Kiểm tra của chương lớp 10.
  with todo as (
    select e.id, e.title from public.exams e where e.id in (
      select er.exam_id from public.exam_results er
      where er.created_at >= s.starts_on::timestamp
        and er.student_id in (select uc.user_id from public.user_classes uc
          where uc.status = 'active' and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids)))
      union
      select unnest(li.exam_ids) from public.lesson_items li
      join public.lessons l on l.id = li.lesson_id
      join public.chapter_classes cc on cc.chapter_id = l.chapter_id and cc.class_id = any (s.class_ids)
      where li.kind in ('bai_tap_ve_nha', 'kiem_tra'))
    and not exists (select 1 from public.rank_sources rs
      where rs.season_id = s.id and rs.source_kind = 'exam' and rs.source_id = e.id)
  ), ins as (
    insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
    select s.id, 'exam', id, case when title ilike 'Kiểm tra nhanh%' then 10 else 20 end, true from todo
    returning source_kind, source_id, max_rp
  )
  insert into public.rank_sources_backup_20261011 (season_id, source_kind, source_id, max_rp)
  select s.id, source_kind, source_id, max_rp from ins;
  get diagnostics v_exam = row_count;

  -- 1b. Mục luyện tập: đã nộp, hoặc thuộc chương lớp 10.
  with todo as (
    select li.id from public.lesson_items li
    where li.kind = 'luyen_tap' and li.id in (
      select ps.item_id from public.practice_sessions ps
      where ps.created_at >= s.starts_on::timestamp
        and ps.student_id in (select uc.user_id from public.user_classes uc
          where uc.status = 'active' and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids)))
      union
      select li2.id from public.lesson_items li2
      join public.lessons l on l.id = li2.lesson_id
      join public.chapter_classes cc on cc.chapter_id = l.chapter_id and cc.class_id = any (s.class_ids)
      where li2.kind = 'luyen_tap')
    and not exists (select 1 from public.rank_sources rs
      where rs.season_id = s.id and rs.source_kind = 'practice_item' and rs.source_id = li.id)
  ), ins as (
    insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
    select s.id, 'practice_item', id, 20, true from todo
    returning source_kind, source_id, max_rp
  )
  insert into public.rank_sources_backup_20261011 (season_id, source_kind, source_id, max_rp)
  select s.id, source_kind, source_id, max_rp from ins;
  get diagnostics v_item = row_count;

  update public.rank_seasons
    set config = coalesce(config, '{}'::jsonb) || '{"rp_first_attempt_only": 0}'::jsonb
    where id = s.id;

  select id into v_admin from public.profiles where role = 'admin' order by created_at limit 1;
  if v_admin is null then raise exception 'Không tìm thấy admin để tính lại'; end if;
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);
  v_n := public.rank_recompute_season(s.id);

  raise notice 'Mùa 5: bật % đề + % mục luyện tập; tính lại % học sinh', v_exam, v_item, v_n;
end $$;
