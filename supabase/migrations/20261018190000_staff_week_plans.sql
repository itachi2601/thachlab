-- Lịch tuần của giảng viên (skill lich-tuan) hiển thị ở /tai-khoan.
-- Mỗi người một dòng/tuần; chỉ chủ tài khoản đọc được; ghi bằng service_role (script trên Mac).
-- Idempotent.
create table if not exists public.staff_week_plans (
  user_id uuid not null references public.profiles (id) on delete cascade,
  week_start date not null,                 -- thứ Hai của tuần
  events jsonb not null default '[]'::jsonb, -- [{weekday 1..7, start 'HH:MM', end 'HH:MM', title, where, src, note, clash}]
  warnings jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, week_start)
);

alter table public.staff_week_plans enable row level security;
revoke all on public.staff_week_plans from anon, authenticated;
grant select on public.staff_week_plans to authenticated;

drop policy if exists staff_week_plans_select_own on public.staff_week_plans;
create policy staff_week_plans_select_own on public.staff_week_plans
  for select to authenticated using (user_id = (select auth.uid()));

-- ROLLBACK:
--   drop table if exists public.staff_week_plans;
