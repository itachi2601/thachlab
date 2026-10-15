-- ============================================================================
-- fix(rank): Vinh danh tuần — hoà điểm không cắt theo ABC, không công khai tỉ lệ đúng (15/10/2026)
-- Rà theo góc nhìn HS 14–18 (nhạy địa vị trước bạn cùng lứa, Dahl–Steinberg):
--   1. 'improved_acc' bỏ khoá 'acc' (tỉ lệ đúng tuần này). Trang chủ là anon/công khai: khen
--      "tiến bộ" mà lộ "đạt 45%" làm em xấu hổ hơn là vui. Chỉ giữ 'gain'.
--   2. Bục (tối đa 5 bạn) và các mục hoà điểm khác xếp theo md5(user_id || tuần) thay cho full_name:
--      vẫn ổn định trong tuần, nhưng mỗi tuần một thứ tự khác → em tên V không thua mãi vì vần.
--   3. Thêm khoá 'me' (chỉ khi người gọi là HS đang đăng nhập, có mùa đang chạy):
--      { rp_week, rp_prev } — dòng "Tuần của em" chỉ em đó thấy, so với chính mình (SDT), không lộ hạng.
--      Tính cả em chọn ẩn tên (ẩn là ẩn với người khác). Gộp trong RPC sẵn có, không thêm round-trip.
-- Chỉ thay 1 hàm, không đổi bảng/quyền. Client cũ đọc 'acc' → hiện NaN nên deploy client cùng lúc
-- (client mới đã bỏ phần "đạt X%").
--
-- Cách chạy: bash scripts/run-migrations.sh
-- Rollback:  supabase db query --linked -f perf/rollback/20261015120000_vinh_danh_hoa_diem_xoay_vong.down.sql
-- ============================================================================

