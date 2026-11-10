-- Mở lại khai giờ trợ giảng cả một tháng để các bạn rà lần cuối trước khi thầy chốt sổ (30/10/2026).
-- Bình thường: trợ giảng chỉ sửa buổi "Chờ duyệt" trong 7 ngày kể từ ngày làm.
-- Khi mở lại: trợ giảng sửa được MỌI buổi của mình trong tháng mở lại (kể cả đã duyệt/từ chối) tới hạn reopen_until.
-- Buổi đã duyệt/từ chối mà trợ giảng sửa sẽ quay về "Chờ duyệt" để thầy duyệt lại. Tháng đã chốt vẫn khoá
-- (trigger ta_policy_session_guard), mọi thay đổi vẫn ghi ta_policy_audit.
-- Đóng sớm: update public.ta_settings set reopen_until = now() where id;

alter table public.ta_settings
  add column if not exists reopen_month date,
  add column if not exists reopen_until timestamptz;

create or replace function public.ta_reopen_active(p_work_date date)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.ta_settings s
    where s.id and s.reopen_month = date_trunc('month', p_work_date)::date and now() < s.reopen_until
  );
$$;
revoke all on function public.ta_reopen_active(date) from public, anon;
grant execute on function public.ta_reopen_active(date) to authenticated;

-- Cho trang trợ giảng biết đang mở lại tháng nào, tới khi nào (null khi không mở).
create or replace function public.ta_reopen_window()
returns table(month date, until timestamptz)
language sql
stable
security definer
set search_path = public
as $$
  select s.reopen_month, s.reopen_until from public.ta_settings s
  where s.id and s.reopen_month is not null and now() < s.reopen_until;
$$;
revoke all on function public.ta_reopen_window() from public, anon;
grant execute on function public.ta_reopen_window() to authenticated;

drop policy if exists "ta sua buoi thang mo lai" on public.ta_sessions;
create policy "ta sua buoi thang mo lai" on public.ta_sessions
  for update to authenticated
  using (assistant_id = ta_current_assistant_id() and ta_reopen_active(work_date))
  with check (assistant_id = ta_current_assistant_id() and status = 'submitted' and ta_reopen_active(work_date));

-- Trợ giảng sửa buổi đã duyệt/từ chối → về Chờ duyệt. Chỉ áp cho lệnh UPDATE trực tiếp qua RLS
-- (current_user = authenticated); hàm SECURITY DEFINER chạy dưới owner nên không bị đổi trạng thái.
create or replace function public.ta_reopen_status_reset()
returns trigger
language plpgsql
as $$
begin
  if current_user = 'authenticated' and not public.is_admin() and old.status in ('approved', 'rejected') then
    new.status := 'submitted';
    new.approved_at := null;
    new.reject_reason := null;
  end if;
  return new;
end;
$$;
drop trigger if exists ta_reopen_status_reset on public.ta_sessions;
create trigger ta_reopen_status_reset before update on public.ta_sessions
  for each row execute function public.ta_reopen_status_reset();

-- Mở tháng 10/2026 tới hết Chủ nhật 02/11/2026 (giờ Việt Nam).
update public.ta_settings set reopen_month = date '2026-10-01', reopen_until = timestamptz '2026-11-02 23:59:59+07' where id;

-- ROLLBACK:
--   drop policy if exists "ta sua buoi thang mo lai" on public.ta_sessions;
--   drop trigger if exists ta_reopen_status_reset on public.ta_sessions;
--   drop function if exists public.ta_reopen_status_reset();
--   drop function if exists public.ta_reopen_window();
--   drop function if exists public.ta_reopen_active(date);
--   alter table public.ta_settings drop column if exists reopen_month, drop column if exists reopen_until;
