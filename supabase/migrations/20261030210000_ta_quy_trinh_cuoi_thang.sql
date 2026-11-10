-- Quy trình xem lại công trợ giảng mỗi cuối tháng (thầy chốt 30/10/2026).
--   Ngày cuối tháng, 19h (giờ VN): báo mọi trợ giảng "ngày 1–3 tháng sau mở xem lại công tháng này".
--   Ngày 1, 0h: mở lại tháng vừa qua tới 23:59 ngày 3 (ta_settings.reopen_*, xem 20261030200000) + báo đã mở.
--   Ngày 3, 8h: nhắc hôm nay hạn cuối.
--   Hết hạn: tháng cũ KHOÁ với trợ giảng (trigger ta_month_lock_guard, kể cả buổi còn trong hạn 7 ngày),
--   báo thầy số buổi chờ duyệt + khiếu nại chưa xử lý để duyệt rồi chốt sổ.
-- Khiếu nại: bảng ta_month_appeals, trợ giảng gửi qua RPC ta_submit_appeal chỉ trong đợt mở; thầy trả lời bằng ta_resolve_appeal.
-- Chạy tay một bước: select public.ta_month_cycle();  (idempotent nhờ ta_month_cycle_log)

create table if not exists public.ta_month_appeals (
  id bigserial primary key,
  assistant_id uuid not null references public.ta_assistants (id) on delete cascade,
  month date not null,
  body text not null check (char_length(trim(body)) between 1 and 2000),
  created_at timestamptz not null default now(),
  reply text,
  resolved_at timestamptz,
  resolved_by uuid references auth.users (id)
);
create index if not exists ta_month_appeals_month_idx on public.ta_month_appeals (month, assistant_id);
alter table public.ta_month_appeals enable row level security;
revoke all on public.ta_month_appeals from anon, authenticated;

create table if not exists public.ta_month_cycle_log (
  month date not null,
  step text not null,
  done_at timestamptz not null default now(),
  primary key (month, step)
);
alter table public.ta_month_cycle_log enable row level security;
revoke all on public.ta_month_cycle_log from anon, authenticated;

-- Tháng trước tháng hiện tại (giờ VN) khoá với trợ giảng, trừ khi đang trong đợt mở lại.
-- Không SECURITY DEFINER: current_user là vai gọi thật → chỉ chặn lệnh trợ giảng gửi thẳng qua RLS (như ta_reopen_status_reset);
-- thầy (is_admin), script service_role và các hàm SECURITY DEFINER không bị chặn.
create or replace function public.ta_month_lock_guard()
returns trigger
language plpgsql
set search_path = public
as $$
declare cur date := date_trunc('month', (now() at time zone 'Asia/Ho_Chi_Minh')::date)::date;
begin
  if current_user = 'authenticated' and not public.is_admin() then
    if (date_trunc('month', new.work_date)::date < cur and not public.ta_reopen_active(new.work_date))
       or (TG_OP = 'UPDATE' and date_trunc('month', old.work_date)::date < cur and not public.ta_reopen_active(old.work_date)) then
      raise exception 'Công tháng %/% đã khoá (chỉ mở xem lại ngày 1–3 tháng sau). Cần sửa thì báo thầy.',
        to_char(least(new.work_date, coalesce(old.work_date, new.work_date)), 'MM'),
        to_char(least(new.work_date, coalesce(old.work_date, new.work_date)), 'YYYY');
    end if;
  end if;
  return new;
end;
$$;
drop trigger if exists ta_month_lock_guard on public.ta_sessions;
create trigger ta_month_lock_guard before insert or update on public.ta_sessions
  for each row execute function public.ta_month_lock_guard();

