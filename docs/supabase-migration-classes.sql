-- ============================================================
-- Migration v2: Lớp học + many-to-many + trường lọc đề
-- Chạy SAU supabase-schema.sql (idempotent, chạy lại được)
-- ============================================================

-- ---------- Lớp học ----------
create table if not exists public.classes (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  name text not null unique,          -- "10A1"
  slug text not null unique,          -- "10a1"
  color text not null default '#3B82F6',
  icon text not null default '',      -- emoji, tuỳ chọn
  sort_order int not null default 0,
  active boolean not null default true
);

alter table public.classes enable row level security;

drop policy if exists "anyone reads active classes" on public.classes;
create policy "anyone reads active classes" on public.classes
  for select using (active or public.is_admin());
drop policy if exists "admin manages classes" on public.classes;
create policy "admin manages classes" on public.classes
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ---------- Many-to-many ----------
create table if not exists public.exam_classes (
  exam_id bigint not null references public.exams (id) on delete cascade,
  class_id bigint not null references public.classes (id) on delete cascade,
  primary key (exam_id, class_id)
);

create table if not exists public.post_classes (
  post_id bigint not null references public.posts (id) on delete cascade,
  class_id bigint not null references public.classes (id) on delete cascade,
  primary key (post_id, class_id)
);

create table if not exists public.user_classes (
  user_id uuid not null references public.profiles (id) on delete cascade,
  class_id bigint not null references public.classes (id) on delete cascade,
  primary key (user_id, class_id)
);

alter table public.exam_classes enable row level security;
alter table public.post_classes enable row level security;
alter table public.user_classes enable row level security;

drop policy if exists "read exam classes" on public.exam_classes;
create policy "read exam classes" on public.exam_classes for select using (true);
drop policy if exists "admin manages exam classes" on public.exam_classes;
create policy "admin manages exam classes" on public.exam_classes
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "read post classes" on public.post_classes;
create policy "read post classes" on public.post_classes for select using (true);
drop policy if exists "admin manages post classes" on public.post_classes;
create policy "admin manages post classes" on public.post_classes
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "read own user classes" on public.user_classes;
create policy "read own user classes" on public.user_classes
  for select to authenticated using (user_id = auth.uid() or public.is_admin());
drop policy if exists "admin manages user classes" on public.user_classes;
create policy "admin manages user classes" on public.user_classes
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ---------- Trường lọc cho đề & bài đăng ----------
alter table public.exams add column if not exists topic text not null default '';
alter table public.exams add column if not exists difficulty text not null default ''
  check (difficulty in ('', 'de', 'trung-binh', 'kho'));
alter table public.posts add column if not exists topic text not null default '';

-- ---------- Đăng ký kèm lớp: trigger nhận class_id từ metadata ----------
create or replace function public.handle_new_user()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  cid bigint := nullif(new.raw_user_meta_data ->> 'class_id', '')::bigint;
  cname text := '';
begin
  if cid is not null then
    select name into cname from public.classes where id = cid;
  end if;
  insert into public.profiles (id, full_name, class_name)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'full_name', ''),
    coalesce(cname, new.raw_user_meta_data ->> 'class_name', '')
  );
  if cid is not null then
    insert into public.user_classes (user_id, class_id) values (new.id, cid)
    on conflict do nothing;
  end if;
  return new;
end;
$$;

-- ---------- Storage bucket cho ảnh trong đề (import Word) ----------
insert into storage.buckets (id, name, public)
values ('exam-images', 'exam-images', true)
on conflict (id) do nothing;

drop policy if exists "admin uploads exam images" on storage.objects;
create policy "admin uploads exam images" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'exam-images' and public.is_admin());

drop policy if exists "anyone reads exam images" on storage.objects;
create policy "anyone reads exam images" on storage.objects
  for select using (bucket_id = 'exam-images');

-- ---------- Lớp mẫu ----------
insert into public.classes (name, slug, color, sort_order) values
  ('10A1', '10a1', '#22D3EE', 1),
  ('10A2', '10a2', '#22D3EE', 2),
  ('11A1', '11a1', '#3B82F6', 3),
  ('11A2', '11a2', '#3B82F6', 4),
  ('12A1', '12a1', '#8B5CF6', 5),
  ('12A2', '12a2', '#8B5CF6', 6)
on conflict (name) do nothing;
