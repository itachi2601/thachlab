-- Xét lại danh hiệu chuyên môn theo logic mới (3 mức theo đúng độ khó Dễ/TB/Khó)
-- cho mọi học sinh trong 2 mùa đang mở — CHẠY SAU khi migration
-- 20260928100000_rank_specialist_difficulty.sql đã chạy xong (migration đó backfill
-- cột difficulty cho các lượt làm cũ; recompute này chỉ xét lại danh hiệu bằng dữ
-- liệu vừa backfill, không đụng RP).
-- Không phải migration schema — chỉ gọi lại RPC có sẵn (rank_recompute_season).
-- An toàn chạy lại nhiều lần: rank_grant_title() có khoá unique
-- (student_id, title_code, level) — chỉ MỞ THÊM danh hiệu đã đủ điều kiện,
-- không thu hồi danh hiệu cũ.
--
-- Chạy: supabase db query --linked -f docs/supabase-recompute-rank-titles-20260928.sql

select set_config(
  'request.jwt.claims',
  json_build_object('sub', 'fc1b6773-f1f2-4b2d-9359-76258054ba19', 'role', 'authenticated')::text,
  true
);

select public.rank_recompute_season(4); -- Mùa thử nghiệm — lớp 11 + 12
select public.rank_recompute_season(5); -- Alpha test — lớp 10
