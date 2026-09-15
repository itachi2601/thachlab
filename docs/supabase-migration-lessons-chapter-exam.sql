-- ============================================================
-- Migration: bài "Kiểm tra chương" ở cuối mỗi chương (chủ đề)
--
-- Bổ sung lesson_kind = 'kiem_tra_chuong' bên cạnh hai loại đã có
-- ('kiem_tra_giua_ki', 'kiem_tra_cuoi_ki'), rồi tạo sẵn MỘT bài
-- "Kiểm tra chương" ở cuối mỗi chương của lớp 10, 11, 12 kèm mục
-- "Kiểm tra" rỗng để chờ gắn đề qua /quan-tri/nhap-bai.
--
-- Chạy SAU supabase-migration-lessons-periodic-exam.sql
-- và supabase-migration-grade-classes.sql.
-- Idempotent: chạy lại không sinh bài trùng.
-- ============================================================

-- ---------- 1. Nới constraint lesson_kind ----------
alter table public.lessons
  drop constraint if exists lessons_lesson_kind_check;

alter table public.lessons
  add constraint lessons_lesson_kind_check check (lesson_kind in
    ('bai_hoc', 'kiem_tra_chuong', 'kiem_tra_giua_ki', 'kiem_tra_cuoi_ki'));

-- ---------- 2. Tạo bài "Kiểm tra chương" cho từng chương ----------
-- Phạm vi mặc định: chương của lớp 10, 11, 12, môn Vật lí.
--   • Thêm môn khác  → nối thêm code vào mảng v_subjects, vd
--     array['vat-ly', 'toan'].
--   • Thêm/bớt lớp   → sửa mảng v_class_slugs.
--   • Gồm cả chương "toàn trường" (không gán lớp nào) → đổi
--     v_include_unassigned := true.
do $$
declare
  v_class_slugs text[] := array['lop-10', 'lop-11', 'lop-12'];
  v_subjects text[] := array['vat-ly'];
  v_include_unassigned boolean := false;
  v_title text := 'Kiểm tra chương';
  v_created int := 0;
  v_items int := 0;
  ch record;
  v_lesson_id bigint;
begin
  for ch in
    select c.id, c.title
    from public.chapters c
    where c.subject_code = any (v_subjects)
      and (
        exists (
          select 1
          from public.chapter_classes cc
          join public.classes cl on cl.id = cc.class_id
          where cc.chapter_id = c.id
            and cl.slug = any (v_class_slugs)
        )
        or (
          v_include_unassigned
          and not exists (
            select 1 from public.chapter_classes cc where cc.chapter_id = c.id
          )
        )
      )
      -- chương nào đã có bài kiểm tra chương thì bỏ qua → chạy lại an toàn
      and not exists (
        select 1
        from public.lessons l
        where l.chapter_id = c.id
          and l.lesson_kind = 'kiem_tra_chuong'
      )
    order by c.sort_order, c.id
  loop
    insert into public.lessons (chapter_id, title, lesson_kind, sort_order, published)
    values (
      ch.id,
      v_title,
      'kiem_tra_chuong',
      coalesce(
        (select max(l.sort_order) from public.lessons l where l.chapter_id = ch.id),
        0
      ) + 1,
      true
    )
    returning id into v_lesson_id;

    v_created := v_created + 1;

    -- Mục "Kiểm tra" rỗng: trang nhập bài sẽ cập nhật đúng mục này
    -- (update-or-insert theo kind) nên không sinh mục trùng.
    insert into public.lesson_items (lesson_id, kind, title, sort_order)
    values (v_lesson_id, 'kiem_tra', 'Kiểm tra', 5);

    v_items := v_items + 1;
  end loop;

  raise notice 'Đã tạo % bài "Kiểm tra chương" và % mục Kiểm tra.', v_created, v_items;
end $$;

-- ---------- 3. Xem lại kết quả ----------
-- select cl.name as lop, c.title as chuong, l.title, l.sort_order
-- from public.lessons l
-- join public.chapters c on c.id = l.chapter_id
-- left join public.chapter_classes cc on cc.chapter_id = c.id
-- left join public.classes cl on cl.id = cc.class_id
-- where l.lesson_kind = 'kiem_tra_chuong'
-- order by cl.sort_order, c.sort_order;
