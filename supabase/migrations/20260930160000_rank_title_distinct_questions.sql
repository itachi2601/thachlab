-- ============================================================================
-- GĐ 1 — Chống cày danh hiệu (30/9/2026)
--
-- Trước: rank_title_stats đếm de_correct/tb_correct/kho_correct theo LƯỢT giải đúng, nên làm lại
-- cùng một câu nhiều lần vẫn cộng dồn tới min_de/min_tb/min_kho.
-- Sau: đếm số CÂU KHÁC NHAU đã từng giải đúng. Khoá câu:
--   - có exam_id: (exam_id, vị trí câu trong đề) — question_index của đề = source_index của luyện tập
--   - luyện tập không có exam_id (đề nguồn đã xoá): (session_id, question_index) — không nhận diện được
--     câu lặp nên mỗi lượt vẫn là một câu.
-- n / correct / acc / covered giữ nguyên nghĩa "lượt" (dùng cho tỉ lệ đúng và cổng bậc).
-- RP mỗi bài đã là "lượt tốt nhất" sẵn: rank_award chỉ cộng phần chênh trên mỗi (kind:source_id).
-- Danh hiệu ĐÃ CÓ không bị thu hồi (rank_grant_title không thu hồi). Chạy giờ nào cũng được.
-- Chỉ đổi 1 hàm, cùng chữ ký. Rollback: perf/rollback/20260930160000_rank_title_distinct_questions.down.sql
-- ============================================================================

create or replace function public.rank_title_stats(p_student uuid, p_title text)
returns table(n int, correct int, covered int, total_topics int, acc int, de_correct int, tb_correct int, kho_correct int)
language sql stable set search_path = public
as $$
  with topics as (
    select tt.topic_id from public.rank_title_topics tt where tt.title_code = p_title
  ),
  rows_ as (
    select coalesce(t.parent_id, t.id) as lesson_topic, eqr.is_correct, eqr.difficulty,
           'e' || eqr.exam_id || ':' || eqr.question_index as qkey
    from public.exam_question_results eqr
    join public.question_topics t on t.id = eqr.topic_id
    where eqr.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
    union all
    select coalesce(t.parent_id, t.id), pqr.is_correct, pqr.difficulty,
           case when pqr.exam_id is not null then 'e' || pqr.exam_id || ':' || pqr.source_index
                else 'p' || pqr.session_id || ':' || pqr.question_index end
    from public.practice_question_results pqr
    join public.question_topics t on t.id = pqr.topic_id
    where pqr.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
  ),
  per_topic as (
    select lesson_topic, count(*) as c from rows_ group by lesson_topic
  )
  select
    (select count(*) from rows_)::int,
    (select count(*) filter (where is_correct) from rows_)::int,
    (select count(*) from per_topic where c >= 3)::int,
    (select count(*) from topics)::int,
    case when (select count(*) from rows_) > 0
      then round((select count(*) filter (where is_correct) from rows_) * 100.0 / (select count(*) from rows_))::int
      else 0 end,
    (select count(distinct qkey) filter (where is_correct and difficulty = 'de') from rows_)::int,
    (select count(distinct qkey) filter (where is_correct and difficulty = 'trung-binh') from rows_)::int,
    (select count(distinct qkey) filter (where is_correct and difficulty = 'kho') from rows_)::int;
$$;
