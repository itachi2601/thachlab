-- ============================================================================
-- Phụ huynh tự nối tài khoản với con ở /phu-huynh (không cần link mời)
--
-- Khớp bằng ĐỦ 3 thứ: họ tên con (bỏ dấu, không phân biệt hoa thường, gộp khoảng trắng)
-- + ngày sinh con (profiles.birth_date) + SĐT phụ huynh đã khai (9 số cuối) ở một trong:
--   · thpt_registration_requests.parent_phone (user_id = em)
--   · thpt_registrations.contact (student_id = em; text tự do, lấy các chuỗi số)
--   · auth.users.raw_user_meta_data->>'parent_phone' (em) — chỗ thầy/TA sửa bằng
--     staff_set_student_phones (20261014120000), nên tính luôn.
-- Không khớp → phụ huynh gửi yêu cầu cho thầy duyệt tay.
--
-- Thêm:
--   · bảng parent_link_attempts (đếm lần thử, khoá 24 giờ sau 5 lần sai) — không policy
--   · bảng parent_link_requests (yêu cầu chờ duyệt) — chỉ select qua policy
--   · hàm nội bộ pl_fold_name, pl_digits, pl_student_phone_match, pl_student_class_label,
--     pl_notify_staff_of_student, pl_link_parent (không grant cho authenticated)
--   · RPC claim_parent_by_child_info, request_parent_link_review,
--     review_parent_link_request, search_students_for_link
-- Tái dùng apply_parent_link (luật đổi role 'parent', chặn admin, chặn tự nối).
-- notifications.kind không có ràng buộc check → không cần mở rộng cho 3 kind mới.
-- Chỉ thêm bảng + hàm, chạy lúc nào cũng được.
--
-- AI ĐỌC / GHI ĐƯỢC GÌ
-- | Bảng / hàm                      | Học sinh / phụ huynh            | Trợ giảng (active)                      | Giảng viên                              | Admin    |
-- |---------------------------------|---------------------------------|-----------------------------------------|-----------------------------------------|----------|
-- | parent_link_attempts            | không đọc, không ghi            | không                                   | không                                   | không (chỉ qua SQL editor) |
-- | parent_link_requests (select)   | yêu cầu do mình gửi             | yêu cầu đã khớp được em (teaches_student đúng với mọi em khi TA active) | yêu cầu khớp em thuộc lớp mình dạy | tất cả |
-- | parent_link_requests (ghi)      | chỉ qua request_parent_link_review | chỉ qua review_parent_link_request   | như TA                                  | như TA   |
-- | claim_parent_by_child_info      | được (nối cho chính mình)       | được (nối cho chính mình)               | được                                    | bị apply_parent_link chặn |
-- | review_parent_link_request      | không                           | duyệt em mình teaches_student           | duyệt em lớp mình                       | tất cả   |
-- | search_students_for_link        | không (raise)                   | em teaches_student                      | em lớp mình                             | tất cả   |
-- ============================================================================

begin;

-- ---------- 1. Hàm nội bộ ----------

-- Bỏ dấu tiếng Việt: tách tổ hợp (NFD) rồi xoá dấu kết hợp U+0300–U+036F; đ/Đ không tách
-- được nên translate riêng. Chạy được cả với chuỗi gõ dạng tổ hợp (bàn phím Mac).
create or replace function public.pl_fold_name(p text)
returns text
language sql immutable
set search_path = public
as $$
  select btrim(regexp_replace(
           lower(translate(
             regexp_replace(normalize(coalesce(p, ''), NFD), '[̀-ͯ]', '', 'g'),
             'đĐ', 'dd')),
           '\s+', ' ', 'g'));
$$;

create or replace function public.pl_digits(p text)
returns text
language sql immutable
set search_path = public
as $$
  select regexp_replace(coalesce(p, ''), '[^0-9]', '', 'g');
$$;

