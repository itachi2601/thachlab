-- Gắn khối 10 cho câu ngân hàng đến từ các đề lớp 10 (đợt đăng đề L10 năm 24-25 và /23, 4/10/2026) đang có grade rỗng.
-- Chỉ gắn khi MỌI mục chứa đề gốc đều thuộc chương của lớp 10 (chapter_classes -> classes.name = '10');
-- đề không gắn mục nào hoặc gắn lẫn lớp khác thì bỏ qua (để xem tay).
-- Chỉ đụng cột grade (không kích hoạt trg_bank_tags_to_exams — trigger chỉ chạy khi đổi topic/form/difficulty).
-- Chạy lúc nào cũng được (một UPDATE ngắn, idempotent). Kỳ vọng ~6.250 câu.
create table if not exists public.question_bank_grade_fix_20261005 (id bigint primary key);

with exam_grade as (
  select e.id as exam_id,
         bool_and(cl.name = '10') as all_l10
  from public.exams e
  join public.lesson_items li on e.id = any(li.exam_ids)
  join public.lessons l on l.id = li.lesson_id
  join public.chapter_classes cc on cc.chapter_id = l.chapter_id
  join public.classes cl on cl.id = cc.class_id
  group by e.id
), todo as (
  select qb.id
  from public.question_bank qb
  join exam_grade eg on eg.exam_id = qb.source_exam_id and eg.all_l10
  where qb.grade = ''
), logged as (
  insert into public.question_bank_grade_fix_20261005 select id from todo on conflict do nothing returning id
)
update public.question_bank set grade = '10' where id in (select id from todo);

-- ROLLBACK:
--   update public.question_bank set grade = '' where id in (select id from public.question_bank_grade_fix_20261005);
--   drop table public.question_bank_grade_fix_20261005;
