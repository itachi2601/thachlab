-- Ghi chú của giáo viên lúc đang dạy trên trang bài học (chế độ trình chiếu): một dòng gắn đúng
-- bài + mục (trang chiếu) đang xem, để cuối tuần cùng Claude xem lại và đề xuất cải tiến.
-- Chỉ người viết (giáo viên/trợ giảng) đọc và sửa được; học sinh không thấy gì. Idempotent.

create table if not exists public.teacher_lesson_notes (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  user_id uuid not null default auth.uid() references public.profiles(id) on delete cascade,
  lesson_id bigint not null references public.lessons(id) on delete cascade,
  -- Mục lý thuyết (lesson_items) và trang chiếu đang xem. page_heading lưu thẳng tiêu đề lúc ghi
  -- để ghi chú vẫn đọc được dù bài về sau bị sửa/đổi chỗ.
  item_id bigint references public.lesson_items(id) on delete set null,
  page_key text not null default '',
  page_heading text not null default '',
  tag text not null default 'y_tuong'
    check (tag in ('hs_hieu_sai', 'thieu_hinh', 'vi_du', 'dai_nhanh', 'loi', 'y_tuong')),
  body text not null check (length(btrim(body)) between 1 and 1000),
  status text not null default 'moi' check (status in ('moi', 'da_xem', 'da_xu_ly')),
  resolution text not null default ''
);

create index if not exists teacher_lesson_notes_lesson_idx on public.teacher_lesson_notes (lesson_id, created_at desc);
create index if not exists teacher_lesson_notes_open_idx on public.teacher_lesson_notes (created_at desc) where status <> 'da_xu_ly';

alter table public.teacher_lesson_notes enable row level security;
revoke all on public.teacher_lesson_notes from anon, authenticated;
grant select, insert, update, delete on public.teacher_lesson_notes to authenticated;

drop policy if exists "teacher_lesson_notes_own" on public.teacher_lesson_notes;
create policy "teacher_lesson_notes_own" on public.teacher_lesson_notes
  for all to authenticated
  using (user_id = (select auth.uid()) and public.is_staff())
  with check (user_id = (select auth.uid()) and public.is_staff());

-- Rollback:
--   drop table if exists public.teacher_lesson_notes;
