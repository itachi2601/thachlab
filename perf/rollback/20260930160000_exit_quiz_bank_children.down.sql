-- Rollback cho supabase/migrations/20260930160000_exit_quiz_bank_children.sql (trả lại policy chỉ khớp đúng tầng bài)
drop policy if exists "student reads exit-quiz bank questions" on public.question_bank;
create policy "student reads exit-quiz bank questions" on public.question_bank
  as permissive
  for select
  to authenticated
  using (
    archived = false
    and exists (
      select 1 from public.tutoring_needs n
      where n.student_id = (select auth.uid())
        and n.topic_id = question_bank.topic_id
        and n.status in ('open', 'assigned', 'tutored')
    )
  );
