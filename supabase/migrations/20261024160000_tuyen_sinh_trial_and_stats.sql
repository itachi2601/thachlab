-- GĐ 0 chuẩn bị tuyển sinh riêng (T1b, 24/10/2026).
-- 1) trial_requests: phụ huynh đăng ký học thử ở /gioi-thieu; anon chỉ ghi qua submit_trial_request(jsonb)
--    (giới hạn 3 lần/SĐT/ngày + 20 lần/IP/giờ), thầy/trợ giảng đọc-sửa qua RLS; mỗi đơn mới báo chuông cho admin/instructor.
-- 2) public_stats_cache + refresh_public_stats() + get_public_stats(): số liệu ẩn danh cho trang giới thiệu,
--    tính 1 lần/ngày lúc 03:00 VN (pg_cron) nên trang công khai không quét bảng lớn.
-- 3) referrals: theo dõi nguồn giới thiệu (người giới thiệu → đơn học thử); thpt_courses.referral_discount_pct.
-- Chạy lúc nào cũng được (bảng mới, không khoá bảng lớn; lần refresh đầu quét exam_results 12 tháng — nên chạy sau 22h).
-- Rollback: perf/rollback/20261024160000_tuyen_sinh_trial_and_stats.down.sql
begin;

-- ───────── 1. trial_requests ─────────
create table if not exists public.trial_requests (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  parent_name text not null check (char_length(parent_name) between 2 and 80),
  phone text not null check (phone ~ '^0[0-9]{9}$'),
  grade smallint not null check (grade in (9, 10, 11, 12)),
  school text check (school is null or char_length(school) <= 120),
  preferred_evenings text[] not null default '{}',
  note text check (note is null or char_length(note) <= 500),
  source text not null default 'web' check (char_length(source) <= 60),
  status text not null default 'new'
    check (status in ('new', 'called', 'trial_scheduled', 'enrolled', 'declined')),
  handled_by uuid references public.profiles(id) on delete set null,
  handled_at timestamptz
);
create index if not exists trial_requests_status_created on public.trial_requests (status, created_at desc);
create index if not exists trial_requests_phone_created on public.trial_requests (phone, created_at desc);

alter table public.trial_requests enable row level security;
revoke all on public.trial_requests from anon, authenticated;
grant select, update on public.trial_requests to authenticated;

drop policy if exists trial_requests_staff_select on public.trial_requests;
create policy trial_requests_staff_select on public.trial_requests
  for select to authenticated using ((select public.is_staff()));
drop policy if exists trial_requests_staff_update on public.trial_requests;
create policy trial_requests_staff_update on public.trial_requests
  for update to authenticated using ((select public.is_staff())) with check ((select public.is_staff()));

-- Báo chuông cho thầy (admin, instructor) khi có đơn mới.
create or replace function public.trial_request_notify()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  insert into public.notifications (user_id, kind, title, body, href)
  select p.id, 'trial_request',
         'Đăng ký học thử mới: lớp ' || new.grade,
         new.parent_name || ' · ' || new.phone,
         '/dashboard-thpt'
    from public.profiles p where p.role in ('admin', 'instructor');
  return new;
end; $$;
drop trigger if exists trg_trial_request_notify on public.trial_requests;
create trigger trg_trial_request_notify after insert on public.trial_requests
  for each row execute function public.trial_request_notify();

-- anon gọi được; mọi kiểm tra nằm trong hàm. Trả {ok:true} hoặc raise với mã ngắn để form hiện câu thân thiện.
create or replace function public.submit_trial_request(p jsonb)
returns jsonb language plpgsql volatile security definer set search_path = public
as $$
declare
  v_name text := btrim(coalesce(p->>'parent_name', ''));
  v_phone text := regexp_replace(coalesce(p->>'phone', ''), '[\s.\-]', '', 'g');
  v_grade smallint;
  v_school text := nullif(btrim(coalesce(p->>'school', '')), '');
  v_note text := nullif(btrim(coalesce(p->>'note', '')), '');
  v_source text := coalesce(nullif(btrim(coalesce(p->>'source', '')), ''), 'web');
  v_evenings text[];
  v_id bigint;
begin
  if v_phone ~ '^\+84[0-9]{9}$' then v_phone := '0' || substr(v_phone, 4); end if;
  if char_length(v_name) < 2 or char_length(v_name) > 80 then raise exception 'invalid_name'; end if;
  if v_phone !~ '^0[0-9]{9}$' then raise exception 'invalid_phone'; end if;
  begin
    v_grade := (p->>'grade')::smallint;
  exception when others then
    raise exception 'invalid_grade';
  end;
  if v_grade not in (9, 10, 11, 12) then raise exception 'invalid_grade'; end if;
  v_school := left(v_school, 120);
  v_note := left(v_note, 500);
  v_source := left(v_source, 60);
  select coalesce(array_agg(e), '{}') into v_evenings
    from (select distinct e from jsonb_array_elements_text(coalesce(p->'preferred_evenings', '[]'::jsonb)) e
          where e in ('t2', 't3', 't4', 't5', 't6', 't7', 'cn')) s;

  if not public.rl_allow('trial:ip:' || public.rl_client_ip(), 20, interval '1 hour')
     or not public.rl_allow('trial:phone:' || v_phone, 3, interval '1 day') then
    raise exception 'rate_limited';
  end if;

  insert into public.trial_requests (parent_name, phone, grade, school, preferred_evenings, note, source)
  values (v_name, v_phone, v_grade, v_school, v_evenings, v_note, v_source)
  returning id into v_id;
  return jsonb_build_object('ok', true);
