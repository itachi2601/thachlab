-- ============================================================================
-- fix(rank): học sinh làm nhiều nhưng không được cộng RP (11/10/2026)
--
-- Chẩn đoán 7 ngày qua, mùa 4: 141/170 lượt nộp đề kiểm tra nằm trên đề CHƯA bật làm nguồn RP (KTTX, Kiểm tra nhanh,
-- Đề nhanh...), 34/99 lượt luyện tập cũng vậy; 98 lượt làm lại không cộng thêm do quy tắc "chỉ lượt đầu".
--
-- Thầy chốt 11/10/2026:
--   1. Bật làm nguồn RP mọi đề / mục luyện tập mà học sinh mùa 4 đã nộp từ ngày mở mùa (Kiểm tra nhanh tối đa 10 RP,
--      còn lại 20 RP — khớp mức đang dùng), rồi tính lại mùa.
--   3. Làm lại thì thưởng phần CHÊNH LỆCH: đặt rp_first_attempt_only = 0. rank_award chỉ cộng khi điểm mới vượt
--      mức đã nhận (delta > 0, tối đa max_rp của bài) nên làm lại không "bơm" được quá trần của bài.
--   (2 — thông báo trước khi làm — là phần code giao diện, không nằm trong migration này.)
--
-- Sao lưu các dòng rank_sources thêm mới vào rank_sources_backup_20261011 để hoàn tác đúng phần đã thêm.
-- RP đã cộng / đã thu hồi 10/10 KHÔNG bị động (rank_award không bao giờ trừ; mục tiêu tuần đã về 30 RP, tiến bộ tuần
-- cần >= 60%, nên tính lại không đưa các khoản đó trở lại).
--
-- Cách chạy: bash scripts/run-migrations.sh — NGOÀI giờ học sinh làm bài (tính lại cả mùa, ~150 học sinh).
-- Rollback: perf/rollback/20261011160000_rank_bat_nguon_thuong_chenh_lech.down.sql
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
  select * into s from public.rank_seasons where id = 4 and status = 'active';
  if s.id is null then raise exception 'Mùa 4 không còn active — dừng'; end if;

  -- 1a. Đề đã có học sinh mùa 4 nộp mà chưa là nguồn.
  with todo as (
    select distinct er.exam_id as id, e.title
    from public.exam_results er
    join public.exams e on e.id = er.exam_id
    where er.created_at >= s.starts_on::timestamp
      and er.student_id in (
        select uc.user_id from public.user_classes uc
        where uc.status = 'active' and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids)))
      and not exists (select 1 from public.rank_sources rs
        where rs.season_id = s.id and rs.source_kind = 'exam' and rs.source_id = er.exam_id)
  ), ins as (
    insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
    select s.id, 'exam', id, case when title ilike 'Kiểm tra nhanh%' then 10 else 20 end, true from todo
    returning source_kind, source_id, max_rp
  )
  insert into public.rank_sources_backup_20261011 (season_id, source_kind, source_id, max_rp)
  select s.id, source_kind, source_id, max_rp from ins;
  get diagnostics v_exam = row_count;

  -- 1b. Mục luyện tập tương tự.
  with todo as (
    select distinct ps.item_id as id
    from public.practice_sessions ps
    join public.lesson_items li on li.id = ps.item_id
    where ps.created_at >= s.starts_on::timestamp
      and ps.student_id in (
        select uc.user_id from public.user_classes uc
        where uc.status = 'active' and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids)))
      and not exists (select 1 from public.rank_sources rs
        where rs.season_id = s.id and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id)
  ), ins as (
    insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
    select s.id, 'practice_item', id, 20, true from todo
    returning source_kind, source_id, max_rp
  )
  insert into public.rank_sources_backup_20261011 (season_id, source_kind, source_id, max_rp)
  select s.id, source_kind, source_id, max_rp from ins;
  get diagnostics v_item = row_count;

  -- 3. Làm lại thưởng chênh lệch.
  update public.rank_seasons
    set config = coalesce(config, '{}'::jsonb) || '{"rp_first_attempt_only": 0}'::jsonb
    where id = s.id;

  -- Tính lại mùa (cần quyền staff: giả lập JWT của một admin trong phiên này).
  select id into v_admin from public.profiles where role = 'admin' order by created_at limit 1;
  if v_admin is null then raise exception 'Không tìm thấy admin để tính lại'; end if;
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);
  v_n := public.rank_recompute_season(s.id);

  raise notice 'Đã bật % đề + % mục luyện tập; tính lại % học sinh', v_exam, v_item, v_n;
end $$;

-- ROLLBACK (xem perf/rollback/20261011160000_rank_bat_nguon_thuong_chenh_lech.down.sql)
