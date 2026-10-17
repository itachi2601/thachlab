-- DT-12 (docs/thachlab-design-thinking-audit.md): cờ tính năng theo lớp để thử một thay đổi trên MỘT lớp
-- rồi so với lớp cũ. Không có dòng cờ = tắt. Chỉ admin bật/tắt; HS đọc cờ của lớp mình qua feature_enabled().
--
--   select public.feature_enabled('on_tap_1_3_7');   -- true nếu HS thuộc lớp (đang active) có cờ bật
--
-- Chỉ số trước/sau lấy từ learning_events (20261017230000) và exam_question_results, so lớp có cờ với lớp không có.
-- Rollback ở cuối file.

create table if not exists public.feature_flags (
  flag text not null check (flag ~ '^[a-z0-9_]{1,60}$'),
  class_id bigint not null references public.classes(id) on delete cascade,
  enabled boolean not null default true,
  note text,
  created_by uuid default auth.uid() references public.profiles(id) on delete set null,
  created_at timestamptz not null default now(),
  primary key (flag, class_id)
);

alter table public.feature_flags enable row level security;
revoke all on public.feature_flags from anon, authenticated;
grant select, insert, update, delete on public.feature_flags to authenticated;

drop policy if exists "admin quan ly co tinh nang" on public.feature_flags;
create policy "admin quan ly co tinh nang" on public.feature_flags
  as permissive for all to authenticated
  using (public.is_admin())
  with check (public.is_admin());

drop policy if exists "giao vien xem co tinh nang" on public.feature_flags;
create policy "giao vien xem co tinh nang" on public.feature_flags
  as permissive for select to authenticated
  using (public.is_staff());

create or replace function public.feature_enabled(p_flag text)
returns boolean
language sql stable security definer set search_path = public
as $$
  select exists (
    select 1
    from public.feature_flags f
    join public.user_classes uc on uc.class_id = f.class_id
    where f.flag = p_flag
      and f.enabled
      and uc.user_id = (select auth.uid())
      and uc.status = 'active'
  );
$$;
revoke all on function public.feature_enabled(text) from public, anon;
grant execute on function public.feature_enabled(text) to authenticated;

-- ---------- ROLLBACK ----------
-- drop function if exists public.feature_enabled(text);
-- drop table if exists public.feature_flags;
