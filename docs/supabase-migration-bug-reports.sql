-- Báo lỗi từ người dùng (học sinh, giảng viên, cả khách chưa đăng nhập).
-- Idempotent — chạy lại được. Cần docs/supabase-schema.sql đã chạy trước (dùng public.is_admin()).

create table if not exists public.bug_reports (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  user_id uuid references public.profiles(id) on delete set null,
  reporter_name text not null default '',
  reporter_email text not null default '',
  page_url text not null default '',
  category text not null default 'khac' check (category in ('hien_thi', 'diem', 'dang_nhap', 'de_xuat', 'khac')),
  description text not null,
  screenshot_path text,
  status text not null default 'moi' check (status in ('moi', 'dang_xu_ly', 'da_xu_ly')),
  admin_note text not null default ''
);

create index if not exists bug_reports_status_idx on public.bug_reports (status, created_at desc);
create index if not exists bug_reports_user_idx on public.bug_reports (user_id, created_at desc) where user_id is not null;

alter table public.bug_reports enable row level security;

-- Ai cũng gửi được (kể cả khách chưa đăng nhập) — nhưng không được gắn user_id của người khác.
drop policy if exists "anyone reports bug" on public.bug_reports;
create policy "anyone reports bug" on public.bug_reports
  for insert to anon, authenticated
  with check (user_id is null or user_id = auth.uid());

drop policy if exists "read own or admin bug reports" on public.bug_reports;
create policy "read own or admin bug reports" on public.bug_reports
  for select to authenticated
  using (user_id = auth.uid() or public.is_admin());

drop policy if exists "admin updates bug reports" on public.bug_reports;
create policy "admin updates bug reports" on public.bug_reports
  for update to authenticated
  using (public.is_admin())
  with check (public.is_admin());

drop policy if exists "admin deletes bug reports" on public.bug_reports;
create policy "admin deletes bug reports" on public.bug_reports
  for delete to authenticated
  using (public.is_admin());

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('bug-report-screenshots', 'bug-report-screenshots', false, 5242880, array['image/png', 'image/jpeg', 'image/webp'])
on conflict (id) do update set
  public = excluded.public, file_size_limit = excluded.file_size_limit, allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "anyone uploads bug report screenshots" on storage.objects;
create policy "anyone uploads bug report screenshots" on storage.objects
  for insert to anon, authenticated
  with check (bucket_id = 'bug-report-screenshots');

drop policy if exists "admin reads bug report screenshots" on storage.objects;
create policy "admin reads bug report screenshots" on storage.objects
  for select to authenticated
  using (bucket_id = 'bug-report-screenshots' and public.is_admin());

drop policy if exists "admin deletes bug report screenshots" on storage.objects;
create policy "admin deletes bug report screenshots" on storage.objects
  for delete to authenticated
  using (bucket_id = 'bug-report-screenshots' and public.is_admin());