-- p_phone9: đúng 9 số cuối SĐT phụ huynh khai. Hàm này là "máy dò SĐT" nên KHÔNG grant.
create or replace function public.pl_student_phone_match(p_student uuid, p_phone9 text)
returns boolean
language sql stable security definer
set search_path = public
as $$
  select length(coalesce(p_phone9, '')) = 9 and (
    exists (
      select 1 from public.thpt_registration_requests r
      where r.user_id = p_student
        and length(public.pl_digits(r.parent_phone)) >= 9
        and right(public.pl_digits(r.parent_phone), 9) = p_phone9
    )
    or exists (
      -- contact là text tự do: cắt theo ký tự không thuộc số điện thoại, xét cả hai mức
      -- (giữ khoảng trắng trong số "0912 345 678", và tách theo khoảng trắng khi hai số
      -- liền nhau "0912345678 0987654321").
      select 1
      from public.thpt_registrations t,
           lateral (
             select public.pl_digits(c) as d
             from regexp_split_to_table(coalesce(t.contact, ''), '[^0-9 .()+-]+') c
             union all
             select public.pl_digits(c)
             from regexp_split_to_table(coalesce(t.contact, ''), '[^0-9.()+-]+') c
           ) x
      where t.student_id = p_student
        and length(x.d) >= 9
        and right(x.d, 9) = p_phone9
    )
    or exists (
      select 1 from auth.users u
      where u.id = p_student
        and length(public.pl_digits(u.raw_user_meta_data->>'parent_phone')) >= 9
        and right(public.pl_digits(u.raw_user_meta_data->>'parent_phone'), 9) = p_phone9
    )
  );
$$;

create or replace function public.pl_student_class_label(p_student uuid)
returns text
language sql stable security definer
set search_path = public
as $$
  select coalesce(
    nullif(btrim(p.class_name), ''),
    (select string_agg(c.name, ', ' order by c.sort_order, c.name)
       from public.user_classes uc join public.classes c on c.id = uc.class_id
      where uc.user_id = p_student and uc.status = 'active')
  )
  from public.profiles p where p.id = p_student;
$$;

-- Giảng viên các lớp của em + mọi admin, mỗi người MỘT thông báo (gọi notify_class_staff
-- theo từng lớp sẽ báo trùng admin khi em học 2 lớp). Em không có lớp → chỉ admin.
create or replace function public.pl_notify_staff_of_student(
  p_student uuid, p_kind text, p_title text, p_body text, p_href text, p_except uuid default null)
returns void
language sql security definer
set search_path = public
as $$
  insert into public.notifications (user_id, kind, title, body, href)
  select distinct s.id, p_kind, p_title, coalesce(p_body, ''), coalesce(p_href, '')
  from (
    select ci.instructor_id as id
    from public.user_classes uc
    join public.class_instructors ci on ci.class_id = uc.class_id
    where p_student is not null and uc.user_id = p_student
    union
    select p.id from public.profiles p where p.role = 'admin'
  ) s
  where s.id is not null and (p_except is null or s.id <> p_except);
$$;

-- Tạo mã PH + apply_parent_link cho p_parent. Trả về id liên kết (raise nếu không nối được).
create or replace function public.pl_link_parent(p_parent uuid, p_student uuid, p_label text, p_by uuid)
returns uuid
language plpgsql security definer
set search_path = public
as $$
declare
  v_code text;
  v_link uuid;
begin
  insert into public.parent_links (code, student_id, label, created_by)
  values ('PH' || upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 6)),
          p_student, coalesce(p_label, ''), p_by)
  returning code into v_code;

  v_link := public.apply_parent_link(p_parent, v_code);
  if v_link is null then
    raise exception 'Không nối được tài khoản — nhờ thầy hỗ trợ.';
  end if;
  return v_link;
end;
$$;

