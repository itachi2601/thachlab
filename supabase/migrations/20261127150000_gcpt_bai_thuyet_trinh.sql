-- GCPT: thêm bài "Hướng dẫn thuyết trình nhóm" vào chương 1 (Tổng quan), đứng sau Bài 1 (sort_order 2).
-- published=false; bật sau khi upload-lesson.mts ghi nội dung (content/lesson-samples/gcpt-thuyet-trinh/bundle.json) và thầy duyệt.
-- Chỉ chèn 1 dòng, idempotent, không đổi schema/policy/hàm. Rollback ở cuối file.
begin;

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, 'Hướng dẫn thuyết trình nhóm', 2, false
from public.chapters x
where x.subject_code = 'gcpt' and x.sort_order = 1
  and not exists (select 1 from public.lessons y where y.chapter_id = x.id and y.title = 'Hướng dẫn thuyết trình nhóm');

commit;

-- In id bài để chạy tiếp: npx tsx scripts/upload-lesson.mts content/lesson-samples/gcpt-thuyet-trinh/bundle.json --lesson <id>
select y.id, y.title, y.sort_order, y.published from public.lessons y join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'gcpt' and x.sort_order = 1 order by y.sort_order;

-- ROLLBACK (chạy tay khi cần):
-- begin;
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'gcpt' and y.title = 'Hướng dẫn thuyết trình nhóm');
-- delete from public.lessons where id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'gcpt' and y.title = 'Hướng dẫn thuyết trình nhóm');
-- commit;
