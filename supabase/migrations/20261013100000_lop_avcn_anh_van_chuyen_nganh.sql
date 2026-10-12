-- Lớp "Anh văn chuyên ngành Cơ khí" (CTTC, vào tự do) + môn 'avcn' + 1 chương + 10 bài (Chapter 1–10 giáo trình
-- Technical English for Mechanical Engineering). Chỉ Chapter 8 công bố (bài mẫu 13/10/2026); 9 chương còn lại ẩn
-- chờ soạn bằng skill soan-bai-avcn. Chỉ chèn dữ liệu, idempotent, không đổi schema/policy. Rollback ở cuối file.
begin;

insert into public.academic_subjects (code, label, icon, sort_order, active)
values ('avcn', 'Anh văn chuyên ngành Cơ khí', '📘', 5, true)
on conflict (code) do nothing;

insert into public.classes (name, slug, color, icon, sort_order, active, requires_approval)
select 'Anh văn chuyên ngành Cơ khí', 'avcn', '#0284C7', '📘', 6, true, false
where not exists (select 1 from public.classes where slug = 'avcn');

insert into public.chapters (title, sort_order, subject_code)
select 'Technical English for Mechanical Engineering', 1, 'avcn'
where not exists (select 1 from public.chapters where subject_code = 'avcn');

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x, public.classes c
where x.subject_code = 'avcn' and c.slug = 'avcn'
  and not exists (select 1 from public.chapter_classes cc where cc.chapter_id = x.id and cc.class_id = c.id);

create temporary table _avcn_ls (so int, title text) on commit drop;
insert into _avcn_ls values
  (1, 'Chapter 1: Engineering and the Mechanical Engineer'),
  (2, 'Chapter 2: Safety at Work'),
  (3, 'Chapter 3: Hand Tools'),
  (4, 'Chapter 4: Measurements'),
  (5, 'Chapter 5: Mechanical Fasteners'),
  (6, 'Chapter 6: Welding'),
  (7, 'Chapter 7: Metal Forming and Casting'),
  (8, 'Chapter 8: Chipping Machining — Gia công cắt gọt'),
  (9, 'Chapter 9: Computer-Aided Design & Manufacturing (CAD/CAM)'),
  (10, 'Chapter 10: Maintenance');

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, l.title, l.so, (l.so = 8)
from _avcn_ls l, public.chapters x
where x.subject_code = 'avcn'
  and not exists (select 1 from public.lessons y where y.chapter_id = x.id and y.sort_order = l.so);

commit;

-- In id bài Chapter 8 để chạy tiếp: npx tsx scripts/upload-lesson.mts content/lesson-samples/avcn-chapter-8-chipping-machining/bundle.json --lesson <id>
select y.id, y.title from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'avcn' order by y.sort_order;

-- ROLLBACK (chạy tay khi cần):
-- begin;
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'avcn');
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'avcn');
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'avcn');
-- delete from public.chapters where subject_code = 'avcn';
-- delete from public.user_classes where class_id in (select id from public.classes where slug = 'avcn');
-- delete from public.classes where slug = 'avcn';
-- delete from public.academic_subjects where code = 'avcn';
-- commit;
