-- ============================================================================
-- 17/10/2026 — Trợ giảng giao BTVN trên web cho TỪNG EM / NHÓM (thay vì báo miệng trên lớp)
--
-- Đã có: BTVN cả lớp qua class_announcements (kèm exam_id, chuông 'homework_new').
-- Còn thiếu: giao riêng cho vài em vừa kèm phụ đạo, theo đúng chủ đề em hổng.
--
--  1. ta_homework_assignments: một dòng = một em × một đề (giao lại thì cập nhật hạn/ghi chú và đặt lại mốc "đã làm").
--     Bảng chỉ truy cập qua hàm bên dưới (RLS bật, thu quyền anon/authenticated).
--  2. ta_homework_assign(): trợ giảng/giáo viên của lớp giao; kiểm em đang học lớp đó và mở được đề; báo chuông CHỈ cho các em được giao.
--  3. my_pending_homework(): học sinh xem bài còn phải làm. "Đã làm" = có exam_results của em cho đề đó SAU lúc giao
--     (một nguồn duy nhất, không có cờ tay nên không thể lệch với bài nộp thật).
--  4. ta_homework_overview(): trợ giảng/thầy xem em nào đã làm, điểm, trễ hạn.
--
-- Chạy: bash scripts/run-migrations.sh — giờ nào cũng được (chỉ thêm bảng + hàm, không đổi dữ liệu cũ).
-- Rollback: perf/rollback/20261017180000_ta_giao_btvn_rieng.down.sql
-- ============================================================================
begin;

