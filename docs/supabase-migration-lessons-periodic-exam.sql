-- ============================================================
-- Migration: bài kiểm tra định kỳ (giữa học kì / cuối học kì)
-- Mỗi bài học trong một chương có thể là bài học thường ('bai_hoc')
-- hoặc một bài kiểm tra định kỳ đặt ở cuối chương tương ứng chương trình:
--   'kiem_tra_giua_ki'  — kiểm tra giữa học kì
--   'kiem_tra_cuoi_ki'  — kiểm tra cuối học kì
-- Bài kiểm tra định kỳ chỉ dùng mục "Kiểm tra" (exam_ids), chấm điểm tự động.
-- Chạy SAU supabase-migration-lessons.sql — idempotent, chạy lại được.
-- ============================================================

alter table public.lessons
  add column if not exists lesson_kind text not null default 'bai_hoc';

alter table public.lessons
  drop constraint if exists lessons_lesson_kind_check;

alter table public.lessons
  add constraint lessons_lesson_kind_check check (lesson_kind in
    ('bai_hoc', 'kiem_tra_giua_ki', 'kiem_tra_cuoi_ki'));
