-- Cho phép Edge Function import-roster nhập danh sách vào khối lớp THPT (body.classId).
-- RPC can_manage_class song song với can_manage_course (supabase-migration-course-instructors.sql):
-- true nếu là admin, hoặc giảng viên được phân công đúng khối lớp này (class_instructors).
-- Idempotent; chạy sau supabase-migration-class-instructors.sql.

create or replace function public.can_manage_class(p_class_id bigint)
returns boolean language sql security definer stable set search_path = public
as $$
  select public.is_admin() or exists (
    select 1 from public.class_instructors
    where class_id = p_class_id and instructor_id = auth.uid()
  );
$$;

-- Không cần policy user_classes mới: Edge Function ghi bằng service_role (bypass RLS) sau khi
-- đã tự kiểm tra quyền qua can_manage_class ở trên.
