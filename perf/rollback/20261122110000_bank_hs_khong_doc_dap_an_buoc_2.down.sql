-- Rollback 20261122110000_bank_hs_khong_doc_dap_an_buoc_2: dựng lại y nguyên 3 policy cũ
-- (bản 20260930160000_exit_quiz_bank_children, 20261017220000_chan_doan_doc_ngan_hang, 20260925140000_perf_rls).
begin;

drop policy if exists "student reads exit-quiz bank questions" on public.question_bank;
create policy "student reads exit-quiz bank questions" on public.question_bank
  as permissive
  for select
  to authenticated
  using (
    archived = false
    and exists (
      select 1
      from public.tutoring_needs n
      where n.student_id = (select auth.uid())
        and n.status in ('open', 'assigned', 'tutored')
        and (
          n.topic_id = question_bank.topic_id
          or exists (
            select 1 from public.question_topics t
            where t.id = question_bank.topic_id and t.parent_id = n.topic_id
          )
        )
    )
  );

drop policy if exists "student reads entry-diagnostic bank questions" on public.question_bank;
create policy "student reads entry-diagnostic bank questions" on public.question_bank
  as permissive
  for select
  to authenticated
  using (
    archived = false
    and (
      topic_id in (select unnest(public.diagnostic_bank_topic_ids()))
      or exists (
        select 1 from public.question_topics t
        where t.id = question_bank.topic_id and t.parent_id in (select unnest(public.diagnostic_bank_topic_ids()))
      )
    )
  );

drop policy if exists "student logs own exit attempt" on public.tutoring_exit_attempts;
create policy "student logs own exit attempt" on public.tutoring_exit_attempts
  as permissive
  for insert
  to authenticated
  with check ((student_id = (select auth.uid())));

commit;
