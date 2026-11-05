-- ============================================================================
-- RPC get_similar_dang_questions — "Làm bài tương tự" ĐÚNG DẠNG cho học sinh đã đăng nhập.
--
-- Nguồn: public.question_dang (20261023120000_on_tap_dang_bai_tap.sql) — câu ngân hàng nào thuộc
-- dạng nào của bài nào (Claude/script gán theo mục Bài tập mẫu). Hàm trả tối đa 10 câu/lần của
-- ĐÚNG MỘT dạng (p_lesson_id + số dạng p_dang_no), ngẫu nhiên. KHÔNG bù câu khác dạng: hết câu
-- thì trả ít hơn / rỗng, client tự xử lý (khác get_similar_bank_questions vốn bù cùng chủ đề).
--
-- Số dạng tách từ dang_label bằng regex '^\s*Dạng\s*(\d+)' (nhãn có dạng
-- "Dạng 2 · Trung bình · <tên dạng>") — KHÔNG so cả nhãn, vì tên dạng sau dấu · có thể được sửa
-- trong Bài tập mẫu mà bảng gán chưa cập nhật.
--
-- Học sinh KHÔNG đọc thẳng được question_dang (revoke all from anon, authenticated) hay
-- question_bank (RLS chỉ staff + policy exit-quiz) — vì vậy hàm SECURITY DEFINER.
--
-- CẢNH BÁO — LỘ ĐÁP ÁN: cột `question` là nguyên jsonb ExamQuestion (features/exams/types.ts),
-- gồm cả `answer` / `statements[].answer`, vì bài luyện chấm phía client (như PracticeSession,
-- get_similar_bank_questions). Chấp nhận được vì đây là bài luyện tự chấm, không tính điểm.
-- KHÔNG dùng hàm này để phát đề thi/kiểm tra tính điểm, đề thăng hạng hay đề "Ôn dạng"
-- (review_build_dang_exam dựng đề từ CÙNG bảng question_dang): học sinh gọi được trực tiếp bằng
-- supabase-js và đọc đáp án của bất kỳ bài/dạng nào (tối đa 10 câu/lần, gọi lặp được). Câu ở đây
-- trùng câu của đề "Ôn dạng" đang mở là rủi ro đã biết.
--
-- Loại câu tự luận (qtype/type = 'essay') vì client không tự chấm được; loại câu archived,
-- câu question null, câu có lint_flags (giống review_build_dang_exam — câu đang bị cờ lỗi),
-- và câu gán unsure = true (cột NOT NULL DEFAULT false nên `not d.unsure` là đủ).
--
-- Cột trả giống get_similar_bank_questions để client dùng chung kiểu; same_form luôn = true.
--
-- Index: question_dang đã có PK (question_id, lesson_id) và question_dang_lesson_label_idx
-- (lesson_id, dang_label) — đủ cho lọc theo lesson_id, KHÔNG tạo index mới. PK đảm bảo mỗi câu
-- xuất hiện tối đa một lần trong một bài, nên không thể trùng câu trong kết quả.
--
-- Cách chạy: bash scripts/run-migrations.sh --yes --only <N>   (hoặc supabase db query --linked -f <file này>)
-- Chạy lúc nào: bất kỳ lúc nào (chỉ tạo 1 hàm, không đụng dữ liệu, không tạo index).
-- Rollback: khối ROLLBACK ở cuối file.
-- ============================================================================

