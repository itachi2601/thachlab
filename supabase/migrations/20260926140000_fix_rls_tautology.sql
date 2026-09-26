-- ============================================================================
-- Vá 2 lỗ hổng RLS phát hiện ở đợt tối ưu tốc độ 9/2026, chưa ai sửa
-- (perf/RESULT.md §9 mục 1–2, ghi vào docs/STATE.md "Lỗ hổng bảo mật cần vá sớm").
--
-- 1) attendance_sessions ("students read course attendance sessions") và
--    equipment_breakdown_reports ("students read equipment breakdown reports"):
--    điều kiện `e.course_id = e.course_id` (so cột với chính nó) LUÔN ĐÚNG ->
--    học sinh chỉ cần có 1 lượt ghi danh active ở BẤT KỲ khoá nào là đọc được
--    buổi điểm danh / báo hỏng máy của MỌI khoá khác, không riêng khoá mình học.
--    Sửa: so đúng course_id của session/report đang xét
--    (`e.course_id = attendance_sessions.course_id`, tương tự cho bảng kia).
--
-- 2) class_assessments ("anyone reads class assessments"): `using (true)` ->
--    mọi tài khoản đã đăng nhập đọc được toàn bộ bảng, kể cả lớp không thuộc về
--    (exam_id, kind, sequence, published_at của mọi lớp). Sửa: chỉ GV/admin quản
--    lớp đó (manages_class, đã tự gồm is_admin()) hoặc học sinh có trong lớp đó
--    (user_classes) mới đọc được — giữ nguyên quyền của "staff manage class
--    assessments" (for all) đang chạy song song, chỉ thay policy đọc.
--
-- Không đổi is_admin()/manages_class(), không đổi bảng nào khác. Idempotent
-- (drop policy if exists trước khi tạo lại).
--
-- Chạy: bash scripts/run-migrations.sh (hoặc supabase db query --linked -f <file>)
-- KHÔNG dùng `supabase db push`. Rollback: perf/rollback/20260926140000_fix_rls_tautology.down.sql
-- ============================================================================

begin;

drop policy if exists "students read course attendance sessions" on public.attendance_sessions;
create policy "students read course attendance sessions" on public.attendance_sessions
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM course_enrollments e
  WHERE ((e.course_id = attendance_sessions.course_id) AND (e.student_id = (select auth.uid())) AND (e.status = 'active'::text))))));

drop policy if exists "students read equipment breakdown reports" on public.equipment_breakdown_reports;
create policy "students read equipment breakdown reports" on public.equipment_breakdown_reports
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM course_enrollments e
  WHERE ((e.course_id = equipment_breakdown_reports.course_id) AND (e.student_id = (select auth.uid())) AND (e.status = 'active'::text))))));

drop policy if exists "anyone reads class assessments" on public.class_assessments;
create policy "class members read class assessments" on public.class_assessments
  as permissive
  for select
  to authenticated
  using ((manages_class(class_id) OR (EXISTS ( SELECT 1
   FROM user_classes uc
  WHERE ((uc.class_id = class_assessments.class_id) AND (uc.user_id = (select auth.uid())))))));

commit;
