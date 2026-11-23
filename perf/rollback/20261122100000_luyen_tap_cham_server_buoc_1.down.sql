-- Rollback 20261122100000_luyen_tap_cham_server_buoc_1: bỏ hàm practice_session_submit.
-- Chỉ chạy khi bước 2 (20261122110500) CHƯA chạy hoặc đã rollback — nếu không HS không lưu được phiên luyện tập nào.
begin;
drop function if exists public.practice_session_submit(uuid, bigint, bigint, jsonb, jsonb, int, boolean, timestamptz);
commit;