create or replace function public.get_similar_dang_questions(
  p_lesson_id   bigint,
  p_dang_no     int,
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
  v_limit int := least(greatest(coalesce(p_limit, 5), 1), 10);
begin
  if auth.uid() is null then
    raise exception 'not authenticated' using errcode = '42501';
  end if;

  if p_lesson_id is null or p_dang_no is null then
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
    true as same_form
  from public.question_bank q
  where q.id in (
      select d.question_id
      from public.question_dang d
      where d.lesson_id = p_lesson_id
        and not d.unsure
        and substring(d.dang_label from '^\s*Dạng\s*(\d+)')::int = p_dang_no
    )
    and q.archived = false
    and q.question is not null
    and not (q.id = any (coalesce(p_exclude_ids, '{}'::bigint[])))
    and coalesce(q.qtype, q.question->>'type', '') <> 'essay'
    and coalesce(q.question->>'type', '') <> 'essay'
    and coalesce(array_length(q.lint_flags, 1), 0) = 0
  order by random()
  limit v_limit;
end;
$$;

comment on function public.get_similar_dang_questions(bigint, int, bigint[], int) is
  'Làm bài tương tự đúng dạng (HS đã đăng nhập): câu question_dang của bài p_lesson_id có số dạng '
  'p_dang_no (regex ^Dạng N trên dang_label), bỏ unsure/archived/essay/lint_flags, không bù khác dạng, '
  'ngẫu nhiên, limit kẹp 1..10. TRẢ CẢ ĐÁP ÁN trong question jsonb — không dùng cho đề thi/kiểm tra tính điểm.';

revoke all on function public.get_similar_dang_questions(bigint, int, bigint[], int) from public;
revoke all on function public.get_similar_dang_questions(bigint, int, bigint[], int) from anon;
grant execute on function public.get_similar_dang_questions(bigint, int, bigint[], int) to authenticated;

-- ============================================================================
-- AI ĐỌC / GHI ĐƯỢC GÌ (không đổi RLS/policy nào; chỉ thêm 1 hàm):
--   Vai                 | question_dang trực tiếp | question_bank trực tiếp      | RPC này
--   anon                | không                   | không                        | không (permission denied)
--   học sinh            | không                   | không (trừ policy exit-quiz) | đọc ≤10 câu/lần của 1 bài+dạng, KÈM đáp án; không ghi
--   trợ giảng           | không                   | theo RLS staff hiện có       | như học sinh
--   admin/thầy          | không (revoke)*         | đọc/ghi theo RLS staff       | như học sinh
--   * thầy ghi question_dang qua SQL Editor/script (postgres), không qua API.
-- Hàm stable, chỉ SELECT — không ghi bảng nào.
-- ============================================================================

-- ============================================================================
-- KIỂM THỬ (chạy tay sau migration, mỗi khối trong transaction rồi rollback).
-- Thay <uuid_hs>, <uuid_tg>, <uuid_admin>, <lesson>, <dang> bằng giá trị thật. Tìm cặp có câu:
--   select lesson_id, substring(dang_label from '^\s*Dạng\s*(\d+)')::int as dang_no, count(*)
--   from public.question_dang where not unsure group by 1, 2 order by 3 desc limit 5;
-- Nhãn KHÔNG khớp regex (kỳ vọng 0 dòng; có dòng thì các câu đó không bao giờ được trả):
--   select lesson_id, dang_label from public.question_dang
--   where substring(dang_label from '^\s*Dạng\s*(\d+)') is null;
--
-- -- Học sinh: nhận <= 5 câu, đúng dạng, same_form = true; đọc thẳng question_dang bị chặn.
-- begin;
--   set local role authenticated;
--   set local request.jwt.claims = '{"sub":"<uuid_hs>","role":"authenticated"}';
--   select id, form, qtype, same_form from public.get_similar_dang_questions(<lesson>, <dang>, '{}', 5);
--   select count(*) from public.question_dang;   -- kỳ vọng: permission denied for table question_dang
-- rollback;
--
-- -- Trợ giảng: RPC chạy như HS; limit kẹp 10; dạng không tồn tại → 0 dòng (không bù).
-- begin;
--   set local role authenticated;
--   set local request.jwt.claims = '{"sub":"<uuid_tg>","role":"authenticated"}';
--   select count(*) from public.get_similar_dang_questions(<lesson>, <dang>, '{}', 99);  -- kỳ vọng <= 10
--   select count(*) from public.get_similar_dang_questions(<lesson>, 99);               -- kỳ vọng 0
-- rollback;
--
-- -- Admin: loại id trong p_exclude_ids; tham số null → 0 dòng.
-- begin;
--   set local role authenticated;
--   set local request.jwt.claims = '{"sub":"<uuid_admin>","role":"authenticated"}';
--   select id from public.get_similar_dang_questions(<lesson>, <dang>, array[<id_bất_kỳ>]::bigint[], 10);
--   select count(*) from public.get_similar_dang_questions(null, <dang>);               -- kỳ vọng 0
-- rollback;
--
-- -- Ẩn danh: phải lỗi permission denied for function.
-- begin;
--   set local role anon;
--   select * from public.get_similar_dang_questions(<lesson>, <dang>);
-- rollback;
-- ============================================================================

-- ============================================================================
-- ROLLBACK (chạy tay nếu cần; migration không tạo index nên chỉ cần drop hàm):
-- drop function if exists public.get_similar_dang_questions(bigint, int, bigint[], int);
-- ============================================================================
