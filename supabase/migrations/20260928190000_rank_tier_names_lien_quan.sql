-- ============================================================================
-- feat(rank): đổi tên các bậc rank theo bậc rank Liên Quân Mobile, 28/9/2026
-- ============================================================================
-- CHƯA CHẠY LÊN PRODUCTION. Chạy: bash scripts/run-migrations.sh (hoặc
-- supabase db query --linked -f supabase/migrations/20260928190000_rank_tier_names_lien_quan.sql).
-- Idempotent — chạy lại được. Không đổi bảng/cột/`code`/min_rp/điều kiện lên bậc,
-- chỉ đổi cột `name` (nhãn hiển thị cho học sinh) + hàm gieo tên mùa mới.
--
-- Đổi theo đúng 7 bậc đầu của Liên Quân Mobile (Đồng → Cao Thủ, thấp lên cao).
-- "Thách Đấu" (bậc thứ 8 của LQM) dùng cho danh vị Vô Song/Paragon phía frontend
-- (features/rank/types.ts PARAGON_META) — không thêm dòng vào rank_tiers vì Vô Song
-- không nằm trên thang RP, xem supabase/migrations/20260926100000_rank_paragon.sql.
-- ============================================================================

-- Hàm gieo bậc mặc định cho mùa mới — đổi tên hiển thị, giữ nguyên code/min_rp/điều kiện.
create or replace function public.rank_seed_tiers(p_season bigint)
returns void
language sql security definer set search_path = public
as $$
  insert into public.rank_tiers (season_id, code, sort, name, min_rp, has_divisions, required_title_count, required_title_level)
  values
    (p_season, 'tan_binh',   1, 'Đồng',      0,    true,  0, null),
    (p_season, 'chien_binh', 2, 'Bạc',       200,  true,  0, null),
    (p_season, 'tinh_anh',   3, 'Vàng',      500,  true,  1, 'thuc_tinh'),
    (p_season, 'tinh_nhue',  4, 'Bạch Kim',  900,  true,  2, 'thuc_tinh'),
    (p_season, 'dai_su',     5, 'Kim Cương', 1400, true,  1, 'lam_chu'),
    (p_season, 'cao_thu',    6, 'Tinh Anh',  2000, false, 2, 'lam_chu'),
    (p_season, 'thach_dau',  7, 'Cao Thủ',   2600, false, 3, 'lam_chu')
  on conflict (season_id, code) do nothing;
$$;

-- Đổi tên các dòng bậc đã gieo cho MỌI mùa hiện có (kể cả mùa đã đóng) — chỉ đổi nhãn
-- hiển thị, không đụng min_rp/điều kiện/sort nên an toàn với dữ liệu RP đã tính.
update public.rank_tiers set name = 'Đồng'      where code = 'tan_binh';
update public.rank_tiers set name = 'Bạc'       where code = 'chien_binh';
update public.rank_tiers set name = 'Vàng'      where code = 'tinh_anh';
update public.rank_tiers set name = 'Bạch Kim'  where code = 'tinh_nhue';
update public.rank_tiers set name = 'Kim Cương' where code = 'dai_su';
update public.rank_tiers set name = 'Tinh Anh'  where code = 'cao_thu';
update public.rank_tiers set name = 'Cao Thủ'   where code = 'thach_dau';

-- ============================================================================
-- ROLLBACK (perf/rollback/20260928190000_rank_tier_names_lien_quan.down.sql):
--   supabase db query --linked -f perf/rollback/20260928190000_rank_tier_names_lien_quan.down.sql
-- Nội dung: khôi phục hàm rank_seed_tiers + tên 7 bậc về bộ tên cũ (Tinh Quang…Chí Tôn).
-- ============================================================================
