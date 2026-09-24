-- ============================================================
-- Migration: bảng tuần của lớp trên trang chủ học sinh
-- Chạy SAU: supabase-migration-rank-system.sql, supabase-migration-rank-avatar.sql
-- Idempotent — chạy lại được (create or replace function).
--
-- rank_class_board(p_class_id) trả 3 khối cho ClassRankBoard.tsx:
--   1. top_week   : 3 bạn có RP KIẾM ĐƯỢC TRONG TUẦN cao nhất (Thứ Hai – CN giờ VN), không phải RP tổng.
--   2. me         : vị trí của người gọi theo RP tuần + 1 bạn ngay trên, 1 bạn ngay dưới (không lộ cả bảng).
--   3. improved   : "Tiến bộ nhất tuần" — bạn NGOÀI top 3 có RP tuần tăng nhiều nhất so với tuần trước.
--      weekly     : ghi nhận tuần này (đạt mục tiêu tuần / lên bậc / danh hiệu), giống rank_class_groups.
-- RP tổng của từng bạn KHÔNG trả về — giữ nguyên tinh thần "cùng bậc là ngang nhau".
-- Chỉ thành viên lớp (user_classes active) hoặc GV quản lớp gọi được; ngoài ra trả null.
-- ============================================================

create or replace function public.rank_class_board(p_class_id bigint)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_me uuid := auth.uid();
  v_season bigint;
  s public.rank_seasons%rowtype;
  v_week date := public.rank_week_start(now());
  v_from timestamptz := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_prev_from timestamptz := ((v_week - 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_top jsonb;
  v_total int;
  v_me_json jsonb;
  v_improved jsonb;
  v_weekly jsonb;
begin
  if not (public.manages_class(p_class_id) or exists (
    select 1 from public.user_classes where user_id = v_me and class_id = p_class_id and status = 'active'
  )) then
    return null;
  end if;

  select rs.id into v_season from public.rank_seasons rs
  where rs.status = 'active' and public.rank_vn_date(now()) between rs.starts_on and rs.ends_on
    and (cardinality(rs.class_ids) = 0 or p_class_id = any (rs.class_ids))
  order by rs.starts_on desc limit 1;
  if v_season is null then return jsonb_build_object('season', null); end if;
  select * into s from public.rank_seasons where id = v_season;

  with members as (
    select uc.user_id, p.full_name, p.avatar_url, m.tier_code, m.division
    from public.user_classes uc
    join public.profiles p on p.id = uc.user_id
    left join public.rank_student_seasons m on m.season_id = v_season and m.student_id = uc.user_id
    where uc.class_id = p_class_id and uc.status = 'active' and p.role = 'student'
  ),
  wk as (
    select mm.*,
      coalesce((select sum(l.amount) from public.rank_rp_ledger l
                where l.season_id = v_season and l.student_id = mm.user_id and l.created_at >= v_from), 0)::int as rp_week,
      coalesce((select sum(l.amount) from public.rank_rp_ledger l
                where l.season_id = v_season and l.student_id = mm.user_id
                  and l.created_at >= v_prev_from and l.created_at < v_from), 0)::int as rp_prev
    from members mm
  ),
  ranked as (
    select w.*, rank() over (order by w.rp_week desc) as pos from wk w
  )
  select
    (select coalesce(jsonb_agg(jsonb_build_object(
        'pos', t.pos, 'name', t.full_name, 'avatar', t.avatar_url, 'rp_week', t.rp_week,
        'tier_code', t.tier_code, 'division', t.division, 'is_me', t.user_id = v_me
      ) order by t.pos, t.full_name), '[]'::jsonb)
     from (select * from ranked where rp_week > 0 order by pos, full_name limit 3) t),
    (select count(*) from ranked),
    (select jsonb_build_object(
        'pos', r.pos, 'rp_week', r.rp_week,
        'tied', (select count(*) from ranked x where x.rp_week = r.rp_week) - 1,
        'above', (select jsonb_build_object('name', x.full_name, 'avatar', x.avatar_url, 'rp_week', x.rp_week)
                  from ranked x where x.rp_week > r.rp_week order by x.rp_week asc, x.full_name limit 1),
        'below', (select jsonb_build_object('name', x.full_name, 'avatar', x.avatar_url, 'rp_week', x.rp_week)
                  from ranked x where x.rp_week < r.rp_week order by x.rp_week desc, x.full_name limit 1)
      ) from ranked r where r.user_id = v_me),
    (select jsonb_build_object('name', t.full_name, 'avatar', t.avatar_url, 'rp_week', t.rp_week, 'delta', t.rp_week - t.rp_prev)
     from ranked t where t.rp_week > 0 and t.rp_week - t.rp_prev > 0 and t.pos > 3
     order by (t.rp_week - t.rp_prev) desc, t.full_name limit 1)
  into v_top, v_total, v_me_json, v_improved;

  with members as (
    select uc.user_id, p.full_name from public.user_classes uc join public.profiles p on p.id = uc.user_id
    where uc.class_id = p_class_id and uc.status = 'active' and p.role = 'student'
  ),
  ev as (
    select mm.full_name, 'weekly_goal' as kind, 'đạt mục tiêu tuần' as label, l.created_at as happened_at
    from public.rank_rp_ledger l join members mm on mm.user_id = l.student_id
    where l.season_id = v_season and l.source_kind = 'weekly_goal' and l.created_at >= v_from
    union all
    select mm.full_name, 'tier_up', 'lên bậc ' || t.name, m.tier_reached_at
    from public.rank_student_seasons m join members mm on mm.user_id = m.student_id
    join public.rank_tiers t on t.season_id = m.season_id and t.code = m.tier_code
    where m.season_id = v_season and m.tier_reached_at >= v_from and m.tier_sort > 1
    union all
    select mm.full_name, 'title', 'nhận danh hiệu ' || rt.name || case a.level when 'thuc_tinh' then ' · Thức Tỉnh' when 'lam_chu' then ' · Làm Chủ' when 'huyen_thoai' then ' · Huyền Thoại' else '' end, a.awarded_at
    from public.rank_title_awards a join members mm on mm.user_id = a.student_id
    join public.rank_titles rt on rt.code = a.title_code
    where a.awarded_at >= v_from
  )
  select coalesce(jsonb_agg(jsonb_build_object('name', e.full_name, 'kind', e.kind, 'label', e.label, 'at', e.happened_at) order by e.happened_at desc), '[]'::jsonb)
  into v_weekly from (select * from ev order by happened_at desc limit 20) e;

  return jsonb_build_object(
    'season', jsonb_build_object('id', s.id, 'name', s.name, 'starts_on', s.starts_on, 'ends_on', s.ends_on),
    'week_start', v_week,
    'total', v_total,
    'top_week', v_top,
    'me', v_me_json,
    'improved', v_improved,
    'weekly', v_weekly
  );
end; $$;
grant execute on function public.rank_class_board(bigint) to authenticated;
