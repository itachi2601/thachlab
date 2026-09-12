-- ============================================================
-- Module Quản lý trợ giảng (chấm công + đánh giá hiệu suất)
-- App export tĩnh, không có API route/server action — mọi truy cập đi qua
-- @supabase/supabase-js phía client, bảo mật hoàn toàn bằng RLS bên dưới.
-- "Giáo viên" = public.is_admin() (role = 'admin' trong profiles), tái dùng
-- hàm đã có ở docs/supabase-schema.sql thay vì phát minh custom claim mới.
-- ============================================================

-- ---------- 1. ta_assistants ----------
create table if not exists public.ta_assistants (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null unique references auth.users(id) on delete cascade,
  full_name text not null,
  short_name text not null,
  tier text not null check (tier in ('B1', 'B2', 'B3')),
  retained_rate integer,
  bank_name text,
  bank_account text,
  active boolean not null default true,
  started_at date not null default current_date,
  created_at timestamptz not null default now()
);

-- ---------- 2. ta_rates ----------
-- Đơn giá theo bậc, có hiệu lực theo tháng — đổi giá sau này không tính lại quá khứ.
create table if not exists public.ta_rates (
  id uuid primary key default gen_random_uuid(),
  tier text not null check (tier in ('B1', 'B2', 'B3')),
  effective_from date not null,
  base_rate integer not null,
  unique (tier, effective_from)
);

insert into public.ta_rates (tier, effective_from, base_rate) values
  ('B1', '2026-10-01', 40000),
  ('B2', '2026-10-01', 50000),
  ('B3', '2026-10-01', 60000)
on conflict (tier, effective_from) do update set base_rate = excluded.base_rate;

-- ---------- 3. ta_sessions ----------
-- session_type 'video' (mục 8): buổi sản xuất video TikTok — không có giờ bắt đầu/kết thúc,
-- không cộng giờ quy đổi, không cộng giờ tích lũy, không tính vào điểm hiệu suất mục 4.
create table if not exists public.ta_sessions (
  id uuid primary key default gen_random_uuid(),
  assistant_id uuid not null references public.ta_assistants(id) on delete cascade,
  work_date date not null,
  session_type text not null check (session_type in ('lop', 'phudao', 'chambai', 'hanhchinh', 'video')),
  class_label text,
  start_time time,
  end_time time,
  hours numeric generated always as (extract(epoch from (end_time - start_time)) / 3600.0) stored,
  student_touches integer,
  touch_names text[] not null default '{}',
  error_note text,
  error_note_at timestamptz,
  homework_given text,
  student_recap_ok boolean,
  papers_graded integer,
  video_url text,
  video_tier text check (video_tier in ('don_gian', 'dung_ky')),
  published_at timestamptz,
  topic_source_id uuid references public.ta_sessions(id) on delete set null,
  note text,
  status text not null default 'submitted' check (status in ('submitted', 'approved', 'rejected')),
  reject_reason text,
  created_at timestamptz not null default now(),
  approved_at timestamptz,
  check (session_type = 'video' or (start_time is not null and end_time is not null and end_time > start_time)),
  check (session_type <> 'lop' or (error_note is not null and length(trim(error_note)) > 0)),
  check (session_type <> 'video' or (start_time is null and end_time is null)),
  check (session_type <> 'video' or video_tier in ('don_gian', 'dung_ky')),
  check (session_type = 'video' or topic_source_id is null)
);

create index if not exists ta_sessions_assistant_idx on public.ta_sessions(assistant_id, work_date desc);
create index if not exists ta_sessions_status_idx on public.ta_sessions(status);

-- Ghi error_note_at bằng giờ server tại lúc lưu (không tin giờ máy client) —
-- dùng để đối chiếu "nộp phiếu lỗi trong ngày" ở ta_monthly_score.
create or replace function public.trg_ta_sessions_error_note_at()
returns trigger
language plpgsql
as $$
begin
  if new.session_type = 'lop' and new.error_note is not null and new.error_note_at is null then
    new.error_note_at := now();
  end if;
  return new;
end;
$$;

drop trigger if exists trg_ta_sessions_error_note_at on public.ta_sessions;
create trigger trg_ta_sessions_error_note_at
  before insert on public.ta_sessions
  for each row execute function public.trg_ta_sessions_error_note_at();

