-- Theo dõi vệ sinh máy theo nhóm (đầu ca / cuối ca) gắn với điểm danh hằng ngày.
-- Chạy sau docs/supabase-migration-course-attendance.sql.

-- Sinh viên chọn máy đã dùng trong buổi (T1..T8 máy tiện, P1..P8 máy phay).
alter table public.attendance_records add column if not exists machine_code text;

-- Ảnh kiểm tra máy (đầu ca/cuối ca) + ảnh toàn xưởng (XUONG) + ảnh thùng rác (RAC) theo buổi.
-- Chỉ cần 1 sinh viên trong nhóm nộp là đủ cho cả nhóm (unique theo session+machine+checkpoint).
create table if not exists public.attendance_machine_photos (
  id bigint generated always as identity primary key,
  session_id bigint not null references public.attendance_sessions(id) on delete cascade,
  machine_code text not null,
  checkpoint text not null default 'end' check (checkpoint in ('start','end')),
  storage_path text not null,
  note text not null default '',
  uploaded_by uuid references public.profiles(id) on delete set null,
  created_at timestamptz not null default now(),
  unique(session_id, machine_code, checkpoint)
);
create index if not exists attendance_machine_photos_session_idx on public.attendance_machine_photos(session_id);

-- Điểm cộng/trừ áp dụng chung cho cả nhóm dùng 1 máy trong buổi (tách khỏi điểm cộng/trừ cá nhân).
create table if not exists public.attendance_machine_scores (
  session_id bigint not null references public.attendance_sessions(id) on delete cascade,
  machine_code text not null,
  bonus_points integer not null default 0,
  note text not null default '',
  updated_at timestamptz not null default now(),
  primary key(session_id, machine_code)
);

alter table public.attendance_machine_photos enable row level security;
alter table public.attendance_machine_scores enable row level security;

drop policy if exists "admins manage attendance machine photos" on public.attendance_machine_photos;
create policy "admins manage attendance machine photos" on public.attendance_machine_photos
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "students read attendance machine photos" on public.attendance_machine_photos;
create policy "students read attendance machine photos" on public.attendance_machine_photos
  for select to authenticated using (
    public.is_admin() or exists(
      select 1 from public.attendance_sessions s
      join public.course_enrollments e on e.course_id = s.course_id and e.student_id = auth.uid() and e.status = 'active'
      where s.id = session_id
    )
  );

drop policy if exists "admins manage attendance machine scores" on public.attendance_machine_scores;
create policy "admins manage attendance machine scores" on public.attendance_machine_scores
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "students read attendance machine scores" on public.attendance_machine_scores;
create policy "students read attendance machine scores" on public.attendance_machine_scores
  for select to authenticated using (
    public.is_admin() or exists(
      select 1 from public.attendance_sessions s
      join public.course_enrollments e on e.course_id = s.course_id and e.student_id = auth.uid() and e.status = 'active'
      where s.id = session_id
    )
  );

-- Sinh viên chọn máy đã dùng cho buổi mình đã điểm danh.
create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_machine_code !~ '^(T[1-8]|P[1-8])$' then raise exception 'Mã máy không hợp lệ.'; end if;
  update public.attendance_records set machine_code = p_machine_code, updated_at = now()
  where session_id = p_session_id and student_id = auth.uid();
  if not found then raise exception 'Bạn chưa điểm danh buổi này.'; end if;
end; $$;
revoke all on function public.select_attendance_machine(bigint, text) from public;
grant execute on function public.select_attendance_machine(bigint, text) to authenticated;

-- Ghi nhận 1 ảnh (đầu ca/cuối ca cho máy thật, hoặc XUONG/RAC cho ảnh chung).
-- Bất kỳ sinh viên nào thuộc buổi đều được nộp XUONG/RAC; với máy thật phải là người đã chọn đúng máy đó.
create or replace function public.submit_attendance_machine_photo(
  p_session_id bigint, p_machine_code text, p_checkpoint text, p_storage_path text, p_note text default ''
) returns void language plpgsql security definer set search_path = public as $$
declare own_machine text;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_checkpoint not in ('start','end') then raise exception 'Mốc kiểm tra không hợp lệ.'; end if;
  if p_machine_code not in ('XUONG','RAC') then
    select machine_code into own_machine from public.attendance_records
      where session_id = p_session_id and student_id = auth.uid();
    if own_machine is null or own_machine <> p_machine_code then
      raise exception 'Bạn chưa chọn máy này trong buổi điểm danh.';
    end if;
  else
    if not exists(select 1 from public.attendance_records where session_id = p_session_id and student_id = auth.uid()) then
      raise exception 'Bạn chưa điểm danh buổi này.';
    end if;
  end if;
  insert into public.attendance_machine_photos(session_id, machine_code, checkpoint, storage_path, note, uploaded_by)
  values (p_session_id, p_machine_code, p_checkpoint, p_storage_path, p_note, auth.uid())
  on conflict (session_id, machine_code, checkpoint) do nothing;
end; $$;
revoke all on function public.submit_attendance_machine_photo(bigint, text, text, text, text) from public;
grant execute on function public.submit_attendance_machine_photo(bigint, text, text, text, text) to authenticated;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('attendance-machine-photos', 'attendance-machine-photos', false, 10485760,
  array['image/png','image/jpeg','image/webp','image/heic','application/octet-stream'])
on conflict (id) do update set
  public = excluded.public, file_size_limit = excluded.file_size_limit, allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "students upload attendance machine photos" on storage.objects;
create policy "students upload attendance machine photos" on storage.objects
  for insert to authenticated
  with check (
    bucket_id = 'attendance-machine-photos'
    and exists(
      select 1 from public.attendance_sessions s
      join public.course_enrollments e on e.course_id = s.course_id and e.student_id = auth.uid() and e.status = 'active'
      where s.id::text = (storage.foldername(name))[1]
    )
  );
drop policy if exists "read attendance machine photos" on storage.objects;
create policy "read attendance machine photos" on storage.objects
  for select to authenticated
  using (
    bucket_id = 'attendance-machine-photos'
    and (public.is_admin() or exists(
      select 1 from public.attendance_sessions s
      join public.course_enrollments e on e.course_id = s.course_id and e.student_id = auth.uid() and e.status = 'active'
      where s.id::text = (storage.foldername(name))[1]
    ))
  );
