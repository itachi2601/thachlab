-- Rollback 20261122110500_luyen_tap_cham_server_buoc_2: dựng lại y nguyên 2 policy INSERT (bản 20260925140000_perf_rls).
begin;

drop policy if exists "student inserts own practice sessions" on public.practice_sessions;
create policy "student inserts own practice sessions" on public.practice_sessions
  as permissive
  for insert
  to authenticated
  with check ((student_id = (select auth.uid())));

drop policy if exists "student inserts own practice question results" on public.practice_question_results;
create policy "student inserts own practice question results" on public.practice_question_results
  as permissive
  for insert
  to authenticated
  with check ((student_id = (select auth.uid())));

commit;
