-- Rollback cho 20260927110000_bug_report_question_link.sql.
-- Đổi các dòng đang gắn 'cau_hoi' về 'khac' TRƯỚC khi khôi phục constraint cũ
-- (constraint cũ không cho phép 'cau_hoi'), rồi mới xoá cột.

update public.bug_reports set category = 'khac' where category = 'cau_hoi';

alter table public.bug_reports drop constraint if exists bug_reports_category_check;
alter table public.bug_reports add constraint bug_reports_category_check
  check (category in ('hien_thi', 'diem', 'dang_nhap', 'de_xuat', 'khac'));

drop index if exists bug_reports_exam_idx;
alter table public.bug_reports drop column if exists exam_id;
alter table public.bug_reports drop column if exists question_index;
