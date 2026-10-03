-- Trang phụ huynh: (1) cho phụ huynh ĐỌC thông báo lớp của con (bài tập về nhà, việc hôm nay) —
-- trước đây policy chỉ cho học sinh đang active trong lớp nên khối "Bài tập về nhà" ở /phu-huynh
-- luôn rỗng; (2) RPC điểm danh theo buổi cho phụ huynh (bảng thpt_attendance_* chỉ cho chính học sinh đọc).
-- Chỉ ĐỌC, không đổi dữ liệu. Chạy lúc nào cũng được (không khoá bảng lâu).
-- Rollback: perf/rollback/20261003130000_parent_attendance_announcements.down.sql

drop policy if exists "parents read child class announcements" on public.class_announcements;
create policy "parents read child class announcements" on public.class_announcements
  as permissive
  for select
  to authenticated
  using (exists (
    select 1
    from public.user_classes uc
    where uc.class_id = class_announcements.class_id
      and uc.status = 'active'
      and public.is_parent_of(uc.user_id)
  ));

-- Các buổi điểm danh gần nhất của một học sinh (mọi lớp em đang active). Buổi chưa có bản ghi của em
-- trả status = null để giao diện KHÔNG đếm là vắng. Người được gọi: chính em, giáo viên của em, phụ huynh đã nhận mã.
create or replace function public.parent_attendance_summary(p_student uuid, p_limit integer default 40)
returns table(session_id bigint, session_date date, title text, status text)
language plpgsql
stable
security definer
set search_path to 'public'
as $function$
begin
  if p_student is null then
    return;
  end if;
  if not (
    p_student = (select auth.uid())
    or public.teaches_student(p_student)
    or public.is_parent_of(p_student)
  ) then
    return;
  end if;

  return query
  select s.id, s.session_date, s.title, r.status
  from public.thpt_attendance_sessions s
  join public.user_classes uc
    on uc.class_id = s.class_id and uc.user_id = p_student and uc.status = 'active'
  left join public.thpt_attendance_records r
    on r.session_id = s.id and r.student_id = p_student
  order by s.session_date desc, s.id desc
  limit greatest(1, least(coalesce(p_limit, 40), 200));
end;
$function$;

revoke all on function public.parent_attendance_summary(uuid, integer) from public;
grant execute on function public.parent_attendance_summary(uuid, integer) to authenticated;

-- ROLLBACK (đã chép sang perf/rollback/20261003130000_parent_attendance_announcements.down.sql):
-- drop function if exists public.parent_attendance_summary(uuid, integer);
-- drop policy if exists "parents read child class announcements" on public.class_announcements;
