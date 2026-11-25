-- Gọi tên ngẫu nhiên trong bài học (nút "Gọi tên" ở /lop-hoc/bai, chỉ giáo viên/trợ giảng thấy).
-- user_classes chỉ admin đọc thẳng được (RLS "read own user classes"), nên thêm một hàm SECURITY DEFINER
-- trả danh sách HS đang học (status active, role student, bỏ tài khoản thử) của MỘT lớp cho người dạy lớp đó.
-- Chỉ đọc, không thêm bảng, không ghi gì. Ai được gọi trong buổi lưu ở trình duyệt (localStorage) của thầy.
begin;

create or replace function public.class_call_roster(p_class_id bigint)
returns table (student_id uuid, full_name text)
language sql
security definer
stable
set search_path = public
as $$
  select p.id, coalesce(nullif(trim(p.full_name), ''), 'Học sinh') as full_name
  from public.user_classes uc
  join public.profiles p on p.id = uc.user_id
  where uc.class_id = p_class_id
    and uc.status = 'active'
    and p.role = 'student'
    and coalesce(p.is_test, false) = false
    and (public.is_admin() or public.manages_class(p_class_id) or public.assists_class(p_class_id))
  order by p.full_name;
$$;

revoke all on function public.class_call_roster(bigint) from public, anon;
grant execute on function public.class_call_roster(bigint) to authenticated;

commit;

-- Rollback:
-- drop function if exists public.class_call_roster(bigint);
