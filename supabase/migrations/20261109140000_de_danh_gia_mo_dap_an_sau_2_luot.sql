-- ============================================================================
-- Đề đánh giá: mở đáp án + lời giải sau 2 lượt nộp (trước: 3) và cho em xem "vì sao phương án em chọn sai" ngay sau mỗi lượt.
-- Thầy chốt 9/11/2026 sau báo lỗi lớp 11 (đề 1297: 29/51 lượt nộp bị khoá, em chưa đạt chỉ biết sai mà không biết vì sao).
--  1. exam_answers_revealed: ngưỡng lượt 3 -> 2 (giữ nhánh quiz lý thuyết 27/10, nhánh đạt pass_score, đề không phải đánh giá).
--  2. get_exam_wrong_notes(p_result_id): trả distractorNotes CHỈ của phương án em đã chọn sai (câu trắc nghiệm A–D),
--     không trả đáp án đúng/lời giải. Em đã biết phương án đó sai (câu bị tính sai), nên không lộ thêm. Đúng–sai không trả
--     (ghi chú theo ý sẽ lộ đáp án từng ý).
-- Chạy: lúc nào cũng được (chỉ thay hàm + thêm hàm). Rollback: perf/rollback/20261109140000_de_danh_gia_mo_dap_an_sau_2_luot.down.sql
-- ============================================================================
create or replace function public.exam_answers_revealed(p_exam_id bigint, p_uid uuid)
returns boolean
language sql stable security definer set search_path = public
as $$
  select not public.exam_is_assessment(p_exam_id)
      or exists (select 1 from public.lesson_items li
                 where li.kind = 'ly_thuyet' and p_exam_id = any (li.exam_ids))
      or (select count(*) from public.exam_results er where er.exam_id = p_exam_id and er.student_id = p_uid) >= 2
      or exists (select 1 from public.exam_results er join public.exams e on e.id = er.exam_id
                 where er.exam_id = p_exam_id and er.student_id = p_uid
                   and e.pass_score is not null and er.score >= e.pass_score)
$$;

create or replace function public.get_exam_wrong_notes(p_result_id bigint)
returns jsonb
language sql stable security definer set search_path = public
as $$
  select coalesce(jsonb_agg(jsonb_build_object(
           'question_index', x.i - 1,
           'label', chr(65 + r.pick),
           'note', trim(x.v -> 'distractorNotes' ->> chr(65 + r.pick))) order by x.i), '[]'::jsonb)
  from public.exam_results er
  join public.exams e on e.id = er.exam_id
  cross join lateral jsonb_array_elements(case when jsonb_typeof(e.questions) = 'array' then e.questions else '[]'::jsonb end)
    with ordinality as x (v, i)
  cross join lateral (
    select case when jsonb_typeof(er.detail -> 'responses' -> (x.i - 1)::int) = 'number'
                then (er.detail -> 'responses' ->> (x.i - 1)::int)::int end as pick) r
  where er.id = p_result_id
    and er.student_id = (select auth.uid())
    and x.v ->> 'type' = 'multiple_choice'
    and r.pick between 0 and 3
    and r.pick <> (x.v ->> 'answer')::int
    and nullif(trim(x.v -> 'distractorNotes' ->> chr(65 + r.pick)), '') is not null
$$;
revoke all on function public.get_exam_wrong_notes(bigint) from public, anon;
grant execute on function public.get_exam_wrong_notes(bigint) to authenticated;
