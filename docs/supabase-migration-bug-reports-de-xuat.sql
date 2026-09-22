-- Mở rộng bug_reports để nhận cả đề xuất tính năng, không chỉ báo lỗi.
-- Chạy sau docs/supabase-migration-bug-reports.sql. Idempotent.

alter table public.bug_reports drop constraint if exists bug_reports_category_check;
alter table public.bug_reports add constraint bug_reports_category_check
  check (category in ('hien_thi', 'diem', 'dang_nhap', 'de_xuat', 'khac'));
