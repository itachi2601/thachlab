-- Khoá Vật lí HSG & chuyên — đợt 4 (Quang – Trái Đất, Điện từ – năng lượng): tạo mục ly_thuyet + bai_tap_mau (rỗng) cho CĐ06, CĐ07, CĐ14, CĐ08, CĐ09
-- (lesson 151, 156, 158, 152, 163; CĐ17 = 178 đã có mục) để cap-nhat-ly-thuyet.sh /
-- publish-bai-tap-mau.mts ghi nội dung vào. Bài vẫn ẩn (published=false) tới khi thầy duyệt. Chỉ thêm dữ liệu, idempotent.
begin;

insert into public.lesson_items (lesson_id, kind, title, subtitle, body_html, sort_order, required, exam_ids, questions, published_at)
select ls.id, 'ly_thuyet', 'Lý thuyết nâng cao', '', '<p>Đang soạn.</p>', 1, true, '{}', '[]'::jsonb, now()
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where ls.id in (151, 156, 158, 152, 163)
  and not exists (select 1 from public.lesson_items i where i.lesson_id = ls.id and i.kind = 'ly_thuyet');

insert into public.lesson_items (lesson_id, kind, title, subtitle, body_html, sort_order, required, exam_ids, questions, published_at)
select ls.id, 'bai_tap_mau', 'Các dạng bài tập', '', '', 2, true, '{}', '[]'::jsonb, now()
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where ls.id in (151, 156, 158, 152, 163)
  and not exists (select 1 from public.lesson_items i where i.lesson_id = ls.id and i.kind = 'bai_tap_mau');

commit;

-- ROLLBACK (chỉ khi chưa ghi nội dung):
--   delete from public.lesson_items where lesson_id in (151,156,158,152,163) and kind in ('ly_thuyet','bai_tap_mau')
--     and (body_html in ('', '<p>Đang soạn.</p>')) and questions = '[]'::jsonb;
