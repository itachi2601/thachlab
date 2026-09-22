-- ============================================================
-- Thông báo tự động trong web (chuông trên thanh điều hướng + trang /thong-bao)
--
-- Mỗi dòng notifications là MỘT thông báo cho MỘT người. Mọi thông báo đều do trigger
-- trong DB sinh ra (security definer) — client chỉ đọc và đánh dấu đã đọc, không tự tạo.
--
-- Sự kiện -> ai nhận:
--   · Đăng ký khoá mới (thpt_registrations insert)      -> giáo viên phụ trách khối + admin
--   · Duyệt / bù bài / từ chối (status đổi)             -> em + người đăng ký hộ + phụ huynh đã nối;
--                                                          bù xong (catchup -> active) báo cả giáo viên
--   · Buổi phụ đạo gạch được một bài đang bù            -> em + phụ huynh
--   · Trợ giảng mở ca có bài em đang cần bù             -> em + phụ huynh
--   · Phụ huynh nối tài khoản với con                    -> giáo viên phụ trách khối
--   · Gắn tài khoản cho đăng ký "con chưa có tài khoản" -> phụ huynh đã đăng ký hộ
--
-- Chạy SAU: supabase-migration-bu-bai.sql. Idempotent — chạy lại được.
-- ============================================================

-- ---------- 1. Bảng ----------
create table if not exists public.notifications (
  id bigint generated always as identity primary key,
  user_id uuid not null references public.profiles (id) on delete cascade,
  kind text not null,
  title text not null,
  body text not null default '',
  -- đường dẫn nội bộ để bấm vào là tới đúng chỗ ("/dashboard-thpt", "/phu-huynh"…)
  href text not null default '',
  created_at timestamptz not null default now(),
  read_at timestamptz
);
create index if not exists notifications_user_idx on public.notifications (user_id, created_at desc);
create index if not exists notifications_unread_idx on public.notifications (user_id) where read_at is null;

alter table public.notifications enable row level security;

drop policy if exists "read own notifications" on public.notifications;
create policy "read own notifications" on public.notifications
  for select to authenticated using (user_id = auth.uid());

-- Chỉ được đánh dấu đã đọc dòng của mình (không đổi nội dung — client chỉ update read_at).
drop policy if exists "mark own notifications read" on public.notifications;
create policy "mark own notifications read" on public.notifications
  for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists "delete own notifications" on public.notifications;
create policy "delete own notifications" on public.notifications
  for delete to authenticated using (user_id = auth.uid());

-- ---------- 2. Hàm gửi ----------
create or replace function public.notify_user(p_user uuid, p_kind text, p_title text, p_body text default '', p_href text default '')
returns void
language sql security definer set search_path = public
as $$
  insert into public.notifications (user_id, kind, title, body, href)
  select p_user, p_kind, p_title, coalesce(p_body, ''), coalesce(p_href, '')
  where p_user is not null;
$$;
revoke all on function public.notify_user(uuid, text, text, text, text) from public, anon, authenticated;

-- Giáo viên được phân công khối + admin. p_except: người gây ra sự kiện, khỏi tự báo mình.
create or replace function public.notify_class_staff(p_class_id bigint, p_kind text, p_title text, p_body text default '', p_href text default '', p_except uuid default null)
returns void
language sql security definer set search_path = public
as $$
  insert into public.notifications (user_id, kind, title, body, href)
  select distinct u.id, p_kind, p_title, coalesce(p_body, ''), coalesce(p_href, '')
  from (
    select ci.instructor_id as id from public.class_instructors ci where ci.class_id = p_class_id
    union
    select p.id from public.profiles p where p.role = 'admin'
  ) u
  where u.id is not null and (p_except is null or u.id <> p_except);
$$;
revoke all on function public.notify_class_staff(bigint, text, text, text, text, uuid) from public, anon, authenticated;

-- Em + phụ huynh đã nối (+ người đăng ký hộ nếu truyền).
create or replace function public.notify_student_side(p_student uuid, p_kind text, p_title text, p_body text default '', p_href_student text default '', p_href_parent text default '', p_extra uuid default null)
returns void
language sql security definer set search_path = public
as $$
  insert into public.notifications (user_id, kind, title, body, href)
  select distinct u.id, p_kind, p_title, coalesce(p_body, ''),
         case when u.id = p_student then coalesce(p_href_student, '') else coalesce(p_href_parent, '') end
  from (
    select p_student as id
    union
    select pl.parent_id from public.parent_links pl where pl.student_id = p_student and pl.claimed_at is not null
    union
    select p_extra
  ) u
  where u.id is not null;
