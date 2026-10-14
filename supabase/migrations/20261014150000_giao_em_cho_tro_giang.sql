-- ============================================================================
-- Nút "Giao trợ giảng" cho em mới vào (thầy chốt 14/10/2026)
-- Thầy chọn 1 trợ giảng cho 1 em: (1) ghi người phụ trách vào ta_student_handoffs, (2) tuỳ chọn mời em làm kiểm tra đầu vào
-- (gọi thpt_invite_entry_diagnostic), (3) báo trợ giảng qua chuông, (4) các mục phụ đạo đang mở của em chuyển sang "đã nhận"
-- và mọi mục MỚI mở cho em (kể cả sau kiểm tra đầu vào) tự gán cho trợ giảng đó (trigger trên tutoring_needs).
-- Chỉ chọn được trợ giảng đã được gán lớp của em (ta_assistant_classes) — không tự nới quyền xem dữ liệu.
-- Thêm: bảng ta_student_handoffs (RLS bật, không ai đọc/ghi trực tiếp), hàm ta_handoff_options / ta_handoff_assign / ta_handoff_clear,
--       trigger tutoring_needs_handoff_assign. Không đổi dữ liệu cũ.
-- Cách chạy: bash scripts/run-migrations.sh --yes --only N — chạy lúc nào cũng được.
-- Rollback: perf/rollback/20261014150000_giao_em_cho_tro_giang.down.sql
-- ============================================================================

create table if not exists public.ta_student_handoffs (
  student_id uuid primary key references public.profiles (id) on delete cascade,
  assistant_id uuid not null references public.ta_assistants (id) on delete cascade,
  assigned_by uuid references public.profiles (id),
  created_at timestamptz not null default now()
);
alter table public.ta_student_handoffs enable row level security;
revoke all on public.ta_student_handoffs from anon, authenticated;

-- Lớp đang học của em (lớp mới nhất còn hoạt động) và quyền giao: thầy phụ trách lớp đó hoặc admin.
create or replace function public.ta_handoff_can_assign(p_student uuid)
returns boolean
language sql stable security definer set search_path = public
as $$
  select auth.uid() is not null and (
    public.is_admin()
    or exists (
      select 1 from public.user_classes uc
      join public.class_instructors ci on ci.class_id = uc.class_id and ci.instructor_id = auth.uid()
      where uc.user_id = p_student and uc.status = 'active'
    )
  );
$$;
revoke all on function public.ta_handoff_can_assign(uuid) from public, anon;
grant execute on function public.ta_handoff_can_assign(uuid) to authenticated;

-- Danh sách trợ giảng chọn được cho em này + người đang phụ trách.
create or replace function public.ta_handoff_options(p_student uuid)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_assistants jsonb;
  v_current jsonb;
begin
  if not public.ta_handoff_can_assign(p_student) then
    raise exception 'Không có quyền' using errcode = '42501';
  end if;
  select coalesce(jsonb_agg(jsonb_build_object('id', a.id, 'name', coalesce(nullif(a.short_name, ''), a.full_name)) order by a.full_name), '[]'::jsonb)
    into v_assistants
  from public.ta_assistants a
  where a.active
    and a.user_id is not null
    and exists (
      select 1 from public.ta_assistant_classes ac
      join public.user_classes uc on uc.class_id = ac.class_id and uc.user_id = p_student and uc.status = 'active'
      where ac.assistant_id = a.id);
  select jsonb_build_object('id', a.id, 'name', coalesce(nullif(a.short_name, ''), a.full_name), 'since', h.created_at)
    into v_current
  from public.ta_student_handoffs h join public.ta_assistants a on a.id = h.assistant_id
  where h.student_id = p_student;
  return jsonb_build_object('assistants', v_assistants, 'current', v_current);
end;
$$;
revoke all on function public.ta_handoff_options(uuid) from public, anon;
grant execute on function public.ta_handoff_options(uuid) to authenticated;

-- Giao em cho trợ giảng. p_course (tuỳ chọn): mời em làm kiểm tra đầu vào theo khoá đó.
create or replace function public.ta_handoff_assign(p_student uuid, p_assistant uuid, p_course bigint default null)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_ta public.ta_assistants%rowtype;
  v_name text;
  v_ta_name text;
  v_assigned int := 0;
  v_invited boolean := false;
  v_done boolean;
