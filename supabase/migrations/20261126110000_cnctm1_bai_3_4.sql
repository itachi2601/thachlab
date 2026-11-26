-- Công nghệ chế tạo máy 1 (lớp/môn 'cnctm', đã tạo ở 20261126100000_lop_cnctm1_bai_1_2.sql):
--   thêm chương 3 + Bài 3 Phôi và lượng dư gia công, chương 4 + Bài 4 Chuẩn
--   (published=false, bật sau khi upload-lesson.mts ghi nội dung và thầy duyệt).
-- Chỉ chèn dữ liệu, idempotent, không đổi schema/policy/hàm. Rollback ở cuối file.
begin;

create temporary table _cnctm_ls34 (so int, chuong text, bai text) on commit drop;
insert into _cnctm_ls34 values
  (3, 'Phôi và lượng dư gia công', 'Bài 3. Phôi và lượng dư gia công'),
  (4, 'Chuẩn', 'Bài 4. Chuẩn');

insert into public.chapters (title, sort_order, subject_code)
select l.chuong, l.so, 'cnctm'
from _cnctm_ls34 l
where not exists (select 1 from public.chapters x where x.subject_code = 'cnctm' and x.sort_order = l.so);

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x
join _cnctm_ls34 l on l.so = x.sort_order
cross join public.classes c
where x.subject_code = 'cnctm' and c.slug = 'cnctm'
  and not exists (select 1 from public.chapter_classes cc where cc.chapter_id = x.id and cc.class_id = c.id);

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, l.bai, l.so, false
from _cnctm_ls34 l
join public.chapters x on x.subject_code = 'cnctm' and x.sort_order = l.so
where not exists (select 1 from public.lessons y where y.chapter_id = x.id);

commit;

-- In id bài để chạy tiếp: npx tsx scripts/upload-lesson.mts content/lesson-samples/cnctm1-bai-<n>-…/bundle.json --lesson <id>
select y.id, y.title, y.published from public.lessons y join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'cnctm' and x.sort_order in (3, 4) order by x.sort_order;

-- ROLLBACK (chạy tay khi cần; chỉ gỡ chương/bài 3 và 4 của môn cnctm):
-- begin;
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'cnctm' and x.sort_order in (3, 4));
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'cnctm' and sort_order in (3, 4));
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'cnctm' and sort_order in (3, 4));
-- delete from public.chapters where subject_code = 'cnctm' and sort_order in (3, 4);
-- commit;
