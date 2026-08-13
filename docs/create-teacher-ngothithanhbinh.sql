-- Chạy một lần trong Supabase SQL Editor.
-- 1) Trước tiên tạo user trong Authentication > Users:
--    Email: ngothithanhbinh@thachlab.local
--    Password: mật khẩu giáo viên đã cung cấp
--    Auto Confirm User: bật
-- 2) Sau đó chạy câu lệnh dưới đây để cấp vai trò giáo viên.
update public.profiles
set full_name = 'Ngô Thị Thanh Bình', class_name = '', role = 'admin'
where id = (select id from auth.users where email = 'ngothithanhbinh@thachlab.local');
