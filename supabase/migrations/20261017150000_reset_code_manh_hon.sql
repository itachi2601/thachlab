-- Đợt 3b rà soát 17/10/2026: mã đặt lại mật khẩu dài hơn + chặn hạn quá xa.
-- Trước: 'RS' + 6 hex (≈16,7 triệu khả năng). Sau: 'RS' + 10 hex (≈1,1 nghìn tỉ). Mã cũ còn hạn vẫn dùng được
-- (hàm reset-password tra theo chuỗi mã, không phụ thuộc độ dài). Hạn mặc định đã là 24 giờ (kiểm 17/10).
-- Thêm ràng buộc hạn tối đa 7 ngày cho bản ghi MỚI (NOT VALID: không quét bản ghi cũ, không thể lỗi vì dữ liệu cũ).
-- Chạy lúc nào cũng được (đổi default + thêm CHECK, không khoá bảng lâu).
alter table public.password_reset_codes
  alter column code set default ('RS'::text || upper(substr(replace((gen_random_uuid())::text, '-'::text, ''::text), 1, 10)));

alter table public.password_reset_codes
  drop constraint if exists password_reset_codes_expires_max;
alter table public.password_reset_codes
  add constraint password_reset_codes_expires_max
  check (expires_at <= created_at + interval '7 days') not valid;

-- Hậu kiểm: select column_default from information_schema.columns where table_name='password_reset_codes' and column_name='code';
--           insert thử qua RPC/giao diện, mã mới phải dài 12 ký tự.
-- ROLLBACK:
--   alter table public.password_reset_codes drop constraint if exists password_reset_codes_expires_max;
--   alter table public.password_reset_codes alter column code set default
--     ('RS'::text || upper(substr(replace((gen_random_uuid())::text, '-'::text, ''::text), 1, 6)));