revoke all on function public.pl_student_phone_match(uuid, text) from public, anon, authenticated;
revoke all on function public.pl_student_class_label(uuid) from public, anon, authenticated;
revoke all on function public.pl_notify_staff_of_student(uuid, text, text, text, text, uuid) from public, anon, authenticated;
revoke all on function public.pl_link_parent(uuid, uuid, text, uuid) from public, anon, authenticated;
-- pl_fold_name / pl_digits vô hại, để mặc định (public execute).

-- ---------- 2. Bảng ----------
create table if not exists public.parent_link_attempts (
  id bigint generated always as identity primary key,
  user_id uuid not null references public.profiles (id) on delete cascade,
  success boolean not null,
  created_at timestamptz not null default now()
);
create index if not exists parent_link_attempts_user_idx
  on public.parent_link_attempts (user_id, created_at desc);

alter table public.parent_link_attempts enable row level security;
revoke all on public.parent_link_attempts from anon, authenticated;

create table if not exists public.parent_link_requests (
  id bigint generated always as identity primary key,
  parent_id uuid not null references public.profiles (id) on delete cascade,
  child_name text not null,
  child_birth date,
  parent_phone text not null,
  note text,
  matched_student_id uuid references public.profiles (id) on delete set null,
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  reviewed_by uuid references public.profiles (id),
  reviewed_at timestamptz,
  created_at timestamptz not null default now()
);
create index if not exists parent_link_requests_parent_idx on public.parent_link_requests (parent_id, status);
create index if not exists parent_link_requests_pending_idx on public.parent_link_requests (created_at desc)
  where status = 'pending';
create index if not exists parent_link_requests_matched_idx on public.parent_link_requests (matched_student_id)
  where matched_student_id is not null;

alter table public.parent_link_requests enable row level security;
revoke all on public.parent_link_requests from anon, authenticated;
grant select on public.parent_link_requests to authenticated;

drop policy if exists "read parent link requests" on public.parent_link_requests;
create policy "read parent link requests" on public.parent_link_requests
  for select to authenticated
  using (
    parent_id = (select auth.uid())
    or public.is_admin()
    or (matched_student_id is not null and public.teaches_student(matched_student_id))
  );

-- ---------- 3. Phụ huynh tự nối ----------
create or replace function public.claim_parent_by_child_info(p_name text, p_birth date, p_phone text)
returns table (status text, student_name text, class_name text)
language plpgsql
security definer
set search_path = public
as $$
#variable_conflict use_column
declare
  v_user uuid := auth.uid();
  v_name text := public.pl_fold_name(p_name);
  v_phone text := public.pl_digits(p_phone);
  v_p9 text;
  v_ids uuid[];
  v_student uuid;
  v_student_name text;
  v_parent_name text;
begin
  if v_user is null then
    raise exception 'Phụ huynh cần đăng nhập trước khi nối với con.';
  end if;

  if (select count(*) from public.parent_link_attempts a
      where a.user_id = v_user and not a.success
        and a.created_at > now() - interval '24 hours') >= 5 then
    return query select 'locked'::text, null::text, null::text;
    return;
  end if;

  -- Thiếu dữ liệu → không thể khớp; không ghi lần thử (không dò được gì từ DB).
  if v_name = '' or p_birth is null or length(v_phone) < 9 then
    return query select 'no_match'::text, null::text, null::text;
    return;
  end if;
  v_p9 := right(v_phone, 9);

  select array_agg(p.id) into v_ids
  from public.profiles p
  where p.role <> 'admin'
    and p.id <> v_user
    and p.birth_date = p_birth
    and public.pl_fold_name(p.full_name) = v_name
    and public.pl_student_phone_match(p.id, v_p9);

  if coalesce(array_length(v_ids, 1), 0) <> 1 then
    insert into public.parent_link_attempts (user_id, success) values (v_user, false);
    return query select 'no_match'::text, null::text, null::text;
    return;
  end if;

  v_student := v_ids[1];
  select p.full_name into v_student_name from public.profiles p where p.id = v_student;

  if exists (select 1 from public.parent_links pl
             where pl.student_id = v_student and pl.parent_id = v_user and pl.claimed_at is not null) then
    return query select 'already'::text, v_student_name, public.pl_student_class_label(v_student);
    return;
  end if;

  perform public.pl_link_parent(v_user, v_student, 'Tự nối (tên + ngày sinh + SĐT)', v_user);
  insert into public.parent_link_attempts (user_id, success) values (v_user, true);

  select coalesce(nullif(btrim(p.full_name), ''), 'Phụ huynh') into v_parent_name
  from public.profiles p where p.id = v_user;

  perform public.notify_user(
    v_student, 'parent_linked', 'Phụ huynh vừa nối với tài khoản của em',
    v_parent_name || ' vừa nối tài khoản phụ huynh với em lúc '
      || to_char(now() at time zone 'Asia/Ho_Chi_Minh', 'HH24:MI DD/MM')
      || '. Nếu không phải bố mẹ em, báo thầy ngay.',
    '/tai-khoan');

  perform public.pl_notify_staff_of_student(
    v_student, 'parent_linked', 'Phụ huynh tự nối với con',
    v_parent_name || ' nối với ' || coalesce(v_student_name, 'học sinh') || ' bằng tên + ngày sinh + SĐT.',
    '/dashboard-thpt', null);

  return query select 'linked'::text, v_student_name, public.pl_student_class_label(v_student);
