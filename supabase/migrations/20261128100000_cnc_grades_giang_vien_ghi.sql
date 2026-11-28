-- Bảng điểm học phần CNC (cnc_grades): cho giảng viên (is_admin) GHI từ màn chấm trên web
-- (nút "Gửi điểm cho SV" ở Bảng điều khiển → Năng lực → Chấm thi thực hành tổng hợp).
-- Trước đây chỉ ghi được bằng service role qua script nạp CSV. SV vẫn chỉ đọc dòng của mình.
-- Chỉ thêm quyền + policy, không đụng dữ liệu. Rollback ở cuối file.
begin;

grant insert, update on public.cnc_grades to authenticated;

drop policy if exists "admin inserts cnc grades" on public.cnc_grades;
create policy "admin inserts cnc grades" on public.cnc_grades
  for insert to authenticated
  with check ((select public.is_admin()));

drop policy if exists "admin updates cnc grades" on public.cnc_grades;
create policy "admin updates cnc grades" on public.cnc_grades
  for update to authenticated
  using ((select public.is_admin()))
  with check ((select public.is_admin()));

commit;

-- ROLLBACK:
-- begin;
-- drop policy if exists "admin inserts cnc grades" on public.cnc_grades;
-- drop policy if exists "admin updates cnc grades" on public.cnc_grades;
-- revoke insert, update on public.cnc_grades from authenticated;
-- commit;
