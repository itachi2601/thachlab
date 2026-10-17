-- Khoá Vật lí HSG & chuyên — thêm YCCĐ (question_topics) cho CĐ14 Gương phẳng, bóng tối (bài 158) và CĐ17 Thiên văn (bài 178).
-- Ngân hàng chưa có chủ đề nào về phản xạ/gương phẳng/bóng hay Trái Đất – bầu trời, nên bài tập mẫu hai bài này
-- không gắn được topic (publish-bai-tap-mau.mts bắt topic phải có trong question-topics.json). Chỉ chèn, idempotent theo tên.
begin;

with cha(name, lesson_id, sort_order) as (values
  ('Gương phẳng, bóng tối và nửa tối', 158, 400),
  ('Trái Đất và bầu trời', 178, 410))
insert into public.question_topics (subject_code, grade, chapter_id, lesson_id, name, sort_order, parent_id)
select 'vat-ly', '9', 35, c.lesson_id, c.name, c.sort_order, null from cha c
where not exists (select 1 from public.question_topics t where t.name = c.name and t.parent_id is null);

with con(parent, name, lesson_id, sort_order) as (values
  ('Gương phẳng, bóng tối và nửa tối', 'Định luật phản xạ ánh sáng', 158, 401),
  ('Gương phẳng, bóng tối và nửa tối', 'Ảnh của vật tạo bởi gương phẳng', 158, 402),
  ('Gương phẳng, bóng tối và nửa tối', 'Bóng tối, bóng nửa tối', 158, 403),
  ('Trái Đất và bầu trời', 'Pha Mặt Trăng, nhật thực và nguyệt thực', 178, 411),
  ('Trái Đất và bầu trời', 'Chuyển động nhìn thấy của Mặt Trời, ngày đêm và mùa', 178, 412),
  ('Trái Đất và bầu trời', 'Hệ Mặt Trời và Ngân Hà', 178, 413))
insert into public.question_topics (subject_code, grade, chapter_id, lesson_id, name, sort_order, parent_id)
select 'vat-ly', '9', 35, c.lesson_id, c.name, c.sort_order, p.id
from con c join public.question_topics p on p.name = c.parent and p.parent_id is null
where not exists (select 1 from public.question_topics t where t.name = c.name);

commit;

-- ROLLBACK (khi chưa có câu nào gắn các topic này):
--   delete from public.question_topics where lesson_id in (158,178) and parent_id is not null;
--   delete from public.question_topics where lesson_id in (158,178) and parent_id is null;
