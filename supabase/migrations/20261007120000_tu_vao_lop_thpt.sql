-- Alpha test miễn phí (7/10/2026): học sinh THPT tự vào khối lớp, không cần giáo viên duyệt.
-- CTTC không đổi (vẫn cần mã khóa, bảng course_enrollments).
begin;

-- Sao lưu các yêu cầu đang chờ trước khi chuyển thành active.
create table public.user_classes_backup_20261007 as
  select * from public.user_classes where status = 'pending';
alter table public.user_classes_backup_20261007 enable row level security;
revoke all on public.user_classes_backup_20261007 from anon, authenticated;

drop policy if exists "students request own class" on public.user_classes;
create policy "students request own class" on public.user_classes
  as permissive for insert to authenticated
  with check (user_id = (select auth.uid()) and status in ('pending', 'active'));

drop policy if exists "students resubmit rejected class request" on public.user_classes;
create policy "students resubmit rejected class request" on public.user_classes
  as permissive for update to authenticated
  using (user_id = (select auth.uid()) and status in ('rejected', 'pending'))
  with check (user_id = (select auth.uid()) and status = 'active');

-- Yêu cầu đang chờ từ trước: duyệt luôn theo quy tắc mới.
update public.user_classes set status = 'active', reviewed_at = now() where status = 'pending';

commit;

-- ROLLBACK (chỉ khi cần):
-- begin;
-- drop policy "students request own class" on public.user_classes;
-- create policy "students request own class" on public.user_classes as permissive for insert to authenticated
--   with check (user_id = (select auth.uid()) and status = 'pending');
-- drop policy "students resubmit rejected class request" on public.user_classes;
-- create policy "students resubmit rejected class request" on public.user_classes as permissive for update to authenticated
--   using (user_id = (select auth.uid()) and status = 'rejected') with check (user_id = (select auth.uid()) and status = 'pending');
-- update public.user_classes uc set status='pending', reviewed_at=null from public.user_classes_backup_20261007 b where uc.user_id=b.user_id and uc.class_id=b.class_id;
-- commit;
