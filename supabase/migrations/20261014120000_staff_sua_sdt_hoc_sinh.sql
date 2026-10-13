-- Thầy/trợ giảng phụ trách sửa SĐT học sinh + SĐT phụ huynh ngay trong hồ sơ (trước đây chỉ xem).
-- SĐT nằm ở auth.users.raw_user_meta_data (phone, parent_phone) — hàm này chỉ ghi hai khoá đó.
-- Thêm: hàm staff_set_student_phones. Không đụng bảng/RLS. Chạy lúc nào cũng được.
create or replace function public.staff_set_student_phones(p_student uuid, p_phone text, p_parent_phone text)
returns void
language plpgsql
security definer
set search_path = public, auth
as $$
declare
  v_phone text := nullif(regexp_replace(coalesce(p_phone, ''), '[^0-9]', '', 'g'), '');
  v_parent text := nullif(regexp_replace(coalesce(p_parent_phone, ''), '[^0-9]', '', 'g'), '');
begin
  if not (public.is_admin() or public.teaches_student(p_student)) then
    raise exception 'Không có quyền sửa học sinh này.' using errcode = '42501';
  end if;
  if (v_phone is not null and length(v_phone) not between 9 and 11)
     or (v_parent is not null and length(v_parent) not between 9 and 11) then
    raise exception 'Số điện thoại phải có 9–11 chữ số.';
  end if;
  update auth.users
     set raw_user_meta_data = coalesce(raw_user_meta_data, '{}'::jsonb)
                              || jsonb_build_object('phone', coalesce(v_phone, ''), 'parent_phone', coalesce(v_parent, ''))
   where id = p_student;
end;
$$;

revoke all on function public.staff_set_student_phones(uuid, text, text) from public, anon;
grant execute on function public.staff_set_student_phones(uuid, text, text) to authenticated;

-- ROLLBACK:
-- drop function if exists public.staff_set_student_phones(uuid, text, text);
