-- Hoàn tác: bỏ sàn bậc (hàm rank_refresh_student bản có sàn vẫn chạy được khi bảng rỗng). Sau đó rank_recompute_season(4) và (5).
delete from public.rank_tier_floor where reason like 'Giữ bậc sau khi nâng ngưỡng%';
