-- AVCN: thêm chương 12 + bài 12 "Đề thi thử cuối kỳ" (chứa 10 đề thi thử ở mục Kiểm tra).
-- Chỉ dữ liệu (chapters / chapter_classes / lessons), không đổi schema/policy/hàm. Idempotent.
-- Bài tạo published=false; 10 đề được nạp bằng content/lesson-samples/avcn-de-thi-thu/sql.py rồi bật Hiện sau khi soát.

begin;

insert into public.chapters (title, sort_order, subject_code)
select 'Đề thi thử cuối kỳ', 12, 'avcn'
where not exists (select 1 from public.chapters where subject_code = 'avcn' and sort_order = 12);

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x
join public.classes c on c.slug = 'avcn'
where x.subject_code = 'avcn' and x.sort_order = 12
on conflict do nothing;

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, 'Đề thi thử cuối kỳ (Mock Exams)', 12, false
from public.chapters x
where x.subject_code = 'avcn' and x.sort_order = 12
  and not exists (select 1 from public.lessons y where y.chapter_id = x.id and y.sort_order = 12);

commit;

-- Kiểm: phải có 1 dòng.
select y.id, y.title, y.published from public.lessons y join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'avcn' and y.sort_order = 12;

-- ROLLBACK (chạy tay khi cần):
-- begin;
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'avcn' and y.sort_order = 12);
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'avcn' and sort_order = 12);
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'avcn' and sort_order = 12);
-- delete from public.chapters where subject_code = 'avcn' and sort_order = 12;
-- commit;
