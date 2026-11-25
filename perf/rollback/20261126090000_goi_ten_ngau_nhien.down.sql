-- Rollback 20261126090000_goi_ten_ngau_nhien.sql — bỏ hàm gọi tên ngẫu nhiên (client tự ẩn danh sách khi hàm lỗi).
drop function if exists public.class_call_roster(bigint);
