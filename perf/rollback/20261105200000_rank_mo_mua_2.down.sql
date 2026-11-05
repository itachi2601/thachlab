-- Hoàn tác 20261105200000_rank_mo_mua_2.sql
--   1. Xoá 4 mùa mới. FK on delete cascade dọn theo season_id: rank_tiers, rank_sources, rank_rp_awards, rank_rp_ledger,
--      rank_student_seasons, rank_gate_passes, rank_gate_attempts, rank_fix_attempts, rank_season_results, rank_tier_floor.
--      rank_title_awards.season_id và student_mistake_review_attempts.season_id chỉ set null — danh hiệu em đã nhận GIỮ NGUYÊN.
--   2. Mở lại mùa 5 "Alpha test" (active, closed_at null) và xoá kết quả mùa 5 vừa chụp lúc đóng.
-- KHÔNG gỡ: chuông "+N RP" đã gửi khi recompute (notifications kind 'rp_bonus'), thành tích rank_eval_achievements đã cấp.
-- Lưu ý: nếu HS đã làm bài/thi cửa ở mùa mới thì lịch sử đó mất theo cascade — chỉ dùng ngay sau khi chạy.
begin;

delete from public.rank_seasons
 where name in ('Mùa 2 · Lôi Đình Cảm Ứng', 'Mùa 2 · Thợ Săn Sóng', 'Mùa 2 · Kỷ Nguyên Newton', 'Mùa 1 · Bẻ Cong Ánh Sáng')
   and starts_on = date '2026-11-02';

delete from public.rank_season_results
 where season_id = 5 and closed_at >= timestamptz '2026-11-05 00:00+07';

update public.rank_seasons
   set status = 'active', closed_at = null
 where id = 5 and name = 'Alpha test' and status = 'closed' and closed_at >= timestamptz '2026-11-05 00:00+07';

commit;

select id, name, status, closed_at,
       (select count(*) from public.rank_season_results x where x.season_id = s.id) as results
from public.rank_seasons s order by id;
