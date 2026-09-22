-- ============================================================
-- Khoá học THPT công khai: đăng lịch, phụ huynh / học sinh tự ghi danh
--
-- Vì sao không dùng course_offerings: bảng đó là của hệ CTTC — trigger
-- set_profile_track_cttc (supabase-migration-student-track.sql) đổi track của học sinh
-- sang 'cttc' ngay khi có dòng course_enrollments, và /tai-khoan coi mọi enrollment là
-- khoá CTTC. Khoá THPT có bộ bảng riêng, và "vào lớp" vẫn là một dòng user_classes như
-- luồng THPT hiện có (duyệt xong -> user_classes active -> đọc được bài, có trong bảng điểm).
--
-- Luồng:
--   giáo viên (dashboard THPT, tab Ghi danh) tạo khoá cho khối + lịch tuần + sức chứa
--   -> /khoa-hoc (không cần đăng nhập) liệt kê khoá đang mở
--   -> phụ huynh (tài khoản đã nối con) hoặc học sinh bấm Đăng ký -> thpt_register()
--      · có student_id -> thêm user_classes 'pending' (đúng chỗ giáo viên vẫn duyệt)
--      · con chưa có tài khoản -> ghi tên + liên hệ, giáo viên gắn tài khoản sau
--   -> giáo viên duyệt: thpt_review_registration() -> user_classes 'active'
--   -> phí: payment_status do giáo viên tích tay (unpaid / paid_center / paid_transfer)
--
-- Chạy SAU: supabase-migration-user-classes-approval.sql, supabase-migration-phu-huynh.sql
-- Idempotent — chạy lại được. Chạy trong Supabase → SQL Editor.
-- ============================================================

-- ---------- 1. Bảng ----------
create table if not exists public.thpt_courses (
  id bigint generated always as identity primary key,
  class_id bigint not null references public.classes (id) on delete restrict,
  name text not null,
  description text not null default '',
  school_year text not null,
  starts_at date,
  ends_at date,
  -- null = không giới hạn
  capacity int check (capacity is null or capacity > 0),
  -- "600k/tháng, đóng tại trung tâm" — chỉ hiển thị, không tính toán
  fee_note text not null default '',
  is_public boolean not null default true,
  status text not null default 'active'
    check (status in ('draft', 'active', 'completed', 'archived')),
  created_by uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now()
);
create index if not exists thpt_courses_class_idx on public.thpt_courses (class_id, status);

-- Lịch tuần: mỗi dòng một buổi. weekday 1 = Thứ hai … 7 = Chủ nhật.
create table if not exists public.thpt_course_schedules (
  id bigint generated always as identity primary key,
  course_id bigint not null references public.thpt_courses (id) on delete cascade,
  weekday smallint not null check (weekday between 1 and 7),
  start_time time not null,
  end_time time not null,
  location text not null default '',
  check (end_time > start_time)
);
create index if not exists thpt_course_schedules_course_idx
  on public.thpt_course_schedules (course_id, weekday, start_time);

create table if not exists public.thpt_registrations (
  id bigint generated always as identity primary key,
  course_id bigint not null references public.thpt_courses (id) on delete cascade,
  -- null khi phụ huynh đăng ký cho con chưa có tài khoản; giáo viên gắn sau.
  student_id uuid references public.profiles (id) on delete cascade,
  registered_by uuid references public.profiles (id) on delete set null,
  child_name text not null default '',
  contact text not null default '',
  note text not null default '',
  -- catchup: vào trễ, đang phụ đạo bù bài trước khi vào lớp (bước 3)
  status text not null default 'pending'
    check (status in ('pending', 'catchup', 'active', 'rejected', 'left')),
  -- đăng ký sau ngày khai giảng — để giáo viên biết cần xếp bù bài
  joined_late boolean not null default false,
  payment_status text not null default 'unpaid'
    check (payment_status in ('unpaid', 'paid_center', 'paid_transfer')),
  payment_note text not null default '',
  created_at timestamptz not null default now(),
  reviewed_by uuid references public.profiles (id) on delete set null,
  reviewed_at timestamptz
);
create index if not exists thpt_registrations_course_idx on public.thpt_registrations (course_id, status);
create index if not exists thpt_registrations_student_idx on public.thpt_registrations (student_id)
  where student_id is not null;
create index if not exists thpt_registrations_by_idx on public.thpt_registrations (registered_by);
-- Một em chỉ có một dòng cho một khoá.
create unique index if not exists thpt_registrations_course_student_idx
  on public.thpt_registrations (course_id, student_id) where student_id is not null;

