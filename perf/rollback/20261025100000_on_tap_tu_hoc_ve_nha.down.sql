-- Rollback chế độ Tự học ở nhà. Buổi 'live' chạy y như trước; cột mode/due_at/sequential để lại vô hại.
begin;
drop function if exists public.review_session_meta(bigint);
drop function if exists public.review_create_self(bigint, text, int, jsonb, timestamptz, boolean);
commit;
