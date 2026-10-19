-- Lớp "Giải Vật lí trên máy tính cầm tay" (Casio fx-580VN X) + môn 'casio-vat-ly' + 1 chương + 5 bài (ẩn):
-- sổ tay máy, dao động cơ, sóng cơ, điện xoay chiều, điện từ & sóng ánh sáng. Nội dung đăng sau bằng
-- scripts/dang-casio-vat-ly.mts. Chỉ chèn dữ liệu, idempotent, không đổi schema/policy. Rollback ở cuối file.
begin;

insert into public.academic_subjects (code, label, icon, sort_order, active)
values ('casio-vat-ly', 'Giải Vật lí trên máy tính cầm tay', '🧮', 6, true)
on conflict (code) do nothing;

insert into public.classes (name, slug, color, icon, sort_order, active, requires_approval)
select 'Giải Vật lí trên máy tính cầm tay', 'casio-vat-ly', '#F59E0B', '🧮', 7, true, false
where not exists (select 1 from public.classes where slug = 'casio-vat-ly');

insert into public.chapters (title, sort_order, subject_code)
select 'Giải Vật lí bằng Casio fx-580VN X', 1, 'casio-vat-ly'
where not exists (select 1 from public.chapters where subject_code = 'casio-vat-ly');

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x, public.classes c
where x.subject_code = 'casio-vat-ly' and c.slug = 'casio-vat-ly'
  and not exists (select 1 from public.chapter_classes cc where cc.chapter_id = x.id and cc.class_id = c.id);

create temporary table _casio_ls (so int, title text) on commit drop;
insert into _casio_ls values
  (1, 'Sổ tay máy Casio fx-580VN X'),
  (2, 'Dao động cơ'),
  (3, 'Sóng cơ'),
  (4, 'Điện xoay chiều'),
  (5, 'Điện từ và sóng ánh sáng');

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, l.title, l.so, false
from _casio_ls l, public.chapters x
where x.subject_code = 'casio-vat-ly'
  and not exists (select 1 from public.lessons y where y.chapter_id = x.id and y.sort_order = l.so);

commit;

-- In id 5 bài để chạy script đăng: bash scripts/dang-casio-vat-ly.sh (script tự tra id theo tên bài)
select y.id, y.title, y.published from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'casio-vat-ly' order by y.sort_order;

-- ROLLBACK (chạy tay khi cần):
-- begin;
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'casio-vat-ly');
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'casio-vat-ly');
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'casio-vat-ly');
-- delete from public.chapters where subject_code = 'casio-vat-ly';
-- delete from public.user_classes where class_id in (select id from public.classes where slug = 'casio-vat-ly');
-- delete from public.classes where slug = 'casio-vat-ly';
-- delete from public.academic_subjects where code = 'casio-vat-ly';
-- commit;
