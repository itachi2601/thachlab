-- Backfill RP cho các đề Kiểm tra vừa được bật làm nguồn RP (lớp 10/11/12).
-- Không phải migration schema — chỉ gọi lại RPC có sẵn (rank_recompute_season)
-- để tính RP cho các lượt làm bài ĐÃ có từ trước lúc nguồn được bật enabled=true.
-- An toàn chạy lại nhiều lần: rank_award() chỉ cộng phần chênh lệch (delta),
-- có khoá unique (season_id, student_id, source_kind, source_ref).
--
-- Chạy: supabase db query --linked -f docs/supabase-recompute-rank-backfill-20260927.sql

select set_config(
  'request.jwt.claims',
  json_build_object('sub', 'fc1b6773-f1f2-4b2d-9359-76258054ba19', 'role', 'authenticated')::text,
  true
);

select public.rank_recompute_season(4); -- Mùa thử nghiệm — lớp 11 + 12
select public.rank_recompute_season(5); -- Alpha test — lớp 10
