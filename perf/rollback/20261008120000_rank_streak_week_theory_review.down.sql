-- Hoàn tác 20261008120000_rank_streak_week_theory_review.sql. RP ôn lại đã cộng: xoá awards/ledger có ref 'theory_review:%' rồi gọi rank_recompute_season.
drop function if exists public.rank_theory_review_submit(bigint, jsonb);
drop function if exists public.rank_theory_review_open(bigint);
drop function if exists public.rank_my_streak_days(int);
delete from public.rank_rp_awards where source_kind = 'theory' and source_ref like 'theory\_review:%';
drop table if exists public.theory_reviews;
