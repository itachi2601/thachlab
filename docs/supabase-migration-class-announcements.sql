-- ============================================================
-- Thông báo lớp: "việc cần làm buổi hôm nay" + "bài tập về nhà"
-- ============================================================
-- Chạy SAU:
--   docs/supabase-migration-exam-analytics.sql   (is_admin, manages_class)
--   docs/supabase-migration-tutoring-needs.sql   (assists_class)
--   docs/supabase-migration-classes.sql          (bảng classes)
-- Idempotent — chạy lại được.
--
-- Giáo viên và trợ giảng của một lớp đăng một dòng thông báo ngắn, học sinh trong
-- lớp thấy ở trang chủ của mình. Chỉ giữ dòng MỚI NHẤT của mỗi loại (kind) làm nội
-- dung hiện hành — đăng dòng mới là thay dòng cũ, xoá dòng là gỡ thông báo.
-- ============================================================

create table if not exists public.class_announcements (
  id bigint generated always as identity primary key,
  class_id bigint not null references public.classes (id) on delete cascade,
  kind text not null check (kind in ('today_task', 'homework')),
  body text not null check (length(trim(body)) > 0),
  created_by uuid not null references public.profiles (id) on delete cascade,
  created_at timestamptz not null default now()
);
create index if not exists class_announcements_class_idx
  on public.class_announcements (class_id, kind, created_at desc);

alter table public.class_announcements enable row level security;

drop policy if exists "staff post announcements" on public.class_announcements;
create policy "staff post announcements" on public.class_announcements
  for insert to authenticated
  with check (
    created_by = auth.uid()
    and (public.manages_class(class_id) or public.assists_class(class_id) or public.is_admin())
  );

drop policy if exists "staff delete announcements" on public.class_announcements;
create policy "staff delete announcements" on public.class_announcements
  for delete to authenticated
  using (public.manages_class(class_id) or public.assists_class(class_id) or public.is_admin());

drop policy if exists "staff read announcements" on public.class_announcements;
create policy "staff read announcements" on public.class_announcements
  for select to authenticated
  using (public.manages_class(class_id) or public.assists_class(class_id) or public.is_admin());

drop policy if exists "students read class announcements" on public.class_announcements;
create policy "students read class announcements" on public.class_announcements
  for select to authenticated
  using (exists (
    select 1 from public.user_classes uc
    where uc.user_id = auth.uid() and uc.class_id = class_announcements.class_id and uc.status = 'active'
  ));
