-- ============================================================================
-- Quiz "Kiểm tra nhanh" gắn vào mục ly_thuyet luôn mở đáp án sau khi nộp.
-- Sự cố 27/10/2026: đề 1147 (Bài 7, lớp 10) bị TA giao BTVN (ta_homework_assignments) → exam_is_assessment = true →
-- em phải đủ 3 lượt/đạt điểm mới thấy đáp án. Quiz lý thuyết là tự kiểm tra, không nên khoá.
-- Chỉ đổi exam_answers_revealed (hiện đáp án + câu vào kho luyện tập); KHÔNG đổi exam_is_assessment để phụ đạo vẫn tính điểm đề này.
-- Chạy: lúc nào cũng được (chỉ thay hàm). Rollback: perf/rollback/20261027200000_quiz_ly_thuyet_mo_dap_an.down.sql
-- ============================================================================
create or replace function public.exam_answers_revealed(p_exam_id bigint, p_uid uuid)
returns boolean
language sql stable security definer set search_path = public
as $$
  select not public.exam_is_assessment(p_exam_id)
      or exists (select 1 from public.lesson_items li
                 where li.kind = 'ly_thuyet' and p_exam_id = any (li.exam_ids))
      or (select count(*) from public.exam_results er where er.exam_id = p_exam_id and er.student_id = p_uid) >= 3
      or exists (select 1 from public.exam_results er join public.exams e on e.id = er.exam_id
                 where er.exam_id = p_exam_id and er.student_id = p_uid
                   and e.pass_score is not null and er.score >= e.pass_score)
$$;
