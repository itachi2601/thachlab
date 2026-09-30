-- Độ phủ ngân hàng theo danh hiệu chuyên môn (CHỈ ĐỌC) — GĐ 1.
-- Với mỗi danh hiệu: số câu KHÁC NHAU (trắc nghiệm, đề đã đăng) theo Dễ/TB/Khó so với ngưỡng
-- min_de/min_tb/min_kho. Cột *_thieu > 0 = học sinh không thể đạt mức đó -> tắt danh hiệu hoặc hạ ngưỡng.
-- Chạy trên Mac: supabase db query --linked -f scripts/sql/title-bank-coverage.sql
with per_q as (
  select rt.code,
         e.id as exam_id, q.idx,
         q.q ->> 'difficulty' as difficulty
  from public.rank_titles rt
  join public.rank_title_topics tt on tt.title_code = rt.code
  join public.question_topics qt on qt.id = tt.topic_id or qt.parent_id = tt.topic_id
  join public.exams e on e.published
  cross join lateral jsonb_array_elements(e.questions) with ordinality as q(q, idx)
  where rt.kind = 'specialist' and rt.enabled
    and btrim(q.q ->> 'topic') = qt.name
    and coalesce(q.q ->> 'type', '') <> 'essay'
  group by rt.code, e.id, q.idx, q.q ->> 'difficulty'
)
select rt.code, rt.name,
       count(*) filter (where p.difficulty = 'de')         as cau_de,   rt.min_de  as can_de,
       count(*) filter (where p.difficulty = 'trung-binh') as cau_tb,   rt.min_tb  as can_tb,
       count(*) filter (where p.difficulty = 'kho')        as cau_kho,  rt.min_kho as can_kho,
       greatest(rt.min_de  - count(*) filter (where p.difficulty = 'de'), 0)         as de_thieu,
       greatest(rt.min_tb  - count(*) filter (where p.difficulty = 'trung-binh'), 0) as tb_thieu,
       greatest(rt.min_kho - count(*) filter (where p.difficulty = 'kho'), 0)        as kho_thieu
from public.rank_titles rt
left join per_q p on p.code = rt.code
where rt.kind = 'specialist' and rt.enabled
group by rt.code, rt.name, rt.min_de, rt.min_tb, rt.min_kho, rt.sort
order by (greatest(rt.min_de - count(*) filter (where p.difficulty = 'de'), 0)
        + greatest(rt.min_tb - count(*) filter (where p.difficulty = 'trung-binh'), 0)
        + greatest(rt.min_kho - count(*) filter (where p.difficulty = 'kho'), 0)) desc, rt.sort;
