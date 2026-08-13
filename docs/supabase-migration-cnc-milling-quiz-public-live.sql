-- Cho phép học sinh tham gia bài kiểm tra vận hành phay không cần đăng nhập.
-- Chạy sau supabase-migration-cnc-milling-quiz-realtime.sql.

alter table public.cnc_milling_quiz_attempts
  alter column student_id drop not null;

alter table public.cnc_milling_quiz_attempts
  add column if not exists participant_key uuid not null default gen_random_uuid(),
  add column if not exists participant_name text not null default 'Học sinh',
  add column if not exists class_name text not null default '';

update public.cnc_milling_quiz_attempts as attempt
set participant_name = coalesce(nullif(profile.full_name, ''), 'Học sinh'),
    class_name = coalesce(profile.class_name, '')
from public.profiles as profile
where attempt.student_id = profile.id
  and attempt.participant_name = 'Học sinh';

alter table public.cnc_milling_quiz_attempts
  drop constraint if exists cnc_milling_quiz_attempts_student_id_key;

create unique index if not exists cnc_milling_quiz_attempts_participant_key_idx
  on public.cnc_milling_quiz_attempts (participant_key);

drop policy if exists "students read own milling quiz attempt" on public.cnc_milling_quiz_attempts;
drop policy if exists "students create own milling quiz attempt" on public.cnc_milling_quiz_attempts;
drop policy if exists "students update own milling quiz attempt" on public.cnc_milling_quiz_attempts;
drop policy if exists "classroom reads live milling attempts" on public.cnc_milling_quiz_attempts;
drop policy if exists "classroom creates live milling attempts" on public.cnc_milling_quiz_attempts;
drop policy if exists "classroom updates live milling attempts" on public.cnc_milling_quiz_attempts;
drop policy if exists "admins reset live milling attempts" on public.cnc_milling_quiz_attempts;

create policy "classroom reads live milling attempts"
  on public.cnc_milling_quiz_attempts for select to anon, authenticated
  using (true);

create policy "classroom creates live milling attempts"
  on public.cnc_milling_quiz_attempts for insert to anon, authenticated
  with check (participant_key is not null and length(trim(participant_name)) > 0);

create policy "classroom updates live milling attempts"
  on public.cnc_milling_quiz_attempts for update to anon, authenticated
  using (true)
  with check (participant_key is not null and length(trim(participant_name)) > 0);

create policy "admins reset live milling attempts"
  on public.cnc_milling_quiz_attempts for delete to authenticated
  using (public.is_admin());
