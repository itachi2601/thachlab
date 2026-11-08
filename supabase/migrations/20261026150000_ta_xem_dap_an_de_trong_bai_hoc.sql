-- ============================================================================
-- Trợ giảng xem đáp án đề gắn trong bài học của lớp mình (sửa lỗi 26/10/2026)
-- ============================================================================
-- Lỗi: trợ giảng bấm "Xem đề và đáp án" ở trang bài nhận "Em chưa có quyền xem đáp án của đề này"
-- với đề chỉ gắn qua lesson_items.exam_ids mà không có dòng exam_classes (vd. 26 đề quiz lý thuyết 1076–1101,
-- đề Kiểm tra nhanh mồ côi). exam_staff_can_read chỉ xét exam_classes / xem trước / BTVN / HS lớp đã nộp.
--
-- Sửa: thêm nhánh cho tro_giang — đề published nằm trong exam_ids của một mục bài học (lesson_items) thuộc bài
-- (lessons) của chương (chapter_classes) mà trợ giảng đang hỗ trợ lớp đó (assists_class). Giữ nguyên mọi nhánh cũ.
-- Quyền xem đáp án chỉ MỞ THÊM cho TA đúng lớp; HS không đổi. Chỉ create or replace 1 hàm → chạy giờ nào cũng được.
-- Kiểm sau khi chạy: đăng nhập TA lớp có quiz lý thuyết → /lop-hoc/bai → "Xem đề và đáp án" thấy đáp án.
--   (SQL) select public.exam_staff_can_read(1076);  -- với auth.uid() của TA lớp đó → true
-- Rollback: khối cuối file.
-- ============================================================================

begin;

create or replace function public.exam_staff_can_read(p_exam_id bigint)
returns boolean
language sql stable security definer set search_path = public
as $$
  select case (select p.role from public.profiles p where p.id = (select auth.uid()))
    when 'admin' then exists (select 1 from public.exams e where e.id = p_exam_id)
    when 'instructor' then exists (select 1 from public.exams e where e.id = p_exam_id and e.published)
    when 'tro_giang' then
         exists (select 1 from public.exam_ta_previews t where t.exam_id = p_exam_id and public.assists_class(t.class_id))
      or exists (select 1 from public.exams e join public.exam_classes ec on ec.exam_id = e.id
                 where e.id = p_exam_id and e.published and public.assists_class(ec.class_id))
      or exists (select 1 from public.ta_homework_assignments h where h.exam_id = p_exam_id and public.assists_class(h.class_id))
      -- đề gắn trong mục bài học của chương thuộc lớp mình trợ giảng (không cần dòng exam_classes)
      or exists (select 1 from public.exams e
                 join public.lesson_items li on p_exam_id = any (li.exam_ids)
                 join public.lessons l on l.id = li.lesson_id
                 join public.chapter_classes cc on cc.chapter_id = l.chapter_id
                 where e.id = p_exam_id and e.published and public.assists_class(cc.class_id))
      -- đề toàn trường (không gán lớp): chỉ khi đã có HS lớp mình nộp → để chữa bài
      or exists (select 1 from public.exam_results er
                 join public.user_classes uc on uc.user_id = er.student_id and uc.status = 'active'
                 where er.exam_id = p_exam_id and public.assists_class(uc.class_id))
    else false
  end
$$;

commit;

-- ============================================================================
-- ROLLBACK (bỏ "-- " đầu dòng rồi chạy): chép lại bản cũ không có nhánh lesson_items
-- ============================================================================
-- begin;
-- create or replace function public.exam_staff_can_read(p_exam_id bigint)
-- returns boolean language sql stable security definer set search_path = public as $$
--   select case (select p.role from public.profiles p where p.id = (select auth.uid()))
--     when 'admin' then exists (select 1 from public.exams e where e.id = p_exam_id)
--     when 'instructor' then exists (select 1 from public.exams e where e.id = p_exam_id and e.published)
--     when 'tro_giang' then
--          exists (select 1 from public.exam_ta_previews t where t.exam_id = p_exam_id and public.assists_class(t.class_id))
--       or exists (select 1 from public.exams e join public.exam_classes ec on ec.exam_id = e.id
--                  where e.id = p_exam_id and e.published and public.assists_class(ec.class_id))
--       or exists (select 1 from public.ta_homework_assignments h where h.exam_id = p_exam_id and public.assists_class(h.class_id))
--       or exists (select 1 from public.exam_results er
--                  join public.user_classes uc on uc.user_id = er.student_id and uc.status = 'active'
--                  where er.exam_id = p_exam_id and public.assists_class(uc.class_id))
--     else false
--   end
-- $$;
-- commit;
