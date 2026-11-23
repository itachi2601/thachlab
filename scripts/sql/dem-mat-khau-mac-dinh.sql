-- CHỈ ĐỌC — đếm theo lớp số tài khoản HS còn mật khẩu mặc định (= mã số HS, do import-roster / reset-password đặt).
-- Đo tác dụng của màn "Đổi mật khẩu trước khi học tiếp" (22/11/2026): chạy trước khi deploy và 1–2 tuần sau.
-- Không in tên/mã số HS. Mỗi dòng tốn 1 phép bcrypt (~0,1 s CPU) → vài trăm HS mất ~1 phút: chạy sau 22h.
-- Cách chạy (Mac, đứng ở checkout chính): supabase db query --linked -f scripts/sql/dem-mat-khau-mac-dinh.sql
select coalesce(nullif(p.class_name, ''), '(không ghi lớp)') as lop,
       count(*) as so_tai_khoan,
       count(*) filter (where u.encrypted_password = extensions.crypt(p.student_code, u.encrypted_password)) as con_mat_khau_mac_dinh
from public.profiles p
join auth.users u on u.id = p.id
where p.role = 'student'
  and coalesce(p.student_code, '') <> ''
  and u.encrypted_password like '$2%'
group by 1
order by 3 desc, 1;
