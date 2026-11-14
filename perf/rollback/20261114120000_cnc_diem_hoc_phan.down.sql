-- Rollback 20261114120000_cnc_diem_hoc_phan.sql: xoá bảng điểm học phần CNC (mất dữ liệu điểm đã nạp — sao lưu trước nếu cần).
begin;
drop table if exists public.cnc_grades;
commit;
