-- ============================================================
-- Seed: Lớp KHTN 9 (phần Vật lý) — 5 chương, 17 bài
-- Chạy trong Supabase Dashboard → SQL Editor (idempotent, chạy lại được)
-- ============================================================

insert into public.classes (name, slug, color, icon, sort_order)
select 'KHTN 9', 'khtn-9', '#10B981', '🔬', 0
where not exists (select 1 from public.classes where name = 'KHTN 9');

do $$
declare
  v_class_id bigint;
  v_chapter_id bigint;
  v_exists boolean;
begin
  select id into v_class_id from public.classes where name = 'KHTN 9';

  select exists (
    select 1 from public.chapters ch
    join public.chapter_classes cc on cc.chapter_id = ch.id
    where cc.class_id = v_class_id and ch.title = 'Chương 1: Năng lượng cơ học'
  ) into v_exists;

  if v_exists then
    raise notice 'Dữ liệu KHTN 9 đã tồn tại — bỏ qua.';
    return;
  end if;

  insert into public.chapters (title, sort_order) values ('Chương 1: Năng lượng cơ học', 1)
    returning id into v_chapter_id;
  insert into public.chapter_classes (chapter_id, class_id) values (v_chapter_id, v_class_id);
  insert into public.lessons (chapter_id, title, sort_order) values
    (v_chapter_id, 'Bài 2. Động năng. Thế năng', 1),
    (v_chapter_id, 'Bài 3. Cơ năng', 2),
    (v_chapter_id, 'Bài 4. Công và công suất', 3);

  insert into public.chapters (title, sort_order) values ('Chương 2: Ánh sáng', 2)
    returning id into v_chapter_id;
  insert into public.chapter_classes (chapter_id, class_id) values (v_chapter_id, v_class_id);
  insert into public.lessons (chapter_id, title, sort_order) values
    (v_chapter_id, 'Bài 5. Khúc xạ ánh sáng', 1),
    (v_chapter_id, 'Bài 6. Phản xạ toàn phần', 2),
    (v_chapter_id, 'Bài 7. Lăng kính', 3),
    (v_chapter_id, 'Bài 8. Thấu kính', 4),
    (v_chapter_id, 'Bài 9. Thực hành đo tiêu cự của thấu kính hội tụ', 5),
    (v_chapter_id, 'Bài 10. Kính lúp. Bài tập thấu kính', 6);

  insert into public.chapters (title, sort_order) values ('Chương 3: Điện', 3)
    returning id into v_chapter_id;
  insert into public.chapter_classes (chapter_id, class_id) values (v_chapter_id, v_class_id);
  insert into public.lessons (chapter_id, title, sort_order) values
    (v_chapter_id, 'Bài 11. Điện trở. Định luật Ohm', 1),
    (v_chapter_id, 'Bài 12. Đoạn mạch nối tiếp, song song', 2),
    (v_chapter_id, 'Bài 13. Năng lượng của dòng điện và công suất điện', 3);

  insert into public.chapters (title, sort_order) values ('Chương 4: Điện từ', 4)
    returning id into v_chapter_id;
  insert into public.chapter_classes (chapter_id, class_id) values (v_chapter_id, v_class_id);
  insert into public.lessons (chapter_id, title, sort_order) values
    (v_chapter_id, 'Bài 14. Cảm ứng điện từ. Nguyên tắc tạo ra dòng điện xoay chiều', 1),
    (v_chapter_id, 'Bài 15. Tác dụng của dòng điện xoay chiều', 2);

  insert into public.chapters (title, sort_order) values ('Chương 5: Năng lượng với cuộc sống', 5)
    returning id into v_chapter_id;
  insert into public.chapter_classes (chapter_id, class_id) values (v_chapter_id, v_class_id);
  insert into public.lessons (chapter_id, title, sort_order) values
    (v_chapter_id, 'Bài 16. Vòng năng lượng trên Trái Đất. Năng lượng hóa thạch', 1),
    (v_chapter_id, 'Bài 17. Một số dạng năng lượng tái tạo', 2);
end $$;