create or replace function public.ta_submit_appeal(p_month date, p_body text)
returns bigint
language plpgsql
security definer
set search_path = public
as $$
declare a public.ta_assistants; m date := date_trunc('month', p_month)::date; new_id bigint;
begin
  select * into a from public.ta_assistants where id = public.ta_current_assistant_id();
  if a.id is null then raise exception 'Không phải tài khoản trợ giảng'; end if;
  if not public.ta_reopen_active(m) then raise exception 'Chỉ gửi khiếu nại trong 3 ngày đầu tháng sau'; end if;
  if nullif(trim(p_body), '') is null then raise exception 'Ghi nội dung khiếu nại'; end if;
  insert into public.ta_month_appeals (assistant_id, month, body) values (a.id, m, trim(p_body)) returning id into new_id;
  insert into public.notifications (user_id, kind, title, body, href)
  select p.id, 'ta_appeal', a.short_name || ' khiếu nại công tháng ' || to_char(m, 'MM/YYYY'), left(trim(p_body), 300),
         '/quan-tri/tro-giang/luong-thang'
  from public.profiles p where p.role = 'admin';
  return new_id;
end;
$$;

create or replace function public.ta_list_appeals(p_assistant_id uuid, p_month date)
returns setof public.ta_month_appeals
language sql
stable
security definer
set search_path = public
as $$
  select * from public.ta_month_appeals
  where assistant_id = p_assistant_id and month = date_trunc('month', p_month)::date
    and (public.is_admin() or assistant_id = public.ta_current_assistant_id())
  order by created_at;
$$;

create or replace function public.ta_resolve_appeal(p_id bigint, p_reply text)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare r public.ta_month_appeals;
begin
  if not public.is_admin() then raise exception 'Chỉ thầy trả lời khiếu nại'; end if;
  update public.ta_month_appeals set reply = nullif(trim(p_reply), ''), resolved_at = now(), resolved_by = auth.uid()
  where id = p_id returning * into r;
  if r.id is null then raise exception 'Không thấy khiếu nại'; end if;
  insert into public.notifications (user_id, kind, title, body, href)
  select a.user_id, 'ta_appeal_reply', 'Thầy đã xử lý khiếu nại công tháng ' || to_char(r.month, 'MM/YYYY'),
         coalesce(left(r.reply, 300), 'Đã xem.'), '/tro-giang'
  from public.ta_assistants a where a.id = r.assistant_id and a.user_id is not null;
end;
$$;

revoke all on function public.ta_submit_appeal(date, text), public.ta_list_appeals(uuid, date), public.ta_resolve_appeal(bigint, text) from public, anon;
grant execute on function public.ta_submit_appeal(date, text), public.ta_list_appeals(uuid, date), public.ta_resolve_appeal(bigint, text) to authenticated;

-- Chạy mỗi giờ; mỗi bước chỉ làm một lần nhờ ta_month_cycle_log.
create or replace function public.ta_month_cycle()
returns text
language plpgsql
security definer
set search_path = public
as $$
declare
  local_now timestamp := now() at time zone 'Asia/Ho_Chi_Minh';
  today date := local_now::date;
  hr int := extract(hour from local_now);
  cur date := date_trunc('month', today)::date;
  prev date := (date_trunc('month', today) - interval '1 month')::date;
  until_ts timestamptz := ((cur + 2)::timestamp + time '23:59:59') at time zone 'Asia/Ho_Chi_Minh';
  s public.ta_settings;
  pending int; appeals int;
  done text := '';