-- topic_source_id (mục 8.4) phải trỏ tới đúng 1 buổi 'lop' của CHÍNH trợ giảng đó —
-- tránh lấy đề tài từ lỗi của bạn khác hoặc từ 1 buổi không phải lên lớp.
create or replace function public.trg_ta_sessions_video_topic_check()
returns trigger
language plpgsql
as $$
declare
  v_type text;
  v_assistant uuid;
begin
  if new.session_type = 'video' and new.topic_source_id is not null then
    select session_type, assistant_id into v_type, v_assistant
    from public.ta_sessions where id = new.topic_source_id;

    if v_type is null then
      raise exception 'Đề tài gốc không tồn tại.';
    elsif v_type <> 'lop' then
      raise exception 'Đề tài video phải trỏ tới một buổi lên lớp (session_type = lop).';
    elsif v_assistant <> new.assistant_id then
      raise exception 'Chỉ được lấy đề tài từ chính buổi lỗi của bạn.';
    end if;
  end if;
  return new;
end;
$$;

drop trigger if exists trg_ta_sessions_video_topic_check on public.ta_sessions;
create trigger trg_ta_sessions_video_topic_check
  before insert or update on public.ta_sessions
  for each row execute function public.trg_ta_sessions_video_topic_check();

-- ---------- 4. ta_flags ----------
create table if not exists public.ta_flags (
  id uuid primary key default gen_random_uuid(),
  assistant_id uuid not null references public.ta_assistants(id) on delete cascade,
  flag_date date not null default current_date,
  note text,
  created_at timestamptz not null default now()
);

create index if not exists ta_flags_assistant_idx on public.ta_flags(assistant_id, flag_date desc);

-- ---------- 5. Hàm quy đổi giờ 1 buổi (dùng chung, tránh lặp công thức) ----------
-- 'video' luôn = 0: mảng video trả riêng theo ta_video_ledger (mục 8), không cộng giờ
-- quy đổi, không cộng giờ tích lũy, không vào lương/điểm ở ta_monthly_score.
create or replace function public.ta_converted_hours(p_session_type text, p_hours numeric)
returns numeric
language sql
immutable
as $$
  select case p_session_type
    when 'lop' then p_hours * 1.00
    when 'phudao' then p_hours * 1.25
    when 'chambai' then 0
    when 'hanhchinh' then p_hours * 1.00
    when 'video' then 0
    else 0
  end;
$$;

-- ---------- 6. Xác định assistant_id của người đang đăng nhập ----------
create or replace function public.ta_current_assistant_id()
returns uuid
language sql
security definer
stable
set search_path = public
as $$
  select id from public.ta_assistants where user_id = auth.uid();
$$;

grant execute on function public.ta_converted_hours(text, numeric) to authenticated;
grant execute on function public.ta_current_assistant_id() to authenticated;

-- ---------- 7. Giờ tích lũy trọn đời (xét lên bậc) ----------
-- Chỉ tính buổi 'lop' và 'phudao' đã duyệt, loại 'hanhchinh' và 'chambai'.
-- SECURITY DEFINER nên phải tự kiểm tra quyền: chỉ chính trợ giảng đó hoặc giáo viên
-- mới được xem, tránh 1 trợ giảng dò điểm/giờ của người khác qua RPC.
create or replace function public.ta_accrued_hours(p_assistant_id uuid)
returns numeric
language plpgsql
stable
security definer
set search_path = public
as $$
begin
  if not public.is_admin() and p_assistant_id is distinct from public.ta_current_assistant_id() then
    raise exception 'không có quyền xem dữ liệu trợ giảng này';
  end if;

  return coalesce((
    select sum(public.ta_converted_hours(session_type, hours))
    from public.ta_sessions
    where assistant_id = p_assistant_id
      and status = 'approved'
      and session_type in ('lop', 'phudao')
  ), 0);
end;
$$;

grant execute on function public.ta_accrued_hours(uuid) to authenticated;

