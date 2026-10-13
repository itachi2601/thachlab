-- Thêm môn học 'avcn' vào danh mục môn CTTC (bảng subjects) + mở sẵn 2 lớp học phần
-- 'CĐN CGKL 23A' và 'CĐ CK 23A' cho Anh văn chuyên ngành (năm học 2026-2027).
-- Giảng viên có thể vào Dashboard -> Môn "Anh văn chuyên ngành" -> tab "Danh sách lớp"
-- để tải file Excel danh sách lớp lên (tự tạo tài khoản + bảng điểm) hoặc dùng mã tham gia.
-- Idempotent, chỉ chèn dữ liệu, không đổi schema/policy. Rollback ở cuối file.

begin;

-- 1. Thêm môn Anh văn chuyên ngành vào bảng subjects
insert into public.subjects (code, name, area, is_practicum)
values ('avcn', 'Anh văn chuyên ngành', 'cttc', false)
on conflict (code) do update set
  name = excluded.name,
  area = excluded.area,
  is_practicum = excluded.is_practicum;

-- 2. Thêm lớp học phần CĐN CGKL 23A (khớp file điểm CĐN CGKL 23A-Tiếng Anh chuyên ngành.xls)
insert into public.course_offerings (subject_id, name, class_label, school_year, join_code, enrollment_mode, status)
select s.id, 'CÐN CGKL 23A - Tiếng Anh chuyên ngành', 'CÐN CGKL 23A', '2026-2027', 'AVCN-23A', 'approval', 'active'
from public.subjects s
where s.code = 'avcn'
  and not exists (
    select 1 from public.course_offerings co
    where co.subject_id = s.id and co.class_label = 'CÐN CGKL 23A' and co.school_year = '2026-2027'
  );

-- 3. Thêm lớp học phần CĐ CK 23A (lớp Cơ khí chính quy)
insert into public.course_offerings (subject_id, name, class_label, school_year, join_code, enrollment_mode, status)
select s.id, 'CĐ CK 23A - Tiếng Anh chuyên ngành', 'CĐ CK 23A', '2026-2027', 'AVCN-CK23A', 'approval', 'active'
from public.subjects s
where s.code = 'avcn'
  and not exists (
    select 1 from public.course_offerings co
    where co.subject_id = s.id and co.class_label = 'CĐ CK 23A' and co.school_year = '2026-2027'
  );

commit;

-- ROLLBACK (chạy tay khi cần):
-- begin;
-- delete from public.course_enrollments where course_id in (
--   select co.id from public.course_offerings co join public.subjects s on s.id = co.subject_id where s.code = 'avcn'
-- );
-- delete from public.course_offerings where subject_id in (
--   select id from public.subjects where code = 'avcn'
-- );
-- delete from public.subjects where code = 'avcn';
-- commit;
