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
-- Chuẩn hoá văn bản một lần cho mỗi câu (CTE `t`) rồi mới ghép cặp trong chủ đề, thay vì gọi lại
-- question_bank_plain_text() nhiều lần cho từng cặp — bản đầu (gọi lặp trong cả SELECT lẫn WHERE)
-- từng bị statement_timeout trên bảng vài nghìn câu.
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

-- Không security definer: chạy với quyền người gọi nên RLS của question_bank (chỉ staff) vẫn áp dụng.
grant execute on function public.find_similar_bank_questions(text, real) to authenticated;
