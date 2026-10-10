-- Rollback 20261010400000: khôi phục hai hàm về bản trước và weekly_goal_rp = 90 ở mùa 4.
-- Bản hàm cũ nằm ở supabase/migrations/20260930120000_rank_gd1b_spacing_progress.sql (rank_eval_progress_week)
-- và 20260929130000_rank_weekly_goal_adaptive.sql (rank_eval_weekly_goal): chạy lại đúng khối create or replace của hai hàm đó.
update public.rank_seasons set config = config || '{"weekly_goal_rp": 90}'::jsonb where id = 4;
update public.rank_seasons set config = config - 'weekly_goal_score_floor' where status = 'active';