-- ---------- 8. Điểm hiệu suất + lương tháng — nguồn tính duy nhất ----------
create or replace function public.ta_monthly_score(p_assistant_id uuid, p_month date)
returns table (
  assistant_id uuid,
  month date,
  lop_sessions integer,
  phudao_sessions integer,
  avg_touches numeric,
  touches_score numeric,
  ontime_error_notes integer,
  error_note_rate numeric,
  error_note_score numeric,
  complete_phudao integer,
  phudao_complete_rate numeric,
  phudao_score numeric,
  flag_count integer,
  focus_score numeric,
  total_score numeric,
  bonus_per_hour integer,
  converted_hours numeric,
  papers_graded integer,
  base_pay numeric,
  bonus_pay numeric,
  grading_pay numeric,
  total_pay numeric
)
language plpgsql
stable
security definer
set search_path = public
as $$
declare
  v_month date := date_trunc('month', p_month)::date;
  v_month_end date := (v_month + interval '1 month')::date;
  v_tier text;
  v_retained_rate integer;
  v_base_rate integer;
  v_rate numeric;
begin
  -- SECURITY DEFINER nên phải tự kiểm tra quyền ở đây, không dựa vào RLS của caller.
  if not public.is_admin() and p_assistant_id is distinct from public.ta_current_assistant_id() then
    raise exception 'không có quyền xem dữ liệu trợ giảng này';
  end if;

  select a.tier, a.retained_rate into v_tier, v_retained_rate
  from public.ta_assistants a
  where a.id = p_assistant_id;

  select r.base_rate into v_base_rate
  from public.ta_rates r
  where r.tier = v_tier and r.effective_from <= v_month
  order by r.effective_from desc
  limit 1;

  v_rate := coalesce(v_retained_rate, v_base_rate, 0);

  return query
  with sess as (
    select s.*
    from public.ta_sessions s
    where s.assistant_id = p_assistant_id
      and s.status = 'approved'
      and s.work_date >= v_month
      and s.work_date < v_month_end
  ),
  lop as (select * from sess where session_type = 'lop'),
  phudao_s as (select * from sess where session_type = 'phudao'),
  metrics as (
    select
      (select count(*) from lop)::int as m_lop_count,
      (select count(*) from phudao_s)::int as m_phudao_count,
      coalesce((select avg(student_touches) from lop), 0)::numeric as m_avg_touches,
      coalesce((select count(*) from lop
                where error_note_at is not null and error_note_at::date = work_date), 0)::int as m_ontime,
      coalesce((select count(*) from phudao_s
                where homework_given is not null and length(trim(homework_given)) > 0
                  and student_recap_ok = true), 0)::int as m_complete_phudao,
      coalesce((select sum(sess.papers_graded) from sess where sess.session_type = 'chambai'), 0)::int as m_papers,
      coalesce((select count(*) from public.ta_flags f
                where f.assistant_id = p_assistant_id
                  and f.flag_date >= v_month and f.flag_date < v_month_end), 0)::int as m_flags,
      coalesce((select sum(public.ta_converted_hours(session_type, hours)) from sess), 0)::numeric as m_converted_hours
  ),
  scores as (
    select
      m.*,
      least(40, 40 * m_avg_touches / 12) as s_touches,
      case when m_lop_count = 0 then 0 else 20.0 * m_ontime / m_lop_count end as s_error_note,
      case when m_phudao_count = 0 then 20 else 20.0 * m_complete_phudao / m_phudao_count end as s_phudao,
      greatest(0, 20 - 10 * m_flags) as s_focus
    from metrics m
  ),
  totals as (
    select
      sc.*,
      (sc.s_touches + sc.s_error_note + sc.s_phudao + sc.s_focus) as s_total
    from scores sc
  )
  select
    p_assistant_id,
    v_month,
    t.m_lop_count,
    t.m_phudao_count,
    round(t.m_avg_touches, 2),
    round(t.s_touches, 2),
    t.m_ontime,
    case when t.m_lop_count = 0 then 0 else round(t.m_ontime::numeric / t.m_lop_count, 4) end,
    round(t.s_error_note, 2),
    t.m_complete_phudao,
    case when t.m_phudao_count = 0 then 1 else round(t.m_complete_phudao::numeric / t.m_phudao_count, 4) end,
    round(t.s_phudao, 2),
    t.m_flags,
    round(t.s_focus::numeric, 2),
    round(t.s_total, 2),
    case when t.s_total >= 85 then 4000 when t.s_total >= 70 then 2000 else 0 end,
    round(t.m_converted_hours, 2),
    t.m_papers,
    round(t.m_converted_hours * v_rate, 0) as base_pay,
    round(t.m_converted_hours * (case when t.s_total >= 85 then 4000 when t.s_total >= 70 then 2000 else 0 end), 0) as bonus_pay,
    round(t.m_papers * 1500, 0) as grading_pay,
    round(
      t.m_converted_hours * v_rate
      + t.m_converted_hours * (case when t.s_total >= 85 then 4000 when t.s_total >= 70 then 2000 else 0 end)
      + t.m_papers * 1500
    , 0) as total_pay
  from totals t;