-- ---------- 2. RLS ----------
alter table public.thpt_courses enable row level security;
alter table public.thpt_course_schedules enable row level security;
alter table public.thpt_registrations enable row level security;

-- Người đã đăng ký (chính em, người đăng ký hộ, phụ huynh) vẫn đọc được khoá đã đóng/ẩn để
-- xem trạng thái của mình. Hàm security definer để policy của thpt_courses không đọc
-- thpt_registrations qua RLS (policy bảng đó lại đọc thpt_courses -> Postgres báo đệ quy).
create or replace function public.thpt_has_registration(p_course_id bigint)
returns boolean
language sql security definer stable set search_path = public
as $$
  select auth.uid() is not null and exists (
    select 1 from public.thpt_registrations r
    where r.course_id = p_course_id
      and (r.student_id = auth.uid()
           or r.registered_by = auth.uid()
           or (r.student_id is not null and public.is_parent_of(r.student_id)))
  );
$$;
grant execute on function public.thpt_has_registration(bigint) to authenticated;

-- Khoá công khai đang mở: ai cũng đọc được (kể cả chưa đăng nhập — trang /khoa-hoc).
-- Giáo viên phụ trách khối (manages_class đã gồm admin) đọc/sửa mọi khoá của khối.
drop policy if exists "anyone reads public courses" on public.thpt_courses;
create policy "anyone reads public courses" on public.thpt_courses
  for select using (
    (is_public and status = 'active')
    or (auth.uid() is not null and public.manages_class(class_id))
    or public.thpt_has_registration(id)
  );
drop policy if exists "class managers manage courses" on public.thpt_courses;
create policy "class managers manage courses" on public.thpt_courses
  for all to authenticated
  using (public.manages_class(class_id)) with check (public.manages_class(class_id));

-- Lịch: đọc được khi đọc được khoá (policy trên đã lọc).
drop policy if exists "anyone reads public schedules" on public.thpt_course_schedules;
create policy "anyone reads public schedules" on public.thpt_course_schedules
  for select using (exists (select 1 from public.thpt_courses c where c.id = course_id));
drop policy if exists "class managers manage schedules" on public.thpt_course_schedules;
create policy "class managers manage schedules" on public.thpt_course_schedules
  for all to authenticated
  using (exists (select 1 from public.thpt_courses c where c.id = course_id and public.manages_class(c.class_id)))
  with check (exists (select 1 from public.thpt_courses c where c.id = course_id and public.manages_class(c.class_id)));

-- Đăng ký: chính em, người đăng ký hộ, phụ huynh đã nối — chỉ đọc. Ghi đi qua RPC bên dưới.
drop policy if exists "own registrations" on public.thpt_registrations;
create policy "own registrations" on public.thpt_registrations
  for select to authenticated
  using (
    student_id = auth.uid()
    or registered_by = auth.uid()
    or (student_id is not null and public.is_parent_of(student_id))
  );
-- Giáo viên phụ trách khối: đọc + cập nhật (phí, ghi chú). Duyệt đi qua RPC để ghi cả user_classes.
drop policy if exists "class managers manage registrations" on public.thpt_registrations;
create policy "class managers manage registrations" on public.thpt_registrations
  for all to authenticated
  using (exists (select 1 from public.thpt_courses c where c.id = course_id and public.manages_class(c.class_id)))
  with check (exists (select 1 from public.thpt_courses c where c.id = course_id and public.manages_class(c.class_id)));

-- Giáo viên cần đọc hồ sơ em đã đăng ký (tên, lớp) — em có thể chưa có dòng user_classes.
drop policy if exists "class managers read registered profiles" on public.profiles;
create policy "class managers read registered profiles" on public.profiles
  for select to authenticated
  using (exists (
    select 1 from public.thpt_registrations r
    join public.thpt_courses c on c.id = r.course_id
    where (r.student_id = profiles.id or r.registered_by = profiles.id)
      and public.manages_class(c.class_id)
  ));

-- ---------- 3. Số chỗ đã lấy — cho trang công khai, không lộ dòng đăng ký ----------
create or replace function public.thpt_course_seats(p_course_ids bigint[])
returns table (course_id bigint, taken int)
language sql stable security definer set search_path = public
as $$
  select r.course_id, count(*)::int
  from public.thpt_registrations r
  join public.thpt_courses c on c.id = r.course_id
  where r.course_id = any (coalesce(p_course_ids, '{}'::bigint[]))
    and r.status in ('pending', 'catchup', 'active')
    and c.is_public and c.status = 'active'
  group by r.course_id;
$$;
grant execute on function public.thpt_course_seats(bigint[]) to anon, authenticated;

