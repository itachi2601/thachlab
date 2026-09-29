-- ============================================================
-- Fix: find_similar_bank_questions() bị statement_timeout
-- ============================================================
-- Bối cảnh: hàm cũ (docs/supabase-migration-question-bank-similarity.sql)
-- ghép CTE `t` với chính nó (self-join) rồi mới lọc similarity() >= threshold.
-- Với một topic có N câu, đó là N*(N-1)/2 lần tính similarity() — index GIN
-- trigram sẵn có (question_bank_plain_text_trgm_idx) không giúp được gì cho
-- kiểu self-join đối xứng này, nên khi một topic tích luỹ nhiều câu là vượt
-- statement_timeout và toàn bộ lần quét trả về lỗi thay vì danh sách trùng.
--
-- Cách sửa: bỏ self-join toàn bộ, chuyển sang nested loop có index — với mỗi
-- câu a, dùng toán tử `%` (pg_trgm) tra thẳng trên biểu thức đã lập chỉ mục
-- của b để Postgres dùng index scan thay vì quét hết topic. set_limit() đặt
-- ngưỡng % trùng threshold truyền vào để index tự lọc bớt trước khi tính
-- similarity() chính xác. Thêm LATERAL LIMIT 20 mỗi câu để chặn trần trường
-- hợp xấu nhất (một cụm rất nhiều câu gần giống nhau vẫn không nổ ra N^2).
--
-- Chạy: supabase db query --linked -f supabase/migrations/20260926150000_fix_question_bank_similarity_timeout.sql
-- Rollback: supabase db query --linked -f perf/rollback/20260926150000_fix_question_bank_similarity_timeout.down.sql

create or replace function public.find_similar_bank_questions(p_grade text, p_threshold real default 0.5)
returns table (
  topic_id bigint,
  topic_name text,
  id1 bigint,
  id2 bigint,
  similarity real
)
language plpgsql
stable
set jit = off
as $$
begin
  perform set_limit(p_threshold);

  return query
  select a.topic_id, a.topic_name, a.id, m.id, m.sim
  from public.question_bank a
  cross join lateral (
    select b.id,
           similarity(
             public.question_bank_plain_text(a.question),
             public.question_bank_plain_text(b.question)
           ) as sim
    from public.question_bank b
    where b.topic_id = a.topic_id
      and b.grade = p_grade
      and b.archived = false
      and b.id > a.id
      and public.question_bank_plain_text(b.question) % public.question_bank_plain_text(a.question)
    order by sim desc
    limit 20
  ) m
  where a.grade = p_grade
    and a.archived = false
    and a.topic_id is not null
  order by m.sim desc
  limit 300;
end;
$$;

grant execute on function public.find_similar_bank_questions(text, real) to authenticated;
