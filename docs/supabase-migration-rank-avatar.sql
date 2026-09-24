-- ============================================================
-- Migration: avatar trong bảng "Bậc trong lớp"
-- Chạy SAU: supabase-migration-rank-system.sql, supabase-migration-avatars.sql
-- Idempotent — chạy lại được (create or replace function).
--
-- rank_class_groups() giờ trả thêm avatar_url của từng thành viên (bậc đã xếp lẫn
-- chưa nhận RP) để ClassRankGroups.tsx hiện ảnh đại diện cạnh tên.
-- ============================================================

create or replace function public.rank_class_groups(p_class_id bigint)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_season bigint;
  s public.rank_seasons%rowtype;
  v_week date := public.rank_week_start(now());
  v_from timestamptz := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_tiers jsonb;
  v_weekly jsonb;
  v_unranked jsonb;
begin
  if not (public.manages_class(p_class_id) or exists (
    select 1 from public.user_classes where user_id = auth.uid() and class_id = p_class_id and status = 'active'
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
    select uc.user_id, p.full_name, p.avatar_url, p.display_title_code, p.display_title_level, m.tier_code, m.tier_sort, m.division
    from public.user_classes uc
    join public.profiles p on p.id = uc.user_id
    left join public.rank_student_seasons m on m.season_id = v_season and m.student_id = uc.user_id
    where uc.class_id = p_class_id and uc.status = 'active' and p.role = 'student'
  )
  select
    (select jsonb_agg(jsonb_build_object('code', t.code, 'name', t.name, 'sort', t.sort,
        'members', (select coalesce(jsonb_agg(jsonb_build_object('name', mm.full_name, 'avatar', mm.avatar_url, 'division', mm.division,
                        'title', (select jsonb_build_object('name', rt.name, 'level', mm.display_title_level) from public.rank_titles rt where rt.code = mm.display_title_code))
                        order by mm.full_name), '[]'::jsonb)
                    from members mm where mm.tier_code = t.code)) order by t.sort desc)
     from public.rank_tiers t where t.season_id = v_season),
    (select coalesce(jsonb_agg(jsonb_build_object('name', mm.full_name, 'avatar', mm.avatar_url) order by mm.full_name), '[]'::jsonb) from members mm where mm.tier_code is null)
  into v_tiers, v_unranked;

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
  into v_weekly from (select * from ev order by happened_at desc limit 40) e;

  return jsonb_build_object(
    'season', jsonb_build_object('id', s.id, 'name', s.name, 'starts_on', s.starts_on, 'ends_on', s.ends_on),
    'tiers', coalesce(v_tiers, '[]'::jsonb),
    'unranked', v_unranked,
    'weekly', v_weekly,
    'week_start', v_week
  );
end; $$;
grant execute on function public.rank_class_groups(bigint) to authenticated;
