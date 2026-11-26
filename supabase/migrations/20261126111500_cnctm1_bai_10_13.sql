-- CNCTM 1 (lớp 'cnctm'): thêm Bài 10–13, mỗi bài một chương (subject_code 'cnctm', sort_order 10–13)
--   Bài 10 Gia công ren · Bài 11 Gia công then – then hoa · Bài 12 Gia công bánh răng · Bài 13 Gia công mặt định hình.
--   published=false, bật sau khi upload-lesson.mts ghi nội dung và thầy duyệt.
-- Cần chạy sau 20261126100000_lop_cnctm1_bai_1_2.sql (môn/lớp 'cnctm' đã có). Không chèn lại môn/lớp/lớp học phần.
-- Chỉ chèn dữ liệu, idempotent, không đổi schema/policy/hàm. Rollback ở cuối file.
begin;

create temporary table _cnctm_ls_10_13 (so int, chuong text, bai text) on commit drop;
insert into _cnctm_ls_10_13 values
  (10, 'Gia công ren', 'Bài 10. Gia công ren'),
  (11, 'Gia công then – then hoa', 'Bài 11. Gia công then – then hoa'),
  (12, 'Gia công bánh răng', 'Bài 12. Gia công bánh răng'),
  (13, 'Gia công mặt định hình', 'Bài 13. Gia công mặt định hình');

insert into public.chapters (title, sort_order, subject_code)
select l.chuong, l.so, 'cnctm'
from _cnctm_ls_10_13 l
where not exists (select 1 from public.chapters x where x.subject_code = 'cnctm' and x.sort_order = l.so);

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x, public.classes c
where x.subject_code = 'cnctm' and x.sort_order between 10 and 13 and c.slug = 'cnctm'
  and not exists (select 1 from public.chapter_classes cc where cc.chapter_id = x.id and cc.class_id = c.id);

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, l.bai, l.so, false
from _cnctm_ls_10_13 l
join public.chapters x on x.subject_code = 'cnctm' and x.sort_order = l.so
where not exists (select 1 from public.lessons y where y.chapter_id = x.id);

commit;

-- In id bài để chạy tiếp: npx tsx scripts/upload-lesson.mts content/lesson-samples/cnctm1-bai-<n>-…/bundle.json --lesson <id>
select x.sort_order, y.id, y.title, y.published from public.lessons y join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'cnctm' and x.sort_order between 10 and 13 order by x.sort_order;

-- ROLLBACK (chạy tay khi cần; chỉ xoá Bài 10–13):
-- begin;
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'cnctm' and x.sort_order between 10 and 13);
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'cnctm' and sort_order between 10 and 13);
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'cnctm' and sort_order between 10 and 13);
-- delete from public.chapters where subject_code = 'cnctm' and sort_order between 10 and 13;
-- commit;
