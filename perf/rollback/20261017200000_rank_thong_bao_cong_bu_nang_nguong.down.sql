-- Hoàn tác ngưỡng bậc (thông báo đã gửi không thu hồi). Sau đó chạy lại rank_recompute_season(4) và (5) bằng JWT staff.
update public.rank_tiers t set min_rp = b.min_rp from public.rank_tiers_backup_20261017 b
  where t.season_id = b.season_id and t.code = b.code;
