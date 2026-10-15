-- 20261015233000_ngay_sinh_tu_dang_ky.sql
-- Ngày sinh học sinh khai ở /dang-ky nằm trong auth.users.raw_user_meta_data->>'birth_date' nhưng
-- handle_new_user() chưa bao giờ chép sang profiles.birth_date (0/291 HS THPT có ngày sinh trong hồ sơ,
-- 134 em có trong metadata) → phụ huynh tự nối con (claim_parent_by_child_info, 20261015180000) không khớp được ai.
--   1. Chép ngày sinh từ metadata sang hồ sơ cho dòng đang trống, chỉ khi đúng dạng YYYY-MM-DD và năm 1990–2015
--      (loại 8 giá trị năm 2026 = ô chọn ngày để mặc định). Sao lưu id đã ghi để hoàn tác.
--   2. handle_new_user(): chép luôn birth_date (cùng điều kiện) cho tài khoản đăng ký mới. Giữ nguyên phần còn lại
--      (lấy từ pg_get_functiondef bản đang chạy 15/10/2026).
-- Chạy lúc nào cũng được (chỉ ghi cột đang NULL + thay một hàm).

-- ---------- 0. Hàm kiểm ngày sinh hợp lệ ----------
-- Không bao giờ raise: hàm chạy trong trigger đăng ký, lỗi ở đây = học sinh không tạo được tài khoản.
create or replace function public.pl_safe_birth(p text)
returns date
language plpgsql immutable
set search_path = public
as $$
begin
  if p is null or p !~ '^\d{4}-\d{2}-\d{2}$' or substr(p, 1, 4)::int not between 1990 and 2015 then
    return null;
  end if;
  return p::date;  -- 2010-02-31 → lỗi → null ở dưới
exception when others then
  return null;
end;
$$;
revoke all on function public.pl_safe_birth(text) from public, anon;

-- ---------- 1. Sao lưu + chép ----------
create table if not exists public._bak_profiles_birth_20261015 (
  id uuid primary key,
  copied_at timestamptz not null default now()
);
alter table public._bak_profiles_birth_20261015 enable row level security;
revoke all on public._bak_profiles_birth_20261015 from anon, authenticated;

with src as (
  select p.id, public.pl_safe_birth(u.raw_user_meta_data ->> 'birth_date') as b
  from public.profiles p
  join auth.users u on u.id = p.id
  where p.birth_date is null
), upd as (
  update public.profiles p
  set birth_date = src.b
  from src
  where p.id = src.id and src.b is not null
  returning p.id
)
insert into public._bak_profiles_birth_20261015 (id)
select id from upd
on conflict (id) do nothing;

-- ---------- 2. Tài khoản mới tự có ngày sinh trong hồ sơ ----------
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path to 'public'
as $function$
declare
  cid bigint := nullif(new.raw_user_meta_data ->> 'class_id', '')::bigint;
  requested_cid bigint := nullif(new.raw_user_meta_data ->> 'requested_class_id', '')::bigint;
  cname text := '';
begin
  if cid is not null then
    select name into cname from public.classes where id = cid and active = true;
  end if;

  insert into public.profiles (id, full_name, class_name, birth_date)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'full_name', ''),
    coalesce(cname, new.raw_user_meta_data ->> 'class_name', ''),
    public.pl_safe_birth(new.raw_user_meta_data ->> 'birth_date')
  );

  if cid is not null and cname <> '' then
    insert into public.user_classes (user_id, class_id) values (new.id, cid)
    on conflict do nothing;
  end if;

  if requested_cid is not null and exists (
    select 1 from public.classes where id = requested_cid and active = true
  ) then
    insert into public.thpt_registration_requests (
      user_id, requested_class_id, full_name, username, email, phone,
      parent_phone, birth_date, gender, student_code
    ) values (
      new.id,
      requested_cid,
      coalesce(new.raw_user_meta_data ->> 'full_name', ''),
      coalesce(new.raw_user_meta_data ->> 'username', ''),
      coalesce(new.raw_user_meta_data ->> 'contact_email', ''),
      coalesce(new.raw_user_meta_data ->> 'phone', ''),
      coalesce(new.raw_user_meta_data ->> 'parent_phone', ''),
      nullif(new.raw_user_meta_data ->> 'birth_date', '')::date,
      coalesce(new.raw_user_meta_data ->> 'gender', ''),
      coalesce(new.raw_user_meta_data ->> 'student_code', '')
    );
  end if;
  return new;
end;
$function$;

-- ============================================================================
-- ROLLBACK (chạy tay nếu cần):
-- begin;
-- update public.profiles set birth_date = null
--   where id in (select id from public._bak_profiles_birth_20261015);
-- -- handle_new_user: chạy lại bản cũ = bản trên nhưng bỏ cột birth_date trong insert profiles
-- --   (insert into public.profiles (id, full_name, class_name) values (new.id, …full_name…, …class_name…)).
-- drop table if exists public._bak_profiles_birth_20261015;
-- drop function if exists public.pl_safe_birth(text);  -- chỉ sau khi đã đổi handle_new_user về bản cũ
-- commit;
-- ============================================================================
