-- ============================================================
-- Migration: "Các dạng bài tập" và "Luyện tập" sang dạng lưới câu hỏi
-- + cho phép 1 mục gắn nhiều đề (thay vì chỉ 1 exam_id).
-- Chạy SAU supabase-migration-lessons.sql (và restructure.sql nếu đã có),
-- idempotent, chạy lại được.
-- ============================================================

alter table public.lesson_items
  add column if not exists exam_ids bigint[] not null default '{}';

alter table public.lesson_items
  add column if not exists questions jsonb not null default '[]'::jsonb;

-- Chuyển exam_id đơn lẻ (nếu cột còn tồn tại) sang mảng exam_ids.
do $$
begin
  if exists (
    select 1 from information_schema.columns
    where table_schema = 'public' and table_name = 'lesson_items' and column_name = 'exam_id'
  ) then
    update public.lesson_items
      set exam_ids = array[exam_id]
      where exam_id is not null and (exam_ids is null or exam_ids = '{}');
    alter table public.lesson_items drop column exam_id;
  end if;
end $$;

-- Bọc body_html cũ của "bai_tap_mau" thành 1 dạng bài trong questions, rồi xóa body_html.
update public.lesson_items
  set questions = jsonb_build_array(jsonb_build_object('label', 'Dạng 1', 'body_html', body_html)),
      body_html = ''
  where kind = 'bai_tap_mau' and trim(body_html) <> '' and questions = '[]'::jsonb;
