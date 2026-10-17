-- DT-01 (docs/thachlab-design-thinking-audit.md): ghi sự kiện học tập nối tiếp để biết HS mở mục nào,
-- ở lại bao lâu, nộp lúc nào. Bảng chỉ thêm, không sửa; khác student_learning_presence (1 dòng/HS, chỉ "đang ở đâu").
--
--   * Ghi qua RPC log_learning_events(jsonb) — tối đa 50 sự kiện/lần, ép student_id = auth.uid(),
--     ép kind và thời lượng vào khoảng hợp lệ. HS không có quyền insert trực tiếp.
--   * Đọc: HS xem của mình; giáo viên/trợ giảng xem HS mình dạy (teaches_student); admin xem tất cả.
--   * Giữ 12 tháng: purge_learning_events() xoá sự kiện cũ, pg_cron 3:30 VN ngày 1 hằng tháng (nếu bật được).
--
-- Rollback ở cuối file.

create table if not exists public.learning_events (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.profiles(id) on delete cascade,
  lesson_id bigint references public.lessons(id) on delete set null,
  item_id bigint references public.lesson_items(id) on delete set null,
  kind text not null check (kind in ('open', 'leave', 'submit')),
  duration_s integer check (duration_s is null or (duration_s >= 0 and duration_s <= 3600)),
  occurred_at timestamptz not null default now()
);

create index if not exists learning_events_student_time_idx on public.learning_events (student_id, occurred_at desc);
create index if not exists learning_events_item_time_idx on public.learning_events (item_id, occurred_at desc);

alter table public.learning_events enable row level security;
revoke all on public.learning_events from anon, authenticated;
grant select on public.learning_events to authenticated;

drop policy if exists "hs xem su kien hoc cua minh" on public.learning_events;
create policy "hs xem su kien hoc cua minh" on public.learning_events
  as permissive for select to authenticated
  using (student_id = (select auth.uid()));

drop policy if exists "giao vien xem su kien hoc cua lop" on public.learning_events;
create policy "giao vien xem su kien hoc cua lop" on public.learning_events
  as permissive for select to authenticated
  using (public.teaches_student(student_id) or public.is_admin());

-- p_events: [{"lessonId":12,"itemId":34,"kind":"open|leave|submit","durationS":45,"at":"2026-10-17T09:00:00Z"}]
-- "at" tuỳ chọn; lệch quá 1 ngày so với now() thì dùng now() (chống ghi giả ngày).
create or replace function public.log_learning_events(p_events jsonb)
returns integer
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_n integer := 0;
  v_e jsonb;
  v_kind text;
  v_dur integer;
  v_at timestamptz;
begin
  if v_uid is null then
    raise exception 'Chưa đăng nhập' using errcode = '42501';
  end if;
  if p_events is null or jsonb_typeof(p_events) <> 'array' then
    return 0;
  end if;
  for v_e in select * from jsonb_array_elements(p_events) limit 50 loop
    v_kind := v_e ->> 'kind';
    continue when v_kind is null or v_kind not in ('open', 'leave', 'submit');
    v_dur := case when (v_e ->> 'durationS') ~ '^[0-9]{1,5}$' then least((v_e ->> 'durationS')::integer, 3600) end;
    begin
      v_at := (v_e ->> 'at')::timestamptz;
    exception when others then
      v_at := null;
    end;
    if v_at is null or v_at > now() + interval '5 minutes' or v_at < now() - interval '1 day' then
      v_at := now();
    end if;
    insert into public.learning_events (student_id, lesson_id, item_id, kind, duration_s, occurred_at)
    values (
      v_uid,
      case when (v_e ->> 'lessonId') ~ '^[0-9]{1,18}$' then (v_e ->> 'lessonId')::bigint end,
      case when (v_e ->> 'itemId') ~ '^[0-9]{1,18}$' then (v_e ->> 'itemId')::bigint end,
      v_kind, v_dur, v_at
    );
    v_n := v_n + 1;
  end loop;
  return v_n;
exception when foreign_key_violation then
  -- lesson_id/item_id không tồn tại: bỏ cả lô, không làm hỏng trang đang học
  return 0;
end;
$$;
revoke all on function public.log_learning_events(jsonb) from public, anon;
grant execute on function public.log_learning_events(jsonb) to authenticated;

create or replace function public.purge_learning_events(p_before timestamptz default (now() - interval '12 months'))
returns bigint
language plpgsql security definer set search_path = public
as $$
declare
  v_n bigint;
begin
  delete from public.learning_events where occurred_at < p_before;
  get diagnostics v_n = row_count;
  return v_n;
end;
$$;
revoke all on function public.purge_learning_events(timestamptz) from public, anon, authenticated;

do $$
begin
  begin
    create extension if not exists pg_cron;
  exception when others then
    raise notice 'pg_cron không bật được (%): chạy tay select public.purge_learning_events(); mỗi học kì', sqlerrm;
  end;
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'learning-events-purge';
    perform cron.schedule('learning-events-purge', '30 20 1 * *', 'select public.purge_learning_events();');
    raise notice 'Đã đặt lịch pg_cron learning-events-purge (3:30 VN ngày 1 hằng tháng)';
  end if;
end $$;

-- ---------- ROLLBACK ----------
-- do $$ begin
--   if exists (select 1 from pg_extension where extname = 'pg_cron') then
--     perform cron.unschedule(jobid) from cron.job where jobname = 'learning-events-purge';
--   end if;
-- end $$;
-- drop function if exists public.purge_learning_events(timestamptz);
-- drop function if exists public.log_learning_events(jsonb);
-- drop table if exists public.learning_events;
