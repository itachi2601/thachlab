-- Rollback 20260930150000_rank_teacher_reports.sql: chỉ có 2 hàm đọc, xoá là xong.
drop function if exists public.rank_monday_list(bigint);
drop function if exists public.rank_quartile_metrics(bigint);
