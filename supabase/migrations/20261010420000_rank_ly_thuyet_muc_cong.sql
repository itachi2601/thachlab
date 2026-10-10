-- ============================================================================
-- config(rank): mức cộng RP bài lý thuyết (thầy chốt 10/10/2026)
--   theory_rp 15 · theory_bonus2 3 · theory_bonus3 5 · theory_min_time_pct 30 · theory_day_cap 45 · theory_week_cap 100
--   theory_review_rp 5 · theory_review_max_rounds 3
-- Giữ: đúng >= 70%, ôn lại cách >= 3 ngày, trần mùa 25%, không trả RP theo thời gian ngồi.
-- Chỉ merge vào rank_seasons.config của mùa đang mở (giữ khoá khác). Chưa có em nào nộp lý thuyết
-- (theory_sessions = 0 lúc 10/10) nên không có RP cũ cần tính lại; rank_award chỉ tăng nên đổi số không làm giảm RP ai.
-- Rollback: update rank_seasons set config = config - 'theory_rp' - 'theory_bonus2' - 'theory_bonus3' - 'theory_min_time_pct'
--   - 'theory_day_cap' - 'theory_week_cap' - 'theory_review_rp' - 'theory_review_max_rounds' where status = 'active';
-- ============================================================================
update public.rank_seasons
  set config = coalesce(config, '{}'::jsonb) || jsonb_build_object(
    'theory_rp', 15, 'theory_bonus2', 3, 'theory_bonus3', 5, 'theory_min_time_pct', 30,
    'theory_day_cap', 45, 'theory_week_cap', 100, 'theory_review_rp', 5, 'theory_review_max_rounds', 3)
  where status = 'active';
