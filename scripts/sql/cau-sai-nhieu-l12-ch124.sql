-- Câu HS sai nhiều nhất theo chủ đề, L12 Ch.1/2/4 (chapters 2, 3, 5), 30 ngày — nguồn tình huống clip bẫy bay-ch1/2/4 (12/11/2026).
-- CHỈ ĐỌC, số gộp, không cột HS. Chạy từ checkout chính: supabase db query --linked -f scripts/sql/cau-sai-nhieu-l12-ch124.sql -o json
-- question_index là chỉ số mảng exams.questions (0-based).
with tp as (
  select t.id, t.name, t.chapter_id from question_topics t where t.chapter_id in (2, 3, 5)
),
g as (
  select r.topic_id, r.exam_id, r.question_index, count(*) luot, count(*) filter (where r.earned < r.max) sai
  from exam_question_results r
  where r.created_at > now() - interval '30 days' and r.topic_id in (select id from tp)
  group by 1, 2, 3 having count(*) >= 12
),
x as (
  select g.*, round(100.0 * sai / luot) pct,
         row_number() over (partition by g.topic_id order by 1.0 * sai / luot desc, luot desc) rk
  from g
)
select tp.chapter_id ch, x.topic_id, tp.name, x.exam_id, x.question_index qi, x.sai, x.luot, x.pct,
       e.questions -> x.question_index ->> 'type' typ,
       e.questions -> x.question_index ->> 'question' cau,
       e.questions -> x.question_index -> 'options' pa,
       e.questions -> x.question_index -> 'answer' da
from x join tp on tp.id = x.topic_id join exams e on e.id = x.exam_id
where x.rk <= 2 order by tp.chapter_id, x.pct desc;
