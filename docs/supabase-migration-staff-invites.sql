-- ============================================================
-- Mời giảng viên / trợ giảng qua email từ trang Phân công giảng viên
--
-- Không gửi email và không cần Edge Function: admin tạo lời mời (sinh mã), tự gửi link
--   https://thachlab.id.vn/loi-moi?ma=<code>
-- qua Zalo/Messenger. Người nhận mở link:
--   - chưa có tài khoản -> đăng ký ngay tại đó bằng email bất kỳ, mã đi kèm trong
--     raw_user_meta_data.invite_code và trigger zz_claim_staff_invite áp dụng lời mời;
--   - đã có tài khoản -> bấm "Nhận lời mời", gọi claim_staff_invite() cho chính mình.
--
-- Toàn bộ việc "áp dụng 1 lời mời" gom trong public.apply_staff_invite() để cả hai lối
-- vào dùng chung một logic, không viết hai bản. Khớp theo mã trước, không có mã thì thử
-- khớp theo email đã ghi trong lời mời.
-- ============================================================

-- ---------- 1. Trợ giảng ↔ lớp ----------
create table if not exists public.ta_assistant_classes (
  assistant_id uuid not null references public.ta_assistants(id) on delete cascade,
  class_id bigint not null references public.classes(id) on delete cascade,
  assigned_by uuid references public.profiles(id) on delete set null,
  assigned_at timestamptz not null default now(),
  primary key (assistant_id, class_id)
);

create index if not exists ta_assistant_classes_class_idx on public.ta_assistant_classes(class_id);

alter table public.ta_assistant_classes enable row level security;

drop policy if exists "admin quan ly lop tro giang" on public.ta_assistant_classes;
create policy "admin quan ly lop tro giang" on public.ta_assistant_classes
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "tro giang doc lop cua minh" on public.ta_assistant_classes;
create policy "tro giang doc lop cua minh" on public.ta_assistant_classes
  for select to authenticated
  using (assistant_id = public.ta_current_assistant_id() or public.is_admin());

-- ---------- 2. Lời mời ----------
create table if not exists public.staff_invites (
  id uuid primary key default gen_random_uuid(),
  -- Mã mời: người được mời mở /loi-moi?ma=<code>, đăng ký bằng email bất kỳ.
  -- Chữ số hex nên không lẫn 0/O hay 1/l khi đọc qua điện thoại.
  code text not null unique default upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 8)),
  -- Email chỉ để ghi nhớ mời ai, không bắt buộc và không dùng để gửi mail.
  email text,
  full_name text not null default '',
  role text not null check (role in ('instructor', 'tro_giang')),
  admin_area text check (admin_area in ('thpt', 'cttc')),
  class_id bigint references public.classes(id) on delete set null,
  course_id bigint references public.course_offerings(id) on delete set null,
  tier text check (tier in ('B1', 'B2', 'B3')),
  invited_by uuid references public.profiles(id) on delete set null,
  invited_at timestamptz not null default now(),
  claimed_at timestamptz,
  claimed_user_id uuid references auth.users(id) on delete set null
);

-- Nâng cấp cho DB đã chạy bản trước (khi đó email bắt buộc và chưa có cột code).
alter table public.staff_invites
  add column if not exists code text default upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 8));
update public.staff_invites
  set code = upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 8)) where code is null;
alter table public.staff_invites alter column code set not null;
alter table public.staff_invites alter column email drop not null;
create unique index if not exists staff_invites_code_idx on public.staff_invites (code);

-- 1 email chỉ có 1 lời mời đang chờ; mời lại thì ghi đè lời mời cũ chưa nhận.
-- (email null không tính — mời bằng mã thì không cần email.)
create unique index if not exists staff_invites_pending_email_idx
  on public.staff_invites (lower(email)) where claimed_at is null and email is not null;

create index if not exists staff_invites_email_idx on public.staff_invites (lower(email));

alter table public.staff_invites enable row level security;

drop policy if exists "admin quan ly loi moi" on public.staff_invites;
create policy "admin quan ly loi moi" on public.staff_invites
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ---------- 3. Áp dụng lời mời (dùng chung cho Edge Function và trigger) ----------
-- Trả về id lời mời đã áp dụng, null nếu email không có lời mời nào đang chờ.
drop function if exists public.apply_staff_invite(uuid, text);

create or replace function public.apply_staff_invite(p_user_id uuid, p_email text, p_code text default null)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
  inv public.staff_invites%rowtype;
  v_assistant_id uuid;
  v_short_name text;
