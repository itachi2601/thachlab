-- ============================================================================
-- 14/10/2026 — Buổi phụ đạo nối với em, phiếu và bài kiểm tra bằng khoá thật (thầy chốt 14/10)
--
--   * tutoring_registrations.attended: trợ giảng điểm danh có mặt/vắng từng em (RPC tutoring_mark_attendance),
--     chỉ khi buổi đã bắt đầu. Em vắng không vào phiếu, không vào bài kiểm tra cuối buổi.
--   * ta_sessions.slot_id: phiếu ghi buổi trỏ về buổi trong lịch. Phiếu có slot_id phải đúng trợ giảng, đúng ngày,
--     và chỉ gồm em đã đăng ký + có mặt. Mỗi buổi chỉ có một phiếu (trừ phiếu bị trả về).
--   * tutoring_exit_windows.slot_id: bài kiểm tra cuối buổi thuộc buổi nào; chỉ mở cho em có mặt của buổi đó.
--   * RPC tutoring_followup_report(lớp, số ngày): mỗi dòng = em × chủ đề đã đăng ký → có mặt → kiểm tra → khắc phục.
--     Chỉ thầy/quản trị đọc được.
-- Chỉ thêm cột/hàm/trigger; dữ liệu cũ giữ nguyên (slot_id rỗng = phiếu kiểu cũ). Chạy giờ nào cũng được.
-- Phụ thuộc: 20261014100000_phu_dao_dang_ky_theo_chu_de.sql
-- Rollback: perf/rollback/20261014110000_phu_dao_diem_danh_noi_phieu.down.sql
-- ============================================================================

alter table public.tutoring_registrations
  add column if not exists attended boolean,
  add column if not exists attended_at timestamptz;

alter table public.ta_sessions
  add column if not exists slot_id bigint references public.tutoring_slots (id) on delete set null;
create unique index if not exists ta_sessions_slot_unique
  on public.ta_sessions (slot_id) where slot_id is not null and status <> 'rejected';

alter table public.tutoring_exit_windows
  add column if not exists slot_id bigint references public.tutoring_slots (id) on delete set null;

-- Điểm danh: chỉ trợ giảng phụ trách buổi (hoặc quản trị), và chỉ khi buổi đã bắt đầu (giờ Việt Nam).
create or replace function public.tutoring_mark_attendance(p_slot_id bigint, p_student_id uuid, p_attended boolean)
returns void
language plpgsql security definer set search_path = public
as $$
declare s public.tutoring_slots;
begin
  select * into s from public.tutoring_slots where id = p_slot_id;
  if not found then raise exception 'Không tìm thấy buổi phụ đạo.'; end if;
  if not (
    exists (select 1 from public.ta_assistants a where a.id = s.assistant_id and a.user_id = auth.uid())
    or public.is_admin()
  ) then
    raise exception 'Chỉ trợ giảng phụ trách buổi này mới điểm danh.';
  end if;
  if ((s.work_date + s.start_time) at time zone 'Asia/Ho_Chi_Minh') > now() then
    raise exception 'Buổi chưa bắt đầu, chưa điểm danh được.';
  end if;
  update public.tutoring_registrations
    set attended = p_attended, attended_at = now()
    where slot_id = p_slot_id and student_id = p_student_id;
  if not found then raise exception 'Em này không có trong danh sách đăng ký của buổi.'; end if;
end; $$;
revoke all on function public.tutoring_mark_attendance(bigint, uuid, boolean) from public, anon;
grant execute on function public.tutoring_mark_attendance(bigint, uuid, boolean) to authenticated;

-- Phiếu có slot_id: đúng trợ giảng, loại phụ đạo, đúng ngày buổi, mọi em đều đã đăng ký + có mặt.
create or replace function public.ta_session_slot_guard()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  s public.tutoring_slots;
  bad int;
begin
  if new.slot_id is null then return new; end if;
  select * into s from public.tutoring_slots where id = new.slot_id;
  if not found then raise exception 'Không tìm thấy buổi phụ đạo trong lịch.'; end if;
  if s.assistant_id <> new.assistant_id then raise exception 'Buổi này của trợ giảng khác.'; end if;
  if new.session_type <> 'phudao' then raise exception 'Chỉ phiếu phụ đạo mới nối được với buổi trong lịch.'; end if;
  if new.work_date <> s.work_date then raise exception 'Ngày ghi phiếu phải trùng ngày buổi trong lịch.'; end if;
  select count(*) into bad
    from unnest(coalesce(new.phudao_student_ids, '{}')) sid
    where not exists (
      select 1 from public.tutoring_registrations r
      where r.slot_id = new.slot_id and r.student_id = sid and r.attended is true
    );
  if bad > 0 then
    raise exception 'Phiếu chỉ được ghi các em đã đăng ký buổi và được điểm danh có mặt.';
  end if;
  return new;
