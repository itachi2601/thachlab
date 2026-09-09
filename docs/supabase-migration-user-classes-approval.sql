-- Cho học sinh tự đăng ký web (không qua roster import) gửi yêu cầu vào 1 khối lớp THPT,
-- và giáo viên/quản trị viên phụ trách khối đó duyệt trước khi học sinh được tính là thành
-- viên chính thức (đọc được bài, hiện trong bảng điểm/điểm danh...).
-- Chạy sau supabase-migration-classes.sql, supabase-migration-class-instructors.sql và
-- supabase-migration-roster-import-thpt.sql (cần bảng class_instructors + hàm can_manage_class).

alter table public.user_classes
  add column if not exists status text not null default 'active'
    check (status in ('pending', 'active', 'rejected'));
alter table public.user_classes add column if not exists requested_at timestamptz not null default now();
alter table public.user_classes add column if not exists reviewed_by uuid references public.profiles(id) on delete set null;
alter table public.user_classes add column if not exists reviewed_at timestamptz;

create index if not exists user_classes_status_idx on public.user_classes(class_id, status);

-- Roster import (Edge Function, service_role) và ClassesAdmin gán tay không đổi hành vi:
-- không set status -> mặc định 'active', vào lớp ngay như trước migration này.

-- Thay policy "chỉ admin" bằng can_manage_class -- giáo viên được phân công khối (class_instructors)
-- cũng duyệt/gán/xoá được, không chỉ quản trị viên. Thu hồi các policy hẹp hơn đã bị policy này
-- bao trùm (assigned instructors read class rosters chỉ có SELECT; policy mới có cả SELECT).
drop policy if exists "admin manages user classes" on public.user_classes;
drop policy if exists "assigned instructors read class rosters" on public.user_classes;
create policy "class managers manage user classes" on public.user_classes
  for all to authenticated
  using (public.can_manage_class(class_id))
  with check (public.can_manage_class(class_id));

-- Học sinh tự gửi yêu cầu vào lớp (luôn ở trạng thái 'pending' -- không tự vào lớp ngay được).
drop policy if exists "students request own class" on public.user_classes;
create policy "students request own class" on public.user_classes
  for insert to authenticated
  with check (user_id = auth.uid() and status = 'pending');

-- Học sinh bị từ chối được gửi lại yêu cầu (chuyển hàng đã có từ 'rejected' về 'pending').
drop policy if exists "students resubmit rejected class request" on public.user_classes;
create policy "students resubmit rejected class request" on public.user_classes
  for update to authenticated
  using (user_id = auth.uid() and status = 'rejected')
  with check (user_id = auth.uid() and status = 'pending');

-- Khoá luôn kẽ hở cũ: nếu ai đó tự truyền class_id trong metadata lúc signUp (auth.signUp),
-- trigger từng cho vào lớp ngay (status mặc định 'active' theo cột mới) -- nay bắt buộc 'pending'
-- để đi qua đúng luồng duyệt như học sinh tự chọn lớp ở /tai-khoan.
create or replace function public.handle_new_user()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  cid bigint := nullif(new.raw_user_meta_data ->> 'class_id', '')::bigint;
  cname text := '';
begin
  if cid is not null then
    select name into cname from public.classes where id = cid;
  end if;
  insert into public.profiles (id, full_name, class_name)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'full_name', ''),
    coalesce(cname, new.raw_user_meta_data ->> 'class_name', '')
  );
  if cid is not null then
    insert into public.user_classes (user_id, class_id, status) values (new.id, cid, 'pending')
    on conflict do nothing;
  end if;
  return new;
end;
$$;
