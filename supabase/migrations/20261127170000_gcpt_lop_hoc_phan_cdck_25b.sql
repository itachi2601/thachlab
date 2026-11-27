-- Lớp học phần "Các PPGCPTT" cho lớp CĐ CK 25B (27/11/2026).
-- Bối cảnh: thầy đã tạo lớp học phần "Các PPGCPTT · CĐ CK 25B" trong dashboard nhưng ô chọn môn chưa có
-- 'Các phương pháp gia công phi truyền thống' (services/subjects.ts thiếu mã 'gcpt') nên lớp rơi vào môn
-- 'khac' → không hiện trong tab lớp của môn GCPT, không có bảng điểm theo học phần.
-- Migration này chỉ sửa dữ liệu, idempotent:
--   1. Chuyển lớp đó sang môn 'gcpt' (giữ nguyên join_code để không phá link/mã đã phát cho SV).
--   2. Ghi danh các SV đang học lớp nội dung 'gcpt' vào lớp học phần (course_enrollments active)
--      để bảng điểm / điểm danh / gọi tên có danh sách.
-- Rollback ở cuối file.

begin;

-- 1. Lớp học phần "Các PPGCPTT" (join_code LOP-77B98E, class_label CĐ CK 25B) → môn gcpt.
update public.course_offerings co
set subject_id = s.id,
    enrollment_mode = 'approval',
    status = 'active'
from public.subjects s
where s.code = 'gcpt'
  and co.join_code = 'LOP-77B98E'
  and co.class_label = 'CĐ CK 25B'
  and co.subject_id <> s.id;

-- 2. SV đang học lớp nội dung 'gcpt' → ghi danh lớp học phần (active, coi như thầy đã duyệt).
insert into public.course_enrollments (course_id, student_id, status, approved_at)
select co.id, uc.user_id, 'active', now()
from public.course_offerings co
join public.subjects s on s.id = co.subject_id and s.code = 'gcpt'
join public.classes c on c.slug = 'gcpt'
join public.user_classes uc on uc.class_id = c.id and uc.status = 'active'
join public.profiles p on p.id = uc.user_id and p.role = 'student'
where co.join_code = 'LOP-77B98E'
on conflict (course_id, student_id) do update
  set status = 'active',
      approved_at = coalesce(course_enrollments.approved_at, now());

commit;

-- Kiểm lại sau khi chạy: lớp đã sang môn gcpt và có bao nhiêu SV active
select co.id, co.name, co.class_label, s.code as subject_code, co.join_code,
       (select count(*) from public.course_enrollments e
         where e.course_id = co.id and e.status = 'active') as active_students
from public.course_offerings co
join public.subjects s on s.id = co.subject_id
where co.join_code = 'LOP-77B98E';

-- ROLLBACK (chạy tay khi cần):
-- begin;
-- update public.course_offerings co
--   set subject_id = (select id from public.subjects where code = 'khac')
--   where co.join_code = 'LOP-77B98E'
--     and co.subject_id = (select id from public.subjects where code = 'gcpt');
-- -- Dòng course_enrollments của lớp giữ nguyên (là ghi danh thật của SV). Muốn xoá sạch:
-- -- delete from public.course_enrollments where course_id = (select id from public.course_offerings where join_code = 'LOP-77B98E');
-- commit;
