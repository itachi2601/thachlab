-- Rollback 20261010500000_notify_rp_thuong.sql (thông báo đã gửi giữ nguyên; muốn xoá: delete from notifications where kind = 'rp_bonus')
drop trigger if exists trg_notify_rp_bonus on public.rank_rp_ledger;
drop function if exists public.trg_notify_rp_bonus();
