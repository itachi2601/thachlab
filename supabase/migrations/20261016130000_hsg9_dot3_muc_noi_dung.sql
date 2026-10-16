-- Khoá Vật lí HSG & chuyên — đợt 3 (mảng Nhiệt – âm): tạo mục ly_thuyet + bai_tap_mau (rỗng) cho CĐ15 Âm thanh,
-- CĐ16 Truyền nhiệt & nở vì nhiệt, CĐ12 Nhiệt học (lesson 150, 164, 153) để cap-nhat-ly-thuyet.sh /
-- publish-bai-tap-mau.mts ghi nội dung vào. Bài vẫn ẩn (published=false) tới khi thầy duyệt. Chỉ thêm dữ liệu, idempotent.
begin;

insert into public.lesson_items (lesson_id, kind, title, subtitle, body_html, sort_order, required, exam_ids, questions, published_at)
select ls.id, 'ly_thuyet', 'Lý thuyết nâng cao', '', '<p>Đang soạn.</p>', 1, true, '{}', '[]'::jsonb, now()
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where ls.id in (150, 153, 164)
  and not exists (select 1 from public.lesson_items i where i.lesson_id = ls.id and i.kind = 'ly_thuyet');

insert into public.lesson_items (lesson_id, kind, title, subtitle, body_html, sort_order, required, exam_ids, questions, published_at)
select ls.id, 'bai_tap_mau', 'Các dạng bài tập', '', '', 2, true, '{}', '[]'::jsonb, now()
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where ls.id in (150, 153, 164)
  and not exists (select 1 from public.lesson_items i where i.lesson_id = ls.id and i.kind = 'bai_tap_mau');

commit;

-- ROLLBACK (chỉ khi chưa ghi nội dung):
--   delete from public.lesson_items where lesson_id in (150,153,164) and kind in ('ly_thuyet','bai_tap_mau')
--     and (body_html in ('', '<p>Đang soạn.</p>')) and questions = '[]'::jsonb;
