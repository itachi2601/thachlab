-- ============================================================
-- Migration: avatar cho học sinh
-- Idempotent — chạy lại được.
--
-- profiles.avatar_url lưu URL công khai của ảnh trong bucket "avatars".
-- "update own profile" (supabase-schema.sql) chỉ cho with check role = 'student' —
-- nên chỉ tài khoản học sinh tự sửa được avatar của chính mình qua policy đó,
-- không cần policy riêng ở bảng profiles.
-- ============================================================

alter table public.profiles add column if not exists avatar_url text;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('avatars', 'avatars', true, 2097152, array['image/png', 'image/jpeg', 'image/webp'])
on conflict (id) do update set
  public = excluded.public, file_size_limit = excluded.file_size_limit, allowed_mime_types = excluded.allowed_mime_types;

-- Mỗi học sinh chỉ upload/xoá được vào đúng thư mục tên uid của mình (avatars/<uid>/...).
drop policy if exists "students upload own avatar" on storage.objects;
create policy "students upload own avatar" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);

drop policy if exists "students delete own avatar" on storage.objects;
create policy "students delete own avatar" on storage.objects
  for delete to authenticated
  using (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);

-- Bucket public — ai cũng xem được avatar (kể cả khách chưa đăng nhập, vd trang xếp hạng công khai sau này).
drop policy if exists "anyone views avatars" on storage.objects;
create policy "anyone views avatars" on storage.objects
  for select to anon, authenticated
  using (bucket_id = 'avatars');
