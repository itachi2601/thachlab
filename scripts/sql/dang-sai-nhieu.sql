-- Dạng bài HS sai nhiều nhất (question_dang × exam_question_results), 60 ngày — chọn dạng gắn ⚖ Lập tỉ số
-- (chặng 8, docs/KE-HOACH-MEO-GIAI-BAI-TAP.md mục 7). CHỈ ĐỌC, số gộp, không cột HS.
-- Chạy từ checkout chính: supabase db query --linked -f scripts/sql/dang-sai-nhieu.sql -o json
-- Nối câu đề → ngân hàng qua (source_exam_id, source_index) = (exam_id, question_index).
with r as (
  select qd.lesson_id, qd.dang_label, r.earned, r.max
  from exam_question_results r
  join question_bank qb on qb.source_exam_id = r.exam_id and qb.source_index = r.question_index
  join question_dang qd on qd.question_id = qb.id
  where r.created_at > now() - interval '60 days' and r.max > 0
)
select r.lesson_id, l.title bai, r.dang_label,
       count(*) luot, count(*) filter (where r.earned < r.max) sai,
       round(100.0 * count(*) filter (where r.earned < r.max) / count(*)) pct
from r join lessons l on l.id = r.lesson_id
group by 1, 2, 3 having count(*) >= 20
order by pct desc, luot desc
limit 150;
