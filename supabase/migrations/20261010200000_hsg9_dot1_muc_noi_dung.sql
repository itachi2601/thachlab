-- Khoá Vật lí HSG & chuyên — đợt 1: tạo mục ly_thuyet + bai_tap_mau (rỗng) cho CĐ00, CĐ10, CĐ11, CĐ13
-- (lesson 160, 155, 154, 162) để cap-nhat-ly-thuyet.sh / publish-bai-tap-mau.mts ghi nội dung vào.
-- Bật Hiện bài CĐ00 (160); CĐ10, CĐ11, CĐ13 đã Hiện sẵn. Chỉ thêm dữ liệu, idempotent.
begin;

insert into public.lesson_items (lesson_id, kind, title, subtitle, body_html, sort_order, required, exam_ids, questions, published_at)
select ls.id, 'ly_thuyet', 'Lý thuyết nâng cao', '', '<p>Đang soạn.</p>', 1, true, '{}', '[]'::jsonb, now()
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where ls.id in (154, 155, 160, 162)
  and not exists (select 1 from public.lesson_items i where i.lesson_id = ls.id and i.kind = 'ly_thuyet');

insert into public.lesson_items (lesson_id, kind, title, subtitle, body_html, sort_order, required, exam_ids, questions, published_at)
select ls.id, 'bai_tap_mau', 'Các dạng bài tập', '', '', 2, true, '{}', '[]'::jsonb, now()
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where ls.id in (154, 155, 160, 162)
  and not exists (select 1 from public.lesson_items i where i.lesson_id = ls.id and i.kind = 'bai_tap_mau');

update public.lessons set published = true where id = 160 and title like 'Chuyên đề 00.%';

commit;

-- ROLLBACK (chỉ khi chưa ghi nội dung; nếu đã ghi thì mất nội dung — khôi phục từ scripts/logs/):
--   delete from public.lesson_items where lesson_id in (154,155,160,162) and kind in ('ly_thuyet','bai_tap_mau');
--   update public.lessons set published = false where id = 160;