begin
  -- Ưu tiên mã mời; không có mã thì thử khớp theo email đã ghi trong lời mời.
  if coalesce(trim(p_code), '') <> '' then
    select * into inv
    from public.staff_invites
    where upper(code) = upper(trim(p_code)) and claimed_at is null;
  else
    select * into inv
    from public.staff_invites
    where email is not null and lower(email) = lower(coalesce(p_email, '')) and claimed_at is null
    order by invited_at desc
    limit 1;
  end if;

  if inv.id is null then
    return null;
  end if;

  if inv.role = 'instructor' then
    update public.profiles
    set role = 'instructor',
        admin_area = coalesce(inv.admin_area, admin_area),
        full_name = case when coalesce(full_name, '') = '' then inv.full_name else full_name end
    where id = p_user_id;

    if inv.class_id is not null then
      insert into public.class_instructors (class_id, instructor_id, assigned_by)
      values (inv.class_id, p_user_id, inv.invited_by)
      on conflict do nothing;
    end if;

    if inv.course_id is not null then
      insert into public.course_instructors (course_id, instructor_id, assigned_by)
      values (inv.course_id, p_user_id, inv.invited_by)
      on conflict do nothing;
    end if;
  else
    -- Tên hiển thị ngắn = từ cuối của họ tên ("Ngô Diệu Thạch" -> "Thạch").
    v_short_name := nullif(regexp_replace(trim(coalesce(inv.full_name, '')), '^.*\s', ''), '');

    insert into public.ta_assistants (user_id, full_name, short_name, tier)
    values (
      p_user_id,
      coalesce(nullif(inv.full_name, ''), p_email),
      coalesce(v_short_name, nullif(inv.full_name, ''), p_email),
      coalesce(inv.tier, 'B1')
    )
    on conflict (user_id) do update set
      tier = coalesce(excluded.tier, public.ta_assistants.tier),
      active = true
    returning id into v_assistant_id;

    if inv.class_id is not null and v_assistant_id is not null then
      insert into public.ta_assistant_classes (assistant_id, class_id, assigned_by)
      values (v_assistant_id, inv.class_id, inv.invited_by)
      on conflict do nothing;
    end if;
  end if;

  update public.staff_invites
  set claimed_at = now(), claimed_user_id = p_user_id
  where id = inv.id;

  return inv.id;
end;
$$;

-- Không mở cho authenticated: người dùng không được tự chọn user_id để cấp quyền cho mình.
-- Muốn tự nhận lời mời thì đi qua claim_staff_invite() bên dưới (luôn dùng auth.uid()).
revoke all on function public.apply_staff_invite(uuid, text, text) from public, authenticated, anon;
grant execute on function public.apply_staff_invite(uuid, text, text) to service_role;

-- ---------- 3b. Người đã có tài khoản tự nhận lời mời bằng mã ----------
-- Luôn áp cho chính người đang đăng nhập, không nhận user_id từ client.
create or replace function public.claim_staff_invite(p_code text)
returns table (role text, class_name text, tier text)
language plpgsql
security definer
set search_path = public
as $$
declare
  v_user uuid := auth.uid();
  v_invite_id uuid;
  inv public.staff_invites%rowtype;
begin
  if v_user is null then
    raise exception 'Bạn cần đăng nhập trước khi nhận lời mời.';
  end if;

  select * into inv from public.staff_invites
  where upper(code) = upper(trim(coalesce(p_code, ''))) and claimed_at is null;

  if inv.id is null then
    raise exception 'Mã mời không đúng hoặc đã được dùng.';
  end if;

  v_invite_id := public.apply_staff_invite(
    v_user,
    (select u.email from auth.users u where u.id = v_user),
    p_code
  );

  if v_invite_id is null then
    raise exception 'Không nhận được lời mời này.';
  end if;

  return query
  select inv.role,
         (select c.name from public.classes c where c.id = inv.class_id),
         inv.tier;
end;
$$;

grant execute on function public.claim_staff_invite(text) to authenticated;

-- ---------- 4. Tự nhận lời mời khi người được mời tự đăng ký ----------
-- Tên trigger xếp sau on_auth_user_created để chạy sau khi hồ sơ profiles đã được tạo.
create or replace function public.trg_claim_staff_invite()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  v_code text := nullif(trim(coalesce(new.raw_user_meta_data ->> 'invite_code', '')), '');
begin
  -- Đăng ký từ /loi-moi?ma=<code> thì metadata mang sẵn mã; không có mã thì thử khớp email.
  if v_code is not null or new.email is not null then
    perform public.apply_staff_invite(new.id, new.email, v_code);
  end if;
  return new;
end;
$$;

drop trigger if exists zz_claim_staff_invite on auth.users;
create trigger zz_claim_staff_invite
  after insert on auth.users
  for each row execute function public.trg_claim_staff_invite();
