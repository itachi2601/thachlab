-- Công nghệ chế tạo máy 1 (lớp 'cnctm', CĐ CK 25C): thêm chương/bài 5 và 6.
--   Bài 5. Độ chính xác gia công · Bài 6. Thiết kế quy trình công nghệ (published=false,
--   bật sau khi upload-lesson.mts ghi nội dung và thầy duyệt).
-- Môn, lớp, subjects, course_offering đã có từ 20261126100000_lop_cnctm1_bai_1_2.sql (chạy trước file này).
-- Chỉ chèn dữ liệu, idempotent, không đổi schema/policy/hàm. Rollback ở cuối file.
begin;

create temporary table _cnctm_ls (so int, chuong text, bai text) on commit drop;
insert into _cnctm_ls values
  (5, 'Độ chính xác gia công', 'Bài 5. Độ chính xác gia công'),
  (6, 'Thiết kế quy trình công nghệ', 'Bài 6. Thiết kế quy trình công nghệ');

insert into public.chapters (title, sort_order, subject_code)
select l.chuong, l.so, 'cnctm'
from _cnctm_ls l
where not exists (select 1 from public.chapters x where x.subject_code = 'cnctm' and x.sort_order = l.so);

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x
join _cnctm_ls l on l.so = x.sort_order
cross join public.classes c
where x.subject_code = 'cnctm' and c.slug = 'cnctm'
  and not exists (select 1 from public.chapter_classes cc where cc.chapter_id = x.id and cc.class_id = c.id);

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, l.bai, l.so, false
from _cnctm_ls l
join public.chapters x on x.subject_code = 'cnctm' and x.sort_order = l.so
where not exists (select 1 from public.lessons y where y.chapter_id = x.id);

commit;

-- In id bài để chạy tiếp: npx tsx scripts/upload-lesson.mts content/lesson-samples/cnctm1-bai-<n>-…/bundle.json --lesson <id>
select y.id, y.title, y.published from public.lessons y join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'cnctm' and x.sort_order in (5, 6) order by x.sort_order;

-- ROLLBACK (chạy tay khi cần; chỉ gỡ chương/bài 5–6, giữ môn, lớp và bài khác):
-- begin;
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'cnctm' and x.sort_order in (5, 6));
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'cnctm' and sort_order in (5, 6));
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'cnctm' and sort_order in (5, 6));
-- delete from public.chapters where subject_code = 'cnctm' and sort_order in (5, 6);
-- commit;
