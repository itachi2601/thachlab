-- ============================================================================
-- RPC get_similar_bank_questions — "Câu tương tự" cho học sinh đã đăng nhập.
--
-- Học sinh KHÔNG đọc thẳng được public.question_bank (RLS: chỉ staff + policy bài tự kiểm tra
-- phụ đạo, xem 20260925140000_perf_rls.sql và 20260930160000_exit_quiz_bank_children.sql).
-- Hàm này SECURITY DEFINER, trả tối đa 10 câu/lần của MỘT chủ đề (kể cả chủ đề con một tầng,
-- question_topics.parent_id = p_topic_id — cùng cách policy exit-quiz xử lý), ưu tiên cùng Dạng
-- (form), rồi bù câu cùng chủ đề khác Dạng; ngẫu nhiên.
--
-- CẢNH BÁO — LỘ ĐÁP ÁN: cột `question` là nguyên jsonb ExamQuestion (features/exams/types.ts),
-- gồm cả `answer` / `statements[].answer`, vì bài luyện chấm phía client (như PracticeSession,
-- TopicPracticeModal). Chấp nhận được vì đây là bài luyện tự chấm, không tính điểm.
-- KHÔNG dùng hàm này để phát đề thi/kiểm tra tính điểm hay đề thăng hạng: học sinh gọi được
-- trực tiếp bằng supabase-js và đọc đáp án của bất kỳ chủ đề nào (tối đa 10 câu/lần, gọi lặp
-- được). Câu ngân hàng trùng câu trong đề kiểm tra đang mở là rủi ro đã biết.
--
-- Loại câu tự luận (qtype/type = 'essay') vì client không tự chấm được.
--
-- Cách chạy: bash scripts/run-migrations.sh   (hoặc supabase db query --linked -f <file này>)
-- Chạy lúc nào: bất kỳ lúc nào (chỉ tạo hàm + 1 index partial; index ~22k dòng, vài giây).
-- Rollback: khối ROLLBACK ở cuối file.
-- ============================================================================

-- Index: lọc theo chủ đề + Dạng trên câu đang dùng. Migration cũ chỉ có
-- idx_question_bank_grade_archived_browse (grade, archived, topic_id, ...) và
-- question_bank_topic_idx (topic_id, archived) trong docs/ — chưa có (topic_id, form) partial.
create index if not exists idx_question_bank_topic_form_active
  on public.question_bank (topic_id, form)
  where archived = false;

create or replace function public.get_similar_bank_questions(
  p_topic_id    bigint,
  p_form        text,
  p_exclude_ids bigint[] default '{}',
  p_limit       int default 5
)
returns table (
  id         bigint,
  topic_id   bigint,
  topic_name text,
  form       text,
  qtype      text,
  difficulty text,
  question   jsonb,
  same_form  boolean
)
language plpgsql
stable
security definer
set search_path = public
as $$
declare
  v_limit int  := least(greatest(coalesce(p_limit, 5), 1), 10);
  v_form  text := nullif(lower(btrim(coalesce(p_form, ''))), '');
begin
  if auth.uid() is null then
    raise exception 'not authenticated' using errcode = '42501';
  end if;

  if p_topic_id is null then
    return;
  end if;

  return query
  select
    q.id,
    q.topic_id,
    q.topic_name,
    q.form,
    q.qtype,
    q.difficulty,
    q.question,
    (v_form is not null and lower(btrim(coalesce(q.form, ''))) = v_form) as same_form
  from public.question_bank q
  where q.archived = false
    and (
      q.topic_id = p_topic_id
      or q.topic_id in (select t.id from public.question_topics t where t.parent_id = p_topic_id)
    )
    and not (q.id = any (coalesce(p_exclude_ids, '{}'::bigint[])))
    and coalesce(q.qtype, q.question->>'type', '') <> 'essay'
    and coalesce(q.question->>'type', '') <> 'essay'
    and q.question is not null
  order by
    (v_form is not null and lower(btrim(coalesce(q.form, ''))) = v_form) desc,
    random()
  limit v_limit;
end;
$$;

comment on function public.get_similar_bank_questions(bigint, text, bigint[], int) is
  'Câu tương tự cho bài luyện tự chấm (HS đã đăng nhập). TRẢ CẢ ĐÁP ÁN trong question jsonb — '
  'không dùng cho đề thi/kiểm tra tính điểm. Chủ đề + chủ đề con 1 tầng, ưu tiên cùng form, '
  'loại essay, ngẫu nhiên, limit kẹp 1..10.';

revoke all on function public.get_similar_bank_questions(bigint, text, bigint[], int) from public;
revoke all on function public.get_similar_bank_questions(bigint, text, bigint[], int) from anon;
grant execute on function public.get_similar_bank_questions(bigint, text, bigint[], int) to authenticated;

-- ============================================================================
-- KIỂM THỬ (chạy tay sau migration, mỗi khối trong transaction rồi rollback).
-- Thay <uuid_hs>, <uuid_tg>, <uuid_admin>, <topic> bằng giá trị thật.
--
-- -- Học sinh: nhận <= 5 câu, same_form=true xếp trước; đọc thẳng bảng vẫn bị RLS chặn (0 dòng
-- -- nếu em không có tutoring_needs ở chủ đề đó).
-- begin;
--   set local role authenticated;
--   set local request.jwt.claims = '{"sub":"<uuid_hs>","role":"authenticated"}';
--   select id, form, qtype, same_form from public.get_similar_bank_questions(<topic>, 'Dạng 1', '{}', 5);
--   select count(*) from public.question_bank where topic_id = <topic>;   -- kỳ vọng 0 (RLS)
-- rollback;
--
-- -- Trợ giảng (role='ta'/instructor không thpt): RPC vẫn chạy như HS; limit kẹp 10.
-- begin;
--   set local role authenticated;
--   set local request.jwt.claims = '{"sub":"<uuid_tg>","role":"authenticated"}';
--   select count(*) from public.get_similar_bank_questions(<topic>, null, '{}', 99);  -- kỳ vọng <= 10
-- rollback;
--
-- -- Admin: RPC chạy; loại id trong p_exclude_ids.
-- begin;
--   set local role authenticated;
--   set local request.jwt.claims = '{"sub":"<uuid_admin>","role":"authenticated"}';
--   select id from public.get_similar_bank_questions(<topic>, '', array[<id_bất_kỳ>]::bigint[], 10);
-- rollback;
--
-- -- Ẩn danh: phải lỗi permission denied for function.
-- begin;
--   set local role anon;
--   select * from public.get_similar_bank_questions(<topic>, null);
-- rollback;
-- ============================================================================

-- ============================================================================
-- ROLLBACK (chạy tay nếu cần):
-- drop function if exists public.get_similar_bank_questions(bigint, text, bigint[], int);
-- drop index if exists public.idx_question_bank_topic_form_active;
-- ============================================================================
