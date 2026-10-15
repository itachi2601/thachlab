-- Khoá Vật lí HSG & chuyên — thêm Chuyên đề 17 "Thiên văn" (phần chung ~30% đề cương THI HSG 9 KHTN 26-27:
-- chuyển động nhìn thấy của Mặt Trăng, Hệ Mặt Trời, Ngân Hà) và thu CĐ14 về còn gương phẳng + bóng.
-- Bài mới ẩn (published=false) tới khi thầy duyệt. Chỉ thêm/đổi chữ, idempotent, không đụng nội dung đã soạn.
begin;

-- CĐ14 chưa có nội dung (lesson 158): chỉ đổi tên + mô tả, phần thiên văn chuyển sang CĐ17.
update public.lessons ls
set title = 'Chuyên đề 14. Gương phẳng, bóng tối và nửa tối',
    description = 'Phản xạ ánh sáng, ảnh qua gương phẳng, hệ gương, vùng bóng tối – nửa tối.'
from public.chapters ch
where ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
  and ls.title like 'Chuyên đề 14.%'
  and ls.title <> 'Chuyên đề 14. Gương phẳng, bóng tối và nửa tối';

insert into public.lessons (chapter_id, title, sort_order, published, lesson_kind, description)
select ch.id, 'Chuyên đề 17. Thiên văn: Mặt Trăng, Hệ Mặt Trời và Ngân Hà', 4, false, 'bai_hoc',
       'Chuyển động nhìn thấy của Mặt Trăng, pha Mặt Trăng, nhật thực – nguyệt thực, Hệ Mặt Trời, Ngân Hà, đơn vị khoảng cách thiên văn.'
from public.chapters ch
where ch.subject_code = 'hsg-vat-ly' and ch.title = 'Quang học và Trái Đất – bầu trời'
  and not exists (select 1 from public.lessons x where x.chapter_id = ch.id and x.title like 'Chuyên đề 17.%');

insert into public.lesson_items (lesson_id, kind, title, subtitle, body_html, sort_order, required, exam_ids, questions, published_at)
select ls.id, 'ly_thuyet', 'Lý thuyết nâng cao', '', '<p>Đang soạn.</p>', 1, true, '{}', '[]'::jsonb, now()
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where ls.title like 'Chuyên đề 17.%'
  and not exists (select 1 from public.lesson_items i where i.lesson_id = ls.id and i.kind = 'ly_thuyet');

insert into public.lesson_items (lesson_id, kind, title, subtitle, body_html, sort_order, required, exam_ids, questions, published_at)
select ls.id, 'bai_tap_mau', 'Các dạng bài tập', '', '', 2, true, '{}', '[]'::jsonb, now()
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where ls.title like 'Chuyên đề 17.%'
  and not exists (select 1 from public.lesson_items i where i.lesson_id = ls.id and i.kind = 'bai_tap_mau');

commit;

select ls.id as lesson_id, ls.title, ls.published
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where ls.title like 'Chuyên đề 14.%' or ls.title like 'Chuyên đề 17.%';

-- ROLLBACK (chỉ khi CĐ17 chưa có nội dung):
--   delete from public.lesson_items where lesson_id in (select id from public.lessons where title like 'Chuyên đề 17.%');
--   delete from public.lessons where title like 'Chuyên đề 17.%' and chapter_id in (select id from public.chapters where subject_code='hsg-vat-ly');
--   update public.lessons set title='Chuyên đề 14. Gương phẳng và Trái Đất – bầu trời' where id=158;
