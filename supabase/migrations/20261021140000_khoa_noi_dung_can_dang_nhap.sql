-- 21/10/2026: nội dung bài học chỉ mở cho tài khoản đăng nhập (miễn phí), trừ vài bài xem thử.
-- lessons/chapters/classes giữ công khai (tên bài, menu); lesson_items (lý thuyết, đề, lời giải) khoá khách.
alter table public.lessons add column if not exists is_preview boolean not null default false;
update public.lessons set is_preview = true where id in (2, 20, 46); -- 12: Sự chuyển thể, 11: Dao động điều hoà, 10: Làm quen với Vật lí

drop policy if exists "anyone reads lesson items" on public.lesson_items;
create policy "members or preview read lesson items" on public.lesson_items
  for select to anon, authenticated
  using (
    auth.uid() is not null
    or exists (select 1 from public.lessons l where l.id = lesson_items.lesson_id and l.is_preview)
  );

-- ROLLBACK:
--   drop policy "members or preview read lesson items" on public.lesson_items;
--   create policy "anyone reads lesson items" on public.lesson_items for select to public using (true);
--   alter table public.lessons drop column is_preview;
