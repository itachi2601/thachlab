-- Rollback cho supabase/migrations/20260928160000_rank_public_honor.sql
-- Gỡ RPC vinh danh trang chủ + cột mức lộ tên. Client tự ẩn mục khi RPC không còn.
-- Chạy: supabase db query --linked -f perf/rollback/20260928160000_rank_public_honor.down.sql

drop function if exists public.rank_public_honor();
drop function if exists public.rank_set_honor_visibility(text);
drop function if exists public.rank_honor_name(text, text);
alter table public.profiles drop column if exists honor_visibility;
