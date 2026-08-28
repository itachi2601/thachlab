-- Bucket môn học mặc định cho các lớp học phần lý thuyết (LT) nhập từ Excel mà chưa
-- có khóa CTTC tương ứng (khác CNC/Tiện-Phay, vốn đã có subject riêng).
-- Idempotent; chạy sau supabase-migration-course-instructors.sql.

insert into public.subjects (code, name, area, is_practicum)
values ('khac', 'Môn khác (nhập từ Excel)', 'cttc', false)
on conflict (code) do update set
  name = excluded.name,
  area = excluded.area;

-- Ngày sinh đọc từ file Excel nhập danh sách — lưu lại để xuất file cuối kỳ đúng như mẫu gốc.
alter table public.profiles add column if not exists birth_date date;
