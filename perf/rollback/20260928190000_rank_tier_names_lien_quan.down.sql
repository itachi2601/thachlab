-- Rollback 20260928190000_rank_tier_names_lien_quan.sql:
-- khôi phục hàm rank_seed_tiers + tên 7 bậc rank về bộ tên cũ (Tinh Quang…Chí Tôn),
-- trước khi đổi sang bộ tên Liên Quân Mobile (Đồng…Cao Thủ).

create or replace function public.rank_seed_tiers(p_season bigint)
returns void
language sql security definer set search_path = public
as $$
  insert into public.rank_tiers (season_id, code, sort, name, min_rp, has_divisions, required_title_count, required_title_level)
  values
    (p_season, 'tan_binh',   1, 'Tinh Quang', 0,    true,  0, null),
    (p_season, 'chien_binh', 2, 'Tiên Phong', 200,  true,  0, null),
    (p_season, 'tinh_anh',   3, 'Nhật Hoa',   500,  true,  1, 'thuc_tinh'),
    (p_season, 'tinh_nhue',  4, 'Vương Lễ',   900,  true,  2, 'thuc_tinh'),
    (p_season, 'dai_su',     5, 'Vương Triều', 1400, true,  1, 'lam_chu'),
    (p_season, 'cao_thu',    6, 'Thiên Thể',  2000, false, 2, 'lam_chu'),
    (p_season, 'thach_dau',  7, 'Chí Tôn',    2600, false, 3, 'lam_chu')
  on conflict (season_id, code) do nothing;
$$;

update public.rank_tiers set name = 'Tinh Quang'   where code = 'tan_binh';
update public.rank_tiers set name = 'Tiên Phong'   where code = 'chien_binh';
update public.rank_tiers set name = 'Nhật Hoa'     where code = 'tinh_anh';
update public.rank_tiers set name = 'Vương Lễ'     where code = 'tinh_nhue';
update public.rank_tiers set name = 'Vương Triều'  where code = 'dai_su';
update public.rank_tiers set name = 'Thiên Thể'    where code = 'cao_thu';
update public.rank_tiers set name = 'Chí Tôn'      where code = 'thach_dau';
