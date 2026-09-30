-- ============================================================================
-- Kênh phụ đạo — bài tự kiểm tra: học sinh đọc được câu ngân hàng ở cả các yêu cầu cần đạt CON
-- của bài đang cần phụ đạo. Trước đây policy chỉ khớp topic_id = bài, trong khi câu hỏi phần lớn
-- gắn ở tầng con (parent_id = bài) nên học sinh nhận rỗng ("Ngân hàng chưa có câu nào").
-- Chỉ thay policy; không đổi bảng/dữ liệu. Chạy ngoài giờ HS làm bài càng tốt (đổi policy nhanh).
--
-- Cách chạy: supabase db query --linked -f supabase/migrations/20260930160000_exit_quiz_bank_children.sql
-- Rollback:  supabase db query --linked -f perf/rollback/20260930160000_exit_quiz_bank_children.down.sql
-- ============================================================================
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
