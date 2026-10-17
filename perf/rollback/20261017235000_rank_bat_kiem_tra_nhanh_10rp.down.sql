-- Hoàn tác 20261017235000: gỡ các đề vừa bật khỏi rank_sources (RP đã cộng bù không tự thu hồi; chạy
-- rank_recompute_season(<mùa>) nếu cần tính lại).
delete from public.rank_sources rs using public.rank_sources_backup_20261017b b
  where rs.season_id = b.season_id and rs.source_kind = b.source_kind and rs.source_id = b.source_id;
drop table if exists public.rank_sources_backup_20261017b;