end;
$$;

grant execute on function public.ta_monthly_score(uuid, date) to authenticated;

-- ---------- 9. RLS ----------
alter table public.ta_assistants enable row level security;
alter table public.ta_rates enable row level security;
alter table public.ta_sessions enable row level security;
alter table public.ta_flags enable row level security;

-- ta_assistants: tự xem hồ sơ của mình; giáo viên toàn quyền.
drop policy if exists "ta xem chinh minh" on public.ta_assistants;
create policy "ta xem chinh minh" on public.ta_assistants
  for select to authenticated using (user_id = auth.uid() or public.is_admin());
drop policy if exists "admin toan quyen ta_assistants" on public.ta_assistants;
create policy "admin toan quyen ta_assistants" on public.ta_assistants
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ta_rates: ai đăng nhập cũng đọc được (để tự tính lương dự kiến); chỉ giáo viên sửa.
drop policy if exists "doc don gia" on public.ta_rates;
create policy "doc don gia" on public.ta_rates
  for select to authenticated using (true);
drop policy if exists "admin sua don gia" on public.ta_rates;
create policy "admin sua don gia" on public.ta_rates
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ta_sessions: trợ giảng đọc/tạo/sửa buổi của chính mình (sửa được khi còn "submitted"
-- và trong 3 ngày kể từ work_date); giáo viên đọc/sửa toàn bộ. KHÔNG có policy delete
-- cho bất kỳ ai — muốn huỷ thì chuyển status = 'rejected'.
drop policy if exists "doc buoi lam viec" on public.ta_sessions;
create policy "doc buoi lam viec" on public.ta_sessions
  for select to authenticated
  using (assistant_id = public.ta_current_assistant_id() or public.is_admin());

drop policy if exists "ta tao buoi cua minh" on public.ta_sessions;
create policy "ta tao buoi cua minh" on public.ta_sessions
  for insert to authenticated
  with check (assistant_id = public.ta_current_assistant_id() and status = 'submitted');

drop policy if exists "ta sua buoi trong han" on public.ta_sessions;
create policy "ta sua buoi trong han" on public.ta_sessions
  for update to authenticated
  using (
    assistant_id = public.ta_current_assistant_id()
    and status = 'submitted'
    and work_date >= (current_date - 3)
  )
  with check (assistant_id = public.ta_current_assistant_id() and status = 'submitted');

drop policy if exists "admin sua buoi" on public.ta_sessions;
create policy "admin sua buoi" on public.ta_sessions
  for update to authenticated
  using (public.is_admin())
  with check (public.is_admin());

-- ta_flags: trợ giảng chỉ đọc flag của mình (không sửa được); giáo viên toàn quyền trừ việc
-- ai cũng không xoá được ta_sessions (không liên quan bảng này nên giáo viên vẫn xoá được flag
-- nếu đánh nhầm).
drop policy if exists "ta doc flag cua minh" on public.ta_flags;
create policy "ta doc flag cua minh" on public.ta_flags
  for select to authenticated
  using (assistant_id = public.ta_current_assistant_id() or public.is_admin());
drop policy if exists "admin quan ly flag" on public.ta_flags;
create policy "admin quan ly flag" on public.ta_flags
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ============================================================
-- MỤC 8 — Mảng video TikTok: dòng công việc riêng, trả riêng, không cộng giờ
-- công lên lớp, không tính vào điểm hiệu suất ở ta_monthly_score.
-- ============================================================