-- ---------- 4. Ghi danh ----------
-- p_student_id: chính mình, hoặc con đã nối (is_parent_of). null = con chưa có tài khoản,
-- khi đó bắt buộc p_child_name.
create or replace function public.thpt_register(
  p_course_id bigint,
  p_student_id uuid default null,
  p_child_name text default '',
  p_contact text default '',
  p_note text default ''
)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_user uuid := auth.uid();
  c public.thpt_courses%rowtype;
  v_taken int;
  v_late boolean;
  v_status text;
  v_id bigint;
  v_student_role text;
begin
  if v_user is null then
    raise exception 'Bạn cần đăng nhập trước khi đăng ký.';
  end if;

  select * into c from public.thpt_courses where id = p_course_id;
  if c.id is null or c.status <> 'active' or not (c.is_public or public.manages_class(c.class_id)) then
    raise exception 'Khoá học không còn mở đăng ký.';
  end if;

  if p_student_id is not null then
    if p_student_id <> v_user and not public.is_parent_of(p_student_id) then
      raise exception 'Bạn chỉ đăng ký được cho chính mình hoặc cho con đã nối với tài khoản.';
    end if;
    select role into v_student_role from public.profiles where id = p_student_id;
    if v_student_role in ('admin', 'instructor', 'tro_giang') then
      raise exception 'Tài khoản này không phải tài khoản học sinh.';
    end if;
  elsif coalesce(trim(p_child_name), '') = '' then
    raise exception 'Nhập họ tên của con.';
  end if;

  if c.capacity is not null then
    select count(*) into v_taken from public.thpt_registrations
    where course_id = c.id and status in ('pending', 'catchup', 'active')
      and (p_student_id is null or student_id is distinct from p_student_id);
    if v_taken >= c.capacity then
      raise exception 'Lớp đã đủ chỗ (%/%). Nhắn giáo viên để xếp lớp khác.', v_taken, c.capacity;
    end if;
  end if;

  v_late := c.starts_at is not null and c.starts_at < current_date;
  v_status := 'pending';

  if p_student_id is not null then
    insert into public.thpt_registrations
      (course_id, student_id, registered_by, child_name, contact, note, status, joined_late)
    values
      (c.id, p_student_id, v_user, coalesce(trim(p_child_name), ''), coalesce(trim(p_contact), ''),
       coalesce(trim(p_note), ''), v_status, v_late)
    on conflict (course_id, student_id) where student_id is not null do update
      set status = case
                     when public.thpt_registrations.status in ('rejected', 'left') then excluded.status
                     else public.thpt_registrations.status
                   end,
          joined_late = case
                     when public.thpt_registrations.status in ('rejected', 'left') then excluded.joined_late
                     else public.thpt_registrations.joined_late
                   end,
          note = case when excluded.note <> '' then excluded.note else public.thpt_registrations.note end,
          contact = case when excluded.contact <> '' then excluded.contact else public.thpt_registrations.contact end,
          created_at = case
                     when public.thpt_registrations.status in ('rejected', 'left') then now()
                     else public.thpt_registrations.created_at
                   end
    returning id, status into v_id, v_status;

    -- Vào đúng hàng chờ duyệt của khối — /tai-khoan của em hiện "Đang chờ giáo viên duyệt",
    -- tab Nhập danh sách / trang Học sinh của giáo viên vẫn thấy như học sinh tự xin vào lớp.
    if v_status = 'pending' then
      insert into public.user_classes (user_id, class_id, status)
      values (p_student_id, c.class_id, 'pending')
      on conflict (user_id, class_id) do update
        set status = case when public.user_classes.status = 'rejected' then 'pending' else public.user_classes.status end,
            requested_at = case when public.user_classes.status = 'rejected' then now() else public.user_classes.requested_at end;
    end if;
  else
    insert into public.thpt_registrations
      (course_id, student_id, registered_by, child_name, contact, note, status, joined_late)
    values
      (c.id, null, v_user, trim(p_child_name), coalesce(trim(p_contact), ''), coalesce(trim(p_note), ''),
       v_status, v_late)
    returning id into v_id;
  end if;

  return jsonb_build_object(
    'registration_id', v_id,
    'status', v_status,
    'joined_late', v_late,
    'course_name', c.name
  );
end;
$$;
revoke all on function public.thpt_register(bigint, uuid, text, text, text) from public, anon;
grant execute on function public.thpt_register(bigint, uuid, text, text, text) to authenticated;

-- ---------- 5. Giáo viên duyệt / từ chối / cho nghỉ ----------
create or replace function public.thpt_review_registration(p_id bigint, p_status text)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  r public.thpt_registrations%rowtype;
  c public.thpt_courses%rowtype;
