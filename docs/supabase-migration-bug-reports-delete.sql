-- Cho phép admin xoá báo lỗi/đề xuất (và ảnh chụp màn hình đính kèm).
-- Chạy sau docs/supabase-migration-bug-reports.sql. Idempotent.

drop policy if exists "admin deletes bug reports" on public.bug_reports;
create policy "admin deletes bug reports" on public.bug_reports
  for delete to authenticated
  using (public.is_admin());

drop policy if exists "admin deletes bug report screenshots" on storage.objects;
create policy "admin deletes bug report screenshots" on storage.objects
  for delete to authenticated
  using (bucket_id = 'bug-report-screenshots' and public.is_admin());
