-- Kho ảnh cho bài học THPT (trang /quan-tri/nhap-bai đăng bài từ LaTeX).
-- Ảnh vẽ lại được (đồ thị, sơ đồ) đi thẳng vào HTML dạng <svg> nội tuyến — không cần bucket.
-- Chỉ ảnh chụp/scan thật mới upload lên đây; URL công khai được nhúng thẳng vào body_html.
-- Chạy một lần trong Supabase Dashboard → SQL Editor. Idempotent.

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'lesson-media',
  'lesson-media',
  true,
  10485760, -- 10 MB
  array[
    'image/png',
    'image/jpeg',
    'image/webp',
    'image/gif',
    'image/svg+xml'
  ]
)
on conflict (id) do update set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "public reads lesson media storage" on storage.objects;
create policy "public reads lesson media storage" on storage.objects
  for select using (bucket_id = 'lesson-media');

drop policy if exists "admin uploads lesson media storage" on storage.objects;
create policy "admin uploads lesson media storage" on storage.objects
  for insert to authenticated with check (
    bucket_id = 'lesson-media' and public.is_admin()
  );

drop policy if exists "admin updates lesson media storage" on storage.objects;
create policy "admin updates lesson media storage" on storage.objects
  for update to authenticated using (
    bucket_id = 'lesson-media' and public.is_admin()
  ) with check (
    bucket_id = 'lesson-media' and public.is_admin()
  );

drop policy if exists "admin deletes lesson media storage" on storage.objects;
create policy "admin deletes lesson media storage" on storage.objects
  for delete to authenticated using (
    bucket_id = 'lesson-media' and public.is_admin()
  );
