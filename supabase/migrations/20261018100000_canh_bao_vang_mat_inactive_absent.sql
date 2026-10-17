-- DT-07 (docs/thachlab-design-thinking-audit.md): thêm 2 loại cảnh báo sớm cho giáo viên/trợ giảng vào student_alerts.
--
--   inactive_7d   — học sinh không hoạt động >= 7 ngày (urgent từ 14 ngày). "Hoạt động" = lần mới nhất của
--                   đăng nhập, student_learning_presence, nộp đề, buổi luyện tập, tiến độ bài, learning_events.
--                   Tài khoản mới hơn 7 ngày không bị tính.
--   absent_streak — vắng (status='absent', KHÔNG tính excused) từ 3 buổi điểm danh THPT gần nhất liên tiếp.
--                   Buổi chưa có bản ghi của em đó bị bỏ qua (không đoán là vắng).
--
-- sweep_engagement_alerts(p_class, p_days, p_absent_min):
--   * p_class = null → quét mọi lớp; chỉ admin hoặc pg_cron (không có auth.uid()) được gọi.
--   * p_class có giá trị → cần manages_class(p_class), dùng cho nút "Rà lại" trên dashboard.
--   * Tự đóng ('resolved') cảnh báo còn 'open' khi em đã hoạt động lại / đi học lại; mở lại cảnh báo đã
--     resolved, hoặc dismissed quá 14 ngày, nếu vẫn thoả điều kiện. Cảnh báo contacted/tutoring giữ nguyên.
--   * Cảnh báo này chỉ giáo viên thấy: policy hiện có cho HS chỉ đọc cảnh báo status <> 'open' (không đổi).
-- Lịch pg_cron 6:00 VN hằng ngày (nếu bật được). Rollback ở cuối file.

alter table public.student_alerts drop constraint if exists student_alerts_kind_check;
alter table public.student_alerts add constraint student_alerts_kind_check
  check (kind in ('low_score_streak', 'missed_assessment', 'exam_violation', 'inactive_7d', 'absent_streak'));

create or replace function public.sweep_engagement_alerts(
  p_class bigint default null,
  p_days int default 7,
  p_absent_min int default 3
)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_inactive int := 0;
  v_absent int := 0;
  v_closed int := 0;
  r record;
