-- Rollback 20261111190000_va_bao_mat_buoc_1_ham_moi.sql (chỉ chạy khi client đã quay về bản cũ).
begin;
drop function if exists public.notify_user_staff(uuid, text, text, text, text);
drop function if exists public.get_cnc_quiz_banks(text[]);
drop function if exists public.cnc_milling_quiz_save(bigint, uuid, text, text, jsonb, integer, integer, text);

create policy "classroom creates live checklist attempts"
  on public.cnc_milling_checklist_attempts for insert to anon, authenticated
  with check (participant_key is not null and length(trim(participant_name)) > 0);
create policy "classroom updates live checklist attempts"
  on public.cnc_milling_checklist_attempts for update to anon, authenticated
  using (true)
  with check (participant_key is not null and length(trim(participant_name)) > 0);
commit;
-- get_student_learning_history + exam_has_essay: để nguyên (kết quả y như bản cũ); bản cũ ở 20260925130000_perf_rpc_gv.sql.
-- rank_fix_quiz_submit(bigint, integer): KHÔNG khôi phục (bản nhận số câu đúng từ máy là lỗ hổng);
-- nếu buộc phải có lại, định nghĩa gốc nằm ở docs/supabase-migration-rank-system.sql.
