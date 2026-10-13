-- ============================================================================
-- 13/10/2026 — Bổ sung cho 20261013230000: danh sách khoá mà người gọi được ghi tiến trình dạy
-- (thầy phụ trách khối / admin / trợ giảng được phân công), kèm LỊCH TUẦN đã đăng, vì policy thpt_courses
-- không cho trợ giảng đọc khoá không công khai. Chỉ thêm hàm, không đụng dữ liệu.
-- Rollback: cuối file.
-- ============================================================================

begin;

create or replace function public.teaching_courses(p_class bigint default null)
returns jsonb
language sql stable security definer set search_path = public
as $$
  select coalesce(jsonb_agg(jsonb_build_object(
    'id', c.id, 'name', c.name, 'classId', c.class_id, 'className', cl.name,
    'schoolYear', c.school_year, 'status', c.status, 'startsAt', c.starts_at, 'endsAt', c.ends_at,
    'currentTopicId', c.current_topic_id,
    'schedules', coalesce((
      select jsonb_agg(jsonb_build_object('weekday', s.weekday, 'start', s.start_time, 'end', s.end_time, 'location', s.location)
                       order by s.weekday, s.start_time)
      from public.thpt_course_schedules s where s.course_id = c.id
    ), '[]'::jsonb)
  ) order by (c.status = 'active') desc, c.created_at desc), '[]'::jsonb)
  from public.thpt_courses c
  join public.classes cl on cl.id = c.class_id
  where public.can_edit_teaching(c.class_id)
    and (p_class is null or c.class_id = p_class);
$$;
revoke all on function public.teaching_courses(bigint) from public, anon;
grant execute on function public.teaching_courses(bigint) to authenticated;

commit;

-- ROLLBACK: drop function if exists public.teaching_courses(bigint);
