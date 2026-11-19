-- Mục Sức khỏe › Dinh dưỡng (/suc-khoe/dinh-duong): nhật ký ăn theo ngày + hồ sơ tính năng lượng.
-- Mỗi người chỉ đọc/ghi dòng của mình. Bảng mới, không đụng dữ liệu cũ. Idempotent.

create table if not exists public.nutrition_days (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  day date not null,
  items jsonb not null default '[]'::jsonb,   -- [{id, name, unit, qty, kcal, p, c, f}] (kcal/p/c/f cho 1 phần)
  weight_kg numeric(5,1),                     -- cân buổi sáng (tuỳ chọn) để xem xu hướng tuần
  note text,
  updated_at timestamptz not null default now(),
  unique (user_id, day)
);

create table if not exists public.nutrition_profile (
  user_id uuid primary key default auth.uid() references public.profiles (id) on delete cascade,
  birth_year int check (birth_year between 1900 and 2100),
  sex text check (sex in ('nam', 'nu')),
  activity numeric(4,3) check (activity between 1.1 and 2.2),
  goal text check (goal in ('tang', 'giu', 'giam')) default 'tang',
  kcal_adjust int not null default 0 check (kcal_adjust between -1500 and 1500),
  updated_at timestamptz not null default now()
);

alter table public.nutrition_days enable row level security;
alter table public.nutrition_profile enable row level security;
revoke all on public.nutrition_days from anon, authenticated;
revoke all on public.nutrition_profile from anon, authenticated;
grant select, insert, update, delete on public.nutrition_days to authenticated;
grant select, insert, update, delete on public.nutrition_profile to authenticated;

drop policy if exists nutrition_days_own on public.nutrition_days;
create policy nutrition_days_own on public.nutrition_days
  for all to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));

drop policy if exists nutrition_profile_own on public.nutrition_profile;
create policy nutrition_profile_own on public.nutrition_profile
  for all to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));

-- ROLLBACK: perf/rollback/20261119090000_dinh_duong.down.sql
