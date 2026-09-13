-- ============================================================
-- Phụ đạo nhiều em trong cùng một buổi
--
-- Trước: 1 buổi phụ đạo = 1 em (ghi ở class_label), hệ số quy đổi cố định 1,25.
-- Nay:   1 buổi ghi được nhiều em (ta_sessions.phudao_students), hệ số tính theo số em —
--        1,1 cho em đầu tiên, cộng thêm 0,1 cho mỗi em kế tiếp, tức 1,0 + 0,1 × số em.
--        1 em = 1,1 · 2 em = 1,2 · 3 em = 1,3 …
--
-- Công thức vẫn nằm duy nhất trong ta_converted_hours(); 4 hàm gọi nó chỉ cần truyền
-- thêm số em. Các loại buổi khác không đổi.
-- ============================================================

alter table public.ta_sessions
  add column if not exists phudao_students text[] not null default '{}';

-- Buổi phụ đạo cũ chỉ có 1 em ghi trong class_label -> đưa vào mảng để tính đúng hệ số.
update public.ta_sessions
set phudao_students = array[trim(class_label)]
where session_type = 'phudao'
  and coalesce(array_length(phudao_students, 1), 0) = 0
  and coalesce(trim(class_label), '') <> '';

-- ---------- Hệ số quy đổi ----------
drop function if exists public.ta_converted_hours(text, numeric);

create or replace function public.ta_converted_hours(
  p_session_type text,
  p_hours numeric,
  p_student_count integer default 1
)
returns numeric
language sql
immutable
as $$
  select case p_session_type
    when 'lop' then p_hours * 1.00
    -- 1,1 cho em đầu, +0,1 mỗi em kế tiếp. Buổi cũ chưa ghi danh sách coi như 1 em.
    when 'phudao' then p_hours * (1.0 + 0.1 * greatest(1, coalesce(p_student_count, 1)))
    when 'chambai' then 0
    when 'hanhchinh' then p_hours * 1.00
    when 'video' then 0
    else 0
  end;
$$;

grant execute on function public.ta_converted_hours(text, numeric, integer) to authenticated;

-- Số em của 1 buổi — dùng lại ở mọi chỗ gọi ta_converted_hours để khỏi lặp coalesce/array_length.
create or replace function public.ta_session_student_count(p_students text[])
returns integer
language sql
immutable
as $$
  select greatest(1, coalesce(array_length(p_students, 1), 0));
$$;

grant execute on function public.ta_session_student_count(text[]) to authenticated;

-- ---------- Cập nhật 4 hàm gọi ----------
create or replace function public.ta_accrued_hours(p_assistant_id uuid)
returns numeric
language plpgsql
stable
security definer
set search_path = public
as $$
begin
  if not public.is_admin() and p_assistant_id is distinct from public.ta_current_assistant_id() then
    raise exception 'không có quyền xem dữ liệu trợ giảng này';
  end if;

  return coalesce((
    select sum(public.ta_converted_hours(session_type, hours, public.ta_session_student_count(phudao_students)))
    from public.ta_sessions
    where assistant_id = p_assistant_id
      and status = 'approved'
      and session_type in ('lop', 'phudao')
  ), 0);
end;
$$;

grant execute on function public.ta_accrued_hours(uuid) to authenticated;

create or replace function public.ta_team_monthly_hours(p_months integer default 12)
returns table (month date, converted_hours numeric, session_count integer)
language plpgsql
stable
security definer
set search_path = public
as $$
begin
  if not public.is_admin() then
    raise exception 'chỉ giáo viên được xem số liệu toàn đội';
  end if;

  return query
  select
    date_trunc('month', s.work_date)::date as m,
    round(sum(public.ta_converted_hours(s.session_type, s.hours, public.ta_session_student_count(s.phudao_students))), 2),
    count(*)::int
  from public.ta_sessions s
  where s.status = 'approved'
    and s.work_date >= (date_trunc('month', current_date) - make_interval(months => p_months - 1))::date
  group by 1
  order by 1;
end;
$$;

grant execute on function public.ta_team_monthly_hours(integer) to authenticated;

create or replace function public.ta_course_total_hours()
returns numeric
language plpgsql
stable
security definer
set search_path = public
as $$
begin
  if not public.is_admin() then
    raise exception 'chỉ giáo viên được xem số liệu toàn đội';
  end if;

  return coalesce((
    select sum(public.ta_converted_hours(session_type, hours, public.ta_session_student_count(phudao_students)))
    from public.ta_sessions
    where status = 'approved'
  ), 0);
end;
$$;

grant execute on function public.ta_course_total_hours() to authenticated;

