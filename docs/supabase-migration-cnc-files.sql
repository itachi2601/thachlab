-- Tệp PowerPoint và tài liệu cho LMS Gia công CNC
-- Chạy một lần trong Supabase SQL Editor.

create table if not exists public.cnc_lesson_files (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  lesson_id text not null,
  kind text not null check (kind in ('powerpoint', 'material')),
  title text not null,
  file_name text not null,
  file_url text not null,
  storage_path text not null unique,
  mime_type text not null default 'application/octet-stream',
  size_bytes bigint not null default 0
);

create index if not exists cnc_lesson_files_lesson_idx
  on public.cnc_lesson_files (lesson_id, kind, created_at desc);

alter table public.cnc_lesson_files enable row level security;

drop policy if exists "anyone reads cnc lesson files" on public.cnc_lesson_files;
create policy "anyone reads cnc lesson files" on public.cnc_lesson_files
  for select using (true);

drop policy if exists "admin manages cnc lesson files" on public.cnc_lesson_files;
create policy "admin manages cnc lesson files" on public.cnc_lesson_files
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- Nhiều video YouTube cho từng bài học CNC.
create table if not exists public.cnc_lesson_videos (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  lesson_id text not null,
  title text not null,
  youtube_url text not null,
  youtube_id text not null check (youtube_id ~ '^[A-Za-z0-9_-]{11}$'),
  sort_order integer not null default 0
);

create index if not exists cnc_lesson_videos_lesson_idx
  on public.cnc_lesson_videos (lesson_id, sort_order, created_at);

alter table public.cnc_lesson_videos enable row level security;

drop policy if exists "anyone reads cnc lesson videos" on public.cnc_lesson_videos;
create policy "anyone reads cnc lesson videos" on public.cnc_lesson_videos
  for select using (true);

drop policy if exists "admin manages cnc lesson videos" on public.cnc_lesson_videos;
create policy "admin manages cnc lesson videos" on public.cnc_lesson_videos
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'cnc-lessons',
  'cnc-lessons',
  true,
  52428800,
  array[
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/zip',
    'text/plain',
    'application/octet-stream'
  ]
)
on conflict (id) do update set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "public reads cnc lesson storage" on storage.objects;
create policy "public reads cnc lesson storage" on storage.objects
  for select using (bucket_id = 'cnc-lessons');

drop policy if exists "admin uploads cnc lesson storage" on storage.objects;
create policy "admin uploads cnc lesson storage" on storage.objects
  for insert to authenticated with check (
    bucket_id = 'cnc-lessons' and public.is_admin()
  );

drop policy if exists "admin updates cnc lesson storage" on storage.objects;
create policy "admin updates cnc lesson storage" on storage.objects
  for update to authenticated using (
    bucket_id = 'cnc-lessons' and public.is_admin()
  ) with check (
    bucket_id = 'cnc-lessons' and public.is_admin()
  );

drop policy if exists "admin deletes cnc lesson storage" on storage.objects;
create policy "admin deletes cnc lesson storage" on storage.objects
  for delete to authenticated using (
    bucket_id = 'cnc-lessons' and public.is_admin()
  );
