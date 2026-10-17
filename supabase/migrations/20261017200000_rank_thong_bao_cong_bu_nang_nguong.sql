-- ============================================================================
-- feat(rank): báo các em được cộng bù RP (migration 20261017190000) + nâng mức đạt bậc ×1,07 (17/10/2026)
--
-- Migration 20261017190000 bật tính RP mọi đề kiểm tra và tính lại mùa 4, 5: các dòng cộng bù ghi vào rank_rp_ledger cùng
-- một created_at = 2026-10-17 07:37:01.176681+00 (một transaction). RP trung bình tăng ~7% nên nâng min_rp mọi bậc ×1,07
-- (làm tròn) ở cả hai mùa để độ khó giữ như cũ (thầy chốt 17/10).
--   1. Chuông cho từng em được bù: tổng RP bù, bấm vào Xếp hạng (không báo phụ huynh; có chốt chống gửi trùng).
--   2. Sao lưu rank_tiers hai mùa rồi nâng min_rp; tính lại hai mùa.
--   3. Em bị tụt bậc do ngưỡng mới thì có chuông riêng giải thích.
-- Cách chạy: bash scripts/run-migrations.sh — ngoài giờ học sinh làm bài.
-- Rollback: perf/rollback/20261017200000_rank_thong_bao_cong_bu_nang_nguong.down.sql (thông báo đã gửi không thu hồi)
-- ============================================================================

create table if not exists public.rank_tiers_backup_20261017 (
  season_id bigint, code text, min_rp int, backed_up_at timestamptz default now()
);
alter table public.rank_tiers_backup_20261017 enable row level security;
revoke all on public.rank_tiers_backup_20261017 from anon, authenticated;

do $$
declare
  v_ts constant timestamptz := timestamptz '2026-10-17 07:37:01.176681+00';
  v_admin uuid;
  v_bu int; v_tut int; v_n int;
begin
  select id into v_admin from public.profiles where role = 'admin' order by created_at limit 1;
  if v_admin is null then raise exception 'Không tìm thấy admin để tính lại'; end if;

  -- 1. Chuông cộng bù
  with bu as (
    select l.student_id, sum(l.amount)::int as rp from public.rank_rp_ledger l
    where l.created_at = v_ts and l.season_id in (4, 5) group by l.student_id having sum(l.amount) > 0
  )
  insert into public.notifications (user_id, kind, title, body, href)
  select b.student_id, 'rp_bu_kiem_tra',
    '+' || b.rp || ' RP · Cộng bù bài kiểm tra trên lớp',
    'Điểm kiểm tra trên lớp giờ được tính RP. Các bài em đã làm trước đó được cộng bù ' || b.rp
      || ' RP. Mức RP để lên từng bậc cũng được nâng nhẹ (khoảng 7%) cho cân bằng với phần RP mới.',
    '/lop-hoc/xep-hang'
  from bu b
  where not exists (select 1 from public.notifications n where n.user_id = b.student_id and n.kind = 'rp_bu_kiem_tra');
  get diagnostics v_bu = row_count;

  -- 2. Nâng ngưỡng, ghi nhớ bậc trước khi tính lại
  create temp table _tier_truoc on commit drop as
    select season_id, student_id, tier_sort from public.rank_student_seasons where season_id in (4, 5);

  insert into public.rank_tiers_backup_20261017 (season_id, code, min_rp)
    select season_id, code, min_rp from public.rank_tiers where season_id in (4, 5);
  update public.rank_tiers set min_rp = round(min_rp * 1.07)::int where season_id in (4, 5) and min_rp > 0;

  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);
  v_n := public.rank_recompute_season(4) + public.rank_recompute_season(5);

  -- 3. Em tụt bậc
  insert into public.notifications (user_id, kind, title, body, href)
  select s.student_id, 'rank_tier_adjust', 'Mức RP lên bậc đã điều chỉnh',
    'Vì kiểm tra trên lớp giờ được tính RP, mức RP để giữ từng bậc tăng khoảng 7%. RP của em chưa đủ cho bậc cũ; làm thêm bài là lên lại.',
    '/lop-hoc/xep-hang'
  from public.rank_student_seasons s join _tier_truoc t on t.season_id = s.season_id and t.student_id = s.student_id
  where s.tier_sort < t.tier_sort;
  get diagnostics v_tut = row_count;

  raise notice 'Báo cộng bù % em; tính lại % em; % em tụt bậc', v_bu, v_n, v_tut;
end $$;
