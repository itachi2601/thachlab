-- Theo dõi hoạt động học tập gần thời gian thực cho dashboard giáo viên THPT–THCS.
-- Chạy sau migrations classes, class_instructors và lessons. Idempotent.

create table if not exists public.student_learning_presence (
  student_id uuid primary key references public.profiles(id) on delete cascade,
  lesson_id bigint references public.lessons(id) on delete set null,
  activity_type text not null default 'lesson'
    check (activity_type in ('lesson', 'video', 'document', 'practice', 'exam')),
  lesson_opened_at timestamptz not null default now(),
  last_seen_at timestamptz not null default now()
);

create index if not exists student_learning_presence_last_seen_idx
  on public.student_learning_presence(last_seen_at desc);
create index if not exists student_learning_presence_lesson_idx
  on public.student_learning_presence(lesson_id, last_seen_at desc);

alter table public.student_learning_presence enable row level security;

drop policy if exists "students manage own learning presence" on public.student_learning_presence;
create policy "students manage own learning presence" on public.student_learning_presence
  for all to authenticated
  using (student_id = auth.uid())
  with check (student_id = auth.uid());

drop policy if exists "admins read learning presence" on public.student_learning_presence;
create policy "admins read learning presence" on public.student_learning_presence
  for select to authenticated using (public.is_admin());

drop policy if exists "assigned instructors read class learning presence" on public.student_learning_presence;
create policy "assigned instructors read class learning presence" on public.student_learning_presence
  for select to authenticated using (
    exists (
      select 1
      from public.user_classes uc
      join public.class_instructors ci on ci.class_id = uc.class_id
      where uc.user_id = student_learning_presence.student_id
        and ci.instructor_id = auth.uid()
    )
  );

-- Chỉ giữ một dòng mỗi học sinh; client upsert heartbeat mỗi 60 giây.
