-- Ứng dụng tập luyện cá nhân /tai-khoan/tap-luyen (kiểu Hevy): nhật ký buổi tập + số đo cơ thể.
-- Mỗi người chỉ đọc/ghi dòng của mình. Bảng mới, không đụng dữ liệu cũ. Idempotent.

create table if not exists public.workout_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  client_id text not null,                    -- id sinh ở máy, để gửi lại khi mất mạng không bị trùng
  routine_key text,                           -- 'A' | 'B' | 'C' | null (buổi tự do)
  title text not null,
  started_at timestamptz not null,
  ended_at timestamptz not null,
  exercises jsonb not null default '[]'::jsonb, -- [{id, name, note, sets:[{kind:'w'|'n', kg, reps, sec, done}]}]
  note text,
  created_at timestamptz not null default now(),
  unique (user_id, client_id)
);
create index if not exists workout_logs_user_started_idx on public.workout_logs (user_id, started_at desc);

create table if not exists public.body_measurements (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  measured_on date not null,
  height_cm numeric(5,1),
  weight_kg numeric(5,1),
  chest_cm numeric(5,1),
  waist_cm numeric(5,1),
  hip_cm numeric(5,1),
  shoulder_cm numeric(5,1),
  arm_cm numeric(5,1),
  note text,
  created_at timestamptz not null default now(),
  unique (user_id, measured_on)
);

alter table public.workout_logs enable row level security;
alter table public.body_measurements enable row level security;
revoke all on public.workout_logs from anon, authenticated;
revoke all on public.body_measurements from anon, authenticated;
grant select, insert, update, delete on public.workout_logs to authenticated;
grant select, insert, update, delete on public.body_measurements to authenticated;

drop policy if exists workout_logs_own on public.workout_logs;
create policy workout_logs_own on public.workout_logs
  for all to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));

drop policy if exists body_measurements_own on public.body_measurements;
create policy body_measurements_own on public.body_measurements
  for all to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));

-- ROLLBACK: perf/rollback/20261118120000_tap_luyen.down.sql
