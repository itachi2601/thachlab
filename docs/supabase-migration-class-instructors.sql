-- Phân công giảng viên theo khối lớp THPT (song song với course_instructors đã có cho CTTC).
-- 1 khối có thể có nhiều giảng viên, 1 giảng viên có thể phụ trách nhiều khối.
-- Đây là bảng ghi nhận phân công (hiển thị trong trang quản trị) — không mở rộng RLS chi tiết
-- theo từng khối cho các bảng chapters/lessons như đã làm cho CTTC (course_instructors), vì
-- giảng viên được cấp admin_area = 'thpt' đã thấy được toàn bộ khu vực THPT trong /quan-tri.

create table if not exists public.class_instructors (
  class_id bigint not null references public.classes(id) on delete cascade,
  instructor_id uuid not null references public.profiles(id) on delete cascade,
  assigned_by uuid references public.profiles(id) on delete set null,
  assigned_at timestamptz not null default now(),
  primary key (class_id, instructor_id)
);
create index if not exists class_instructors_instructor_idx on public.class_instructors(instructor_id, class_id);

alter table public.class_instructors enable row level security;

drop policy if exists "admins manage class instructors" on public.class_instructors;
create policy "admins manage class instructors" on public.class_instructors
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "instructors read own class assignments" on public.class_instructors;
create policy "instructors read own class assignments" on public.class_instructors
  for select to authenticated using (instructor_id = auth.uid() or public.is_admin());