begin
  if p_class is null then
    if auth.uid() is not null and not public.is_admin() then
      raise exception 'Chỉ admin được rà toàn bộ lớp' using errcode = '42501';
    end if;
  elsif not public.manages_class(p_class) then
    raise exception 'Không có quyền với lớp này' using errcode = '42501';
  end if;

  p_days := greatest(3, least(coalesce(p_days, 7), 60));
  p_absent_min := greatest(2, least(coalesce(p_absent_min, 3), 10));

  -- ---------- inactive_7d ----------
  drop table if exists _sweep_act;
  create temp table _sweep_act on commit drop as
  select uc.class_id, uc.user_id as student_id,
    greatest(
      u.last_sign_in_at,
      (select slp.last_seen_at from public.student_learning_presence slp where slp.student_id = uc.user_id),
      (select max(er.created_at) from public.exam_results er where er.student_id = uc.user_id),
      (select max(ps.created_at) from public.practice_sessions ps where ps.student_id = uc.user_id),
      (select max(lp.done_at) from public.lesson_progress lp where lp.user_id = uc.user_id),
      (select max(le.occurred_at) from public.learning_events le where le.student_id = uc.user_id)
    ) as last_active
  from public.user_classes uc
  join public.profiles p on p.id = uc.user_id and p.role = 'student'
  left join auth.users u on u.id = uc.user_id
  where uc.status = 'active'
    and coalesce(u.email, '') not like '%@thachlab.local' -- bỏ tài khoản HS Test
    and (p_class is null or uc.class_id = p_class)
    and p.created_at < now() - make_interval(days => p_days);

  for r in
    select distinct on (student_id) student_id, class_id, last_active
    from _sweep_act
    where last_active is null or last_active < now() - make_interval(days => p_days)
    order by student_id, class_id
  loop
    insert into public.student_alerts (student_id, class_id, kind, severity, reason, status)
    values (
      r.student_id, r.class_id, 'inactive_7d',
      case when r.last_active is null or r.last_active < now() - interval '14 days' then 'urgent' else 'warning' end,
      case when r.last_active is null then 'Chưa có hoạt động nào được ghi nhận.'
           else 'Chưa hoạt động ' || (current_date - (r.last_active at time zone 'Asia/Ho_Chi_Minh')::date)
                || ' ngày (lần cuối ' || to_char(r.last_active at time zone 'Asia/Ho_Chi_Minh', 'DD/MM') || ').' end,
      'open'
    )
    on conflict (student_id, kind) do update set
      severity = excluded.severity,
      reason = excluded.reason,
      class_id = coalesce(excluded.class_id, student_alerts.class_id),
      updated_at = now(),
      status = case when student_alerts.status = 'resolved'
                      or (student_alerts.status = 'dismissed' and student_alerts.updated_at < now() - interval '14 days')
                    then 'open' else student_alerts.status end,
      handled_note = case when student_alerts.status = 'resolved'
                      or (student_alerts.status = 'dismissed' and student_alerts.updated_at < now() - interval '14 days')
                    then '' else student_alerts.handled_note end;
    v_inactive := v_inactive + 1;
  end loop;

  update public.student_alerts sa
    set status = 'resolved', updated_at = now(),
        handled_note = case when sa.handled_note = '' then 'tự đóng: đã hoạt động lại' else sa.handled_note end
  where sa.kind = 'inactive_7d' and sa.status = 'open'
    and exists (
      select 1 from _sweep_act a
      where a.student_id = sa.student_id and a.last_active >= now() - make_interval(days => p_days)
    );
  get diagnostics v_closed = row_count;

  -- ---------- absent_streak ----------
  for r in
    with recent as (
      select ts.class_id, tr.student_id, tr.status,
             row_number() over (partition by ts.class_id, tr.student_id order by ts.session_date desc, ts.id desc) as rn
      from public.thpt_attendance_sessions ts
      join public.thpt_attendance_records tr on tr.session_id = ts.id
      where p_class is null or ts.class_id = p_class
    )
    select class_id, student_id, count(*) as n
    from recent
    where rn <= p_absent_min
    group by class_id, student_id
    having count(*) = p_absent_min and bool_and(status = 'absent')
  loop
    insert into public.student_alerts (student_id, class_id, kind, severity, reason, status)
    values (
      r.student_id, r.class_id, 'absent_streak',
      case when r.n >= 4 then 'urgent' else 'warning' end,
      'Vắng ' || r.n || ' buổi điểm danh gần nhất liên tiếp (không phép).',
      'open'
    )
    on conflict (student_id, kind) do update set
      severity = excluded.severity,
      reason = excluded.reason,
      class_id = coalesce(excluded.class_id, student_alerts.class_id),
      updated_at = now(),
      status = case when student_alerts.status = 'resolved'
                      or (student_alerts.status = 'dismissed' and student_alerts.updated_at < now() - interval '14 days')
                    then 'open' else student_alerts.status end,
      handled_note = case when student_alerts.status = 'resolved'
                      or (student_alerts.status = 'dismissed' and student_alerts.updated_at < now() - interval '14 days')
                    then '' else student_alerts.handled_note end;
    v_absent := v_absent + 1;
  end loop;

  -- đóng khi buổi gần nhất của em đã có mặt/trễ/có phép
  update public.student_alerts sa
    set status = 'resolved', updated_at = now(),
        handled_note = case when sa.handled_note = '' then 'tự đóng: đã đi học lại' else sa.handled_note end
  where sa.kind = 'absent_streak' and sa.status = 'open'
    and (p_class is null or sa.class_id = p_class)
    and (
      select tr.status
      from public.thpt_attendance_records tr
      join public.thpt_attendance_sessions ts on ts.id = tr.session_id
      where tr.student_id = sa.student_id and ts.class_id = sa.class_id
      order by ts.session_date desc, ts.id desc
      limit 1
    ) is distinct from 'absent';

  return jsonb_build_object('inactive', v_inactive, 'absent', v_absent, 'closedInactive', v_closed);
end;
$$;
revoke all on function public.sweep_engagement_alerts(bigint, int, int) from public, anon;
grant execute on function public.sweep_engagement_alerts(bigint, int, int) to authenticated;

do $$
begin
  begin
    create extension if not exists pg_cron;
  exception when others then
    raise notice 'pg_cron không bật được (%): gọi tay select public.sweep_engagement_alerts(); mỗi tuần', sqlerrm;
  end;
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'engagement-alerts-sweep';
    perform cron.schedule('engagement-alerts-sweep', '0 23 * * *', 'select public.sweep_engagement_alerts();');
    raise notice 'Đã đặt lịch pg_cron engagement-alerts-sweep (6:00 VN hằng ngày)';
  end if;
end $$;

-- ---------- ROLLBACK ----------
-- do $$ begin
--   if exists (select 1 from pg_extension where extname = 'pg_cron') then
--     perform cron.unschedule(jobid) from cron.job where jobname = 'engagement-alerts-sweep';
--   end if;
-- end $$;
-- drop function if exists public.sweep_engagement_alerts(bigint, int, int);
-- delete from public.student_alerts where kind in ('inactive_7d', 'absent_streak');
-- alter table public.student_alerts drop constraint if exists student_alerts_kind_check;
-- alter table public.student_alerts add constraint student_alerts_kind_check
--   check (kind in ('low_score_streak', 'missed_assessment', 'exam_violation'));
