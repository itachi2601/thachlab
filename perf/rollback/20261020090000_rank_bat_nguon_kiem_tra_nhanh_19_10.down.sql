-- Hoàn tác 20261020090000: gỡ 3 đề khỏi rank_sources (RP đã cộng bù không tự thu hồi; chạy rank_recompute_season nếu cần).
delete from public.rank_sources rs using public.rank_sources_backup_20261020 b
  where rs.season_id = b.season_id and rs.source_kind = b.source_kind and rs.source_id = b.source_id;
drop table if exists public.rank_sources_backup_20261020;
