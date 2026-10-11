-- Hoàn tác cấu hình mùa 5 (RP đã cộng bù không tự thu hồi).
delete from public.rank_sources rs using public.rank_sources_backup_20261011 b
  where b.season_id = 5 and rs.season_id = b.season_id and rs.source_kind = b.source_kind and rs.source_id = b.source_id;
update public.rank_seasons set config = coalesce(config, '{}'::jsonb) || '{"rp_first_attempt_only": 1}'::jsonb where id = 5;
