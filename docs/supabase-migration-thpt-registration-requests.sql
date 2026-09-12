-- ============================================================
-- Học sinh THPT tự đăng ký -> giáo viên/admin duyệt vào khối lớp.
-- Chạy sau: supabase-migration-classes.sql và
-- supabase-migration-class-instructors.sql. Idempotent.
-- ============================================================

create table if not exists public.thpt_registration_requests (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  user_id uuid not null unique references public.profiles(id) on delete cascade,
  requested_class_id bigint not null references public.classes(id) on delete restrict,
  full_name text not null,
  username text not null default '',
  email text not null default '',
  phone text not null default '',
  parent_phone text not null default '',
  birth_date date,
  gender text not null default '',
  student_code text not null default '',
  status text not null default 'pending'
    check (status in ('pending', 'approved', 'rejected')),
  reviewed_by uuid references public.profiles(id) on delete set null,
  reviewed_at timestamptz
);

create index if not exists thpt_registration_requests_class_status_idx
  on public.thpt_registration_requests(requested_class_id, status, created_at desc);

alter table public.thpt_registration_requests enable row level security;

drop policy if exists "students read own thpt registration" on public.thpt_registration_requests;
create policy "students read own thpt registration"
  on public.thpt_registration_requests for select to authenticated
  using (user_id = auth.uid());

drop policy if exists "staff read assigned thpt registrations" on public.thpt_registration_requests;
create policy "staff read assigned thpt registrations"
  on public.thpt_registration_requests for select to authenticated
  using (
    public.is_admin() or exists (
      select 1 from public.class_instructors ci
      where ci.class_id = requested_class_id and ci.instructor_id = auth.uid()
    )
  );

-- Giữ nguyên luồng import roster cũ (metadata class_id), đồng thời tạo yêu cầu
-- chờ duyệt khi form tự đăng ký gửi metadata requested_class_id.
create or replace function public.handle_new_user()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  cid bigint := nullif(new.raw_user_meta_data ->> 'class_id', '')::bigint;
  requested_cid bigint := nullif(new.raw_user_meta_data ->> 'requested_class_id', '')::bigint;
  cname text := '';
begin
  if cid is not null then
    select name into cname from public.classes where id = cid and active = true;
  end if;

  insert into public.profiles (id, full_name, class_name)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'full_name', ''),
    coalesce(cname, new.raw_user_meta_data ->> 'class_name', '')
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
$$;

create or replace function public.review_thpt_registration(
  p_request_id bigint,
  p_status text
)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  request_row public.thpt_registration_requests%rowtype;
  class_label text;
begin
  if p_status not in ('approved', 'rejected') then
    raise exception 'Trạng thái duyệt không hợp lệ.';
  end if;

  select * into request_row
  from public.thpt_registration_requests
  where id = p_request_id and status = 'pending'
  for update;

  if not found then
    raise exception 'Yêu cầu không còn ở trạng thái chờ duyệt.';
  end if;

  if not public.is_admin() and not exists (
    select 1 from public.class_instructors
    where class_id = request_row.requested_class_id and instructor_id = auth.uid()
  ) then
    raise exception 'Bạn không có quyền duyệt học sinh của lớp này.';
  end if;

  if p_status = 'approved' then
    select name into class_label from public.classes
    where id = request_row.requested_class_id and active = true;
    if class_label is null then raise exception 'Khối lớp không còn hoạt động.'; end if;

    insert into public.user_classes(user_id, class_id)
    values (request_row.user_id, request_row.requested_class_id)
    on conflict do nothing;

    update public.profiles
    set full_name = request_row.full_name, class_name = class_label
    where id = request_row.user_id;
  end if;

  update public.thpt_registration_requests
  set status = p_status, reviewed_by = auth.uid(), reviewed_at = now(), updated_at = now()
  where id = p_request_id;
end;
$$;

revoke all on function public.review_thpt_registration(bigint, text) from public;
grant execute on function public.review_thpt_registration(bigint, text) to authenticated;
