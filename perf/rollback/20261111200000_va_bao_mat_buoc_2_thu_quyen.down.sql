-- Rollback 20261111200000_va_bao_mat_buoc_2_thu_quyen.sql: trả quyền như trước 11/11/2026.
begin;
grant select on public.exams to anon, authenticated;
grant execute on function public.notify_user(uuid, text, text, text, text) to authenticated;
grant execute on function public.rank_gate_pool_ids(bigint, uuid, text) to anon, authenticated;

create policy "classroom creates live milling attempts"
  on public.cnc_milling_quiz_attempts for insert to anon, authenticated
  with check (participant_key is not null and length(trim(participant_name)) > 0);
create policy "classroom updates live milling attempts"
  on public.cnc_milling_quiz_attempts for update to anon, authenticated
  using (true)
  with check (participant_key is not null and length(trim(participant_name)) > 0);
commit;
