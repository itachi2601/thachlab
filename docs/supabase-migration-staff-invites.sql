-- ============================================================
-- Mời giảng viên / trợ giảng qua email từ trang Phân công giảng viên
--
-- Site export tĩnh nên không gọi được auth.admin.inviteUserByEmail từ trình duyệt.
-- Luồng chính đi qua Edge Function `invite-staff` (xem supabase/functions/invite-staff).
-- Bảng staff_invites vừa là nhật ký lời mời, vừa là lưới an toàn: nếu email mời không
-- tới nơi mà người đó tự đăng ký đúng email, trigger bên dưới vẫn cấp quyền và gán lớp.
--
-- Toàn bộ việc "áp dụng 1 lời mời" gom trong public.apply_staff_invite() để Edge Function
-- và trigger dùng chung một logic, không viết hai bản.
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
  email text not null,
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

-- 1 email chỉ có 1 lời mời đang chờ; mời lại thì ghi đè lời mời cũ chưa nhận.
create unique index if not exists staff_invites_pending_email_idx
  on public.staff_invites (lower(email)) where claimed_at is null;

create index if not exists staff_invites_email_idx on public.staff_invites (lower(email));

alter table public.staff_invites enable row level security;

drop policy if exists "admin quan ly loi moi" on public.staff_invites;
create policy "admin quan ly loi moi" on public.staff_invites
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ---------- 3. Áp dụng lời mời (dùng chung cho Edge Function và trigger) ----------
-- Trả về id lời mời đã áp dụng, null nếu email không có lời mời nào đang chờ.
create or replace function public.apply_staff_invite(p_user_id uuid, p_email text)
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
  select * into inv
  from public.staff_invites
  where lower(email) = lower(p_email) and claimed_at is null
  order by invited_at desc
  limit 1;

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

-- Chỉ Edge Function (service_role) và trigger gọi — không mở cho authenticated để tránh
-- người dùng tự gọi và tự cấp quyền cho mình.
revoke all on function public.apply_staff_invite(uuid, text) from public, authenticated, anon;
grant execute on function public.apply_staff_invite(uuid, text) to service_role;

-- ---------- 4. Tự nhận lời mời khi người được mời tự đăng ký ----------
-- Tên trigger xếp sau on_auth_user_created để chạy sau khi hồ sơ profiles đã được tạo.
create or replace function public.trg_claim_staff_invite()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if new.email is not null then
    perform public.apply_staff_invite(new.id, new.email);
  end if;
  return new;
end;
$$;

drop trigger if exists zz_claim_staff_invite on auth.users;
create trigger zz_claim_staff_invite
  after insert on auth.users
  for each row execute function public.trg_claim_staff_invite();
