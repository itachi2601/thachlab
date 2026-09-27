-- Ngân hàng câu hỏi: tìm các cặp câu "giống nhau" (không trùng tuyệt đối — content_hash đã lo
-- việc đó, xem supabase-migration-question-bank.sql) trong CÙNG MỘT chủ đề (topic_id), dùng độ
-- giống trigram (pg_trgm) trên nội dung câu đã bỏ thẻ HTML. Chỉ để CẢNH BÁO cho thầy tự xem lại
-- ở trang /quan-tri/ngan-hang-cau-hoi — không tự gộp hay xoá câu nào.

create extension if not exists pg_trgm;

create or replace function public.question_bank_plain_text(q jsonb)
returns text
language sql
immutable
as $$
  select trim(regexp_replace(regexp_replace(lower(coalesce(q->>'question', '')), '<[^>]+>', ' ', 'g'), '\s+', ' ', 'g'));
$$;

create index if not exists question_bank_plain_text_trgm_idx
  on public.question_bank using gin (public.question_bank_plain_text(question) gin_trgm_ops);

-- Trả về từng cặp câu active, cùng topic_id, cùng khối, có độ giống >= p_threshold (0..1).
-- v2 (26/9/2026, xem supabase/migrations/20260926150000_fix_question_bank_similarity_timeout.sql):
-- bản v1 ghép CTE `t` với chính nó (self-join N*(N-1)/2 mỗi topic) rồi mới lọc similarity() —
-- index GIN trigram không giúp được cho self-join đối xứng, nên topic nhiều câu vẫn bị
-- statement_timeout. Bản này dùng toán tử `%` tra thẳng lên biểu thức đã lập chỉ mục của b
-- (nested loop + index scan) và set_limit(p_threshold) để index tự lọc theo đúng ngưỡng, cộng
-- LATERAL LIMIT 20/câu để chặn trần trường hợp xấu nhất.
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

-- Không security definer: chạy với quyền người gọi nên RLS của question_bank (chỉ staff) vẫn áp dụng.
grant execute on function public.find_similar_bank_questions(text, real) to authenticated;
