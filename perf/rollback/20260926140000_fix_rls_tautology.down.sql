-- Rollback cho supabase/migrations/20260926140000_fix_rls_tautology.sql
--
-- Khôi phục lại đúng định nghĩa đang chạy trên production TRƯỚC migration này —
-- LƯU Ý: 2 policy attendance_sessions/equipment_breakdown_reports quay lại có
-- BUG (tautology, đọc chéo mọi khoá) và class_assessments quay lại `using (true)`
-- (đọc được toàn bảng). Chỉ chạy nếu migration trên gây lỗi thật cho ứng dụng,
-- không dùng để "quay lại an toàn".
--
-- Chạy: supabase db query --linked -f perf/rollback/20260926140000_fix_rls_tautology.down.sql

begin;

drop policy if exists "students read course attendance sessions" on public.attendance_sessions;
create policy "students read course attendance sessions" on public.attendance_sessions
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM course_enrollments e
  WHERE ((e.course_id = e.course_id) AND (e.student_id = (select auth.uid())) AND (e.status = 'active'::text))))));

drop policy if exists "students read equipment breakdown reports" on public.equipment_breakdown_reports;
create policy "students read equipment breakdown reports" on public.equipment_breakdown_reports
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM course_enrollments e
  WHERE ((e.course_id = e.course_id) AND (e.student_id = (select auth.uid())) AND (e.status = 'active'::text))))));

drop policy if exists "class members read class assessments" on public.class_assessments;
create policy "anyone reads class assessments" on public.class_assessments
  for select to authenticated using (true);

commit;
