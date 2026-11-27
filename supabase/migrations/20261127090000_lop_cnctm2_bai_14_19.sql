-- Học phần "Công nghệ chế tạo máy 2" (CTTC, SV CĐ Cơ khí), theo mẫu CNCTM 1 / gcpt:
--   môn 'cnctm2' (academic_subjects) + lớp 'cnctm2' (classes, vào có duyệt) + mỗi bài một chương,
--   6 bài theo đúng số chương giáo trình (Phần III QTCN chi tiết điển hình): Bài 14 trục … Bài 19 lắp ráp,
--   published=false (bật sau khi upload-lesson.mts ghi nội dung và thầy duyệt).
--   Thêm 'cnctm2' vào danh mục CTTC (subjects). CHƯA tạo lớp học phần (course_offerings) vì chưa biết lớp/năm học
--   — thầy báo rồi thêm (mẫu: migration 20261126100000_lop_cnctm1_bai_1_2.sql).
-- Chỉ chèn dữ liệu, idempotent, không đổi schema/policy/hàm. Rollback ở cuối file.
begin;

insert into public.academic_subjects (code, label, icon, sort_order, active)
values ('cnctm2', 'Công nghệ chế tạo máy 2', '🔩', 8, true)
on conflict (code) do nothing;

insert into public.classes (name, slug, color, icon, sort_order, active, requires_approval)
select 'Công nghệ chế tạo máy 2', 'cnctm2', '#334155', '🔩', 11, true, true
where not exists (select 1 from public.classes where slug = 'cnctm2');

create temporary table _cnctm2_ls (so int, chuong text, bai text) on commit drop;
insert into _cnctm2_ls values
  (14, 'Chi tiết dạng trục', 'Bài 14. Công nghệ gia công chi tiết dạng trục'),
  (15, 'Chi tiết dạng càng', 'Bài 15. Công nghệ gia công chi tiết dạng càng'),
  (16, 'Chi tiết dạng bạc', 'Bài 16. Công nghệ gia công chi tiết dạng bạc'),
  (17, 'Chi tiết dạng hộp', 'Bài 17. Công nghệ gia công chi tiết dạng hộp'),
  (18, 'Chi tiết bánh răng', 'Bài 18. Công nghệ gia công chi tiết bánh răng'),
  (19, 'Công nghệ lắp ráp', 'Bài 19. Công nghệ lắp ráp');

insert into public.chapters (title, sort_order, subject_code)
select l.chuong, l.so, 'cnctm2'
from _cnctm2_ls l
where not exists (select 1 from public.chapters x where x.subject_code = 'cnctm2' and x.sort_order = l.so);

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x, public.classes c
where x.subject_code = 'cnctm2' and c.slug = 'cnctm2'
  and not exists (select 1 from public.chapter_classes cc where cc.chapter_id = x.id and cc.class_id = c.id);

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, l.bai, l.so, false
from _cnctm2_ls l
join public.chapters x on x.subject_code = 'cnctm2' and x.sort_order = l.so
where not exists (select 1 from public.lessons y where y.chapter_id = x.id);

insert into public.subjects (code, name, area, is_practicum)
values ('cnctm2', 'Công nghệ chế tạo máy 2', 'cttc', false)
on conflict (code) do nothing;

commit;

-- In id bài để chạy tiếp: npx tsx scripts/upload-lesson.mts content/lesson-samples/cnctm2-bai-<n>-…/bundle.json --lesson <id>
select y.id, y.title, y.published from public.lessons y join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'cnctm2' order by x.sort_order;

-- ROLLBACK (chạy tay khi cần; xoá cả nội dung bài của môn này):
-- begin;
-- delete from public.subjects where code = 'cnctm2';
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'cnctm2');
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'cnctm2');
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'cnctm2');
-- delete from public.chapters where subject_code = 'cnctm2';
-- delete from public.user_classes where class_id in (select id from public.classes where slug = 'cnctm2');
-- delete from public.classes where slug = 'cnctm2';
-- delete from public.academic_subjects where code = 'cnctm2';
-- commit;
