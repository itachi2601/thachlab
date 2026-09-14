-- ============================================================
-- "Trợ giảng" trở thành một vai trò thật của tài khoản
--
-- Trước đây trợ giảng chỉ là một dòng trong bảng lương public.ta_assistants, còn
-- profiles.role vẫn nằm nguyên ở 'student'. Hậu quả: trợ giảng lẫn vào mọi danh sách
-- học sinh, không có chỗ nào nhìn ra ai là ai, và cách duy nhất để cấp quyền là gửi mã
-- mời. Từ đây role là nguồn sự thật duy nhất, đổi được ngay trong trang quản trị.
--
-- Idempotent — chạy lại được. Chạy trong Supabase → SQL Editor.
-- ============================================================

-- ---------- 1. Vai trò mới ----------
alter table public.profiles drop constraint if exists profiles_role_check;
alter table public.profiles add constraint profiles_role_check
  check (role in ('student', 'admin', 'instructor', 'tro_giang'));

-- Bảo hiểm cho DB chưa chạy 2 migration cột này (hàm tìm tài khoản bên dưới cần chúng).
alter table public.profiles add column if not exists student_code text;
alter table public.profiles add column if not exists track text;

-- ---------- 2. Dọn dữ liệu đang lộn xộn ----------
-- Ai đang có hồ sơ trợ giảng còn hoạt động mà vẫn bị tính là học sinh -> trả về đúng vai trò.
-- Chỉ đụng vào 'student': không hạ quyền admin/giảng viên đang kiêm trợ giảng.
update public.profiles p
set role = 'tro_giang'
where p.role = 'student'
  and exists (select 1 from public.ta_assistants a where a.user_id = p.id and a.active);

-- ---------- 3. Hai lối vào luôn khớp nhau ----------
-- Nhận lời mời (apply_staff_invite chỉ ghi ta_assistants) cũng phải nâng vai trò. Làm bằng
-- trigger để khỏi chép lại nguyên hàm apply_staff_invite ở hai nơi rồi lệch nhau về sau.
create or replace function public.trg_ta_assistant_role()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if new.active then
    update public.profiles set role = 'tro_giang'
    where id = new.user_id and role = 'student';
  end if;
  return new;
end;
$$;

drop trigger if exists ta_assistants_sync_role on public.ta_assistants;
create trigger ta_assistants_sync_role
  after insert or update of active on public.ta_assistants
  for each row execute function public.trg_ta_assistant_role();

-- ---------- 4. Tìm tài khoản (kèm email) cho trang quản trị ----------
-- profiles không lưu email, mà email mới là thứ phân biệt được hai người trùng tên.
-- auth.users thì client không đọc thẳng được -> đi qua hàm security definer, chặn sẵn
-- người không phải quản trị.
create or replace function public.admin_search_accounts(p_query text default '', p_role text default null)
returns table (
  id uuid,
  full_name text,
  class_name text,
  student_code text,
  role text,
  admin_area text,
  track text,
  email text,
  ta_tier text,
  ta_active boolean
)
language plpgsql
security definer
set search_path = public
as $$
declare
  v_query text := coalesce(trim(p_query), '');
begin
  if not public.is_admin() then
    raise exception 'Chỉ quản trị viên mới xem được danh sách tài khoản.';
  end if;

  return query
  select p.id, p.full_name, p.class_name, p.student_code, p.role, p.admin_area, p.track,
         u.email::text, a.tier, a.active
  from public.profiles p
  join auth.users u on u.id = p.id
  left join public.ta_assistants a on a.user_id = p.id
  where (
      v_query = ''
      or p.full_name ilike '%' || v_query || '%'
      or p.class_name ilike '%' || v_query || '%'
      or coalesce(p.student_code, '') ilike '%' || v_query || '%'
      or u.email ilike '%' || v_query || '%'
    )
    and (coalesce(trim(p_role), '') = '' or p.role = trim(p_role))
  order by p.full_name
  limit 50;
end;
$$;

grant execute on function public.admin_search_accounts(text, text) to authenticated;

-- ---------- 5. Đổi vai trò một tài khoản ----------
-- Một cửa duy nhất: đặt role, dọn những thứ đi kèm vai trò cũ, và tạo/tắt hồ sơ trợ giảng.
-- Hồ sơ lương KHÔNG bị xoá khi thôi làm trợ giảng (ta_sessions tham chiếu tới nó và còn
-- là lịch sử trả lương) — chỉ tắt active.
create or replace function public.admin_set_account_role(p_user_id uuid, p_role text, p_tier text default null)
returns text
language plpgsql
security definer
set search_path = public
as $$
declare
  v_full_name text;
  v_email text;
  v_short_name text;
begin
  if not public.is_admin() then
    raise exception 'Chỉ quản trị viên mới đổi được vai trò.';
  end if;

  if p_role not in ('student', 'tro_giang', 'instructor') then
    raise exception 'Vai trò % không hợp lệ.', p_role;
  end if;

  -- Tự bấm nhầm vào chính mình là mất quyền quản trị, không có đường quay lại từ giao diện.
  if p_user_id = auth.uid() then
    raise exception 'Không đổi vai trò của chính mình được — nhờ một quản trị viên khác.';
  end if;

  if exists (select 1 from public.profiles where id = p_user_id and role = 'admin') then
    raise exception 'Đây là tài khoản quản trị. Hạ quyền bằng SQL, không làm từ giao diện.';
  end if;

  select p.full_name, u.email into v_full_name, v_email
  from public.profiles p join auth.users u on u.id = p.id
  where p.id = p_user_id;

  if not found then
    raise exception 'Không tìm thấy tài khoản này.';
  end if;

  update public.profiles
  set role = p_role,
      -- Thôi làm giảng viên thì mất luôn quyền vào khu vực quản trị.
      admin_area = case when p_role = 'instructor' then admin_area else null end
  where id = p_user_id;

  if p_role = 'tro_giang' then
    -- Tên hiển thị ngắn = từ cuối của họ tên ("Ngô Diệu Thạch" -> "Thạch").
    v_short_name := nullif(regexp_replace(trim(coalesce(v_full_name, '')), '^.*\s', ''), '');

    insert into public.ta_assistants (user_id, full_name, short_name, tier)
    values (
      p_user_id,
      coalesce(nullif(v_full_name, ''), v_email),
      coalesce(v_short_name, nullif(v_full_name, ''), v_email),
      coalesce(nullif(trim(coalesce(p_tier, '')), ''), 'B1')
    )
    on conflict (user_id) do update set
      tier = coalesce(nullif(trim(coalesce(p_tier, '')), ''), public.ta_assistants.tier),
      active = true;
  else
    update public.ta_assistants set active = false where user_id = p_user_id;
  end if;

  return p_role;
end;
$$;

grant execute on function public.admin_set_account_role(uuid, text, text) to authenticated;
