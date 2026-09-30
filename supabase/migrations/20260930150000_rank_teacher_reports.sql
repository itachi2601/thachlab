-- ============================================================================
-- GĐ 1b #9 + #10 — báo cáo cho thầy (30/9/2026). Chỉ thêm 2 hàm ĐỌC, không đổi bảng/dữ liệu.
--
-- rank_monday_list(p_class_id): "Danh sách thứ Hai" của lớp cho tuần VỪA QUA (Thứ Hai–Chủ Nhật giờ VN):
--   level_ups — tối đa 5 em có nhiều "lên mức" nhất (nhận danh hiệu/mức danh hiệu mới, lên bậc) để thầy nhắc tên trong lớp;
--   improved  — tối đa 5 em tiến bộ nhất (tăng tỉ lệ đúng so với 2 tuần trước đó của chính em, dùng rank_progress_calc,
--               cần >= 15 câu ở mỗi mốc như luật "tiến bộ tuần").
--   Chỉ admin / giảng viên phụ trách lớp (manages_class).
--
-- rank_quartile_metrics(p_season): đo nhóm 25% THẤP NHẤT của mùa — nhóm chọn theo tỉ lệ đúng của 28 ngày TRƯỚC khi mở mùa
--   (em có >= 10 câu; em chưa có mốc bị tách riêng "no_baseline"). Với mỗi nhóm (bottom / rest) trả:
--   n · active_season (còn làm bài lần nào trong mùa) · active_w45 (còn làm bài ở tuần 4–5 kể từ ngày mở mùa; null nếu chưa tới)
--   · with_badge (nhận >= 1 huy hiệu trong mùa) · cleared (thoát >= 1 chủ đề phụ đạo trong mùa).
--   Ba số hệ giữ chân nhóm dưới: active_w45, with_badge, cleared của "bottom" — nếu không nhúc nhích so với "rest" là hệ đang nới khoảng cách.
--   Chỉ admin / giảng viên (không trợ giảng).
--
-- Cách chạy: bash scripts/run-migrations.sh — giờ nào cũng được. Rollback: perf/rollback/20260930150000_rank_teacher_reports.down.sql
-- ============================================================================

