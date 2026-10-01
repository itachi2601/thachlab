-- Đăng nhập bằng username cho tài khoản đăng ký kèm email thật:
-- trang /dang-nhap gọi hàm này để đổi username -> email auth. Không khớp thì trả null (client dùng <username>@thachlab.local).
create or replace function public.resolve_login_email(p_login text)
returns text
language sql
stable
security definer
set search_path = public, auth
as $$
  select u.email::text
  from auth.users u
  where lower(u.raw_user_meta_data->>'username') = lower(btrim(p_login))
  order by u.created_at
  limit 1;
$$;

revoke all on function public.resolve_login_email(text) from public;
grant execute on function public.resolve_login_email(text) to anon, authenticated;

-- ROLLBACK:
-- drop function if exists public.resolve_login_email(text);