create table if not exists public.ta_homework_assignments (
  id bigint generated always as identity primary key,
  class_id bigint not null references public.classes (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  exam_id bigint not null references public.exams (id) on delete cascade,
  note text not null default '' check (length(note) <= 500),
  due_at timestamptz,
  assigned_by uuid not null references public.profiles (id) on delete cascade,
  created_at timestamptz not null default now(),
  unique (student_id, exam_id)
);
create index if not exists ta_homework_assignments_student_idx on public.ta_homework_assignments (student_id, created_at desc);
create index if not exists ta_homework_assignments_class_idx on public.ta_homework_assignments (class_id, created_at desc);

alter table public.ta_homework_assignments enable row level security;
revoke all on public.ta_homework_assignments from anon, authenticated;

-- ---------- 2. Giao bài ----------
create or replace function public.ta_homework_assign(
  p_class_id bigint,
  p_student_ids uuid[],
  p_exam_id bigint,
  p_due_at timestamptz default null,
  p_note text default ''
) returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_title text;
  v_n int := 0;
  v_student uuid;
  v_note text := left(coalesce(trim(p_note), ''), 500);
begin
  if v_uid is null then raise exception 'Chưa đăng nhập'; end if;
  if not (public.manages_class(p_class_id) or public.assists_class(p_class_id) or public.is_admin()) then
    raise exception 'Bạn không phụ trách lớp này';
  end if;
  if p_student_ids is null or cardinality(p_student_ids) < 1 then raise exception 'Chọn ít nhất 1 em'; end if;
  if cardinality(p_student_ids) > 40 then raise exception 'Tối đa 40 em mỗi lần giao'; end if;
  if p_due_at is not null and p_due_at < now() - interval '1 hour' then raise exception 'Hạn nộp đã qua'; end if;

  select e.title into v_title from public.exams e where e.id = p_exam_id and e.published = true;
  if v_title is null then raise exception 'Đề không tồn tại hoặc chưa công bố'; end if;

  foreach v_student in array (select array(select distinct unnest(p_student_ids))) loop
    if not exists (
      select 1 from public.user_classes uc
      join public.profiles p on p.id = uc.user_id and p.role = 'student'
      where uc.user_id = v_student and uc.class_id = p_class_id and uc.status = 'active'
    ) then
      raise exception 'Có em không thuộc lớp này';
    end if;
    if not public.exam_open_to_student(p_exam_id, v_student) then
      raise exception 'Đề này không mở cho lớp của em (đề đang gán lớp khác)';
    end if;

    insert into public.ta_homework_assignments (class_id, student_id, exam_id, note, due_at, assigned_by)
    values (p_class_id, v_student, p_exam_id, v_note, p_due_at, v_uid)
    on conflict (student_id, exam_id) do update
      set class_id = excluded.class_id, note = excluded.note, due_at = excluded.due_at,
          assigned_by = excluded.assigned_by, created_at = now();

    insert into public.notifications (user_id, kind, title, body, href)
    values (
      v_student, 'ta_homework_new',
      'Bài tập về nhà: ' || v_title,
      case when p_due_at is not null
        then 'Hạn ' || to_char(p_due_at at time zone 'Asia/Ho_Chi_Minh', 'DD/MM HH24:MI') || '. ' || left(v_note, 100)
        else left(v_note, 120) end,
      '/kiem-tra/lam?id=' || p_exam_id);
    v_n := v_n + 1;
  end loop;
  return v_n;
end; $$;
revoke all on function public.ta_homework_assign(bigint, uuid[], bigint, timestamptz, text) from public, anon;
grant execute on function public.ta_homework_assign(bigint, uuid[], bigint, timestamptz, text) to authenticated;

-- ---------- 3. Học sinh: bài còn phải làm ----------
create or replace function public.my_pending_homework()
returns table (id bigint, exam_id bigint, exam_title text, due_at timestamptz, note text, assigned_at timestamptz, assigner_name text)
language sql security definer stable set search_path = public
as $$
  select a.id, a.exam_id, e.title, a.due_at, a.note, a.created_at, coalesce(p.full_name, '')
  from public.ta_homework_assignments a
  join public.exams e on e.id = a.exam_id
  left join public.profiles p on p.id = a.assigned_by
  where a.student_id = auth.uid()
    and e.published
    and public.exam_open_to_student(a.exam_id, a.student_id)
    and not exists (
      select 1 from public.exam_results r
      where r.student_id = a.student_id and r.exam_id = a.exam_id and r.created_at >= a.created_at
    )
  order by a.due_at nulls last, a.created_at
  limit 5;
$$;
revoke all on function public.my_pending_homework() from public, anon;
grant execute on function public.my_pending_homework() to authenticated;

-- ---------- 4. Trợ giảng/thầy: tổng quan ----------
create or replace function public.ta_homework_overview(p_class_id bigint, p_days int default 21)
returns table (
  id bigint, student_id uuid, student_name text, exam_id bigint, exam_title text,
  due_at timestamptz, assigned_at timestamptz, done boolean, best_score numeric, late boolean
)
language plpgsql security definer stable set search_path = public
as $$
begin
  if not (public.manages_class(p_class_id) or public.assists_class(p_class_id) or public.is_admin()) then
    raise exception 'Bạn không phụ trách lớp này';
  end if;
  return query
  select a.id, a.student_id, coalesce(p.full_name, ''), a.exam_id, e.title, a.due_at, a.created_at,
         (r.n > 0), r.best,
         (r.n = 0 and a.due_at is not null and a.due_at < now())
  from public.ta_homework_assignments a
  join public.exams e on e.id = a.exam_id
  left join public.profiles p on p.id = a.student_id
  left join lateral (
    select count(*) as n, max(x.score) as best
    from public.exam_results x
    where x.student_id = a.student_id and x.exam_id = a.exam_id and x.created_at >= a.created_at
  ) r on true
  where a.class_id = p_class_id and a.created_at >= now() - make_interval(days => greatest(p_days, 1))
  order by (r.n > 0), a.due_at nulls last, a.created_at desc;
end; $$;
revoke all on function public.ta_homework_overview(bigint, int) from public, anon;
grant execute on function public.ta_homework_overview(bigint, int) to authenticated;

commit;

-- ============ ROLLBACK (cũng nằm ở perf/rollback/20261017180000_ta_giao_btvn_rieng.down.sql) ============
-- drop function if exists public.ta_homework_overview(bigint, int);
-- drop function if exists public.my_pending_homework();
-- drop function if exists public.ta_homework_assign(bigint, uuid[], bigint, timestamptz, text);
-- drop table if exists public.ta_homework_assignments;
