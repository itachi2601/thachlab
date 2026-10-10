-- Trợ giảng đang hoạt động được ĐỌC danh sách thành viên lớp (user_classes) để mở trang
-- "Chữa bài" (/tro-giang/chua-bai): cần biết học sinh nào thuộc lớp thì mới gom được kết quả đề.
-- Chỉ thêm 1 policy SELECT; kết quả bài làm đã đọc được qua teaches_student() (20261002100000).
drop policy if exists "ta read class members" on public.user_classes;
create policy "ta read class members" on public.user_classes
  as permissive
  for select
  to authenticated
  using (assists_class(class_id));

-- ROLLBACK:
-- drop policy if exists "ta read class members" on public.user_classes;
