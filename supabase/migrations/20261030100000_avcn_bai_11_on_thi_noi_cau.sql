-- AVCN: thêm bài 11 "Ôn tập: Thì và nối câu" (chương 11, 1 bài, published=false — thầy bật sau khi duyệt).
-- Chỉ dữ liệu (chapters / chapter_classes / lessons), không đổi schema/policy/hàm. Idempotent.

begin;

insert into public.chapters (title, sort_order, subject_code)
select 'Ôn thì và nối câu', 11, 'avcn'
where not exists (select 1 from public.chapters where subject_code = 'avcn' and sort_order = 11);

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x
join public.classes c on c.slug = 'avcn'
where x.subject_code = 'avcn' and x.sort_order = 11
on conflict do nothing;

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, 'Ôn tập: Thì và nối câu (Tenses & Joining Sentences)', 11, false
from public.chapters x
where x.subject_code = 'avcn' and x.sort_order = 11
  and not exists (select 1 from public.lessons y where y.chapter_id = x.id and y.sort_order = 11);

commit;

-- Kiểm: phải có 1 dòng, published=false.
select y.id, y.title, y.published from public.lessons y join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'avcn' and y.sort_order = 11;

-- ROLLBACK (chạy tay khi cần):
-- begin;
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'avcn' and y.sort_order = 11);
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'avcn' and sort_order = 11);
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'avcn' and sort_order = 11);
-- delete from public.chapters where subject_code = 'avcn' and sort_order = 11;
-- commit;
