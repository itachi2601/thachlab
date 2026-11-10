-- 20261105220000_similar_practice_attempts.sql
-- Bảng ghi mỗi lượt "Làm bài tương tự" ở bài tập mẫu (components/lessons/SimilarBankPractice.tsx)
-- để đo hiệu quả khối "💡 Mẹo nhìn" (chặng 5): so tỉ lệ đúng lần đầu khi có/không mở mẹo.
--
-- Ai đọc / ghi được gì:
--   | Vai                        | SELECT        | INSERT                       | UPDATE/DELETE |
--   |----------------------------|---------------|------------------------------|---------------|
--   | anon                       | không         | không                        | không         |
--   | học sinh (authenticated)   | không         | chỉ dòng user_id = auth.uid()| không         |
--   | trợ giảng (tro_giang)      | không         | chỉ dòng của mình            | không         |
--   | giáo viên (instructor)     | mọi dòng      | chỉ dòng của mình            | không         |
--   | admin                      | mọi dòng      | chỉ dòng của mình            | không         |
-- Không dùng is_staff() vì hàm đó gồm cả tro_giang; số đo này chỉ cho thầy/admin.
--
-- Bảng mới, rỗng, không quét dữ liệu cũ → chạy giờ nào cũng được.
-- Chạy: bash scripts/run-migrations.sh (KHÔNG supabase db push).
-- Rollback: perf/rollback/20261105220000_similar_practice_attempts.down.sql

create table if not exists public.similar_practice_attempts (
  id            bigint generated always as identity primary key,
  user_id       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  lesson_id     bigint references public.lessons(id) on delete cascade,
  dang_no       int,
  topic_id      bigint references public.question_topics(id) on delete set null,
  form          text,
  nguon         text not null check (nguon in ('dang', 'chu_de')),
  luot          smallint not null default 1 check (luot >= 1),
  co_meo        boolean not null,
  mo_meo        boolean not null,
  dung_lan_dau  smallint not null,
  tong          smallint not null check (tong between 1 and 20),
  created_at    timestamptz not null default now(),
  constraint similar_practice_attempts_dung_chk check (dung_lan_dau >= 0 and dung_lan_dau <= tong)
);

comment on table public.similar_practice_attempts is
  'Mỗi lượt Làm bài tương tự ở bài tập mẫu; đo hiệu quả Mẹo nhìn. HS chỉ insert, instructor/admin đọc.';

create index if not exists similar_practice_attempts_lesson_dang_idx
  on public.similar_practice_attempts (lesson_id, dang_no, created_at);

alter table public.similar_practice_attempts enable row level security;

revoke all on table public.similar_practice_attempts from anon, authenticated;
grant insert, select on table public.similar_practice_attempts to authenticated;
-- identity "generated always" không cần grant usage sequence cho insert.

drop policy if exists "similar_practice_attempts insert own" on public.similar_practice_attempts;
create policy "similar_practice_attempts insert own" on public.similar_practice_attempts
  for insert to authenticated
  with check (user_id = (select auth.uid()));

drop policy if exists "similar_practice_attempts select teacher admin" on public.similar_practice_attempts;
create policy "similar_practice_attempts select teacher admin" on public.similar_practice_attempts
  for select to authenticated
  using (exists (
    select 1 from public.profiles p
    where p.id = (select auth.uid()) and p.role in ('admin', 'instructor')
  ));

-- Kiểm thử sau khi chạy (trong giao dịch, rollback cuối):
-- begin;
--   -- Học sinh: insert được dòng của mình, select ra 0 dòng, insert hộ người khác bị chặn.
--   set local role authenticated;
--   select set_config('request.jwt.claims', json_build_object('sub','<uuid_hs>','role','authenticated')::text, true);
--   insert into public.similar_practice_attempts (lesson_id, dang_no, nguon, co_meo, mo_meo, dung_lan_dau, tong)
--     values (null, 1, 'dang', true, false, 2, 3);                         -- OK
--   select count(*) from public.similar_practice_attempts;                 -- 0
--   insert into public.similar_practice_attempts (user_id, nguon, co_meo, mo_meo, dung_lan_dau, tong)
--     values ('<uuid_khac>', 'dang', true, false, 0, 1);                   -- lỗi RLS
--   update public.similar_practice_attempts set tong = 5;                  -- permission denied
--   -- Trợ giảng: như HS, select = 0.
--   select set_config('request.jwt.claims', json_build_object('sub','<uuid_tro_giang>','role','authenticated')::text, true);
--   select count(*) from public.similar_practice_attempts;                 -- 0
--   -- Admin/instructor: thấy mọi dòng.
--   select set_config('request.jwt.claims', json_build_object('sub','<uuid_admin>','role','authenticated')::text, true);
--   select count(*) from public.similar_practice_attempts;                 -- >= 1
-- rollback;
--
-- ROLLBACK: drop table if exists public.similar_practice_attempts;
--   (file: perf/rollback/20261105220000_similar_practice_attempts.down.sql)