begin
  if not public.ta_handoff_can_assign(p_student) then
    raise exception 'Không có quyền giao em này' using errcode = '42501';
  end if;
  select * into v_ta from public.ta_assistants where id = p_assistant and active;
  if v_ta.id is null or v_ta.user_id is null then
    raise exception 'Không tìm thấy trợ giảng';
  end if;
  if not exists (
    select 1 from public.ta_assistant_classes ac
    join public.user_classes uc on uc.class_id = ac.class_id and uc.user_id = p_student and uc.status = 'active'
    where ac.assistant_id = p_assistant) then
    raise exception 'Trợ giảng này chưa được gán lớp của em. Gán lớp ở trang Nhân sự trước.';
  end if;

  select coalesce(nullif(full_name, ''), 'Học sinh') into v_name from public.profiles where id = p_student;
  v_ta_name := coalesce(nullif(v_ta.short_name, ''), v_ta.full_name);

  insert into public.ta_student_handoffs (student_id, assistant_id, assigned_by)
  values (p_student, p_assistant, auth.uid())
  on conflict (student_id) do update set assistant_id = excluded.assistant_id, assigned_by = excluded.assigned_by, created_at = now();

  -- Mục đang mở (chưa ai nhận) chuyển sang trợ giảng này.
  update public.tutoring_needs
     set assigned_to = v_ta.user_id, status = 'assigned'
   where student_id = p_student and status = 'open' and assigned_to is null;
  get diagnostics v_assigned = row_count;

  if p_course is not null then
    select exists (select 1 from public.entry_diagnostics where student_id = p_student) into v_done;
    if not v_done then
      perform public.thpt_invite_entry_diagnostic(p_course, p_student);
      v_invited := true;
    end if;
  end if;

  insert into public.notifications (user_id, kind, title, body, href)
  values (v_ta.user_id, 'ta_handoff', 'Thầy giao em ' || v_name || ' cho con',
          case when v_invited then 'Em sẽ làm kiểm tra đầu vào trước. Khi em nộp bài, con mở Phiếu xuất phát của em rồi dạy theo thứ tự trong đó.'
               when v_assigned > 0 then 'Có ' || v_assigned || ' phần em đang hổng. Con mở Phiếu xuất phát của em rồi dạy theo thứ tự trong đó.'
               else 'Em chưa có phần hổng nào được ghi. Khi có, mục phụ đạo tự giao cho con.' end,
          '/tro-giang/phu-dao');

  return jsonb_build_object('assistant', v_ta_name, 'assignedNeeds', v_assigned, 'invited', v_invited);
end;
$$;
revoke all on function public.ta_handoff_assign(uuid, uuid, bigint) from public, anon;
grant execute on function public.ta_handoff_assign(uuid, uuid, bigint) to authenticated;

create or replace function public.ta_handoff_clear(p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
begin
  if not public.ta_handoff_can_assign(p_student) then
    raise exception 'Không có quyền' using errcode = '42501';
  end if;
  delete from public.ta_student_handoffs where student_id = p_student;
end;
$$;
revoke all on function public.ta_handoff_clear(uuid) from public, anon;
grant execute on function public.ta_handoff_clear(uuid) to authenticated;

-- Mục phụ đạo MỚI mở cho em đã giao thì tự gán cho trợ giảng đó.
create or replace function public.tutoring_needs_handoff_assign()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare v_user uuid;
begin
  if new.status = 'open' and new.assigned_to is null then
    select a.user_id into v_user
    from public.ta_student_handoffs h join public.ta_assistants a on a.id = h.assistant_id
    where h.student_id = new.student_id and a.active;
    if v_user is not null then
      new.assigned_to := v_user;
      new.status := 'assigned';
    end if;
  end if;
  return new;
end;
$$;
drop trigger if exists trg_tutoring_needs_handoff_assign on public.tutoring_needs;
create trigger trg_tutoring_needs_handoff_assign before insert on public.tutoring_needs
  for each row execute function public.tutoring_needs_handoff_assign();
