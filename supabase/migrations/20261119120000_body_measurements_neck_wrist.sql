-- Mục Sức khỏe › Số đo: thêm vòng cổ và vòng cổ tay để ước tính % mỡ (công thức Hải quân Mỹ) và cỡ khung xương.
-- Chỉ thêm cột, cho phép null; không đụng dữ liệu cũ. Idempotent. Bảng đã có RLS từ 20261118120000_tap_luyen.
alter table public.body_measurements add column if not exists neck_cm numeric(5,1);
alter table public.body_measurements add column if not exists wrist_cm numeric(5,1);
