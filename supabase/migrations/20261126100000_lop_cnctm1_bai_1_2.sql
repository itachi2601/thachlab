-- Học phần "Công nghệ chế tạo máy 1" (CTTC, lớp CĐ CK 25C, HK2 2026-2027) trên LMS bài học, theo mẫu AVCN:
--   môn 'cnctm' (academic_subjects) + lớp 'cnctm' (classes, vào có duyệt) + mỗi bài một chương
--   + 2 bài đầu: Bài 1 Những khái niệm cơ bản, Bài 2 Các hình thức gia công cơ khí (published=false,
--   bật sau khi upload-lesson.mts ghi nội dung và thầy duyệt).
--   Thêm môn 'cnctm' vào danh mục CTTC (subjects) + lớp học phần CĐ CK 25C (course_offerings) để có danh sách lớp/bảng điểm.
-- Chỉ chèn dữ liệu, idempotent, không đổi schema/policy/hàm. Rollback ở cuối file.
begin;

insert into public.academic_subjects (code, label, icon, sort_order, active)
values ('cnctm', 'Công nghệ chế tạo máy 1', '⚙️', 6, true)
on conflict (code) do nothing;

insert into public.classes (name, slug, color, icon, sort_order, active, requires_approval)
select 'Công nghệ chế tạo máy 1', 'cnctm', '#475569', '⚙️', 9, true, true
where not exists (select 1 from public.classes where slug = 'cnctm');

create temporary table _cnctm_ls (so int, chuong text, bai text) on commit drop;
insert into _cnctm_ls values
  (1, 'Những khái niệm cơ bản', 'Bài 1. Những khái niệm cơ bản'),
  (2, 'Các hình thức gia công cơ khí', 'Bài 2. Các hình thức gia công cơ khí');

insert into public.chapters (title, sort_order, subject_code)
select l.chuong, l.so, 'cnctm'
from _cnctm_ls l
where not exists (select 1 from public.chapters x where x.subject_code = 'cnctm' and x.sort_order = l.so);

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x, public.classes c
where x.subject_code = 'cnctm' and c.slug = 'cnctm'
  and not exists (select 1 from public.chapter_classes cc where cc.chapter_id = x.id and cc.class_id = c.id);

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, l.bai, l.so, false
from _cnctm_ls l
join public.chapters x on x.subject_code = 'cnctm' and x.sort_order = l.so
where not exists (select 1 from public.lessons y where y.chapter_id = x.id);

insert into public.subjects (code, name, area, is_practicum)
values ('cnctm', 'Công nghệ chế tạo máy 1', 'cttc', false)
on conflict (code) do nothing;

insert into public.course_offerings (subject_id, name, class_label, school_year, join_code, enrollment_mode, status)
select s.id, 'CĐ CK 25C - Công nghệ chế tạo máy 1', 'CĐ CK 25C', '2026-2027', 'CNCTM-25C', 'approval', 'active'
from public.subjects s
where s.code = 'cnctm'
  and not exists (
    select 1 from public.course_offerings co
    where co.subject_id = s.id and co.class_label = 'CĐ CK 25C' and co.school_year = '2026-2027'
  );

commit;

-- In id bài để chạy tiếp: npx tsx scripts/upload-lesson.mts content/lesson-samples/cnctm1-bai-<n>-…/bundle.json --lesson <id>
select y.id, y.title, y.published from public.lessons y join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'cnctm' order by x.sort_order;

-- ROLLBACK (chạy tay khi cần; xoá cả bài làm/ghi danh của môn này):
-- begin;
-- delete from public.course_enrollments where course_id in (select co.id from public.course_offerings co join public.subjects s on s.id = co.subject_id where s.code = 'cnctm');
-- delete from public.course_offerings where subject_id in (select id from public.subjects where code = 'cnctm');
-- delete from public.subjects where code = 'cnctm';
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'cnctm');
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'cnctm');
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'cnctm');
-- delete from public.chapters where subject_code = 'cnctm';
-- delete from public.user_classes where class_id in (select id from public.classes where slug = 'cnctm');
-- delete from public.classes where slug = 'cnctm';
-- delete from public.academic_subjects where code = 'cnctm';
-- commit;