end;
$$;

revoke all on function public.claim_parent_by_child_info(text, date, text) from public, anon;
grant execute on function public.claim_parent_by_child_info(text, date, text) to authenticated;

-- ---------- 4. Gửi yêu cầu cho thầy duyệt ----------
create or replace function public.request_parent_link_review(
  p_name text, p_birth date, p_phone text, p_note text default null)
returns bigint
language plpgsql
security definer
set search_path = public
as $$
declare
  v_user uuid := auth.uid();
  v_name text := public.pl_fold_name(p_name);
  v_ids uuid[];
  v_matched uuid;
  v_id bigint;
  v_parent_name text;
begin
  if v_user is null then
    raise exception 'Phụ huynh cần đăng nhập trước khi gửi yêu cầu.';
  end if;
  if v_name = '' then
    raise exception 'Phụ huynh nhập họ tên của con giúp thầy.';
  end if;
  if btrim(coalesce(p_phone, '')) = '' then
    raise exception 'Phụ huynh nhập số điện thoại để thầy liên lạc khi cần.';
  end if;

  if (select count(*) from public.parent_link_requests r
      where r.parent_id = v_user and r.status = 'pending') >= 3 then
    raise exception 'Phụ huynh đã gửi 3 yêu cầu đang chờ thầy xem. Thầy xem xong sẽ báo lại, phụ huynh chưa cần gửi thêm.';
  end if;

  if p_birth is not null then
    select array_agg(p.id) into v_ids
    from public.profiles p
    where p.role <> 'admin' and p.id <> v_user
      and p.birth_date = p_birth
      and public.pl_fold_name(p.full_name) = v_name;
    if coalesce(array_length(v_ids, 1), 0) = 1 then
      v_matched := v_ids[1];
    end if;
  end if;

  if v_matched is null then
    select array_agg(p.id) into v_ids
    from public.profiles p
    where p.role <> 'admin' and p.id <> v_user
      and public.pl_fold_name(p.full_name) = v_name;
    if coalesce(array_length(v_ids, 1), 0) = 1 then
      v_matched := v_ids[1];
    end if;
  end if;

  insert into public.parent_link_requests (parent_id, child_name, child_birth, parent_phone, note, matched_student_id)
  values (v_user, btrim(p_name), p_birth, btrim(p_phone), nullif(btrim(coalesce(p_note, '')), ''), v_matched)
  returning id into v_id;

  select coalesce(nullif(btrim(p.full_name), ''), 'Phụ huynh') into v_parent_name
  from public.profiles p where p.id = v_user;

  perform public.pl_notify_staff_of_student(
    v_matched, 'parent_link_request', 'Phụ huynh xin nối với con',
    v_parent_name || ' xin nối với ' || btrim(p_name)
      || case when p_birth is not null then ' (sinh ' || to_char(p_birth, 'DD/MM/YYYY') || ')' else '' end
      || '.',
    '/dashboard-thpt', v_user);

  return v_id;
