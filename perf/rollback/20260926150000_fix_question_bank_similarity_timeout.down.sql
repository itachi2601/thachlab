-- Rollback cho supabase/migrations/20260926150000_fix_question_bank_similarity_timeout.sql
--
-- Khôi phục find_similar_bank_questions() về bản self-join cũ (chậm/dễ
-- statement_timeout trên topic nhiều câu, nhưng đúng logic gốc).
--
-- Chạy: supabase db query --linked -f perf/rollback/20260926150000_fix_question_bank_similarity_timeout.down.sql

create or replace function public.find_similar_bank_questions(p_grade text, p_threshold real default 0.5)
returns table (
  topic_id bigint,
  topic_name text,
  id1 bigint,
  id2 bigint,
  similarity real
)
language sql
stable
set jit = off
as $$
  with t as (
    select id, topic_id, topic_name, public.question_bank_plain_text(question) as txt
    from public.question_bank
    where grade = p_grade and archived = false and topic_id is not null
  )
  select a.topic_id, a.topic_name, a.id, b.id, similarity(a.txt, b.txt)
  from t a
  join t b on a.topic_id = b.topic_id and a.id < b.id
  where similarity(a.txt, b.txt) >= p_threshold
  order by 5 desc
  limit 300;
$$;

grant execute on function public.find_similar_bank_questions(text, real) to authenticated;
