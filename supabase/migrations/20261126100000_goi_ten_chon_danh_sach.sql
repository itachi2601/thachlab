-- Gọi tên ngẫu nhiên: cho thầy CHỌN danh sách để gọi (lớp THPT hoặc khoá CTTC như "CĐN CGKL 25A"),
-- không chỉ lớp gắn với chương. Thêm 2 hàm chỉ đọc, SECURITY DEFINER:
--   call_roster_lists()            → các danh sách người gọi được dạy (lớp: manages/assists_class; khoá: can_manage_course)
--   course_call_roster(p_course_id) → HS đang học (course_enrollments.status = 'active') của một khoá
-- Không thêm bảng, không ghi gì. Đi sau 20261126090000_goi_ten_ngau_nhien.sql (class_call_roster).
begin;

create or replace function public.call_roster_lists()
returns table (kind text, id bigint, name text, n int)
language sql
security definer
stable
set search_path = public
as $$
  select 'class'::text, c.id, c.name,
         (select count(*)::int from public.user_classes uc join public.profiles p on p.id = uc.user_id
          where uc.class_id = c.id and uc.status = 'active' and p.role = 'student' and coalesce(p.is_test, false) = false)
  from public.classes c
  where c.active and (public.manages_class(c.id) or public.assists_class(c.id))
  union all
  select 'course'::text, o.id, o.name,
         (select count(*)::int from public.course_enrollments e join public.profiles p on p.id = e.student_id
          where e.course_id = o.id and e.status = 'active' and coalesce(p.is_test, false) = false)
  from public.course_offerings o
  where o.status = 'active' and public.can_manage_course(o.id);
$$;

create or replace function public.course_call_roster(p_course_id bigint)
returns table (student_id uuid, full_name text)
language sql
security definer
stable
set search_path = public
as $$
  select p.id, coalesce(nullif(trim(p.full_name), ''), 'Học sinh') as full_name
  from public.course_enrollments e
  join public.profiles p on p.id = e.student_id
  where e.course_id = p_course_id
    and e.status = 'active'
    and coalesce(p.is_test, false) = false
    and public.can_manage_course(p_course_id)
  order by p.full_name;
$$;

revoke all on function public.call_roster_lists() from public, anon;
revoke all on function public.course_call_roster(bigint) from public, anon;
grant execute on function public.call_roster_lists() to authenticated;
grant execute on function public.course_call_roster(bigint) to authenticated;

commit;

-- Rollback: perf/rollback/20261126100000_goi_ten_chon_danh_sach.down.sql