end;
$$;

revoke all on function public.request_parent_link_review(text, date, text, text) from public, anon;
grant execute on function public.request_parent_link_review(text, date, text, text) to authenticated;

-- ---------- 5. Thầy duyệt / từ chối ----------
create or replace function public.review_parent_link_request(p_id bigint, p_student uuid, p_approve boolean)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  v_user uuid := auth.uid();
  req public.parent_link_requests%rowtype;
  v_student_name text;
  v_parent_name text;
begin
  if v_user is null then
    raise exception 'Cần đăng nhập.';
  end if;

  select * into req from public.parent_link_requests r where r.id = p_id for update;
  if req.id is null then
    raise exception 'Không tìm thấy yêu cầu số %.', p_id;
  end if;
  if req.status <> 'pending' then
    raise exception 'Yêu cầu này đã được xử lý rồi.';
  end if;

  if coalesce(p_approve, false) then
    if p_student is null then
      raise exception 'Chọn học sinh trước khi duyệt.';
    end if;
    if not public.teaches_student(p_student) then   -- teaches_student đã gồm is_admin()
      raise exception 'Thầy/cô không phụ trách học sinh này.';
    end if;
    if p_student = req.parent_id then
      raise exception 'Không nối một tài khoản với chính nó.';
    end if;

    perform public.pl_link_parent(req.parent_id, p_student, 'Thầy duyệt yêu cầu #' || p_id, v_user);

    update public.parent_link_requests r
    set status = 'approved', reviewed_by = v_user, reviewed_at = now(), matched_student_id = p_student
    where r.id = p_id;

    select p.full_name into v_student_name from public.profiles p where p.id = p_student;
    select coalesce(nullif(btrim(p.full_name), ''), 'Phụ huynh') into v_parent_name
    from public.profiles p where p.id = req.parent_id;

    perform public.notify_user(
      req.parent_id, 'parent_link_approved', 'Thầy đã nối tài khoản với con',
      'Phụ huynh xem kết quả học tập của ' || coalesce(v_student_name, 'con') || ' tại trang Phụ huynh.',
      '/phu-huynh');

    perform public.notify_user(
      p_student, 'parent_linked', 'Phụ huynh vừa nối với tài khoản của em',
      v_parent_name || ' vừa nối tài khoản phụ huynh với em lúc '
        || to_char(now() at time zone 'Asia/Ho_Chi_Minh', 'HH24:MI DD/MM')
        || '. Nếu không phải bố mẹ em, báo thầy ngay.',
      '/tai-khoan');
  else
    if not (public.is_admin()
            or (req.matched_student_id is not null and public.teaches_student(req.matched_student_id))) then
      raise exception 'Chỉ thầy phụ trách học sinh này hoặc quản trị mới từ chối được.';
    end if;

    update public.parent_link_requests r
    set status = 'rejected', reviewed_by = v_user, reviewed_at = now()
    where r.id = p_id;

    perform public.notify_user(
      req.parent_id, 'parent_link_rejected', 'Chưa nối được với con',
      'Thầy chưa xác nhận được thông tin. Phụ huynh nhắn Zalo cho thầy để được hỗ trợ.',
      '/phu-huynh');
  end if;
end;
$$;

revoke all on function public.review_parent_link_request(bigint, uuid, boolean) from public, anon;
grant execute on function public.review_parent_link_request(bigint, uuid, boolean) to authenticated;

-- ---------- 6. Thầy tìm em để gắn vào yêu cầu ----------
create or replace function public.search_students_for_link(p_query text)
returns table (id uuid, full_name text, class_name text, birth_date date)
language plpgsql
stable
security definer
set search_path = public
as $$
#variable_conflict use_column
declare
  v_q text := public.pl_fold_name(p_query);