begin
  if p_status not in ('active', 'rejected', 'left', 'pending') then
    raise exception 'Trạng thái không hợp lệ: %', p_status;
  end if;
  select * into r from public.thpt_registrations where id = p_id;
  if r.id is null then raise exception 'Không tìm thấy đăng ký.'; end if;
  select * into c from public.thpt_courses where id = r.course_id;
  if not public.manages_class(c.class_id) then
    raise exception 'Bạn không phụ trách khối lớp này.';
  end if;
  if p_status = 'active' and r.student_id is null then
    raise exception 'Con chưa có tài khoản — gắn tài khoản trước rồi mới duyệt được.';
  end if;

  update public.thpt_registrations
  set status = p_status, reviewed_by = auth.uid(), reviewed_at = now()
  where id = p_id;

  if r.student_id is not null then
    if p_status = 'active' then
      insert into public.user_classes (user_id, class_id, status, reviewed_by, reviewed_at)
      values (r.student_id, c.class_id, 'active', auth.uid(), now())
      on conflict (user_id, class_id) do update
        set status = 'active', reviewed_by = excluded.reviewed_by, reviewed_at = excluded.reviewed_at;
    elsif p_status = 'rejected' then
      update public.user_classes
      set status = 'rejected', reviewed_by = auth.uid(), reviewed_at = now()
      where user_id = r.student_id and class_id = c.class_id and status = 'pending';
    end if;
    -- 'left': giữ nguyên user_classes — giáo viên gỡ khỏi lớp bằng nút sẵn có nếu muốn.
  end if;
end;
$$;
revoke all on function public.thpt_review_registration(bigint, text) from public, anon;
grant execute on function public.thpt_review_registration(bigint, text) to authenticated;

-- Gắn tài khoản cho đăng ký "con chưa có tài khoản" (sau khi nhập roster / em tự đăng ký).
create or replace function public.thpt_attach_student(p_id bigint, p_student_id uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  r public.thpt_registrations%rowtype;
  c public.thpt_courses%rowtype;
begin
  select * into r from public.thpt_registrations where id = p_id;
  if r.id is null then raise exception 'Không tìm thấy đăng ký.'; end if;
  select * into c from public.thpt_courses where id = r.course_id;
  if not public.manages_class(c.class_id) then
    raise exception 'Bạn không phụ trách khối lớp này.';
  end if;
  if exists (select 1 from public.thpt_registrations where course_id = r.course_id and student_id = p_student_id and id <> p_id) then
    raise exception 'Em này đã có đăng ký khác trong khoá.';
  end if;
  if not exists (select 1 from public.profiles where id = p_student_id and role = 'student') then
    raise exception 'Tài khoản được chọn không phải học sinh.';
  end if;

  update public.thpt_registrations set student_id = p_student_id where id = p_id;

  if r.status in ('pending', 'catchup') then
    insert into public.user_classes (user_id, class_id, status)
    values (p_student_id, c.class_id, 'pending')
    on conflict do nothing;
  end if;
end;
$$;
revoke all on function public.thpt_attach_student(bigint, uuid) from public, anon;
grant execute on function public.thpt_attach_student(bigint, uuid) to authenticated;

-- ---------- 6. Duyệt ở chỗ cũ vẫn đồng bộ ----------
-- Giáo viên duyệt thẳng trong hàng chờ user_classes (trang Học sinh / tab Nhập danh sách)
-- thì đăng ký tương ứng cũng chuyển active — không để hai nơi lệch nhau.
create or replace function public.trg_sync_thpt_registration()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  if new.status = 'active' and (old.status is distinct from 'active') then
    update public.thpt_registrations r
    set status = 'active', reviewed_by = coalesce(new.reviewed_by, r.reviewed_by), reviewed_at = now()
    from public.thpt_courses c
    where c.id = r.course_id and c.class_id = new.class_id
      and r.student_id = new.user_id and r.status in ('pending', 'catchup');
  elsif new.status = 'rejected' and (old.status is distinct from 'rejected') then
    update public.thpt_registrations r
    set status = 'rejected', reviewed_by = coalesce(new.reviewed_by, r.reviewed_by), reviewed_at = now()
    from public.thpt_courses c
    where c.id = r.course_id and c.class_id = new.class_id
      and r.student_id = new.user_id and r.status in ('pending', 'catchup');
  end if;
  return new;
end;
$$;

drop trigger if exists trg_sync_thpt_registration on public.user_classes;
create trigger trg_sync_thpt_registration
  after update of status on public.user_classes
  for each row execute function public.trg_sync_thpt_registration();
