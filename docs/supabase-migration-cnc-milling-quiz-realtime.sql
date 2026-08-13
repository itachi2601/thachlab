-- Theo dõi realtime bài kiểm tra vận hành máy phay CNC.
-- Chạy sau docs/supabase-schema.sql.

create table if not exists public.cnc_milling_quiz_attempts (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.profiles (id) on delete cascade,
  answers jsonb not null default '{}'::jsonb,
  answered_count integer not null default 0 check (answered_count >= 0),
  score integer not null default 0 check (score >= 0),
  total_questions integer not null default 15 check (total_questions > 0),
  status text not null default 'in_progress'
    check (status in ('in_progress', 'passed', 'failed')),
  started_at timestamptz not null default now(),
  last_activity_at timestamptz not null default now(),
  submitted_at timestamptz,
  unique (student_id)
);

create index if not exists cnc_milling_quiz_attempts_activity_idx
  on public.cnc_milling_quiz_attempts (last_activity_at desc);

alter table public.cnc_milling_quiz_attempts enable row level security;

drop policy if exists "students read own milling quiz attempt" on public.cnc_milling_quiz_attempts;
create policy "students read own milling quiz attempt"
  on public.cnc_milling_quiz_attempts for select to authenticated
  using (student_id = auth.uid() or public.is_admin());

drop policy if exists "students create own milling quiz attempt" on public.cnc_milling_quiz_attempts;
create policy "students create own milling quiz attempt"
  on public.cnc_milling_quiz_attempts for insert to authenticated
  with check (student_id = auth.uid() or public.is_admin());

drop policy if exists "students update own milling quiz attempt" on public.cnc_milling_quiz_attempts;
create policy "students update own milling quiz attempt"
  on public.cnc_milling_quiz_attempts for update to authenticated
  using (student_id = auth.uid() or public.is_admin())
  with check (student_id = auth.uid() or public.is_admin());

do $$
begin
  if not exists (
    select 1
    from pg_publication_tables
    where pubname = 'supabase_realtime'
      and schemaname = 'public'
      and tablename = 'cnc_milling_quiz_attempts'
  ) then
    alter publication supabase_realtime add table public.cnc_milling_quiz_attempts;
  end if;
end $$;
