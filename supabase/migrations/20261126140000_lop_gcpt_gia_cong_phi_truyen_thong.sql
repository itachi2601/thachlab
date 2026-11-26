-- Học phần "Các phương pháp gia công phi truyền thống" (CTTC) trên LMS bài học, theo mẫu cnctm:
--   môn 'gcpt' (academic_subjects) + lớp 'gcpt' (classes, vào có duyệt) + mỗi bài một chương, 12 bài (published=false,
--   bật sau khi upload-lesson.mts ghi nội dung và thầy duyệt) + subjects/course_offerings để có danh sách lớp/bảng điểm.
-- Chỉ chèn dữ liệu, idempotent, không đổi schema/policy/hàm. Rollback ở cuối file.
begin;

insert into public.academic_subjects (code, label, icon, sort_order, active)
values ('gcpt', 'Các phương pháp gia công phi truyền thống', '⚡', 7, true)
on conflict (code) do nothing;

insert into public.classes (name, slug, color, icon, sort_order, active, requires_approval)
select 'Các phương pháp gia công phi truyền thống', 'gcpt', '#7C3AED', '⚡', 10, true, true
where not exists (select 1 from public.classes where slug = 'gcpt');

create temporary table _gcpt_ls (so int, chuong text, bai text) on commit drop;
insert into _gcpt_ls values
  (1,  'Tổng quan gia công phi truyền thống', 'Bài 1. Tổng quan gia công phi truyền thống'),
  (2,  'Gia công tia lửa điện (EDM)', 'Bài 2. Gia công tia lửa điện (EDM)'),
  (3,  'Cắt dây tia lửa điện (WEDM)', 'Bài 3. Cắt dây tia lửa điện (WEDM)'),
  (4,  'Gia công điện hoá (ECM)', 'Bài 4. Gia công điện hoá (ECM)'),
  (5,  'Gia công bằng tia laser (LBM)', 'Bài 5. Gia công bằng tia laser (LBM)'),
  (6,  'Gia công bằng tia nước (WJM, AWJ)', 'Bài 6. Gia công bằng tia nước và tia nước mài (WJM, AWJ)'),
  (7,  'Gia công siêu âm (USM)', 'Bài 7. Gia công siêu âm (USM)'),
  (8,  'Chùm tia điện tử và plasma (EBM, PAM)', 'Bài 8. Gia công bằng chùm tia điện tử và plasma (EBM, PAM)'),
  (9,  'Gia công hoá học và quang hoá (CHM, PCM)', 'Bài 9. Gia công hoá học và quang hoá (CHM, PCM)'),
  (10, 'Gia công bồi đắp và công nghệ lai', 'Bài 10. Gia công bồi đắp (in 3D kim loại) và công nghệ lai'),
  (11, 'Chọn công nghệ gia công cho chi tiết', 'Bài 11. Chọn công nghệ gia công cho chi tiết'),
  (12, 'Ôn thi tự luận', 'Bài 12. Ôn thi tự luận và đề mẫu');

insert into public.chapters (title, sort_order, subject_code)
select l.chuong, l.so, 'gcpt'
from _gcpt_ls l
where not exists (select 1 from public.chapters x where x.subject_code = 'gcpt' and x.sort_order = l.so);

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x, public.classes c
where x.subject_code = 'gcpt' and c.slug = 'gcpt'
  and not exists (select 1 from public.chapter_classes cc where cc.chapter_id = x.id and cc.class_id = c.id);

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, l.bai, l.so, false
from _gcpt_ls l
join public.chapters x on x.subject_code = 'gcpt' and x.sort_order = l.so
where not exists (select 1 from public.lessons y where y.chapter_id = x.id);

insert into public.subjects (code, name, area, is_practicum)
values ('gcpt', 'Các phương pháp gia công phi truyền thống', 'cttc', false)
on conflict (code) do nothing;

commit;

-- Lớp học phần (course_offerings) thầy tạo sau khi biết tên lớp/năm học; chưa chèn ở đây để khỏi đoán.
-- In id bài để chạy tiếp: npx tsx scripts/upload-lesson.mts content/lesson-samples/gcpt-bai-<n>-…/bundle.json --lesson <id>
select y.id, y.title, y.published from public.lessons y join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'gcpt' order by x.sort_order;

-- ROLLBACK (chạy tay khi cần):
-- begin;
-- delete from public.course_enrollments where course_id in (select co.id from public.course_offerings co join public.subjects s on s.id = co.subject_id where s.code = 'gcpt');
-- delete from public.course_offerings where subject_id in (select id from public.subjects where code = 'gcpt');
-- delete from public.subjects where code = 'gcpt';
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'gcpt');
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'gcpt');
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'gcpt');
-- delete from public.chapters where subject_code = 'gcpt';
-- delete from public.user_classes where class_id in (select id from public.classes where slug = 'gcpt');
-- delete from public.classes where slug = 'gcpt';
-- delete from public.academic_subjects where code = 'gcpt';
-- commit;