end; $$;
drop trigger if exists trg_ta_session_slot_guard on public.ta_sessions;
create trigger trg_ta_session_slot_guard before insert or update of slot_id, phudao_student_ids, work_date, session_type
  on public.ta_sessions
  for each row execute function public.ta_session_slot_guard();

-- Bài kiểm tra cuối buổi thuộc buổi nào: chỉ mở cho em có mặt, trong ngày của buổi, đúng trợ giảng.
create or replace function public.tutoring_exit_window_slot_guard()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  s public.tutoring_slots;
  bad int;
begin
  if new.slot_id is null then return new; end if;
  select * into s from public.tutoring_slots where id = new.slot_id;
  if not found then raise exception 'Không tìm thấy buổi phụ đạo trong lịch.'; end if;
  if s.assistant_id <> new.assistant_id then raise exception 'Buổi này của trợ giảng khác.'; end if;
  if s.work_date <> (now() at time zone 'Asia/Ho_Chi_Minh')::date then
    raise exception 'Chỉ mở bài kiểm tra cuối buổi trong ngày diễn ra buổi.';
  end if;
  select count(*) into bad
    from unnest(new.student_ids) sid
    where not exists (
      select 1 from public.tutoring_registrations r
      where r.slot_id = new.slot_id and r.student_id = sid and r.attended is true
    );
  if bad > 0 then
    raise exception 'Chỉ mở bài kiểm tra cho các em đã được điểm danh có mặt.';
  end if;
  return new;
end; $$;
drop trigger if exists trg_tutoring_exit_window_slot_guard on public.tutoring_exit_windows;
create trigger trg_tutoring_exit_window_slot_guard before insert on public.tutoring_exit_windows
  for each row execute function public.tutoring_exit_window_slot_guard();

-- Bảng theo dõi cho thầy: em × chủ đề đã đăng ký trong N ngày gần đây.
create or replace function public.tutoring_followup_report(p_class_id bigint, p_days int default 30)
returns table (
  registration_id bigint, slot_id bigint, work_date date, start_time time, assistant_name text,
  student_id uuid, student_name text, topic_id bigint, topic_name text,
  attended boolean, has_session boolean,
  best_pct int, attempts int, passed boolean, cleared boolean
)
language plpgsql stable security definer set search_path = public
as $$
begin
  if not (public.is_admin() or public.manages_class(p_class_id)) then
    raise exception 'Chỉ thầy cô của lớp xem được bảng theo dõi phụ đạo.';
  end if;
  return query
  select r.id, s.id, s.work_date, s.start_time, a.short_name,
         r.student_id, p.full_name, t.id, t.name,
         r.attended,
         exists (select 1 from public.ta_sessions ts where ts.slot_id = s.id and ts.status <> 'rejected'),
         coalesce(x.best, 0), coalesce(x.n, 0), coalesce(x.ok, false),
         exists (select 1 from public.tutoring_needs n
                 where n.student_id = r.student_id and n.topic_id = t.id and n.status = 'cleared'
                   and n.cleared_at >= (s.work_date + s.start_time) at time zone 'Asia/Ho_Chi_Minh')
  from public.tutoring_slots s
  join public.tutoring_registrations r on r.slot_id = s.id
  join public.ta_assistants a on a.id = s.assistant_id
  join public.profiles p on p.id = r.student_id
  cross join lateral unnest(case when cardinality(r.topic_ids) = 0 then array[null::bigint] else r.topic_ids end) as u(tid)
  left join public.question_topics t on t.id = u.tid
  left join lateral (
    select max(e.pct)::int as best, count(*)::int as n, bool_or(e.passed) as ok
    from public.tutoring_exit_attempts e
    where e.student_id = r.student_id and e.topic_id = t.id
      and e.created_at >= (s.work_date + s.start_time) at time zone 'Asia/Ho_Chi_Minh'
  ) x on true
  where s.class_id = p_class_id and s.status = 'open'
    and s.work_date >= current_date - p_days
  order by s.work_date desc, s.start_time desc, p.full_name;
end; $$;
revoke all on function public.tutoring_followup_report(bigint, int) from public, anon;
grant execute on function public.tutoring_followup_report(bigint, int) to authenticated;
