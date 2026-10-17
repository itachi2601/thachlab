-- Chỉ đọc. Kiểm độ mạnh mã đặt lại mật khẩu (password_reset_codes.code) và giá trị mặc định của cột.
-- Chạy: supabase db query --linked -f scripts/sql/kiem-do-manh-ma-reset.sql
select column_default from information_schema.columns
 where table_schema='public' and table_name='password_reset_codes' and column_name='code';
select length(code) as do_dai, count(*) as so_ma, min(code) as vi_du_nho_nhat, max(code) as vi_du_lon_nhat
  from public.password_reset_codes group by 1 order by 1;
select count(*) filter (where code ~ '^[0-9]+$') as chi_so, count(*) as tong from public.password_reset_codes;
-- Đánh giá: mã chỉ-số < 8 ký tự hoặc không gen từ gen_random_bytes/gen_random_uuid => dễ dò; đổi default sang
-- upper(substr(encode(gen_random_bytes(8),'hex'),1,10)) trong Đợt sau.
