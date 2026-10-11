-- Trợ giảng đang hoạt động được ĐỌC kết quả làm đề (exam_results) của học sinh để dùng tab Phân tích
-- (/dashboard-thpt) và trang Chữa bài (/tro-giang/chua-bai). Trước đây exam_results chỉ cho đọc:
-- chính học sinh, admin (is_admin() = role 'admin'), và giảng viên có trong class_instructors —
-- trợ giảng không thuộc nhóm nào nên danh sách đề của lớp luôn rỗng và bảng chữa bài không có số liệu.
-- Ghi chú ở 20261010700000_ta_doc_thanh_vien_lop ("đã đọc được qua teaches_student()") đúng cho
-- exam_question_results / exam_attempts nhưng KHÔNG đúng cho exam_results.
-- Cùng mức quyền trợ giảng đã có trên exam_question_results (teaches_student). Chỉ thêm 1 policy SELECT.
drop policy if exists "ta read student results" on public.exam_results;
create policy "ta read student results" on public.exam_results
  as permissive
  for select
  to authenticated
  using (public.teaches_student(student_id));

-- ROLLBACK:
-- drop policy if exists "ta read student results" on public.exam_results;
