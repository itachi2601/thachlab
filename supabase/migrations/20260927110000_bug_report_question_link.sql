-- Gắn báo lỗi vào đúng câu hỏi trong đề (không chỉ URL trang) — để trang
-- /quan-tri/sua-de nhảy thẳng vào đúng đề + tô đậm đúng câu bị báo lỗi, admin
-- không phải tự dò trong đề dài. Idempotent.
-- Cần docs/supabase-migration-bug-reports.sql + docs/supabase-migration-bug-reports-de-xuat.sql
-- đã chạy trước (bảng bug_reports + constraint category).

alter table public.bug_reports
  add column if not exists exam_id bigint references public.exams(id) on delete set null,
  add column if not exists question_index int;

create index if not exists bug_reports_exam_idx on public.bug_reports (exam_id) where exam_id is not null;

alter table public.bug_reports drop constraint if exists bug_reports_category_check;
alter table public.bug_reports add constraint bug_reports_category_check
  check (category in ('hien_thi', 'diem', 'dang_nhap', 'de_xuat', 'cau_hoi', 'khac'));