create or replace function public.rank_public_honor()
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_week date := public.rank_week_start(now());
  v_from timestamptz := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_prev_from timestamptz := ((v_week - 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_today date := public.rank_vn_date(now());
  v_grades jsonb;
  v_me jsonb;
  v_my_season bigint;
begin
  with cls as (
    select c.id as class_id, substring(c.name from '\d+') as grade
    from public.classes c
    where c.name ~ '\d'
  ),
  seas as (
    select cl.class_id, cl.grade, rs.id as season_id, rs.name as season_name, rs.ends_on
    from cls cl
    join lateral (
      select rs.* from public.rank_seasons rs
      where rs.status = 'active' and v_today between rs.starts_on and rs.ends_on
        and (cardinality(rs.class_ids) = 0 or cl.class_id = any (rs.class_ids))
      order by rs.starts_on desc limit 1
    ) rs on true
  ),
  members as (
    select distinct on (s.grade, uc.user_id)
      s.grade, s.season_id, uc.user_id, p.full_name, p.avatar_url, p.honor_visibility,
      p.display_title_code, p.display_title_level,
      m.tier_code, m.tier_sort, m.division, m.tier_reached_at
    from seas s
    join public.user_classes uc on uc.class_id = s.class_id and uc.status = 'active'
    join public.profiles p on p.id = uc.user_id and p.role = 'student'
    left join public.rank_student_seasons m on m.season_id = s.season_id and m.student_id = uc.user_id
    where p.honor_visibility <> 'hidden'
    order by s.grade, uc.user_id, s.season_id desc
  ),
  wk as (
    select mm.*,
      coalesce((select sum(l.amount) from public.rank_rp_ledger l
                where l.season_id = mm.season_id and l.student_id = mm.user_id and l.created_at >= v_from), 0)::int as rp_cur,
      coalesce((select sum(l.amount) from public.rank_rp_ledger l
                where l.season_id = mm.season_id and l.student_id = mm.user_id
                  and l.created_at >= v_prev_from and l.created_at < v_from), 0)::int as rp_prev
    from members mm
  ),
  gmode as (
    select grade, (max(rp_cur) = 0 and max(rp_prev) > 0) as use_prev from wk group by grade
  ),
  eff as (
    select w.*, g.use_prev,
      case when g.use_prev then w.rp_prev else w.rp_cur end as rp_week,
      case when g.use_prev then 0 else w.rp_prev end as rp_before,
      case when g.use_prev then v_prev_from else v_from end as win_from,
      case when g.use_prev then v_from else now() + interval '1 day' end as win_to
    from wk w join gmode g on g.grade = w.grade
  ),
  ranked as (
    select e.*, rank() over (partition by e.grade order by e.rp_week desc) as pos from eff e
  )
  select coalesce(jsonb_agg(jsonb_build_object(
      'grade', g.grade,
      'use_prev', g.use_prev,
      'season', (select jsonb_build_object('id', s.season_id, 'name', s.season_name, 'ends_on', s.ends_on)
                 from seas s where s.grade = g.grade order by s.ends_on desc limit 1),
      'total', (select count(*) from ranked r where r.grade = g.grade),
      'top', (select coalesce(jsonb_agg(jsonb_build_object(
                'pos', t.pos,
                'name', public.rank_honor_name(t.full_name, t.honor_visibility),
                'avatar', t.avatar_url,
                'rp_week', t.rp_week,
                'tier_code', t.tier_code, 'division', t.division,
                'paragon', t.tier_code = 'thach_dau' and public.rank_is_paragon(t.user_id),
                'title', (select jsonb_build_object('code', rt.code, 'name', rt.name, 'level', t.display_title_level)
                          from public.rank_titles rt where rt.code = t.display_title_code)
              ) order by t.pos, md5(t.user_id::text || v_week::text)), '[]'::jsonb)
              from (select * from ranked r where r.grade = g.grade and r.rp_week > 0 and r.pos <= 3
                    order by r.pos, md5(r.user_id::text || v_week::text) limit 5) t),
      'top_more', greatest(0, (select count(*) from ranked r where r.grade = g.grade and r.rp_week > 0 and r.pos <= 3) - 5),
      'improved', (select jsonb_build_object(
                     'name', public.rank_honor_name(t.full_name, t.honor_visibility),
                     'avatar', t.avatar_url, 'delta', t.rp_week - t.rp_before, 'rp_week', t.rp_week)
                   from ranked t
                   where t.grade = g.grade and not g.use_prev and t.pos > 3 and t.rp_week > 0 and t.rp_week - t.rp_before > 0
                   order by (t.rp_week - t.rp_before) desc, md5(t.user_id::text || v_week::text) limit 1),
      'improved_acc', (select jsonb_build_object(
                         'name', public.rank_honor_name(z.full_name, z.honor_visibility),
                         'avatar', z.avatar_url, 'gain', z.gain)
                       from (select t.full_name, t.honor_visibility, t.avatar_url, c.gain
                             from ranked t
                             join public.rank_rp_awards a
                               on a.season_id = t.season_id and a.student_id = t.user_id
                              and a.source_kind = 'progress_week' and a.awarded > 0
                              and a.source_ref = (case when g.use_prev then v_week - 7 else v_week end)::text
                             cross join lateral public.rank_progress_calc(t.user_id, case when g.use_prev then v_week - 7 else v_week end) c
                             where t.grade = g.grade and t.pos > 3 and c.gain > 0
                             order by c.gain desc, md5(t.user_id::text || v_week::text) limit 1) z),
      'tier_ups', (select coalesce(jsonb_agg(jsonb_build_object(
                     'name', public.rank_honor_name(t.full_name, t.honor_visibility),
                     'tier_code', t.tier_code, 'division', t.division) order by t.tier_reached_at desc), '[]'::jsonb)
                   from (select * from ranked r
                         where r.grade = g.grade and r.tier_sort > 1
                           and r.tier_reached_at >= r.win_from and r.tier_reached_at < r.win_to
                         order by r.tier_reached_at desc limit 4) t),
      'streak', (select jsonb_build_object('name', public.rank_honor_name(s.full_name, s.honor_visibility), 'days', s.days)
                 from (select r.full_name, r.honor_visibility,
                              public.rank_daily_streak_len(r.season_id, r.user_id, now()) as days
                       from ranked r
                       where r.grade = g.grade and exists (
                         select 1 from public.rank_rp_awards a
                         where a.season_id = r.season_id and a.student_id = r.user_id
                           and a.source_kind = 'daily_streak' and a.awarded > 0
                           and a.source_ref in (v_today::text, (v_today - 1)::text))
                      ) s
                 where s.days >= 3 order by s.days desc, s.full_name limit 1)
    ) order by g.grade::int), '[]'::jsonb)
  into v_grades
  from (select distinct grade, use_prev from ranked) g;

  if auth.uid() is not null then
    select rs.id into v_my_season
    from public.rank_seasons rs
    join public.user_classes uc on uc.user_id = auth.uid() and uc.status = 'active'
    join public.profiles p on p.id = uc.user_id and p.role = 'student'
    where rs.status = 'active' and v_today between rs.starts_on and rs.ends_on
      and (cardinality(rs.class_ids) = 0 or uc.class_id = any (rs.class_ids))
    order by rs.starts_on desc limit 1;
    if v_my_season is not null then
      select jsonb_build_object(
          'rp_week', coalesce(sum(l.amount) filter (where l.created_at >= v_from), 0)::int,
          'rp_prev', coalesce(sum(l.amount) filter (where l.created_at < v_from), 0)::int)
      into v_me
      from public.rank_rp_ledger l
      where l.season_id = v_my_season and l.student_id = auth.uid() and l.created_at >= v_prev_from;
    end if;
  end if;

  return jsonb_build_object('week_start', v_week, 'grades', v_grades, 'me', v_me);
end; $$;
grant execute on function public.rank_public_honor() to anon, authenticated;
