-- Bucket công khai cho clip hiện tượng tự dựng/tự quay trong bài lý thuyết (thay YouTube cho clip của mình).
-- Chỉ nhận mp4 + ảnh bìa webp, ≤ 5 MB/file. Đọc công khai qua URL public; ghi chỉ bằng service role
-- (scripts/tai-clip-len-storage.mts) nên không thêm policy cho anon/authenticated.
-- Quy tắc: docs/QUY-TAC-THIET-KE.md V9 · kế hoạch: docs/KE-HOACH-CLIP-ANH-DONG.md
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('lesson-clips', 'lesson-clips', true, 5242880, array['video/mp4', 'image/webp'])
on conflict (id) do nothing;

-- ROLLBACK (chỉ khi bucket còn trống; có file thì xoá file qua Storage trước):
-- delete from storage.buckets where id = 'lesson-clips';
