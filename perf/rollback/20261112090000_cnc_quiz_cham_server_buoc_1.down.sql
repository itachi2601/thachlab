-- Rollback 20261112090000: bỏ 2 hàm chấm quiz CNC ở server. Chỉ chạy khi client đã quay về bản gọi record_cnc_learning_result
-- và bước 2 (20261112100000) đã rollback.
begin;
drop function if exists public.cnc_quiz_submit(bigint, text, text, jsonb);
drop function if exists public.cnc_quiz_bank_of(text, text);
commit;
