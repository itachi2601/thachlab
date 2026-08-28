-- ============================================================
-- Migration: gộp cấu trúc bài học từ 6 mục còn 5 mục
-- Lý thuyết trọng tâm → Video bài giảng → Các dạng bài tập → Luyện tập → Kiểm tra
-- Gộp "luyen_tap_sach" + "luyen_tap_de" thành 1 mục "luyen_tap" (đề trắc nghiệm).
-- Chạy SAU supabase-migration-lessons.sql, idempotent, chạy lại được.
-- ============================================================

update public.lesson_items
  set kind = 'luyen_tap'
  where kind in ('luyen_tap_sach', 'luyen_tap_de');

alter table public.lesson_items
  drop constraint if exists lesson_items_kind_check;

alter table public.lesson_items
  add constraint lesson_items_kind_check check (kind in
    ('ly_thuyet', 'video', 'bai_tap_mau', 'luyen_tap', 'kiem_tra'));