-- ---------- 10. ta_video_rates ----------
-- Toàn bộ đơn giá/ngưỡng thưởng của mảng video, có hiệu lực theo tháng — không viết
-- cứng trong hàm, đổi ở đây là áp dụng ngay cho video phát sinh từ tháng đó trở đi.
create table if not exists public.ta_video_rates (
  id uuid primary key default gen_random_uuid(),
  effective_from date not null unique,
  price_don_gian integer not null default 120000,
  price_dung_ky integer not null default 200000,
  view_threshold_1 integer not null default 10000,
  view_bonus_1 integer not null default 50000,
  view_threshold_2 integer not null default 50000,
  view_bonus_2 integer not null default 150000,
  lead_bonus integer not null default 300000,
  monthly_budget_cap integer not null default 1200000
);

insert into public.ta_video_rates (effective_from) values ('2026-10-01')
on conflict (effective_from) do nothing;

-- ---------- 11. ta_video_stats ----------
-- Nhập tay mỗi tuần (TikTok không có API công khai) — luôn lấy bản ghi checked_at mới
-- nhất của mỗi video để tính thưởng, xem ta_video_ledger.
create table if not exists public.ta_video_stats (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.ta_sessions(id) on delete cascade,
  checked_at date not null default current_date,
  views integer not null default 0,
  saves integer not null default 0,
  comments integer not null default 0,
  created_at timestamptz not null default now(),
  unique (session_id, checked_at)
);

create index if not exists ta_video_stats_session_idx on public.ta_video_stats(session_id, checked_at desc);

-- ---------- 12. ta_leads ----------
-- Học sinh mới đăng ký — chỉ giáo viên ghi/sửa, dùng để chi thưởng đăng ký.
create table if not exists public.ta_leads (
  id uuid primary key default gen_random_uuid(),
  student_name text not null,
  source text not null default 'tiktok',
  attributed_session_id uuid references public.ta_sessions(id) on delete set null,
  registered_at date not null default current_date,
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now()
);

create index if not exists ta_leads_session_idx on public.ta_leads(attributed_session_id);
create index if not exists ta_leads_registered_idx on public.ta_leads(registered_at);

-- ---------- 13. ta_video_ledger — nguồn tính tiền duy nhất cho mảng video ----------
-- Trả về 1 dòng / video, dùng chung cho cả /tro-giang/video (p_assistant_id = chính mình)
-- và /admin/tro-giang tab video (p_assistant_id = null, chỉ giáo viên).
create or replace function public.ta_video_ledger(p_assistant_id uuid default null)
returns table (
  session_id uuid,
  assistant_id uuid,
  work_date date,
  video_tier text,
  video_url text,
  published_at timestamptz,
  status text,
  reject_reason text,
  topic_source_id uuid,
  latest_checked_at date,
  latest_views integer,
  latest_saves integer,
  latest_comments integer,
  view_bonus numeric,
  production_pay numeric,
  lead_count integer,
  lead_bonus numeric,
  total_pay numeric
)
language plpgsql
stable
security definer
set search_path = public
as $$
declare
  v_target uuid;
  v_has_target boolean;
