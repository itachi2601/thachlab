-- ============================================================================
-- fix(rank): vinh danh tuần — làm sạch tên học sinh tự nhập + đếm số bạn đồng hạng bị cắt
-- 28/9/2026 — sau khi chạy 20260928160000 trên production thấy 2 vấn đề từ dữ liệu thật:
--   1. full_name do HS tự nhập rất bẩn: "đỗ đăng duy(oguri cap number one fan)",
--      "7A4-45- Nguyễn Minh Bảo Trân", "Nguyễn Cát Minh Hằng.", "Gia Huy 10a1" → tên rút gọn
--      thành "fan) đ.", "Trân 7.", "Hằng. N."... rank_honor_name giờ bỏ phần trong ngoặc,
--      bỏ từ có chữ số, bỏ ký tự không phải chữ, viết hoa chữ cái đầu ở dạng rút gọn.
--   2. Sáng Thứ Hai khối 10 có >5 bạn đồng hạng 1 (cùng 20 RP tuần trước) → bục chỉ hiện 5,
--      cắt theo ABC không công bằng → trả thêm 'top_more' = số bạn cùng top 3 không được hiện
--      để client ghi "và N bạn khác cùng hạng".
-- Chỉ thay 2 hàm, không đổi bảng/quyền. Client cũ vẫn chạy (bỏ qua top_more).
--
-- Cách chạy: supabase db query --linked -f supabase/migrations/20260928180000_rank_public_honor_v2.sql
-- Rollback:  supabase db query --linked -f perf/rollback/20260928180000_rank_public_honor_v2.down.sql
-- ============================================================================

create or replace function public.rank_honor_name(p_name text, p_vis text)
returns text
language plpgsql immutable
as $$
declare
  raw text[];
  a text[] := '{}';
  t text;
  clean text;
begin
  -- Bỏ phần trong ngoặc (biệt danh, ghi chú) trước khi tách từ.
  raw := regexp_split_to_array(btrim(regexp_replace(coalesce(p_name, ''), '\([^)]*\)', ' ', 'g')), '\s+');
  foreach t in array raw loop
    if t ~ '\d' then continue; end if;                   -- "7A4-45-", "10a1", "010"
    clean := regexp_replace(t, '[^[:alpha:]]', '', 'g'); -- "Hằng." → "Hằng", "-" → ""
    if clean <> '' then a := a || clean; end if;
  end loop;
  if cardinality(a) = 0 then return 'Bạn học sinh'; end if;
  if p_vis = 'full' then return array_to_string(a, ' '); end if;
  if cardinality(a) = 1 then return initcap(a[1]); end if;
  return initcap(a[cardinality(a)]) || ' ' || upper(left(a[1], 1)) || '.';
end; $$;

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
              ) order by t.pos, t.full_name), '[]'::jsonb)
              from (select * from ranked r where r.grade = g.grade and r.rp_week > 0 and r.pos <= 3
                    order by r.pos, r.full_name limit 5) t),
      'top_more', greatest(0, (select count(*) from ranked r where r.grade = g.grade and r.rp_week > 0 and r.pos <= 3) - 5),
      'improved', (select jsonb_build_object(
                     'name', public.rank_honor_name(t.full_name, t.honor_visibility),
                     'avatar', t.avatar_url, 'delta', t.rp_week - t.rp_before, 'rp_week', t.rp_week)
                   from ranked t
                   where t.grade = g.grade and not g.use_prev and t.pos > 3 and t.rp_week > 0 and t.rp_week - t.rp_before > 0
                   order by (t.rp_week - t.rp_before) desc, t.full_name limit 1),
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

  return jsonb_build_object('week_start', v_week, 'grades', v_grades);
end; $$;
grant execute on function public.rank_public_honor() to anon, authenticated;

-- Kiểm nhanh sau khi chạy (đọc, không ghi):
--   select public.rank_honor_name('đỗ đăng duy(oguri cap number one fan)', 'short');  -- Duy Đ.
--   select public.rank_honor_name('7A4-45- Nguyễn Minh Bảo Trân', 'short');           -- Trân N.
--   select public.rank_honor_name('Nguyễn Cát Minh Hằng.', 'full');                   -- Nguyễn Cát Minh Hằng

-- ============================================================================
-- ROLLBACK: perf/rollback/20260928180000_rank_public_honor_v2.down.sql
--   khôi phục rank_honor_name + rank_public_honor bản 20260928160000 (không có top_more).
-- ============================================================================
