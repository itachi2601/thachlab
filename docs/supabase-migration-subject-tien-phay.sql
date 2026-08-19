-- Thêm môn học mới "Tiện – Phay truyền thống" để mở trang khóa học riêng tại
-- /lop-hoc/tien-phay, dùng lại nguyên hệ điểm danh/chọn máy/5S/báo hỏng đã tổng quát
-- theo course_id (xem docs/supabase-migration-machines.sql cho danh mục máy Xưởng C1.1).
-- Chạy sau docs/supabase-migration-machines.sql.

insert into public.subjects (code, name, area)
values ('tien-phay', 'Tiện – Phay truyền thống', 'cttc')
on conflict (code) do update set name = excluded.name, area = excluded.area, active = true;
