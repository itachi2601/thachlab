-- Thẻ "Thông tin tài khoản" trong hồ sơ học sinh: admin / giáo viên phụ trách xem username, email đăng nhập,
-- email liên hệ, SĐT, SĐT phụ huynh, ngày sinh, giới tính, lần đăng nhập cuối. Dữ liệu nằm ở auth.users nên
-- cần security definer; tự kiểm quyền bằng is_admin() / teaches_student(). Mật khẩu được mã hoá một chiều — không có
-- cách đọc lại, chỉ đặt lại (PasswordResetCard).
create or replace function public.staff_student_account(p_student uuid)
returns table (
  login_email text,
  username text,
  contact_email text,
  phone text,
  parent_phone text,
  birth_date text,
  gender text,
  student_code text,
  created_at timestamptz,
  last_sign_in_at timestamptz,
  from_roster boolean
)
language plpgsql
stable
security definer
set search_path = public, auth
as $$
begin
  if not (public.is_admin() or public.teaches_student(p_student)) then
    raise exception 'Không có quyền xem tài khoản này.' using errcode = '42501';
  end if;
  return query
  select u.email::text,
         coalesce(nullif(u.raw_user_meta_data->>'username', ''), nullif(p.student_code, ''), split_part(u.email, '@', 1)),
         nullif(u.raw_user_meta_data->>'contact_email', ''),
         nullif(u.raw_user_meta_data->>'phone', ''),
         nullif(u.raw_user_meta_data->>'parent_phone', ''),
         coalesce(nullif(u.raw_user_meta_data->>'birth_date', ''), p.birth_date::text),
         nullif(u.raw_user_meta_data->>'gender', ''),
         p.student_code,
         u.created_at,
         u.last_sign_in_at,
         (u.raw_user_meta_data->>'username') is null
  from auth.users u
  left join public.profiles p on p.id = u.id
  where u.id = p_student;
end;
$$;

revoke all on function public.staff_student_account(uuid) from public, anon;
grant execute on function public.staff_student_account(uuid) to authenticated;

-- ROLLBACK:
-- drop function if exists public.staff_student_account(uuid);
