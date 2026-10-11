-- Lịch sử nhắc việc trợ giảng hằng tuần (skill kiem-tra-tro-giang-tuan).
-- Mỗi trợ giảng tối đa MỘT dòng/tuần: chống nhắc trùng và để đếm số tuần nhắc liên tiếp (tăng dần mức nhắc).
-- Chỉ service_role (script chạy trên Mac) ghi/đọc; trợ giảng đọc nội dung nhắc qua bảng notifications.
-- Idempotent.
create table if not exists public.ta_reminders (
  id bigint generated always as identity primary key,
  assistant_id uuid not null references public.ta_assistants (id) on delete cascade,
  week_start date not null,                 -- thứ Hai của tuần được kiểm
  level smallint not null default 1 check (level between 1 and 3),
  items jsonb not null default '[]'::jsonb, -- [{code, text}]
  title text not null,
  body text not null default '',
  notification_id bigint references public.notifications (id) on delete set null,
  created_at timestamptz not null default now(),
  unique (assistant_id, week_start)
);
create index if not exists ta_reminders_week_idx on public.ta_reminders (week_start desc);

alter table public.ta_reminders enable row level security;
revoke all on public.ta_reminders from anon, authenticated;

-- ROLLBACK:
--   drop table if exists public.ta_reminders;
