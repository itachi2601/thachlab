-- Cho phép phân công mỗi giảng viên cộng tác chỉ được vào ĐÚNG 1 khu vực quản trị
-- (THPT hoặc CTTC) thay vì toàn bộ /quan-tri. Tài khoản role = 'admin' (chủ trang)
-- vẫn luôn thấy được cả 2 khu vực, không bị cột này giới hạn.
--
-- admin_area = null  -> giảng viên này chưa được cấp quyền vào /quan-tri (mặc định).
-- admin_area = 'thpt' hoặc 'cttc' -> chỉ vào được đúng khu vực đó.

alter table public.profiles
  add column if not exists admin_area text check (admin_area in ('thpt', 'cttc'));
