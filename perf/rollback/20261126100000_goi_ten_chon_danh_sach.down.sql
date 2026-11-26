-- Rollback 20261126100000_goi_ten_chon_danh_sach.sql — client quay về danh sách lớp theo chương khi hàm lỗi.
drop function if exists public.call_roster_lists();
drop function if exists public.course_call_roster(bigint);
