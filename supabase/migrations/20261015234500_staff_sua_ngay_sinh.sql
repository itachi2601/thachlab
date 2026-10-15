-- 20261015234500_staff_sua_ngay_sinh.sql
-- Thầy/trợ giảng phụ trách sửa ngày sinh học sinh ở thẻ "Liên lạc gia đình" (cạnh SĐT) — 165/291 em THPT chưa
-- có ngày sinh (vào hệ thống không qua /dang-ky có ô ngày sinh), mà phụ huynh tự nối con cần ngày sinh.
-- Ghi CẢ profiles.birth_date (claim_parent_by_child_info đọc) LẪN metadata birth_date (staff_student_account
-- ưu tiên đọc metadata) để hai nơi không lệch nhau. Cùng quyền với staff_set_student_phones.
-- Chạy lúc nào cũng được (chỉ thêm một hàm).

create or replace function public.staff_set_student_birth(p_student uuid, p_birth date)
returns void
language plpgsql
security definer
set search_path = public, auth
as $$
begin
  if not (public.is_admin() or public.teaches_student(p_student)) then
    raise exception 'Không có quyền sửa học sinh này.' using errcode = '42501';
  end if;
  if p_birth is not null and extract(year from p_birth) not between 1990 and 2015 then
    raise exception 'Ngày sinh không hợp lệ (năm phải từ 1990 đến 2015).';
  end if;
  update public.profiles set birth_date = p_birth where id = p_student;
  update auth.users
     set raw_user_meta_data = coalesce(raw_user_meta_data, '{}'::jsonb)
                              || jsonb_build_object('birth_date', coalesce(to_char(p_birth, 'YYYY-MM-DD'), ''))
   where id = p_student;
end;
$$;

revoke all on function public.staff_set_student_birth(uuid, date) from public, anon;
grant execute on function public.staff_set_student_birth(uuid, date) to authenticated;

-- ROLLBACK:
-- drop function if exists public.staff_set_student_birth(uuid, date);