$$;
revoke all on function public.notify_student_side(uuid, text, text, text, text, text, uuid) from public, anon, authenticated;

-- Tên hiển thị của một đăng ký (em có tài khoản -> tên hồ sơ, không thì tên phụ huynh khai).
create or replace function public.thpt_registration_display_name(p_reg public.thpt_registrations)
returns text
language sql stable security definer set search_path = public
as $$
  select coalesce(nullif((select full_name from public.profiles where id = p_reg.student_id), ''), nullif(p_reg.child_name, ''), 'Học sinh');
$$;

-- ---------- 3. Ghi danh ----------
create or replace function public.trg_notify_registration()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  c public.thpt_courses%rowtype;
  v_name text;
  v_class text;
begin
  select * into c from public.thpt_courses where id = new.course_id;
  select name into v_class from public.classes where id = c.class_id;
  v_name := public.thpt_registration_display_name(new);

  if tg_op = 'INSERT' then
    perform public.notify_class_staff(
      c.class_id, 'registration_new',
      'Đăng ký mới: ' || v_name || ' · ' || c.name,
      case when new.joined_late then 'Đăng ký sau khai giảng — cần xếp bù bài trước khi vào lớp.' else 'Đang chờ duyệt trong tab Ghi danh.' end
        || case when new.student_id is null then ' Con chưa có tài khoản, cần gắn tài khoản trước.' else '' end,
      '/dashboard-thpt', new.registered_by
    );
    return new;
  end if;

  -- UPDATE: chỉ báo khi trạng thái đổi
  if new.status is distinct from old.status then
    if new.status = 'active' and old.status = 'catchup' then
      perform public.notify_student_side(
        new.student_id, 'catchup_done',
        'Đã bù xong bài — chính thức vào lớp ' || c.name,
        'Từ giờ học theo lịch lớp bình thường.',
        '/tai-khoan', '/phu-huynh', new.registered_by
      );
      perform public.notify_class_staff(
        c.class_id, 'catchup_done',
        v_name || ' đã bù xong bài · ' || c.name,
        'Em chuyển sang "Đã vào lớp".', '/dashboard-thpt'
      );
    elsif new.status = 'active' then
      perform public.notify_student_side(
        new.student_id, 'registration_approved',
        'Đã được duyệt vào lớp ' || c.name,
        'Vào Tài khoản để xem bài học và lịch lớp.' || case when new.payment_status = 'unpaid' and c.fee_note <> '' then ' ' || c.fee_note else '' end,
        '/tai-khoan', '/phu-huynh', new.registered_by
      );
    elsif new.status = 'catchup' then
      perform public.notify_student_side(
        new.student_id, 'registration_catchup',
        'Đã được duyệt · cần bù ' || cardinality(new.catchup_topic_ids) || ' bài trước khi vào lớp ' || c.name,
        'Mở mục "Bù bài" để đăng ký ca phụ đạo — bài lớp vừa học trước.',
        '/tai-khoan', '/phu-huynh', new.registered_by
      );
    elsif new.status = 'rejected' then
      perform public.notify_student_side(
        new.student_id, 'registration_rejected',
        'Đăng ký vào ' || c.name || ' chưa được duyệt',
        'Liên hệ giáo viên để biết lý do hoặc chọn lớp khác.',
        '/khoa-hoc', '/phu-huynh', new.registered_by
      );
    end if;
  end if;

  -- Gắn tài khoản cho đăng ký "con chưa có tài khoản" -> báo phụ huynh đã đăng ký hộ.
  if old.student_id is null and new.student_id is not null and new.registered_by is not null then
    perform public.notify_user(
      new.registered_by, 'registration_attached',
      'Đã tạo tài khoản cho ' || v_name,
      'Nhờ giáo viên gửi mã phụ huynh để nối tài khoản và theo dõi kết quả của con.',
      '/phu-huynh'
    );
  end if;

  -- Buổi phụ đạo gạch được bài (danh sách bù ngắn lại, vẫn đang catchup).
  -- Hết danh sách thì trigger bù bài chuyển sang active ngay sau đó -> đã có thông báo "bù xong".
  if new.status = 'catchup' and old.status = 'catchup'
     and cardinality(new.catchup_topic_ids) < cardinality(old.catchup_topic_ids)
     and cardinality(new.catchup_topic_ids) > 0 then
    perform public.notify_student_side(
      new.student_id, 'catchup_progress',
      'Đã bù thêm bài · còn ' || cardinality(new.catchup_topic_ids) || ' bài',
      case when cardinality(new.catchup_topic_ids) > 0
           then 'Bài kế tiếp: ' || coalesce((select name from public.question_topics where id = new.catchup_topic_ids[1]), '')
           else '' end,
      '/tai-khoan', '/phu-huynh', new.registered_by
    );
  end if;

  return new;