end; $$;
revoke all on function public.submit_trial_request(jsonb) from public;
grant execute on function public.submit_trial_request(jsonb) to anon, authenticated;

-- ───────── 2. Số liệu ẩn danh cho trang giới thiệu ─────────
create table if not exists public.public_stats_cache (
  id smallint primary key check (id = 1),
  computed_at timestamptz not null default now(),
  stats jsonb not null
);
alter table public.public_stats_cache enable row level security;
revoke all on public.public_stats_cache from anon, authenticated;

-- Định nghĩa các số (chỉ HS thật: role='student', is_test=false):
--  active_students_by_grade: số HS có user_classes.status='active' ở lớp tên chứa 10/11/12, và có ≥1 bài nộp 90 ngày qua.
--  attempts_90d: số bài đã nộp (exam_results) 90 ngày qua.
--  weekly_active_rate: tỉ lệ HS đang học (như trên, ghi danh bất kỳ lớp active) có ≥1 bài nộp trong 7 ngày qua.
--  avg_improvement: với HS có ≥2 bài nộp trong 12 tháng, trung bình (điểm bài gần nhất − điểm bài đầu tiên), thang 10;
--    null nếu < 10 HS đủ điều kiện (tránh số vô nghĩa/nhận diện được).
create or replace function public.refresh_public_stats()
returns void language plpgsql volatile security definer set search_path = public
as $$
declare v jsonb;
begin
  with stu as (
    select p.id from public.profiles p where p.role = 'student' and coalesce(p.is_test, false) = false
  ),
  enrolled as (
    select distinct uc.user_id, case
        when c.name ~ '12' then 12 when c.name ~ '11' then 11 when c.name ~ '10' then 10 end as grade
      from public.user_classes uc
      join public.classes c on c.id = uc.class_id
      join stu on stu.id = uc.user_id
     where uc.status = 'active'
  ),
  res as (
    select r.student_id, r.score, r.created_at
      from public.exam_results r join stu on stu.id = r.student_id
     where r.created_at > now() - interval '12 months' and r.score is not null
  ),
  active90 as (select distinct student_id from res where created_at > now() - interval '90 days'),
  active7 as (select distinct student_id from res where created_at > now() - interval '7 days'),
  firstlast as (
    select student_id,
           (array_agg(score order by created_at asc))[1] as s_first,
           (array_agg(score order by created_at desc))[1] as s_last,
           count(*) as n
      from res group by student_id having count(*) >= 2
  )
  select jsonb_build_object(
    'active_students_by_grade', jsonb_build_object(
      'g10', (select count(distinct e.user_id) from enrolled e join active90 a on a.student_id = e.user_id where e.grade = 10),
      'g11', (select count(distinct e.user_id) from enrolled e join active90 a on a.student_id = e.user_id where e.grade = 11),
      'g12', (select count(distinct e.user_id) from enrolled e join active90 a on a.student_id = e.user_id where e.grade = 12)),
    'attempts_90d', (select count(*) from res where created_at > now() - interval '90 days'),
    'weekly_active_rate', (
      select case when count(distinct e.user_id) = 0 then null
             else round(100.0 * count(distinct a.student_id) / count(distinct e.user_id)) end
        from enrolled e left join active7 a on a.student_id = e.user_id),
    'avg_improvement', (
      select case when count(*) < 10 then null else round(avg(s_last - s_first), 1) end from firstlast)
  ) into v;

  insert into public.public_stats_cache (id, computed_at, stats) values (1, now(), v)
  on conflict (id) do update set computed_at = excluded.computed_at, stats = excluded.stats;
end; $$;
revoke all on function public.refresh_public_stats() from public;

-- Trang công khai đọc 1 dòng đã tính sẵn; không id/tên nào.
create or replace function public.get_public_stats()
returns jsonb language sql stable security definer set search_path = public
as $$
  select jsonb_build_object('computed_at', computed_at) || stats from public.public_stats_cache where id = 1;
$$;
revoke all on function public.get_public_stats() from public;
grant execute on function public.get_public_stats() to anon, authenticated;

select public.refresh_public_stats();

do $$
begin
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    -- 03:00 giờ VN = 20:00 UTC
    perform cron.schedule('public-stats-refresh', '0 20 * * *', 'select public.refresh_public_stats();');
  end if;
end $$;

-- ───────── 3. Giới thiệu bạn bè ─────────
alter table public.thpt_courses add column if not exists referral_discount_pct int not null default 0
  check (referral_discount_pct between 0 and 50);

create table if not exists public.referrals (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  referrer_user_id uuid references public.profiles(id) on delete set null,
  referred_request_id bigint references public.trial_requests(id) on delete cascade,
  status text not null default 'pending' check (status in ('pending', 'enrolled', 'void'))
);
create index if not exists referrals_request on public.referrals (referred_request_id);
alter table public.referrals enable row level security;
revoke all on public.referrals from anon, authenticated;
grant select, update on public.referrals to authenticated;
drop policy if exists referrals_staff_all on public.referrals;
create policy referrals_staff_all on public.referrals
  for all to authenticated using ((select public.is_staff())) with check ((select public.is_staff()));

commit;

-- ROLLBACK (đã đặt ở perf/rollback/20261024160000_tuyen_sinh_trial_and_stats.down.sql)
