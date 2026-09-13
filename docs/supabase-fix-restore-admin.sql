-- ============================================================
-- Khôi phục quyền quản trị cho một tài khoản bị "tụt quyền" do bấm nhầm link mời
-- (/loi-moi?ma=...). Chạy trong Supabase Dashboard → SQL Editor (bỏ qua RLS).
--
-- Nhận một lời mời làm 2 việc:
--   - lời mời 'instructor' -> ghi đè profiles.role = 'instructor' (mất quyền admin);
--   - lời mời 'tro_giang'  -> thêm 1 dòng public.ta_assistants (role giữ nguyên),
--     khiến tài khoản hiện ra ở khu /tro-giang và trong bảng lương trợ giảng.
-- File này gỡ cả hai, và trả lời mời về trạng thái chưa nhận để người được mời
-- thật vẫn dùng được mã cũ.
--
-- Đổi email dưới đây nếu cần khôi phục cho người khác.
-- ============================================================

-- ---------- 0. Xem hiện trạng trước khi sửa ----------
select p.id, u.email, p.full_name, p.role, p.admin_area,
       (select count(*) from public.ta_assistants a where a.user_id = p.id) as co_ho_so_tro_giang,
       (select count(*) from public.ta_sessions s
          join public.ta_assistants a on a.id = s.assistant_id
         where a.user_id = p.id) as so_buoi_da_ghi
from public.profiles p
join auth.users u on u.id = p.id
where lower(u.email) = lower('itachi2601@gmail.com');

-- ---------- 1. Trả role về admin ----------
-- admin_area = null vì role 'admin' luôn thấy cả THPT lẫn CTTC; cột này chỉ giới hạn 'instructor'.
update public.profiles p
set role = 'admin', admin_area = null
from auth.users u
where u.id = p.id and lower(u.email) = lower('itachi2601@gmail.com');

-- ---------- 2. Gỡ hồ sơ trợ giảng vừa bị tạo ----------
-- Chỉ xóa khi chưa ghi buổi làm việc nào (xóa ta_assistants sẽ cascade mất ta_sessions).
-- Nếu đã lỡ ghi buổi, câu này không xóa gì — khi đó hãy tự quyết định ở phần 2b.
delete from public.ta_assistants a
using auth.users u
where a.user_id = u.id
  and lower(u.email) = lower('itachi2601@gmail.com')
  and not exists (select 1 from public.ta_sessions s where s.assistant_id = a.id);

-- 2b. (chỉ chạy nếu phần 2 không xóa được vì đã có buổi ghi) — giữ dữ liệu, chỉ tắt hoạt động:
-- update public.ta_assistants a set active = false
-- from auth.users u where a.user_id = u.id and lower(u.email) = lower('itachi2601@gmail.com');

-- ---------- 3. Trả lời mời về "chưa nhận" để người được mời thật vẫn dùng được mã ----------
update public.staff_invites
set claimed_at = null, claimed_user_id = null
where claimed_user_id = (select id from auth.users where lower(email) = lower('itachi2601@gmail.com'));

-- ---------- 4. Kiểm tra lại ----------
select p.id, u.email, p.full_name, p.role, p.admin_area,
       (select count(*) from public.ta_assistants a where a.user_id = p.id) as co_ho_so_tro_giang
from public.profiles p
join auth.users u on u.id = p.id
where lower(u.email) = lower('itachi2601@gmail.com');

-- Sau khi chạy: đăng xuất rồi đăng nhập lại (hồ sơ role được đọc lúc mở phiên).
