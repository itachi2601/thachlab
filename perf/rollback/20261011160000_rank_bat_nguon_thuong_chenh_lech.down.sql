-- Hoàn tác phần cấu hình; RP đã cộng bù KHÔNG tự thu hồi (cần thì báo để làm riêng).
delete from public.rank_sources rs using public.rank_sources_backup_20261011 b
  where rs.season_id = b.season_id and rs.source_kind = b.source_kind and rs.source_id = b.source_id;
update public.rank_seasons set config = coalesce(config, '{}'::jsonb) || '{"rp_first_attempt_only": 1}'::jsonb where id = 4;