create or replace function public.rank_monday_list(p_class_id bigint)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_week date := public.rank_week_start(now()) - 7;
  v_from timestamptz := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to timestamptz := ((v_week + 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_min_q int := 15;
  v_up jsonb;
  v_imp jsonb;
begin
  if not public.manages_class(p_class_id) then return null; end if;

  with members as (
    select uc.user_id, p.full_name
    from public.user_classes uc join public.profiles p on p.id = uc.user_id
    where uc.class_id = p_class_id and uc.status = 'active' and p.role = 'student'
  ),
  ev as (
    select mm.user_id, mm.full_name,
      rt.name || case a.level when 'thuc_tinh' then ' · Thức Tỉnh' when 'lam_chu' then ' · Làm Chủ'
                              when 'huyen_thoai' then ' · Huyền Thoại' else '' end as item
    from public.rank_title_awards a
    join members mm on mm.user_id = a.student_id
    join public.rank_titles rt on rt.code = a.title_code
    where a.awarded_at >= v_from and a.awarded_at < v_to
    union all
    select mm.user_id, mm.full_name, 'Lên bậc ' || t.name
    from public.rank_student_seasons m
    join members mm on mm.user_id = m.student_id
    join public.rank_tiers t on t.season_id = m.season_id and t.code = m.tier_code
    where m.tier_reached_at >= v_from and m.tier_reached_at < v_to and m.tier_sort > 1
  ),
  agg as (
    select user_id, full_name, count(*) as n, jsonb_agg(item order by item) as items
    from ev group by user_id, full_name
  )
  select coalesce(jsonb_agg(jsonb_build_object('student_id', x.user_id, 'name', x.full_name, 'count', x.n, 'items', x.items)
                            order by x.n desc, x.full_name), '[]'::jsonb)
  into v_up
  from (select * from agg order by n desc, full_name limit 5) x;

  with members as (
    select uc.user_id, p.full_name
    from public.user_classes uc join public.profiles p on p.id = uc.user_id
    where uc.class_id = p_class_id and uc.status = 'active' and p.role = 'student'
  ),
  calc as (
    select mm.user_id, mm.full_name, c.acc_now, c.acc_base, c.gain
    from members mm
    cross join lateral public.rank_progress_calc(mm.user_id, v_week) c
    where c.q_now >= v_min_q and c.q_base >= v_min_q and c.gain is not null and c.gain > 0
  )
  select coalesce(jsonb_agg(jsonb_build_object('student_id', x.user_id, 'name', x.full_name,
           'acc_now', x.acc_now, 'acc_base', x.acc_base, 'gain', x.gain) order by x.gain desc, x.full_name), '[]'::jsonb)
  into v_imp
  from (select * from calc order by gain desc, full_name limit 5) x;

  return jsonb_build_object('week_start', v_week, 'week_end', v_week + 6, 'level_ups', v_up, 'improved', v_imp);
end; $$;
revoke all on function public.rank_monday_list(bigint) from public, anon;
grant execute on function public.rank_monday_list(bigint) to authenticated;

create or replace function public.rank_quartile_metrics(p_season bigint)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  s public.rank_seasons%rowtype;
  v_from timestamptz;
  v_to timestamptz;
  v_base_from timestamptz;
  v_w4_from timestamptz;
  v_w4_to timestamptz;
  v_out jsonb;
begin
  if not exists (select 1 from public.profiles where id = auth.uid() and role in ('admin', 'instructor')) then
    return null;
  end if;
  select * into s from public.rank_seasons where id = p_season;
  if s.id is null then return null; end if;

  v_from := (s.starts_on::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to := ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_base_from := ((s.starts_on - 28)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_w4_from := ((s.starts_on + 21)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_w4_to := (least(s.starts_on + 35, s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh';

  with cohort as (
    select distinct uc.user_id as id
    from public.user_classes uc join public.profiles p on p.id = uc.user_id
    where uc.status = 'active' and p.role = 'student'
      and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids))
  ),
  base as (
    select c.id,
      (select sum(coalesce(r.earned, 0)) / nullif(sum(r.max), 0) from (
         select earned, max from public.exam_question_results
         where student_id = c.id and created_at >= v_base_from and created_at < v_from and max > 0 and qtype is distinct from 'essay'
         union all
         select earned, max from public.practice_question_results
         where student_id = c.id and created_at >= v_base_from and created_at < v_from and max > 0 and qtype is distinct from 'essay'
       ) r) as acc,
      (select count(*) from (
         select 1 from public.exam_question_results
         where student_id = c.id and created_at >= v_base_from and created_at < v_from and max > 0 and qtype is distinct from 'essay'
         union all
         select 1 from public.practice_question_results
         where student_id = c.id and created_at >= v_base_from and created_at < v_from and max > 0 and qtype is distinct from 'essay'
       ) q) as n
    from cohort c
  ),
  grp as (
    select b.id,
      case when b.n < 10 or b.acc is null then 'no_baseline'
           when ntile(4) over (partition by (b.n >= 10 and b.acc is not null) order by b.acc) = 1 then 'bottom'
           else 'rest' end as g
    from base b
  ),
  m as (
    select g.g, g.id,
      exists (select 1 from public.exam_results er where er.student_id = g.id and er.created_at >= v_from and er.created_at < v_to
              union all select 1 from public.practice_sessions ps where ps.student_id = g.id and ps.created_at >= v_from and ps.created_at < v_to) as act_season,
      exists (select 1 from public.exam_results er where er.student_id = g.id and er.created_at >= v_w4_from and er.created_at < v_w4_to
              union all select 1 from public.practice_sessions ps where ps.student_id = g.id and ps.created_at >= v_w4_from and ps.created_at < v_w4_to) as act_w45,
      exists (select 1 from public.rank_title_awards a where a.student_id = g.id and a.awarded_at >= v_from and a.awarded_at < v_to) as badge,
      exists (select 1 from public.tutoring_needs n where n.student_id = g.id and n.status = 'cleared' and n.cleared_at >= v_from and n.cleared_at < v_to) as cleared
    from grp g
  )
  select jsonb_build_object(
    'season_id', s.id, 'starts_on', s.starts_on, 'ends_on', s.ends_on,
    'w45_ready', now() >= v_w4_from,
    'baseline', 'tỉ lệ đúng 28 ngày trước ngày mở mùa (>= 10 câu)',
    'groups', coalesce((
      select jsonb_object_agg(x.g, x.j) from (
        select m.g, jsonb_build_object(
          'n', count(*),
          'active_season', count(*) filter (where act_season),
          'active_w45', case when now() >= v_w4_from then count(*) filter (where act_w45) end,
          'with_badge', count(*) filter (where badge),
          'cleared', count(*) filter (where cleared)) as j
        from m group by m.g) x), '{}'::jsonb))
  into v_out;
  return v_out;
end; $$;
revoke all on function public.rank_quartile_metrics(bigint) from public, anon;
grant execute on function public.rank_quartile_metrics(bigint) to authenticated;
