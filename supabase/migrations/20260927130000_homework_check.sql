-- ============================================================
-- Trợ giảng/giáo viên chấm % học sinh đã làm bài tập về nhà ngay trên lớp
-- + chuông thông báo khi đăng BTVN mới
-- Nguồn: docs/supabase-migration-homework-check.sql — xem file đó để biết lý do thiết kế.
-- Idempotent — chạy lại được.
-- ============================================================

-- ---------- 1. Cho phép nguồn RP mới 'homework_check' ----------
alter table public.rank_rp_awards drop constraint if exists rank_rp_awards_source_kind_check;
alter table public.rank_rp_awards add constraint rank_rp_awards_source_kind_check
  check (source_kind in ('practice', 'fix', 'weekly_goal', 'daily_streak', 'manual', 'homework_check'));

-- ---------- 2. Bảng ghi % đã chấm cho từng em ----------
create table if not exists public.class_homework_checks (
  id bigint generated always as identity primary key,
  announcement_id bigint not null references public.class_announcements (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  percent int not null check (percent between 0 and 100),
  checked_by uuid not null references public.profiles (id) on delete cascade,
  checked_at timestamptz not null default now(),
  unique (announcement_id, student_id)
);
create index if not exists class_homework_checks_announcement_idx
  on public.class_homework_checks (announcement_id);

alter table public.class_homework_checks enable row level security;

drop policy if exists "staff read homework checks" on public.class_homework_checks;
create policy "staff read homework checks" on public.class_homework_checks
  for select to authenticated
  using (exists (
    select 1 from public.class_announcements a
    where a.id = class_homework_checks.announcement_id
      and (public.manages_class(a.class_id) or public.assists_class(a.class_id) or public.is_admin())
  ));

drop policy if exists "student read own homework check" on public.class_homework_checks;
create policy "student read own homework check" on public.class_homework_checks
  for select to authenticated
  using (student_id = auth.uid() or public.is_parent_of(student_id));

-- ---------- 3. RPC chấm — ghi % + cộng RP nếu lớp đang có mùa rank mở ----------
create or replace function public.homework_check_set(
  p_announcement_id bigint, p_student_id uuid, p_percent int, p_season bigint default null
)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_class_id bigint;
  v_class_name text;
  v_awarded int;
begin
  select class_id into v_class_id from public.class_announcements
  where id = p_announcement_id and kind = 'homework';
  if v_class_id is null then
    raise exception 'Không tìm thấy bài tập về nhà này';
  end if;
  if not (public.manages_class(v_class_id) or public.assists_class(v_class_id) or public.is_admin()) then
    raise exception 'Không có quyền chấm bài tập của lớp này';
  end if;
  if p_percent < 0 or p_percent > 100 then
    raise exception 'Phần trăm phải từ 0 đến 100';
  end if;

  insert into public.class_homework_checks (announcement_id, student_id, percent, checked_by, checked_at)
  values (p_announcement_id, p_student_id, p_percent, auth.uid(), now())
  on conflict (announcement_id, student_id) do update
    set percent = excluded.percent, checked_by = excluded.checked_by, checked_at = now();

  v_awarded := round(10 * p_percent / 100.0)::int;
  if p_season is not null then
    perform public.rank_ensure_member(p_season, p_student_id);
    perform public.rank_award(
      p_season, p_student_id, 'homework_check', p_announcement_id::text, v_awarded,
      'Chấm BTVN trên lớp: ' || p_percent || '% đã làm'
    );
    perform public.rank_eval_gates(p_season, p_student_id);
    perform public.rank_refresh_student(p_season, p_student_id);
  end if;

  select name into v_class_name from public.classes where id = v_class_id;
  perform public.notify_student_side(
    p_student_id, 'homework_checked',
    'Đã chấm bài tập về nhà · ' || coalesce(v_class_name, 'lớp'),
    'Trợ giảng ghi nhận em đã làm ' || p_percent || '% bài tập về nhà.'
      || case when p_season is not null and v_awarded > 0 then ' +' || v_awarded || ' RP.' else '' end,
    '/tai-khoan', '/phu-huynh'
  );
end;
$$;
grant execute on function public.homework_check_set(bigint, uuid, int, bigint) to authenticated;

-- ---------- 4. Thông báo khi đăng BTVN mới — cả lớp + phụ huynh đã nối ----------
create or replace function public.trg_notify_homework_announcement()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  v_class_name text;
  r record;
begin
  if new.kind <> 'homework' then return new; end if;
  select name into v_class_name from public.classes where id = new.class_id;
  for r in
    select uc.user_id as student_id
    from public.user_classes uc
    where uc.class_id = new.class_id and uc.status = 'active'
  loop
    perform public.notify_student_side(
      r.student_id, 'homework_posted',
      'Bài tập về nhà mới · ' || coalesce(v_class_name, 'lớp'),
      left(new.body, 140),
      '/tai-khoan', '/phu-huynh'
    );
  end loop;
  return new;
end;
$$;

drop trigger if exists trg_notify_homework_announcement on public.class_announcements;
create trigger trg_notify_homework_announcement
  after insert on public.class_announcements
  for each row execute function public.trg_notify_homework_announcement();