begin
  if auth.uid() is null or not (public.is_admin() or public.is_staff()) then
    raise exception 'Chỉ thầy/cô và trợ giảng dùng được chức năng này.';
  end if;
  if length(v_q) < 2 then
    return;
  end if;

  return query
  select p.id, p.full_name, public.pl_student_class_label(p.id), p.birth_date
  from public.profiles p
  where p.role not in ('admin', 'parent')
    and strpos(public.pl_fold_name(p.full_name), v_q) > 0
    and public.teaches_student(p.id)
  order by p.full_name, p.id
  limit 10;
end;
$$;

revoke all on function public.search_students_for_link(text) from public, anon;
grant execute on function public.search_students_for_link(text) to authenticated;

commit;

-- ============================================================================
-- KIỂM THỬ (chạy tay trong SQL editor sau migration; thay <...> bằng uuid thật; mọi
-- khối bọc begin/rollback nên không để lại dữ liệu).
--
-- Tên bỏ dấu:
--   select public.pl_fold_name('  Nguyễn  Văn ĐẠT ');           -- 'nguyen van dat'
--
-- Học sinh/phụ huynh A (<uid_hs>): chỉ thấy yêu cầu của mình, không thấy attempts.
--   begin; set local role authenticated;
--   select set_config('request.jwt.claims', '{"sub":"<uid_hs>","role":"authenticated"}', true);
--   select count(*) from public.parent_link_requests where parent_id <> '<uid_hs>';  -- 0
--   select * from public.parent_link_attempts;                                      -- lỗi permission denied
--   select * from public.search_students_for_link('nguyen');                         -- raise
--   select * from public.claim_parent_by_child_info('x', '2010-01-01', '0900000000'); -- no_match
--   rollback;
--
-- Trợ giảng (<uid_ta>, ta_assistants.active):
--   begin; set local role authenticated;
--   select set_config('request.jwt.claims', '{"sub":"<uid_ta>","role":"authenticated"}', true);
--   select count(*) from public.parent_link_requests;          -- = số yêu cầu có matched_student_id + của chính mình
--   select * from public.search_students_for_link('nguyen');   -- ≤10 dòng
--   select * from public.pl_student_phone_match('<uid_hs>', '912345678'); -- lỗi permission denied
--   rollback;
--
-- Admin (<uid_admin>):
--   begin; set local role authenticated;
--   select set_config('request.jwt.claims', '{"sub":"<uid_admin>","role":"authenticated"}', true);
--   select count(*) from public.parent_link_requests;          -- = tổng số dòng
--   select public.review_parent_link_request(<id>, null, false);  -- từ chối được kể cả chưa khớp em
--   rollback;
-- ============================================================================

-- ROLLBACK (chạy tay nếu cần gỡ; liên kết parent_links đã tạo bởi các hàm này vẫn giữ —
-- xoá theo label 'Tự nối (tên + ngày sinh + SĐT)' / 'Thầy duyệt yêu cầu #%' nếu muốn gỡ cả):
-- begin;
-- drop function if exists public.search_students_for_link(text);
-- drop function if exists public.review_parent_link_request(bigint, uuid, boolean);
-- drop function if exists public.request_parent_link_review(text, date, text, text);
-- drop function if exists public.claim_parent_by_child_info(text, date, text);
-- drop function if exists public.pl_link_parent(uuid, uuid, text, uuid);
-- drop function if exists public.pl_notify_staff_of_student(uuid, text, text, text, text, uuid);
-- drop function if exists public.pl_student_class_label(uuid);
-- drop function if exists public.pl_student_phone_match(uuid, text);
-- drop function if exists public.pl_digits(text);
-- drop function if exists public.pl_fold_name(text);
-- drop table if exists public.parent_link_requests;
-- drop table if exists public.parent_link_attempts;
-- commit;