end;
$$;

drop trigger if exists trg_notify_registration on public.thpt_registrations;
create trigger trg_notify_registration
  after insert or update of status, student_id, catchup_topic_ids on public.thpt_registrations
  for each row execute function public.trg_notify_registration();

-- ---------- 4. Trợ giảng mở ca có bài em đang cần bù ----------
create or replace function public.trg_notify_slot_for_catchup()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  r record;
  v_date text;
begin
  if new.status <> 'open' or cardinality(new.topic_ids) = 0 then return new; end if;
  v_date := to_char(new.work_date, 'DD/MM') || ' ' || to_char(new.start_time, 'HH24:MI');

  for r in
    select reg.student_id, reg.registered_by, reg.catchup_topic_ids[1] as next_topic
    from public.thpt_registrations reg
    join public.thpt_courses c on c.id = reg.course_id
    where reg.status = 'catchup'
      and reg.student_id is not null
      and c.class_id = new.class_id
      and reg.catchup_topic_ids && new.topic_ids
  loop
    perform public.notify_student_side(
      r.student_id, 'slot_for_catchup',
      'Có ca phụ đạo ' || v_date || ' dạy bài ' || case when r.next_topic = any (new.topic_ids) then 'kế tiếp' else 'trong danh sách bù' end,
      'Vào mục "Bù bài" để đăng ký trước khi hết chỗ.',
      '/tai-khoan', '/phu-huynh', r.registered_by
    );
  end loop;
  return new;
end;
$$;

drop trigger if exists trg_notify_slot_for_catchup on public.tutoring_slots;
create trigger trg_notify_slot_for_catchup
  after insert on public.tutoring_slots
  for each row execute function public.trg_notify_slot_for_catchup();

-- ---------- 5. Phụ huynh nối tài khoản ----------
create or replace function public.trg_notify_parent_linked()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  v_student text;
  v_parent text;
  r record;
begin
  if new.claimed_at is null or old.claimed_at is not null then return new; end if;
  select full_name into v_student from public.profiles where id = new.student_id;
  select full_name into v_parent from public.profiles where id = new.parent_id;
  for r in select distinct uc.class_id from public.user_classes uc where uc.user_id = new.student_id loop
    perform public.notify_class_staff(
      r.class_id, 'parent_linked',
      'Phụ huynh đã nối với ' || coalesce(v_student, 'học sinh'),
      coalesce(nullif(v_parent, ''), 'Phụ huynh') || ' giờ xem được kết quả học tập của em.',
      '/dashboard-thpt'
    );
  end loop;
  perform public.notify_user(
    new.parent_id, 'parent_linked',
    'Đã nối với ' || coalesce(v_student, 'con'),
    'Mở "Kết quả của con" để xem điểm, chủ đề còn yếu và lịch phụ đạo.',
    '/phu-huynh'
  );
  return new;
end;
$$;

drop trigger if exists trg_notify_parent_linked on public.parent_links;
create trigger trg_notify_parent_linked
  after update of claimed_at on public.parent_links
  for each row execute function public.trg_notify_parent_linked();

-- ---------- 6. Đếm chưa đọc nhanh cho chuông ----------
create or replace function public.unread_notification_count()
returns int
language sql stable security definer set search_path = public
as $$
  select count(*)::int from public.notifications where user_id = auth.uid() and read_at is null;
$$;
grant execute on function public.unread_notification_count() to authenticated;