begin
  if p_assistant_id is null then
    if not public.is_admin() then
      raise exception 'không có quyền xem dữ liệu video của toàn đội';
    end if;
    v_has_target := false;
  else
    if not public.is_admin() and p_assistant_id is distinct from public.ta_current_assistant_id() then
      raise exception 'không có quyền xem dữ liệu trợ giảng này';
    end if;
    v_target := p_assistant_id;
    v_has_target := true;
  end if;

  return query
  with videos as (
    select s.*
    from public.ta_sessions s
    where s.session_type = 'video'
      and (not v_has_target or s.assistant_id = v_target)
  ),
  latest_stats as (
    select distinct on (vs.session_id)
      vs.session_id, vs.checked_at, vs.views, vs.saves, vs.comments
    from public.ta_video_stats vs
    order by vs.session_id, vs.checked_at desc
  ),
  rates as (
    select v.id as vid, r.price_don_gian, r.price_dung_ky,
           r.view_threshold_1, r.view_bonus_1, r.view_threshold_2, r.view_bonus_2, r.lead_bonus
    from videos v
    left join lateral (
      select * from public.ta_video_rates r2
      where r2.effective_from <= v.work_date
      order by r2.effective_from desc
      limit 1
    ) r on true
  ),
  lead_counts as (
    select l.attributed_session_id as vid, count(*)::int as n
    from public.ta_leads l
    where l.attributed_session_id is not null
    group by l.attributed_session_id
  ),
  combined as (
    select
      v.id, v.assistant_id, v.work_date, v.video_tier, v.video_url, v.published_at,
      v.status, v.reject_reason, v.topic_source_id,
      ls.checked_at as c_checked_at,
      coalesce(ls.views, 0) as c_views,
      coalesce(ls.saves, 0) as c_saves,
      coalesce(ls.comments, 0) as c_comments,
      r.price_don_gian, r.price_dung_ky, r.view_threshold_1, r.view_bonus_1,
      r.view_threshold_2, r.view_bonus_2, r.lead_bonus,
      coalesce(lc.n, 0) as c_lead_count
    from videos v
    left join latest_stats ls on ls.session_id = v.id
    left join rates r on r.vid = v.id
    left join lead_counts lc on lc.vid = v.id
  ),
  computed as (
    select
      c.*,
      (case
        when c.c_views >= coalesce(c.view_threshold_2, 50000) then coalesce(c.view_bonus_1, 0) + coalesce(c.view_bonus_2, 0)
        when c.c_views >= coalesce(c.view_threshold_1, 10000) then coalesce(c.view_bonus_1, 0)
        else 0
      end)::numeric as x_view_bonus,
      (case
        when c.status = 'approved' and c.video_url is not null then
          (case c.video_tier when 'don_gian' then coalesce(c.price_don_gian, 0) when 'dung_ky' then coalesce(c.price_dung_ky, 0) else 0 end)
        else 0
      end)::numeric as x_production_pay,
      (c.c_lead_count * coalesce(c.lead_bonus, 0))::numeric as x_lead_bonus
    from combined c
  )
  select
    x.id, x.assistant_id, x.work_date, x.video_tier, x.video_url, x.published_at,
    x.status, x.reject_reason, x.topic_source_id,
    x.c_checked_at, x.c_views, x.c_saves, x.c_comments,
    x.x_view_bonus, x.x_production_pay, x.c_lead_count, x.x_lead_bonus,
    (x.x_view_bonus + x.x_production_pay + x.x_lead_bonus) as total_pay
  from computed x
  order by x.work_date desc;
end;
$$;

grant execute on function public.ta_video_ledger(uuid) to authenticated;

-- ---------- 14. ta_video_topic_suggestions — kho đề tài chưa dùng (mục 8.4) ----------
-- Luôn scope theo CHÍNH người gọi — trang /tro-giang/video chỉ gợi ý đề tài của mình.
create or replace function public.ta_video_topic_suggestions(p_days integer default 14)
returns table (
  session_id uuid,
  work_date date,
  class_label text,
  error_note text
)
language sql
stable
security definer
set search_path = public
as $$
  select s.id, s.work_date, s.class_label, s.error_note
  from public.ta_sessions s
  where s.assistant_id = public.ta_current_assistant_id()
    and s.session_type = 'lop'
    and s.status = 'approved'
    and s.work_date >= current_date - p_days
    and s.error_note is not null and length(trim(s.error_note)) > 0
    and not exists (
      select 1 from public.ta_sessions v
      where v.session_type = 'video' and v.topic_source_id = s.id
    )
  order by s.work_date desc;
$$;

grant execute on function public.ta_video_topic_suggestions(integer) to authenticated;

-- ---------- 15. ta_topic_exploitation_rate — cho bảng điều khiển giáo viên (mục 8.4) ----------
create or replace function public.ta_topic_exploitation_rate(p_days integer default 14)
returns table (eligible_count integer, used_count integer, rate numeric)
language plpgsql
stable
security definer
set search_path = public
as $$
begin
  if not public.is_admin() then
    raise exception 'chỉ giáo viên được xem số liệu này';
  end if;

  return query
  with eligible as (
    select s.id
    from public.ta_sessions s
    where s.session_type = 'lop'
      and s.status = 'approved'
      and s.work_date >= current_date - p_days
      and s.error_note is not null and length(trim(s.error_note)) > 0
  ),
  used as (
    select e.id from eligible e
    where exists (
      select 1 from public.ta_sessions v
      where v.session_type = 'video' and v.topic_source_id = e.id
    )
  )
  select
    (select count(*) from eligible)::int,
    (select count(*) from used)::int,
    case when (select count(*) from eligible) = 0 then 1
         else round((select count(*) from used)::numeric / (select count(*) from eligible), 4)
    end;
