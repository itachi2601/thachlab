-- ============================================================
-- Migration: gộp cấu trúc bài học từ 6 mục còn 5 mục
-- Lý thuyết trọng tâm → Video bài giảng → Các dạng bài tập → Luyện tập → Kiểm tra
-- Gộp "luyen_tap_sach" + "luyen_tap_de" thành 1 mục "luyen_tap" (đề trắc nghiệm).
-- Chạy SAU supabase-migration-lessons.sql, idempotent, chạy lại được.
-- ============================================================

-- 1. Bỏ ràng buộc kind CŨ trước — nếu không, bước UPDATE bên dưới sẽ vi phạm
--    ràng buộc cũ (chưa có 'luyen_tap' trong danh sách cho phép).
alter table public.lesson_items
  drop constraint if exists lesson_items_kind_check;

-- 2. Đổi các mục cũ sang 'luyen_tap'.
update public.lesson_items
  set kind = 'luyen_tap'
  where kind in ('luyen_tap_sach', 'luyen_tap_de');

-- 3. Thêm lại ràng buộc với danh sách 5 mục mới.
alter table public.lesson_items
  add constraint lesson_items_kind_check check (kind in
    ('ly_thuyet', 'video', 'bai_tap_mau', 'luyen_tap', 'kiem_tra'));