-- ta_monthly_score: chỉ đổi đúng dòng tính m_converted_hours, phần điểm giữ nguyên.
create or replace function public.ta_monthly_score(p_assistant_id uuid, p_month date)
returns table (
  assistant_id uuid,
  month date,
  lop_sessions integer,
  phudao_sessions integer,
  avg_touches numeric,
  touches_score numeric,
  ontime_error_notes integer,
  error_note_rate numeric,
  error_note_score numeric,
  complete_phudao integer,
  phudao_complete_rate numeric,
  phudao_score numeric,
  flag_count integer,
  focus_score numeric,
  total_score numeric,
  bonus_per_hour integer,
  converted_hours numeric,
  papers_graded integer,
  base_pay numeric,
  bonus_pay numeric,
  grading_pay numeric,
  total_pay numeric
)
language plpgsql
stable
security definer
set search_path = public
as $$
declare
  v_month date := date_trunc('month', p_month)::date;
  v_month_end date := (v_month + interval '1 month')::date;
  v_tier text;
  v_retained_rate integer;
  v_base_rate integer;
  v_rate numeric;
begin
  if not public.is_admin() and p_assistant_id is distinct from public.ta_current_assistant_id() then
    raise exception 'không có quyền xem dữ liệu trợ giảng này';
  end if;

  select a.tier, a.retained_rate into v_tier, v_retained_rate
  from public.ta_assistants a
  where a.id = p_assistant_id;

  select r.base_rate into v_base_rate
  from public.ta_rates r
  where r.tier = v_tier and r.effective_from <= v_month
  order by r.effective_from desc
  limit 1;

  v_rate := coalesce(v_retained_rate, v_base_rate, 0);

  return query
  with sess as (
    select s.*
    from public.ta_sessions s
    where s.assistant_id = p_assistant_id
      and s.status = 'approved'
      and s.work_date >= v_month
      and s.work_date < v_month_end
  ),
  lop as (select * from sess where session_type = 'lop'),
  phudao_s as (select * from sess where session_type = 'phudao'),
  metrics as (
    select
      (select count(*) from lop)::int as m_lop_count,
      (select count(*) from phudao_s)::int as m_phudao_count,
      coalesce((select avg(student_touches) from lop), 0)::numeric as m_avg_touches,
      coalesce((select count(*) from lop
                where error_note_at is not null and error_note_at::date = work_date), 0)::int as m_ontime,
      coalesce((select count(*) from phudao_s
                where homework_given is not null and length(trim(homework_given)) > 0
                  and student_recap_ok = true), 0)::int as m_complete_phudao,
      coalesce((select sum(sess.papers_graded) from sess where sess.session_type = 'chambai'), 0)::int as m_papers,
      coalesce((select count(*) from public.ta_flags f
                where f.assistant_id = p_assistant_id
                  and f.flag_date >= v_month and f.flag_date < v_month_end), 0)::int as m_flags,
      coalesce((select sum(public.ta_converted_hours(session_type, hours,
                                                     public.ta_session_student_count(phudao_students)))
                from sess), 0)::numeric as m_converted_hours
  ),
  scores as (
    select
      m.*,
      least(40, 40 * m_avg_touches / 12) as s_touches,
      case when m_lop_count = 0 then 0 else 20.0 * m_ontime / m_lop_count end as s_error_note,
      case when m_phudao_count = 0 then 20 else 20.0 * m_complete_phudao / m_phudao_count end as s_phudao,
      greatest(0, 20 - 10 * m_flags) as s_focus
    from metrics m
  ),
  totals as (
    select
      sc.*,
      (sc.s_touches + sc.s_error_note + sc.s_phudao + sc.s_focus) as s_total
    from scores sc
  )
  select
    p_assistant_id,
    v_month,
    t.m_lop_count,
    t.m_phudao_count,
    round(t.m_avg_touches, 2),
    round(t.s_touches, 2),
    t.m_ontime,
    case when t.m_lop_count = 0 then 0 else round(t.m_ontime::numeric / t.m_lop_count, 4) end,
    round(t.s_error_note, 2),
    t.m_complete_phudao,
    case when t.m_phudao_count = 0 then 1 else round(t.m_complete_phudao::numeric / t.m_phudao_count, 4) end,
    round(t.s_phudao, 2),
    t.m_flags,
    round(t.s_focus::numeric, 2),
    round(t.s_total, 2),
    case when t.s_total >= 85 then 4000 when t.s_total >= 70 then 2000 else 0 end,
    round(t.m_converted_hours, 2),
    t.m_papers,
    round(t.m_converted_hours * v_rate, 0) as base_pay,
    round(t.m_converted_hours * (case when t.s_total >= 85 then 4000 when t.s_total >= 70 then 2000 else 0 end), 0) as bonus_pay,
    round(t.m_papers * 1500, 0) as grading_pay,
    round(
      t.m_converted_hours * v_rate
      + t.m_converted_hours * (case when t.s_total >= 85 then 4000 when t.s_total >= 70 then 2000 else 0 end)
      + t.m_papers * 1500
    , 0) as total_pay
  from totals t;
end;
$$;

grant execute on function public.ta_monthly_score(uuid, date) to authenticated;
