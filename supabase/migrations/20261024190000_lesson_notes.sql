-- Ghi chú riêng của học sinh theo từng mục (heading) trong bài học (24/10/2026).
-- Một dòng = một em + một bài + một mục. Ghi chú RIÊNG TƯ: chỉ chủ sở hữu đọc/ghi;
-- giáo viên, trợ giảng, phụ huynh đều KHÔNG đọc được (không có policy staff).
-- lesson_id là bigint vì lessons.id là int8 (docs/DATABASE.md). Chỉ thêm bảng mới, idempotent.
--
-- Ai đọc / ghi được gì:
-- | Vai                         | select            | insert/update/delete       |
-- |-----------------------------|-------------------|----------------------------|
-- | anon                        | không             | không                      |
-- | học sinh (authenticated)    | chỉ dòng của mình | chỉ dòng user_id = mình    |
-- | trợ giảng / giáo viên       | chỉ dòng của mình | chỉ dòng user_id = mình    |
-- | admin (qua API, authenticated) | chỉ dòng của mình | chỉ dòng user_id = mình |
-- | service_role / postgres     | toàn bộ (bỏ qua RLS) — chỉ dùng tay khi cần hỗ trợ   |

create table if not exists public.lesson_notes (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  lesson_id bigint not null references public.lessons(id) on delete cascade,
  heading_id text not null check (char_length(heading_id) between 1 and 80),
  heading_text text not null default '' check (char_length(heading_text) <= 300),
  body text not null default '' check (char_length(body) <= 4000),
  updated_at timestamptz not null default now(),
  primary key (user_id, lesson_id, heading_id)
);
-- Khoá chính (user_id, lesson_id, heading_id) đủ cho truy vấn "ghi chú của em trong bài X".

alter table public.lesson_notes enable row level security;
revoke all on public.lesson_notes from anon, authenticated;
grant select, insert, update, delete on public.lesson_notes to authenticated;

drop policy if exists "lesson_notes_select_own" on public.lesson_notes;
create policy "lesson_notes_select_own" on public.lesson_notes
  for select to authenticated
  using (user_id = (select auth.uid()));

drop policy if exists "lesson_notes_insert_own" on public.lesson_notes;
create policy "lesson_notes_insert_own" on public.lesson_notes
  for insert to authenticated
  with check (user_id = (select auth.uid()));

drop policy if exists "lesson_notes_update_own" on public.lesson_notes;
create policy "lesson_notes_update_own" on public.lesson_notes
  for update to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));

drop policy if exists "lesson_notes_delete_own" on public.lesson_notes;
create policy "lesson_notes_delete_own" on public.lesson_notes
  for delete to authenticated
  using (user_id = (select auth.uid()));

-- Kiểm thử sau khi chạy (SQL editor, trong giao dịch rồi rollback; thay <uuid_*> và <lesson>):
-- begin;
--   set local role authenticated;
--   -- Học sinh A ghi và đọc được ghi chú của mình:
--   select set_config('request.jwt.claims', '{"sub":"<uuid_hs_a>","role":"authenticated"}', true);
--   insert into public.lesson_notes (lesson_id, heading_id, heading_text, body)
--     values (<lesson>, 'muc-1', 'Mục 1', 'thử');                         -- kỳ vọng: 1 dòng
--   select count(*) from public.lesson_notes;                             -- kỳ vọng: 1
--   insert into public.lesson_notes (user_id, lesson_id, heading_id, body)
--     values ('<uuid_hs_b>', <lesson>, 'muc-1', 'giả mạo');               -- kỳ vọng: lỗi RLS
--   -- Trợ giảng không thấy ghi chú của HS A:
--   select set_config('request.jwt.claims', '{"sub":"<uuid_tro_giang>","role":"authenticated"}', true);
--   select count(*) from public.lesson_notes where user_id = '<uuid_hs_a>';  -- kỳ vọng: 0
--   update public.lesson_notes set body = 'x' where user_id = '<uuid_hs_a>'; -- kỳ vọng: UPDATE 0
--   -- Admin (thầy) cũng không thấy:
--   select set_config('request.jwt.claims', '{"sub":"<uuid_admin>","role":"authenticated"}', true);
--   select count(*) from public.lesson_notes where user_id = '<uuid_hs_a>';  -- kỳ vọng: 0
--   delete from public.lesson_notes where user_id = '<uuid_hs_a>';           -- kỳ vọng: DELETE 0
--   -- anon không có quyền:
--   reset role; set local role anon;
--   select count(*) from public.lesson_notes;                             -- kỳ vọng: permission denied
-- rollback;

-- ROLLBACK (bảng mới, mất ghi chú HS đã viết nếu đã dùng):
-- drop table if exists public.lesson_notes;