begin
  -- 1) Ngày cuối tháng từ 19h: báo trước.
  if (today + 1) = (cur + interval '1 month')::date and hr >= 19
     and not exists (select 1 from public.ta_month_cycle_log where month = cur and step = 'announce') then
    insert into public.notifications (user_id, kind, title, body, href)
    select a.user_id, 'ta_month_review', 'Ngày 1–3 tháng sau: xem lại công tháng ' || to_char(cur, 'MM/YYYY'),
           'Từ 0h ngày 1 đến 23:59 ngày 3, con vào trang Trợ giảng xem lại từng buổi tháng ' || to_char(cur, 'MM')
           || ': ngày, lớp, giờ, số lượt. Sai thì sửa, thiếu thì ghi thêm, thắc mắc thì gửi khiếu nại. Hết ngày 3 công tháng này khoá để thầy chốt sổ.',
           '/tro-giang'
    from public.ta_assistants a where a.active and a.user_id is not null;
    insert into public.ta_month_cycle_log (month, step) values (cur, 'announce');
    done := done || 'announce ';
  end if;

  -- 2) Ngày 1–3: mở lại tháng trước tới 23:59 ngày 3.
  if extract(day from today) between 1 and 3
     and not exists (select 1 from public.ta_month_cycle_log where month = prev and step = 'open') then
    update public.ta_settings set reopen_month = prev, reopen_until = until_ts, updated_at = now() where id;
    insert into public.notifications (user_id, kind, title, body, href)
    select a.user_id, 'ta_month_review', 'Đã mở xem lại công tháng ' || to_char(prev, 'MM/YYYY'),
           'Hạn đến 23:59 ngày ' || to_char(cur + 2, 'DD/MM') || '. Buổi đã duyệt mà con sửa sẽ về Chờ duyệt để thầy duyệt lại.',
           '/tro-giang'
    from public.ta_assistants a where a.active and a.user_id is not null;
    insert into public.ta_month_cycle_log (month, step) values (prev, 'open');
    done := done || 'open ';
  end if;

  -- 3) Ngày 3 từ 8h: nhắc hạn cuối.
  if extract(day from today) = 3 and hr >= 8
     and not exists (select 1 from public.ta_month_cycle_log where month = prev and step = 'last_day') then
    insert into public.notifications (user_id, kind, title, body, href)
    select a.user_id, 'ta_month_review', 'Hôm nay hạn cuối xem lại công tháng ' || to_char(prev, 'MM/YYYY'),
           'Hết 23:59 hôm nay công tháng ' || to_char(prev, 'MM') || ' khoá. Còn sai sót thì sửa hoặc gửi khiếu nại ngay.',
           '/tro-giang'
    from public.ta_assistants a where a.active and a.user_id is not null;
    insert into public.ta_month_cycle_log (month, step) values (prev, 'last_day');
    done := done || 'last_day ';
  end if;

  -- 4) Hết hạn: báo thầy duyệt + chốt sổ.
  select * into s from public.ta_settings where id;
  if s.reopen_month = prev and s.reopen_until is not null and now() >= s.reopen_until
     and not exists (select 1 from public.ta_month_cycle_log where month = prev and step = 'locked') then
    select count(*) into pending from public.ta_sessions
      where status = 'submitted' and work_date >= prev and work_date < cur;
    select count(*) into appeals from public.ta_month_appeals where month = prev and resolved_at is null;
    insert into public.notifications (user_id, kind, title, body, href)
    select p.id, 'ta_month_review', 'Công trợ giảng tháng ' || to_char(prev, 'MM/YYYY') || ' đã khoá — mời thầy chốt sổ',
           pending || ' buổi chờ duyệt, ' || appeals || ' khiếu nại chưa xử lý. Duyệt và trả lời xong rồi bấm Chốt từng bạn.',
           '/quan-tri/tro-giang/luong-thang'
    from public.profiles p where p.role = 'admin';
    insert into public.ta_month_cycle_log (month, step) values (prev, 'locked');
    done := done || 'locked ';
  end if;

  return coalesce(nullif(trim(done), ''), 'không có bước nào');
end;
$$;
revoke all on function public.ta_month_cycle() from public, anon, authenticated;

-- Tháng 10/2026 đang mở tay tới 02/11 (20261030200000); 0h ngày 1/11 bước 2 sẽ kéo hạn tới 23:59 03/11 và báo trợ giảng.

do $$
begin
  begin
    create extension if not exists pg_cron;
  exception when others then
    raise notice 'pg_cron không bật được (%): gọi tay select public.ta_month_cycle(); mỗi giờ', sqlerrm;
  end;
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'ta-month-cycle';
    perform cron.schedule('ta-month-cycle', '5 * * * *', 'select public.ta_month_cycle();');
    raise notice 'Đã đặt lịch pg_cron ta-month-cycle (phút 5 mỗi giờ)';
  end if;
end $$;

-- ROLLBACK:
--   select cron.unschedule(jobid) from cron.job where jobname = 'ta-month-cycle';
--   drop trigger if exists ta_month_lock_guard on public.ta_sessions;
--   drop function if exists public.ta_month_cycle(), public.ta_month_lock_guard(),
--     public.ta_submit_appeal(date, text), public.ta_list_appeals(uuid, date), public.ta_resolve_appeal(bigint, text);
--   drop table if exists public.ta_month_cycle_log, public.ta_month_appeals;