end;
$$;

grant execute on function public.ta_topic_exploitation_rate(integer) to authenticated;

-- ---------- 16. ta_video_admin_summary — tổng hợp tháng cho /admin/tro-giang (mục 8.5) ----------
create or replace function public.ta_video_admin_summary(p_month date)
returns table (
  month date,
  videos_published integer,
  total_views numeric,
  total_saves numeric,
  total_comments numeric,
  leads_count integer,
  production_spend numeric,
  view_bonus_spend numeric,
  lead_bonus_spend numeric,
  total_spend numeric,
  budget_cap integer,
  over_budget boolean,
  cost_per_lead numeric
)
language plpgsql
stable
security definer
set search_path = public
as $$
declare
  v_month date := date_trunc('month', p_month)::date;
  v_month_end date := (v_month + interval '1 month')::date;
  v_cap integer;
  v_leads integer;
begin
  if not public.is_admin() then
    raise exception 'chỉ giáo viên được xem tổng hợp này';
  end if;

  select r.monthly_budget_cap into v_cap
  from public.ta_video_rates r
  where r.effective_from <= v_month
  order by r.effective_from desc
  limit 1;

  select count(*) into v_leads
  from public.ta_leads l
  where l.source = 'tiktok' and l.registered_at >= v_month and l.registered_at < v_month_end;

  return query
  with ledger as (
    select * from public.ta_video_ledger(null) l
    where l.work_date >= v_month and l.work_date < v_month_end
  )
  select
    v_month,
    count(*)::int,
    coalesce(sum(latest_views), 0)::numeric,
    coalesce(sum(latest_saves), 0)::numeric,
    coalesce(sum(latest_comments), 0)::numeric,
    coalesce(v_leads, 0),
    coalesce(sum(production_pay), 0),
    coalesce(sum(view_bonus), 0),
    coalesce(sum(lead_bonus), 0),
    coalesce(sum(total_pay), 0),
    coalesce(v_cap, 1200000),
    coalesce(sum(production_pay), 0) > coalesce(v_cap, 1200000),
    case when coalesce(v_leads, 0) > 0 then round(coalesce(sum(total_pay), 0) / v_leads, 0) else null end
  from ledger;
end;
$$;

grant execute on function public.ta_video_admin_summary(date) to authenticated;

-- ---------- 17. RLS: ta_video_rates / ta_video_stats / ta_leads ----------
alter table public.ta_video_rates enable row level security;
alter table public.ta_video_stats enable row level security;
alter table public.ta_leads enable row level security;

drop policy if exists "doc gia video" on public.ta_video_rates;
create policy "doc gia video" on public.ta_video_rates
  for select to authenticated using (true);
drop policy if exists "admin sua gia video" on public.ta_video_rates;
create policy "admin sua gia video" on public.ta_video_rates
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ta_video_stats: trợ giảng chỉ đọc số liệu của video thuộc về mình; chỉ giáo viên nhập/sửa
-- (số liệu tuần lấy tay từ TikTok, không có API).
drop policy if exists "ta doc stats video cua minh" on public.ta_video_stats;
create policy "ta doc stats video cua minh" on public.ta_video_stats
  for select to authenticated
  using (
    public.is_admin()
    or exists (
      select 1 from public.ta_sessions s
      where s.id = ta_video_stats.session_id and s.assistant_id = public.ta_current_assistant_id()
    )
  );
drop policy if exists "admin quan ly stats video" on public.ta_video_stats;
create policy "admin quan ly stats video" on public.ta_video_stats
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ta_leads: trợ giảng chỉ đọc các dòng gắn với video của mình; chỉ giáo viên ghi/sửa/xoá.
drop policy if exists "ta doc leads cua video minh" on public.ta_leads;
create policy "ta doc leads cua video minh" on public.ta_leads
  for select to authenticated
  using (
    public.is_admin()
    or exists (
      select 1 from public.ta_sessions s
      where s.id = ta_leads.attributed_session_id and s.assistant_id = public.ta_current_assistant_id()
    )
  );
drop policy if exists "admin quan ly leads" on public.ta_leads;
create policy "admin quan ly leads" on public.ta_leads
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
