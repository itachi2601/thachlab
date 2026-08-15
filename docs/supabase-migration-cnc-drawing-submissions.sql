-- Hồ sơ bản vẽ trước khi sinh viên được gia công tiện/phay CNC.
-- Chạy sau docs/supabase-schema.sql.

create table if not exists public.cnc_drawing_submissions (
  id bigint generated always as identity primary key,
  course_id bigint references public.course_offerings (id) on delete cascade,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  student_id uuid not null references public.profiles (id) on delete cascade,
  lesson_id text not null check (lesson_id in ('lesson-5', 'lesson-6', 'lesson-2-simulation', 'lesson-3-simulation')),
  file_name text not null,
  storage_path text not null unique,
  mime_type text not null default 'application/octet-stream',
  size_bytes bigint not null default 0,
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  teacher_feedback text not null default '',
  reviewed_by uuid references public.profiles (id),
  reviewed_at timestamptz,
  unique (student_id, lesson_id)
);

create index if not exists cnc_drawing_submissions_status_idx
  on public.cnc_drawing_submissions (status, updated_at desc);

-- Bảng có thể đã tồn tại thiếu cột course_id (bản migration cũ); bổ sung cho môi trường đã tạo bảng.
alter table public.cnc_drawing_submissions add column if not exists course_id bigint references public.course_offerings (id) on delete cascade;

-- Bài tập 5 (mô phỏng và kiểm chứng) của Lập trình tiện/phay nộp minh chứng qua bảng này
-- với lesson_id "lesson-2-simulation" / "lesson-3-simulation"; nới ràng buộc cho bảng đã tồn tại.
alter table public.cnc_drawing_submissions drop constraint if exists cnc_drawing_submissions_lesson_id_check;
alter table public.cnc_drawing_submissions add constraint cnc_drawing_submissions_lesson_id_check
  check (lesson_id in ('lesson-5', 'lesson-6', 'lesson-2-simulation', 'lesson-3-simulation'));

alter table public.cnc_drawing_submissions enable row level security;

drop policy if exists "students read own cnc drawings" on public.cnc_drawing_submissions;
create policy "students read own cnc drawings" on public.cnc_drawing_submissions
  for select to authenticated
  using (student_id = auth.uid() or public.is_admin());

drop policy if exists "students submit own cnc drawings" on public.cnc_drawing_submissions;
create policy "students submit own cnc drawings" on public.cnc_drawing_submissions
  for insert to authenticated
  with check (
    student_id = auth.uid()
    and status = 'pending'
    and reviewed_by is null
    and reviewed_at is null
  );

drop policy if exists "students resubmit rejected cnc drawings" on public.cnc_drawing_submissions;
create policy "students resubmit rejected cnc drawings" on public.cnc_drawing_submissions
  for update to authenticated
  using (student_id = auth.uid() and status = 'rejected')
  with check (
    student_id = auth.uid()
    and status = 'pending'
    and reviewed_by is null
    and reviewed_at is null
  );

drop policy if exists "admin reviews cnc drawings" on public.cnc_drawing_submissions;
create policy "admin reviews cnc drawings" on public.cnc_drawing_submissions
  for all to authenticated
  using (public.is_admin())
  with check (public.is_admin());

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'cnc-drawings',
  'cnc-drawings',
  false,
  26214400,
  array[
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/png',
    'image/jpeg',
    'image/webp',
    'application/acad',
    'application/x-acad',
    'application/autocad_dwg',
    'image/vnd.dwg',
    'application/dwg',
    'application/dxf',
    'application/octet-stream'
  ]
)
on conflict (id) do update set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "students upload own cnc drawings" on storage.objects;
create policy "students upload own cnc drawings" on storage.objects
  for insert to authenticated
  with check (
    bucket_id = 'cnc-drawings'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

drop policy if exists "students read own cnc drawing files" on storage.objects;
create policy "students read own cnc drawing files" on storage.objects
  for select to authenticated
  using (
    bucket_id = 'cnc-drawings'
    and ((storage.foldername(name))[1] = auth.uid()::text or public.is_admin())
  );

drop policy if exists "students delete own cnc drawing files" on storage.objects;
create policy "students delete own cnc drawing files" on storage.objects
  for delete to authenticated
  using (
    bucket_id = 'cnc-drawings'
    and ((storage.foldername(name))[1] = auth.uid()::text or public.is_admin())
  );
