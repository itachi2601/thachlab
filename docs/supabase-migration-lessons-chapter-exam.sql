-- ============================================================
-- Migration: thêm loại bài "kiểm tra chương" (kiem_tra_chuong)
-- Bài chỉ gồm đề, đặt cuối chương — cùng họ với kiểm tra giữa/cuối học kì.
-- Giá trị này đã có sẵn trong dữ liệu (sửa tay trên Supabase trước đó);
-- migration này chỉ chốt lại ràng buộc cho khớp với code.
-- Chạy SAU supabase-migration-lessons-periodic-exam.sql — idempotent.
-- ============================================================

alter table public.lessons
  drop constraint if exists lessons_lesson_kind_check;

alter table public.lessons
  add constraint lessons_lesson_kind_check check (lesson_kind in
    ('bai_hoc', 'kiem_tra_chuong', 'kiem_tra_giua_ki', 'kiem_tra_cuoi_ki'));
