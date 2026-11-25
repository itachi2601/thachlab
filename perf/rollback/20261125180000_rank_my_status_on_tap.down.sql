-- Rollback 20261125180000_rank_my_status_on_tap.sql — trả rank_my_status về định nghĩa nguyên văn của
-- 20260925140000_perf_rls.sql (bỏ trường on_tap_den_han). Client chỉ coi trường này là tuỳ chọn.
begin;

CREATE OR REPLACE FUNCTION public.rank_my_status()
 RETURNS jsonb
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$ select public.rank_status_of((select auth.uid())); $function$;

commit;
