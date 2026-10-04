-- Gắn khối 12 cho câu ngân hàng đến từ đề thi thử TN / đề phát triển minh hoạ (grade đang rỗng, chưa có chủ đề).
-- Chỉ đụng cột grade (không kích hoạt trg_bank_tags_to_exams, trigger đó chỉ chạy khi đổi topic/form/difficulty).
-- Chạy được lúc nào cũng được (một UPDATE ngắn, idempotent).
create table if not exists public.question_bank_grade_fix_20261004 (id bigint primary key);

with todo as (
  select qb.id
  from public.question_bank qb
  join public.exams e on e.id = qb.source_exam_id
  where qb.grade = ''
    and e.title ~* '(thi thử TN|minh hoạ|minh họa)'
), logged as (
  insert into public.question_bank_grade_fix_20261004 select id from todo on conflict do nothing returning id
)
update public.question_bank set grade = '12' where id in (select id from todo);

-- ROLLBACK:
--   update public.question_bank set grade = '' where id in (select id from public.question_bank_grade_fix_20261004);
--   drop table public.question_bank_grade_fix_20261004;
