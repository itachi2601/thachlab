-- Báo cáo máy/thiết bị hư hỏng — ảnh lưu vĩnh viễn, tách khỏi ảnh 5S đầu ca/cuối ca
-- (ảnh 5S sẽ bị dọn khi buổi điểm danh kế tiếp của khóa mở ra, xem cleanup_old_machine_photos bên dưới).
-- Chạy sau docs/supabase-migration-attendance-machine-duty.sql.
-- Dùng chung course_id + machine_code dạng text (không ràng buộc CNC) để môn học khác có thể tái dùng sau này.

create table if not exists public.equipment_breakdown_reports (
  id bigint generated always as identity primary key,
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  session_id bigint references public.attendance_sessions(id) on delete set null,
  machine_code text not null,
  description text not null default '',
  storage_path text not null,
  status text not null default 'open' check (status in ('open','resolved')),
  reported_by uuid references public.profiles(id) on delete set null,
  resolved_by uuid references public.profiles(id) on delete set null,
  resolved_at timestamptz,
  resolved_note text not null default '',
  created_at timestamptz not null default now()
);
create index if not exists equipment_breakdown_reports_course_idx on public.equipment_breakdown_reports(course_id, status);

alter table public.equipment_breakdown_reports enable row level security;

drop policy if exists "admins manage equipment breakdown reports" on public.equipment_breakdown_reports;
create policy "admins manage equipment breakdown reports" on public.equipment_breakdown_reports
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "students read equipment breakdown reports" on public.equipment_breakdown_reports;
create policy "students read equipment breakdown reports" on public.equipment_breakdown_reports
  for select to authenticated using (
    public.is_admin() or exists(
      select 1 from public.course_enrollments e
      where e.course_id = course_id and e.student_id = auth.uid() and e.status = 'active'
    )
  );

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('equipment-breakdown-photos', 'equipment-breakdown-photos', false, 10485760,
  array['image/png','image/jpeg','image/webp','image/heic','application/octet-stream'])
on conflict (id) do update set
  public = excluded.public, file_size_limit = excluded.file_size_limit, allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "admins upload equipment breakdown photos" on storage.objects;
create policy "admins upload equipment breakdown photos" on storage.objects
  for insert to authenticated with check (bucket_id = 'equipment-breakdown-photos' and public.is_admin());
drop policy if exists "read equipment breakdown photos" on storage.objects;
create policy "read equipment breakdown photos" on storage.objects
  for select to authenticated using (
    bucket_id = 'equipment-breakdown-photos'
    and (public.is_admin() or exists(
      select 1 from public.course_enrollments e
      where e.status = 'active' and e.student_id = auth.uid()
        and e.course_id::text = (storage.foldername(name))[1]
    ))
  );

-- Giáo viên báo hỏng — chỉ giáo viên/admin được gọi (is_admin), ảnh lưu ở bucket riêng nên
-- không bao giờ bị dọn bởi cleanup_old_machine_photos.
create or replace function public.report_equipment_breakdown(
  p_course_id bigint, p_session_id bigint, p_machine_code text, p_description text, p_storage_path text
) returns bigint language plpgsql security definer set search_path = public as $$
declare new_id bigint;
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được báo hỏng máy.'; end if;
  insert into public.equipment_breakdown_reports(course_id, session_id, machine_code, description, storage_path, reported_by)
  values (p_course_id, p_session_id, p_machine_code, p_description, p_storage_path, auth.uid())
  returning id into new_id;
  return new_id;
end; $$;
revoke all on function public.report_equipment_breakdown(bigint, bigint, text, text, text) from public;
grant execute on function public.report_equipment_breakdown(bigint, bigint, text, text, text) to authenticated;

create or replace function public.resolve_equipment_breakdown(p_id bigint, p_note text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'Chỉ giáo viên mới được cập nhật báo cáo.'; end if;
  update public.equipment_breakdown_reports
  set status = 'resolved', resolved_by = auth.uid(), resolved_at = now(), resolved_note = p_note
  where id = p_id;
end; $$;
revoke all on function public.resolve_equipment_breakdown(bigint, text) from public;
grant execute on function public.resolve_equipment_breakdown(bigint, text) to authenticated;

-- Dọn ảnh 5S đầu ca/cuối ca của các buổi CŨ trong cùng khóa học khi một buổi MỚI được mở
-- (giữ nguyên ảnh của buổi hiện tại đang mở). Trả về storage_path đã xóa để client xóa file thật
-- khỏi bucket (xóa hàng ở bảng không tự xóa file trong Storage).
create or replace function public.cleanup_old_machine_photos(p_course_id bigint, p_keep_session_id bigint)
returns text[] language plpgsql security definer set search_path = public as $$
declare deleted_paths text[];
begin
  if not public.is_admin() then raise exception 'Không có quyền.'; end if;
  with stale as (
    delete from public.attendance_machine_photos amp
    using public.attendance_sessions s
    where amp.session_id = s.id
      and s.course_id = p_course_id
      and s.id <> p_keep_session_id
    returning amp.storage_path
  )
  select coalesce(array_agg(storage_path), array[]::text[]) into deleted_paths from stale;
  return deleted_paths;
end; $$;
revoke all on function public.cleanup_old_machine_photos(bigint, bigint) from public;
grant execute on function public.cleanup_old_machine_photos(bigint, bigint) to authenticated;
